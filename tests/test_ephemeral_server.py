import os
import sys
import time
import socket
import unittest
from pathlib import Path

# Add tools directory to path
tools_path = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_path))

from ephemeral_server import is_port_open, wait_for_server, run_ephemeral_server


class TestEphemeralServer(unittest.TestCase):
    def find_free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    def test_port_detection_closed(self):
        port = self.find_free_port()
        self.assertFalse(is_port_open(port))

    def test_startup_failure_timeout(self):
        port = self.find_free_port()
        # Launching a command that fails to open the port
        exit_code = run_ephemeral_server(
            server_cmd="python -c \"import time; time.sleep(10)\"",
            port=port,
            test_cmd=["python", "-c", "print('should not run')"],
            timeout=2
        )
        self.assertEqual(exit_code, 1)

    def test_server_lifecycle_and_cleanup(self):
        port = self.find_free_port()
        # Start a simple HTTP server on the free port
        server_cmd = f"python -m http.server {port}"
        test_cmd = ["python", "-c", "print('test finished successfully')"]

        exit_code = run_ephemeral_server(
            server_cmd=server_cmd,
            port=port,
            test_cmd=test_cmd,
            timeout=10
        )
        self.assertEqual(exit_code, 0)
        
        # Verify the server process was terminated and the port is freed
        time.sleep(1)
        self.assertFalse(is_port_open(port), f"Port {port} should be closed after cleanup.")


if __name__ == "__main__":
    unittest.main()
