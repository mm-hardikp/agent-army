#!/usr/bin/env python3
"""test_dashboard.py - Automated test suite for Mission Control Cockpit server and APIs."""

import unittest
import threading
import time
import json
import urllib.request
import urllib.error
from http.server import HTTPServer
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = BASE_DIR / "tools" / "dashboard"
sys.path.insert(0, str(DASHBOARD_DIR))

from server import DashboardRequestHandler, init_agent_state_dir, get_all_agents, get_all_workflows


class TestDashboardServer(unittest.TestCase):
    """Verifies that the dashboard REST APIs and static assets serve accurately."""

    @classmethod
    def setUpClass(cls):
        init_agent_state_dir()
        cls.port = 8899
        cls.server = HTTPServer(("127.0.0.1", cls.port), DashboardRequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.3)
        cls.base_url = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_get_index_html(self):
        req = urllib.request.Request(f"{self.base_url}/")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/html", resp.headers.get("Content-Type"))
            html = resp.read().decode("utf-8")
            self.assertIn("AGENT ARMY", html)
            self.assertIn("Mission Control", html)

    def test_get_style_css(self):
        req = urllib.request.Request(f"{self.base_url}/style.css")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/css", resp.headers.get("Content-Type"))

    def test_get_app_js(self):
        req = urllib.request.Request(f"{self.base_url}/app.js")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("javascript", resp.headers.get("Content-Type"))

    def test_api_status(self):
        req = urllib.request.Request(f"{self.base_url}/api/status")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "online")
            self.assertIn("state", data)
            self.assertIn("locks", data)

    def test_api_agents(self):
        req = urllib.request.Request(f"{self.base_url}/api/agents")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("total"), 19)
            agents = data.get("agents", [])
            agent_names = [a["name"] for a in agents]
            self.assertIn("orchestrator", agent_names)
            self.assertIn("memory-keeper", agent_names)

    def test_api_workflows(self):
        req = urllib.request.Request(f"{self.base_url}/api/workflows")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("total"), 10)

    def test_api_memory_list_and_search(self):
        req = urllib.request.Request(f"{self.base_url}/api/memory/list")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("memories", data)

        req_search = urllib.request.Request(f"{self.base_url}/api/memory/search?q=sqlite")
        with urllib.request.urlopen(req_search) as resp:
            self.assertEqual(resp.status, 200)
            data_search = json.loads(resp.read().decode("utf-8"))
            self.assertIn("results", data_search)

    def test_api_dispatch_task(self):
        payload = json.dumps({
            "project": "GP-Doctor",
            "workflow": "CAN-WFL-01",
            "goal": "Build automated revenue report endpoint"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/dispatch",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "dispatched")
            self.assertIn("ide_prompt", data)
            self.assertIn("@orchestrator", data["ide_prompt"])


if __name__ == "__main__":
    unittest.main()
