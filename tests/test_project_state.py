#!/usr/bin/env python3
"""test_project_state.py - Automated test suite for Project State Ledger and Orchestrator Lifecycle."""

import unittest
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TestProjectStateLedger(unittest.TestCase):
    """Verifies PROJECT_STATE.md structure, milestone ledger, and orchestrator lifecycle encoding."""

    @classmethod
    def setUpClass(cls):
        cls.base_dir = BASE_DIR
        cls.project_state_file = cls.base_dir / "PROJECT_STATE.md"
        cls.orchestrator_file = cls.base_dir / "canonical" / "agents" / "orchestrator.md"

    def test_project_state_file_exists(self):
        """Verify PROJECT_STATE.md exists at repository root."""
        self.assertTrue(self.project_state_file.exists(), "PROJECT_STATE.md must exist at repository root")
        self.assertGreater(self.project_state_file.stat().st_size, 500, "PROJECT_STATE.md must not be empty")

    def test_project_state_required_sections(self):
        """Verify PROJECT_STATE.md contains all mandatory governance sections."""
        content = self.project_state_file.read_text(encoding="utf-8")
        required_sections = [
            "1. Product Vision & Architectural Invariants",
            "2. Approval Boundary & Governance Rules",
            "3. Milestone Ledger & Historical Progress",
            "4. Evidence & Verification Journal",
            "5. Active Working State, Gaps & Risks",
            "6. Autonomous Next Action Engine"
        ]
        for sec in required_sections:
            self.assertIn(sec, content, f"PROJECT_STATE.md missing required section: '{sec}'")

    def test_milestone_ledger_integrity(self):
        """Verify milestone ledger records all approved milestones and statuses."""
        content = self.project_state_file.read_text(encoding="utf-8")
        expected_milestones = ["MS-01", "MS-02", "MS-03", "MS-04", "MS-05", "MS-5.1", "MS-06", "MS-07"]
        for ms in expected_milestones:
            self.assertIn(ms, content, f"PROJECT_STATE.md ledger missing milestone entry: '{ms}'")

        # Verify completed milestones are marked COMPLETED
        for ms in ["MS-01", "MS-02", "MS-03", "MS-04", "MS-05", "MS-5.1"]:
            pattern = rf"\|.*{re.escape(ms)}.*\|.*COMPLETED.*\|"
            self.assertTrue(
                re.search(pattern, content),
                f"Milestone '{ms}' must be marked COMPLETED in ledger"
            )

    def test_orchestrator_lifecycle_encoding(self):
        """Verify canonical/agents/orchestrator.md encodes lifecycle loop and approval boundaries."""
        self.assertTrue(self.orchestrator_file.exists(), "canonical/agents/orchestrator.md must exist")
        content = self.orchestrator_file.read_text(encoding="utf-8")

        self.assertIn("Project Lifecycle & Persistent Roadmap Governance", content)
        self.assertIn("PROJECT_STATE.md", content)
        self.assertIn("4-Step Orchestrator Lifecycle Loop", content)
        self.assertIn("Strict Approval Boundary Enforcement", content)

if __name__ == "__main__":
    unittest.main()
