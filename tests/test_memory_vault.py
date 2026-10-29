#!/usr/bin/env python3
"""test_memory_vault.py - Automated test suite for persistent memory engine and recall indexer."""

import unittest
import shutil
import tempfile
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "tools"))

from memory_vault import MemoryVault, resolve_vault_path, slugify


class TestMemoryVault(unittest.TestCase):
    """Verifies vault initialization, memory snapshotting, indexing, and recall queries."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="agent_mem_test_"))
        self.vault = MemoryVault(self.temp_dir)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_slugify(self):
        self.assertEqual(slugify("Hello World! 123"), "hello-world-123")
        self.assertEqual(slugify("GP Doctor: Patient Data"), "gp-doctor-patient-data")

    def test_init_vault(self):
        res = self.vault.init_vault(username="testuser")
        self.assertEqual(res["status"], "initialized")
        self.assertTrue((self.temp_dir / "config.json").exists())
        self.assertTrue((self.temp_dir / "index.json").exists())
        self.assertTrue((self.temp_dir / "projects").exists())

        cfg = json.loads((self.temp_dir / "config.json").read_text(encoding="utf-8"))
        self.assertEqual(cfg["default_user"], "testuser")

    def test_store_and_get_memory(self):
        res = self.vault.store_memory(
            project="GP Doctor",
            title="Patient Schema Design",
            what="Designed normalized SQLite patient schema with indexing on patient_id and phone.",
            why="SQLite chosen for zero-dependency local dev compliance.",
            where_files="src/models/patient.py, migrations/001_patient.sql",
            learnings="Ensure foreign key enforcement is turned on via PRAGMA foreign_keys = ON.",
            tags=["sqlite", "database", "schema", "patient"],
            workflow="CAN-WFL-01",
            author="memory-keeper"
        )

        self.assertEqual(res["status"], "stored")
        memory_id = res["memory_id"]
        self.assertTrue(memory_id.startswith("MEM-GP-DOCTOR-"))
        self.assertTrue(Path(res["file_path"]).exists())

        # Verify index updated
        index_data = self.vault.load_index()
        self.assertEqual(len(index_data["entries"]), 1)
        self.assertEqual(index_data["entries"][0]["id"], memory_id)

        # Verify get_memory
        item = self.vault.get_memory(memory_id)
        self.assertIsNotNone(item)
        self.assertEqual(item["title"], "Patient Schema Design")
        self.assertIn("PRAGMA foreign_keys = ON", item["content"])
        self.assertIn("zero-dependency local dev compliance", item["content"])

    def test_search_memories(self):
        self.vault.store_memory(
            project="GP Doctor",
            title="Patient Schema Design",
            what="Designed SQLite patient schema.",
            why="SQLite chosen for local dev.",
            tags=["sqlite", "database"]
        )
        self.vault.store_memory(
            project="GP Doctor",
            title="Revenue Calculation Engine",
            what="Implemented daily revenue aggregation logic.",
            why="Audit trail compliance using integer cents.",
            tags=["revenue", "finance", "billing"]
        )
        self.vault.store_memory(
            project="E-Commerce",
            title="Cart Checkout API",
            what="Built Stripe payment webhook.",
            why="Asynchronous event handling for order confirmation.",
            tags=["stripe", "checkout", "api"]
        )

        # Search by tag
        res_sqlite = self.vault.search_memories("sqlite")
        self.assertEqual(len(res_sqlite), 1)
        self.assertEqual(res_sqlite[0]["title"], "Patient Schema Design")

        # Search by keyword in why
        res_cents = self.vault.search_memories("cents")
        self.assertEqual(len(res_cents), 1)
        self.assertEqual(res_cents[0]["title"], "Revenue Calculation Engine")

        # Filter by project
        res_proj = self.vault.search_memories("API", project="E-Commerce")
        self.assertEqual(len(res_proj), 1)
        self.assertEqual(res_proj[0]["project"], "E-Commerce")

    def test_list_memories(self):
        self.vault.store_memory(project="ProjA", title="Task 1", what="W1", why="Y1")
        self.vault.store_memory(project="ProjB", title="Task 2", what="W2", why="Y2")

        entries = self.vault.list_memories()
        self.assertEqual(len(entries), 2)

        proj_b_entries = self.vault.list_memories(project="ProjB")
        self.assertEqual(len(proj_b_entries), 1)
        self.assertEqual(proj_b_entries[0]["title"], "Task 2")

    def test_cli_execution(self):
        cli_script = BASE_DIR / "tools" / "memory_vault.py"
        
        # Test CLI init
        res_init = subprocess.run(
            [sys.executable, str(cli_script), "--vault", str(self.temp_dir), "init", "--user", "cli_user"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res_init.returncode, 0, f"CLI init failed: {res_init.stderr}")
        data_init = json.loads(res_init.stdout)
        self.assertEqual(data_init["status"], "initialized")

        # Test CLI store
        res_store = subprocess.run(
            [
                sys.executable, str(cli_script), "--vault", str(self.temp_dir), "store",
                "--project", "TestProject",
                "--title", "Auth Token Handling",
                "--what", "Implemented JWT token rotation.",
                "--why", "Mitigate token theft risks.",
                "--tags", "auth,jwt,security"
            ],
            capture_output=True,
            text=True
        )
        self.assertEqual(res_store.returncode, 0, f"CLI store failed: {res_store.stderr}")
        data_store = json.loads(res_store.stdout)
        mem_id = data_store["memory_id"]

        # Test CLI search
        res_search = subprocess.run(
            [sys.executable, str(cli_script), "--vault", str(self.temp_dir), "search", "JWT", "--json"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res_search.returncode, 0, f"CLI search failed: {res_search.stderr}")
        results = json.loads(res_search.stdout)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], mem_id)


if __name__ == "__main__":
    unittest.main()
