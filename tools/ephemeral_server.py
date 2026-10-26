#!/usr/bin/env python3
"""
ephemeral_server.py - Lean test server lifecycle wrapper for headless Playwright test harnesses.
Origin: Derived from anthropics/skills (SKL-010 with_server.py).
Zero external dependencies (uses socket, subprocess, time, sys, signal, os).

Usage:
    python ephemeral_server.py --server "npm run dev" --port 5173 -- python run_tests.py
"""

import subprocess
import socket
import time
import sys
import argparse
import os
import signal


def is_port_open(port: int, host: str = "localhost", timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.error, ConnectionRefusedError, OSError):
        return False


def wait_for_server(port: int, timeout: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(port):
            return True
        time.sleep(0.3)
    return False


def terminate_process(proc: subprocess.Popen):
    """Terminate the process and all child processes cleanly without leaking pipes or ports."""
    if proc is None:
        return

    try:
        if proc.poll() is None:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
            else:
                pgid = os.getpgid(proc.pid)
                os.killpg(pgid, signal.SIGTERM)
                time.sleep(0.3)
                if proc.poll() is None:
                    os.killpg(pgid, signal.SIGKILL)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass
    finally:
        # Close standard streams and wait for reaping to eliminate ResourceWarnings
        try:
            if proc.stdout:
                proc.stdout.close()
            if proc.stderr:
                proc.stderr.close()
            if proc.stdin:
                proc.stdin.close()
            proc.wait(timeout=2)
        except Exception:
            pass


def run_ephemeral_server(server_cmd: str, port: int, test_cmd: list, timeout: int = 30) -> int:
    """Programmatic interface to run an ephemeral server and test command."""
    creationflags = 0
    preexec_fn = None
    if sys.platform != "win32":
        preexec_fn = os.setsid

    server_proc = subprocess.Popen(
        server_cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=preexec_fn
    )

    try:
        ready = wait_for_server(port, timeout=timeout)
        if not ready:
            terminate_process(server_proc)
            return 1

        res = subprocess.run(test_cmd, shell=True)
        return res.returncode
    finally:
        terminate_process(server_proc)


def main():
    parser = argparse.ArgumentParser(description="Ephemeral server wrapper for test suites.")
    parser.add_argument("--server", required=True, help="Shell command to start the server")
    parser.add_argument("--port", type=int, required=True, help="Port to poll for readiness")
    parser.add_argument("--timeout", type=int, default=30, help="Max readiness wait in seconds")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Test command to execute once ready")
    args = parser.parse_args()

    test_cmd = args.command
    if test_cmd and test_cmd[0] == "--":
        test_cmd = test_cmd[1:]

    if not test_cmd:
        print("Error: No test command specified to run after server starts.")
        sys.exit(1)

    code = run_ephemeral_server(args.server, args.port, test_cmd, timeout=args.timeout)
    sys.exit(code)


if __name__ == "__main__":
    main()
