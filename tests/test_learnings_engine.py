#!/usr/bin/env python3
"""test_learnings_engine.py - Automated test suite for self-learning SQLite engine."""

import unittest
import shutil
import tempfile
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "tools"))

from learnings_engine import LearningsEngine, resolve_db_path


class TestLearningsEngine(unittest.TestCase):
    """Verifies SQLite learnings engine, rule insertion, contextual recall, and prompt generation."""

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="agent_learn_test_"))
        self.db_path = self.temp_dir / "learnings_test.db"
        self.engine = LearningsEngine(self.db_path)

    def tearDown(self):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_db(self):
        self.assertTrue(self.db_path.exists())
        with self.engine.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='learned_rules'")
            row = cursor.fetchone()
            self.assertIsNotNone(row)

    def test_add_and_recall_rule(self):
        res = self.engine.add_rule(
            instruction="Always use PowerShell syntax for Windows shell commands.",
            category="environment",
            trigger_context="shell commands",
            reason="User operates on Windows; bash commands fail.",
            source="user_correction"
        )
        self.assertEqual(res["status"], "saved")
        self.assertTrue(res["rule_id"].startswith("LRN-ENV-"))

        # Recall by context
        matches = self.engine.recall_rules(context="shell commands")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["instruction"], "Always use PowerShell syntax for Windows shell commands.")
        self.assertEqual(matches[0]["times_applied"], 1)

        # Recall again increments times_applied
        matches2 = self.engine.recall_rules(query="PowerShell")
        self.assertEqual(len(matches2), 1)
        self.assertEqual(matches2[0]["times_applied"], 2)

    def test_duplicate_instruction_update(self):
        self.engine.add_rule(
            instruction="Keep answers concise.",
            category="style",
            reason="User prefers brevity."
        )
        # Adding same instruction with new reason updates without error
        res = self.engine.add_rule(
            instruction="Keep answers concise.",
            category="style",
            reason="Updated reason."
        )
        self.assertEqual(res["status"], "saved")
        rules = self.engine.list_rules()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["reason"], "Updated reason.")

    def test_delete_rule(self):
        res = self.engine.add_rule(instruction="Temporary rule to delete.", category="general")
        rule_id = res["rule_id"]
        self.assertTrue(self.engine.delete_rule(rule_id))

        # Should not appear in active list
        active_rules = self.engine.list_rules(active_only=True)
        self.assertEqual(len(active_rules), 0)

        # Still in full history
        all_rules = self.engine.list_rules(active_only=False)
        self.assertEqual(len(all_rules), 1)

    def test_format_prompt_context(self):
        self.engine.add_rule(
            instruction="Use type hints in all Python functions.",
            category="technical",
            trigger_context="python",
            reason="Maintainability."
        )
        self.engine.add_rule(
            instruction="Avoid third-party UI frameworks unless requested.",
            category="preference",
            trigger_context="frontend"
        )

        prompt = self.engine.format_prompt_context(context="python")
        self.assertIn("[USER PREFERENCES & LEARNED RULES]", prompt)
        self.assertIn("Use type hints in all Python functions.", prompt)
        self.assertIn("(Reason: Maintainability.)", prompt)

    def test_cli_execution(self):
        cli = BASE_DIR / "tools" / "learnings_engine.py"

        # CLI add
        res_add = subprocess.run(
            [
                sys.executable, str(cli), "--db", str(self.db_path), "add",
                "--instruction", "CLI rule test instruction.",
                "--category", "preference",
                "--context", "cli"
            ],
            capture_output=True,
            text=True
        )
        self.assertEqual(res_add.returncode, 0, f"CLI add failed: {res_add.stderr}")
        data_add = json.loads(res_add.stdout)
        self.assertEqual(data_add["status"], "saved")

        # CLI prompt
        res_prompt = subprocess.run(
            [sys.executable, str(cli), "--db", str(self.db_path), "prompt", "CLI"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res_prompt.returncode, 0)
        self.assertIn("CLI rule test instruction.", res_prompt.stdout)


if __name__ == "__main__":
    unittest.main()
