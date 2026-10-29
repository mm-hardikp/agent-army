#!/usr/bin/env python3
r"""
server.py - Zero-dependency local mission control & dashboard server for AI Agent Army.
Provides REST APIs for live agent telemetry, task dispatching, memory vault search,
and IDE bridge synchronization.

Usage:
    python server.py [--port PORT] [--host HOST]
"""

import os
import sys
import json
import re
import argparse
import subprocess
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path

DASHBOARD_DIR = Path(__file__).resolve().parent
BASE_DIR = DASHBOARD_DIR.parent.parent
CANONICAL_DIR = BASE_DIR / "canonical"
AGENTS_DIR = CANONICAL_DIR / "agents"
SKILLS_DIR = CANONICAL_DIR / "skills"
WORKFLOWS_DIR = CANONICAL_DIR / "workflows"
TOOLS_DIR = BASE_DIR / "tools"
AGENT_STATE_DIR = BASE_DIR / ".agent"

# Add tools to path for direct imports
sys.path.insert(0, str(TOOLS_DIR))
try:
    from memory_vault import MemoryVault, resolve_vault_path
except ImportError:
    MemoryVault = None


def init_agent_state_dir():
    """Ensures .agent runtime directory and default state files exist."""
    AGENT_STATE_DIR.mkdir(parents=True, exist_ok=True)

    state_file = AGENT_STATE_DIR / "state.json"
    if not state_file.exists():
        initial_state = {
            "version": "1.0.0",
            "active_mission": "GP Doctor Web Application",
            "active_workflow": "CAN-WFL-01",
            "current_stage": "Stage 1: Intent & Requirements Intake",
            "active_agent": "product-analyst",
            "status": "READY",
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pipeline": [
                {"id": "s1", "name": "Requirements Intake", "agent": "product-analyst", "status": "COMPLETED"},
                {"id": "s2", "name": "Architecture & Contracts", "agent": "system-architect", "status": "COMPLETED"},
                {"id": "s3a", "name": "Database Schema", "agent": "database-specialist", "status": "IN_PROGRESS"},
                {"id": "s3b", "name": "Backend APIs", "agent": "backend-engineer", "status": "IN_PROGRESS"},
                {"id": "s3c", "name": "Frontend UI", "agent": "frontend-engineer", "status": "PENDING"},
                {"id": "s4", "name": "Quality & Verification", "agent": "code-reviewer", "status": "PENDING"},
                {"id": "s5", "name": "Memory Vault Archive", "agent": "memory-keeper", "status": "PENDING"}
            ],
            "recent_events": [
                {"timestamp": "2026-10-29T15:02:41Z", "agent": "memory-keeper", "type": "VAULT_INIT", "message": "Memory vault initialized at C:\\Agent-Memory"},
                {"timestamp": "2026-10-29T15:05:00Z", "agent": "orchestrator", "type": "MISSION_PLAN", "message": "Decomposed GP Doctor requirements into vertical slices"},
                {"timestamp": "2026-10-29T15:10:00Z", "agent": "database-specialist", "type": "LOCK_ACQUIRED", "message": "Acquired file reservation lock for migrations/001_initial.sql"}
            ]
        }
        state_file.write_text(json.dumps(initial_state, indent=2), encoding="utf-8")

    locks_file = AGENT_STATE_DIR / "locks.json"
    if not locks_file.exists():
        initial_locks = {
            "version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "locks": [
                {
                    "file": "src/models/patient.py",
                    "holder": "database-specialist",
                    "mode": "EXCLUSIVE_WRITE",
                    "expires_at": "2026-10-29T23:59:59Z"
                }
            ]
        }
        locks_file.write_text(json.dumps(initial_locks, indent=2), encoding="utf-8")

    inbox_file = AGENT_STATE_DIR / "inbox.json"
    if not inbox_file.exists():
        initial_inbox = {"version": "1.0.0", "tasks": []}
        inbox_file.write_text(json.dumps(initial_inbox, indent=2), encoding="utf-8")

    settings_file = AGENT_STATE_DIR / "settings.json"
    if not settings_file.exists():
        initial_settings = {
            "default_mode": "IDE_BRIDGE",
            "providers": {
                "gemini": {"enabled": False, "api_key": ""},
                "anthropic": {"enabled": False, "api_key": ""},
                "openai": {"enabled": False, "api_key": ""},
                "ollama": {"enabled": False, "base_url": "http://localhost:11434"}
            }
        }
        settings_file.write_text(json.dumps(initial_settings, indent=2), encoding="utf-8")


def parse_markdown_frontmatter(content: str) -> dict:
    """Extracts frontmatter YAML dictionary from markdown string."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}
    fm_raw = match.group(1)
    data = {}
    current_key = None
    current_list = None

    for line in fm_raw.splitlines():
        line_strip = line.strip()
        if not line_strip or line_strip.startswith("#"):
            continue

        if line_strip.startswith("- ") and current_list is not None:
            val = line_strip[2:].strip().strip('"').strip("'")
            current_list.append(val)
            continue

        kv_match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if kv_match:
            k, v = kv_match.group(1), kv_match.group(2).strip()
            if v == "" or v == ">" or v == "|":
                current_key = k
                current_list = []
                data[k] = current_list
            elif v.startswith("[") and v.endswith("]"):
                items = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
                data[k] = items
                current_key = k
                current_list = None
            else:
                data[k] = v.strip('"').strip("'")
                current_key = k
                current_list = None

    return data


def get_all_agents():
    """Loads all canonical agents and parses their frontmatter."""
    agents = []
    if not AGENTS_DIR.exists():
        return agents

    for f in sorted(AGENTS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_markdown_frontmatter(text)
        if fm.get("id"):
            agents.append({
                "id": fm.get("id"),
                "name": fm.get("name", f.stem),
                "version": fm.get("version", "1.0.0"),
                "battalion": fm.get("battalion", "Core Engineering"),
                "role": fm.get("role", ""),
                "description": fm.get("description", ""),
                "permission_level": fm.get("permission_level", 2),
                "tools_required": fm.get("tools_required", []),
                "skills_required": fm.get("skills_required", []),
                "file_path": str(f.relative_to(BASE_DIR))
            })
    return sorted(agents, key=lambda a: a["id"])


def get_all_workflows():
    """Loads all canonical workflows."""
    workflows = []
    if not WORKFLOWS_DIR.exists():
        return workflows

    for f in sorted(WORKFLOWS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_markdown_frontmatter(text)
        if fm.get("id"):
            workflows.append({
                "id": fm.get("id"),
                "name": fm.get("name", f.stem),
                "version": fm.get("version", "1.0.0"),
                "category": fm.get("category", "Engineering"),
                "description": fm.get("description", ""),
                "participating_agents": fm.get("participating_agents", []),
                "required_skills": fm.get("required_skills", []),
                "file_path": str(f.relative_to(BASE_DIR))
            })
    return sorted(workflows, key=lambda w: w["id"])


class DashboardRequestHandler(BaseHTTPRequestHandler):
    """Handles static files and REST API endpoints."""

    def log_message(self, format, *args):
        # Clean terminal output
        sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]} {args[1]}\n")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static assets
        if path == "/" or path == "/index.html":
            self.serve_file(DASHBOARD_DIR / "index.html", "text/html; charset=utf-8")
            return
        elif path == "/style.css":
            self.serve_file(DASHBOARD_DIR / "style.css", "text/css; charset=utf-8")
            return
        elif path == "/app.js":
            self.serve_file(DASHBOARD_DIR / "app.js", "application/javascript; charset=utf-8")
            return

        # API Endpoints
        if path == "/api/status":
            init_agent_state_dir()
            state_file = AGENT_STATE_DIR / "state.json"
            locks_file = AGENT_STATE_DIR / "locks.json"
            state_data = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
            locks_data = json.loads(locks_file.read_text(encoding="utf-8")) if locks_file.exists() else {}
            self.send_json({
                "status": "online",
                "state": state_data,
                "locks": locks_data.get("locks", []),
                "server_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            })
            return

        elif path == "/api/agents":
            agents = get_all_agents()
            self.send_json({"total": len(agents), "agents": agents})
            return

        elif path == "/api/workflows":
            workflows = get_all_workflows()
            self.send_json({"total": len(workflows), "workflows": workflows})
            return

        elif path == "/api/memory/search":
            q = query.get("q", [""])[0]
            project = query.get("project", [None])[0]
            tag = query.get("tag", [None])[0]
            vault = MemoryVault(resolve_vault_path())
            results = vault.search_memories(q, project=project, tag=tag)
            self.send_json({"query": q, "total": len(results), "results": results})
            return

        elif path == "/api/memory/list":
            project = query.get("project", [None])[0]
            vault = MemoryVault(resolve_vault_path())
            results = vault.list_memories(project=project)
            self.send_json({"total": len(results), "memories": results})
            return

        elif path == "/api/memory/get":
            mem_id = query.get("id", [""])[0]
            vault = MemoryVault(resolve_vault_path())
            res = vault.get_memory(mem_id)
            if res:
                self.send_json(res)
            else:
                self.send_json({"error": f"Memory {mem_id} not found"}, status_code=404)
            return

        elif path == "/api/settings":
            init_agent_state_dir()
            settings_file = AGENT_STATE_DIR / "settings.json"
            data = json.loads(settings_file.read_text(encoding="utf-8"))
            # Mask sensitive keys for display
            display_data = json.loads(json.dumps(data))
            for p, pcfg in display_data.get("providers", {}).items():
                if pcfg.get("api_key"):
                    pcfg["api_key"] = pcfg["api_key"][:4] + "••••••••" + pcfg["api_key"][-4:]
            self.send_json(display_data)
            return

        self.send_json({"error": "Endpoint not found"}, status_code=404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON payload"}, status_code=400)
            return

        init_agent_state_dir()

        if path == "/api/dispatch":
            goal = payload.get("goal", "").strip()
            workflow_id = payload.get("workflow", "CAN-WFL-01")
            project = payload.get("project", "Default-Project")

            if not goal:
                self.send_json({"error": "Goal description cannot be empty"}, status_code=400)
                return

            # Append to inbox
            inbox_file = AGENT_STATE_DIR / "inbox.json"
            inbox_data = json.loads(inbox_file.read_text(encoding="utf-8"))
            task_id = f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            task_record = {
                "task_id": task_id,
                "project": project,
                "workflow_id": workflow_id,
                "goal": goal,
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": "QUEUED"
            }
            inbox_data["tasks"].insert(0, task_record)
            inbox_file.write_text(json.dumps(inbox_data, indent=2), encoding="utf-8")

            # Update active state
            state_file = AGENT_STATE_DIR / "state.json"
            state_data = json.loads(state_file.read_text(encoding="utf-8"))
            state_data["active_mission"] = goal
            state_data["active_workflow"] = workflow_id
            state_data["status"] = "DISPATCHED"
            state_data["current_stage"] = "Stage 1: Intent & Requirements Intake"
            state_data["active_agent"] = "product-analyst"
            state_data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            # Add to recent events
            state_data["recent_events"].insert(0, {
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "agent": "orchestrator",
                "type": "MISSION_DISPATCH",
                "message": f"Dispatched new mission '{goal[:50]}...' under workflow {workflow_id}"
            })
            state_file.write_text(json.dumps(state_data, indent=2), encoding="utf-8")

            # Generate ignition prompt for IDE
            ide_prompt = f"""@orchestrator Execute workflow `{workflow_id}` for project `{project}`:
Goal: {goal}
Reference task in `.agent/inbox.json` (`{task_id}`).
Begin by delegating Stage 1 to `product-analyst` and log file reservations in `.agent/locks.json`."""

            self.send_json({
                "status": "dispatched",
                "task_id": task_id,
                "ide_prompt": ide_prompt,
                "message": "Task queued in .agent/inbox.json. Copy prompt to ignite in Antigravity or Cursor."
            })
            return

        elif path == "/api/gate/respond":
            action = payload.get("action", "").lower()
            feedback = payload.get("feedback", "")
            state_file = AGENT_STATE_DIR / "state.json"
            state_data = json.loads(state_file.read_text(encoding="utf-8"))

            state_data["recent_events"].insert(0, {
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "agent": "human-interruption-gateway",
                "type": "GATE_RESPONSE",
                "message": f"Human supervisor responded with [{action.upper()}]: {feedback or 'Proceed'}"
            })
            state_file.write_text(json.dumps(state_data, indent=2), encoding="utf-8")

            self.send_json({"status": "recorded", "action": action})
            return

        elif path == "/api/tools/run":
            tool_name = payload.get("tool", "")
            output = ""
            code = 0
            start_t = datetime.now()

            if tool_name == "test":
                res = subprocess.run(
                    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True
                )
                output = res.stdout + ("\n" + res.stderr if res.stderr else "")
                code = res.returncode
            elif tool_name == "lint":
                res = subprocess.run(
                    [sys.executable, str(TOOLS_DIR / "lint_ast.py"), str(CANONICAL_DIR)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True
                )
                output = res.stdout + ("\n" + res.stderr if res.stderr else "")
                code = res.returncode
            elif tool_name == "scan":
                res = subprocess.run(
                    [sys.executable, str(TOOLS_DIR / "scan_ast.py"), str(BASE_DIR)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True
                )
                output = res.stdout + ("\n" + res.stderr if res.stderr else "")
                code = res.returncode
            else:
                self.send_json({"error": f"Unknown tool '{tool_name}'"}, status_code=400)
                return

            duration = (datetime.now() - start_t).total_seconds()
            self.send_json({
                "tool": tool_name,
                "returncode": code,
                "duration_seconds": round(duration, 3),
                "output": output
            })
            return

        elif path == "/api/settings":
            settings_file = AGENT_STATE_DIR / "settings.json"
            current = json.loads(settings_file.read_text(encoding="utf-8"))

            if "default_mode" in payload:
                current["default_mode"] = payload["default_mode"]
            if "providers" in payload:
                for p, pdata in payload["providers"].items():
                    if p in current["providers"]:
                        if pdata.get("api_key") and not pdata["api_key"].startswith("••"):
                            current["providers"][p]["api_key"] = pdata["api_key"]
                        if "enabled" in pdata:
                            current["providers"][p]["enabled"] = pdata["enabled"]
                        if "base_url" in pdata:
                            current["providers"][p]["base_url"] = pdata["base_url"]

            settings_file.write_text(json.dumps(current, indent=2), encoding="utf-8")
            self.send_json({"status": "saved", "message": "Settings updated successfully."})
            return

        self.send_json({"error": "Endpoint not found"}, status_code=404)

    def serve_file(self, file_path: Path, content_type: str):
        """Serves a static file from disk."""
        if not file_path.exists():
            self.send_error(404, f"File {file_path.name} not found")
            return
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run_server(port=8765, host="127.0.0.1"):
    """Starts the HTTP server with automatic port retry."""
    init_agent_state_dir()
    for p in range(port, port + 20):
        try:
            server_addr = (host, p)
            httpd = HTTPServer(server_addr, DashboardRequestHandler)
            print("==================================================================")
            print("  AI AGENT ARMY - MISSION CONTROL & COCKPIT DASHBOARD            ")
            print("==================================================================")
            print(f"  [*] Server running at: http://{host}:{p}")
            print(f"  [*] Repository root:   {BASE_DIR}")
            print(f"  [*] Memory Vault at:   C:\\Agent-Memory")
            print(f"  [*] Active Cockpit:    Pattern A (Shared State & IDE Bridge)")
            print("==================================================================")
            print("Press Ctrl+C to stop the dashboard.\n")
            httpd.serve_forever()
            break
        except OSError as e:
            if "address already in use" in str(e).lower() or e.errno in (98, 10048, 10013) or isinstance(e, PermissionError):
                continue
            raise e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent Army Dashboard Server")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface")
    args = parser.parse_args()
    run_server(port=args.port, host=args.host)
