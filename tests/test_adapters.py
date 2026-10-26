#!/usr/bin/env python3
"""test_adapters.py - Automated test suite for optional IDE adapter compilation."""

import unittest
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ADAPTERS_DIR = BASE_DIR / "adapters"
COMPILE_PY = ADAPTERS_DIR / "compile.py"

class TestAdaptersCompilation(unittest.TestCase):
    """Verifies adapter generation, thin pointer integrity, and clean functionality."""

    @classmethod
    def setUpClass(cls):
        cls.base_dir = BASE_DIR
        cls.compile_py = COMPILE_PY
        cls.orchestrator_entry = cls.base_dir / "ORCHESTRATOR.md"

    def test_orchestrator_root_entry_exists(self):
        """Verify ORCHESTRATOR.md exists and contains ignition prompt."""
        self.assertTrue(self.orchestrator_entry.exists(), "ORCHESTRATOR.md must exist at repository root")
        content = self.orchestrator_entry.read_text(encoding="utf-8")
        self.assertIn("canonical/agents/orchestrator.md", content)
        self.assertIn("PROJECT_STATE.md", content)
        self.assertIn("Quick Start: How to Run in Any IDE", content)

    def test_compile_all_targets(self):
        """Verify python adapters/compile.py --target all generates all expected shims."""
        res = subprocess.run(
            [sys.executable, str(self.compile_py), "--target", "all"],
            cwd=str(self.base_dir),
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Compilation failed: {res.stderr}")

        # Check files exist
        antigravity_rule = self.base_dir / ".agents" / "rules" / "orchestrator.md"
        claude_cmd = self.base_dir / ".claude" / "commands" / "orchestrator.md"
        cursor_rule = self.base_dir / ".cursor" / "rules" / "orchestrator.mdc"
        copilot_inst = self.base_dir / ".github" / "copilot-instructions.md"

        self.assertTrue(antigravity_rule.exists(), "Antigravity rule must be generated")
        self.assertTrue(claude_cmd.exists(), "Claude Code command must be generated")
        self.assertTrue(cursor_rule.exists(), "Cursor rule must be generated")
        self.assertTrue(copilot_inst.exists(), "Copilot instructions must be generated")

    def test_thin_pointer_non_duplication(self):
        """Verify generated files are thin pointers that do not duplicate agent bodies."""
        antigravity_rule = self.base_dir / ".agents" / "rules" / "orchestrator.md"
        cursor_rule = self.base_dir / ".cursor" / "rules" / "orchestrator.mdc"

        self.assertTrue(antigravity_rule.exists())
        self.assertTrue(cursor_rule.exists())

        # Assert thinness (< 50 lines)
        self.assertLess(len(antigravity_rule.read_text(encoding="utf-8").splitlines()), 50)
        self.assertLess(len(cursor_rule.read_text(encoding="utf-8").splitlines()), 50)

        # Assert pointer references
        self.assertIn("canonical/agents/orchestrator.md", antigravity_rule.read_text(encoding="utf-8"))
        self.assertIn("canonical/agents/orchestrator.md", cursor_rule.read_text(encoding="utf-8"))

    def test_compiler_verify_flag(self):
        """Verify python adapters/compile.py --verify passes on generated shims."""
        res = subprocess.run(
            [sys.executable, str(self.compile_py), "--verify"],
            cwd=str(self.base_dir),
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Verify check failed: {res.stderr}")
        self.assertIn("[PASS]", res.stdout)

    def test_compiler_clean_flag(self):
        """Verify python adapters/compile.py --clean removes generated shims."""
        res = subprocess.run(
            [sys.executable, str(self.compile_py), "--clean"],
            cwd=str(self.base_dir),
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0, f"Clean failed: {res.stderr}")

        antigravity_rule = self.base_dir / ".agents" / "rules" / "orchestrator.md"
        claude_cmd = self.base_dir / ".claude" / "commands" / "orchestrator.md"
        cursor_rule = self.base_dir / ".cursor" / "rules" / "orchestrator.mdc"
        copilot_inst = self.base_dir / ".github" / "copilot-instructions.md"

        self.assertFalse(antigravity_rule.exists(), "Antigravity rule should be cleaned")
        self.assertFalse(claude_cmd.exists(), "Claude Code command should be cleaned")
        self.assertFalse(cursor_rule.exists(), "Cursor rule should be cleaned")
        self.assertFalse(copilot_inst.exists(), "Copilot instructions should be cleaned")

        # Re-compile so repo has valid shims available
        subprocess.run([sys.executable, str(self.compile_py), "--target", "all"], cwd=str(self.base_dir))

if __name__ == "__main__":
    unittest.main()
