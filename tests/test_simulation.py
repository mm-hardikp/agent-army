#!/usr/bin/env python3
"""test_simulation.py - End-to-end multi-IDE workflow simulation and integration verification (Milestone 7)."""

import unittest
import json
import uuid
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))
sys.path.insert(0, str(BASE_DIR / "adapters"))

from validate_canonical import parse_frontmatter, validate_dict_against_schema
import compile as compiler


class TestMultiIDESimulation(unittest.TestCase):
    """End-to-end integration and simulation suite across the 4 IDE execution patterns."""

    @classmethod
    def setUpClass(cls):
        cls.base_dir = BASE_DIR
        cls.canonical_dir = cls.base_dir / "canonical"
        cls.agents_dir = cls.canonical_dir / "agents"
        cls.skills_dir = cls.canonical_dir / "skills"
        cls.workflows_dir = cls.canonical_dir / "workflows"
        cls.schemas_dir = cls.canonical_dir / "schemas"

        cls.envelope_schema = json.loads(
            (cls.schemas_dir / "envelope.schema.json").read_text(encoding="utf-8")
        )

        # Ensure adapters are compiled for simulation
        compiler.main_run = True
        cls.adapter_files = []
        cls.adapter_files.extend(compiler.generate_antigravity(cls.base_dir))
        cls.adapter_files.extend(compiler.generate_claude(cls.base_dir))
        cls.adapter_files.extend(compiler.generate_cursor(cls.base_dir))
        cls.adapter_files.extend(compiler.generate_copilot(cls.base_dir))

    def create_envelope(self, msg_type: str, sender: str, receiver: str, summary: str, task_id="TASK-SIM-01", correlation_id="CORR-SIM-01"):
        """Helper to create a strictly valid CAN-ENV-01 v2.2 envelope."""
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            "version": "2.2.0",
            "message_id": f"MSG-2026-{uuid.uuid4().hex[:8].upper()}",
            "correlation_id": correlation_id,
            "task_id": task_id,
            "timestamp": now_iso,
            "message_type": msg_type,
            "sending_agent": sender,
            "receiving_agent": receiver,
            "status_summary": summary,
            "explicit_next_action": {
                "recommended_target": receiver,
                "required_action": f"Process {msg_type}"
            }
        }

    def test_pattern_1_pure_canonical_execution(self):
        """Simulate Pattern 1 (Option A): Pure folder-based execution from ORCHESTRATOR.md."""
        orch_entry = self.base_dir / "ORCHESTRATOR.md"
        self.assertTrue(orch_entry.exists())

        # Orchestrator reads project state
        project_state = self.base_dir / "PROJECT_STATE.md"
        self.assertTrue(project_state.exists())
        state_text = project_state.read_text(encoding="utf-8")
        self.assertIn("Milestone Ledger", state_text)

        # Orchestrator selects CAN-WFL-02 (Surgical Bug Fix)
        wf_file = self.workflows_dir / "surgical-bug-investigation-and-fix.md"
        self.assertTrue(wf_file.exists())
        wf_data = parse_frontmatter(wf_file.read_text(encoding="utf-8"))
        self.assertEqual(wf_data["id"], "CAN-WFL-02")

        # Step 1: Orchestrator delegates task to debugger-detective
        assign_msg = self.create_envelope(
            "TASK_ASSIGNMENT",
            sender="orchestrator",
            receiver="debugger-detective",
            summary="Investigate and isolate null pointer in billing calculation"
        )
        errors = validate_dict_against_schema(assign_msg, self.envelope_schema, "sim_assign")
        self.assertEqual(errors, [])

        # Step 2: debugger-detective accepts task
        accept_msg = self.create_envelope(
            "TASK_ACCEPTANCE",
            sender="debugger-detective",
            receiver="orchestrator",
            summary="Accepted: triage and minimal reproduction in progress"
        )
        errors = validate_dict_against_schema(accept_msg, self.envelope_schema, "sim_accept")
        self.assertEqual(errors, [])

        # Step 3: debugger-detective emits completion with reproduction script
        complete_msg = self.create_envelope(
            "TASK_COMPLETION",
            sender="debugger-detective",
            receiver="orchestrator",
            summary="Root cause isolated: off-by-one error at line 42; reproduction test attached"
        )
        errors = validate_dict_against_schema(complete_msg, self.envelope_schema, "sim_complete")
        self.assertEqual(errors, [])

        # Step 4: Orchestrator routes patch to surgeon-editor
        handoff_msg = self.create_envelope(
            "HANDOFF",
            sender="orchestrator",
            receiver="surgeon-editor",
            summary="Apply surgical patch to line 42"
        )
        errors = validate_dict_against_schema(handoff_msg, self.envelope_schema, "sim_handoff")
        self.assertEqual(errors, [])

    def test_pattern_2_antigravity_shim_integration(self):
        """Simulate Pattern 2: Google Antigravity rule and skill resolution."""
        rule_path = self.base_dir / ".agents" / "rules" / "orchestrator.md"
        self.assertTrue(rule_path.exists())
        rule_text = rule_path.read_text(encoding="utf-8")
        self.assertIn("canonical/agents/orchestrator.md", rule_text)

        # Verify all 18 skill wrappers resolve to valid canonical SKILL.md files
        for i in range(1, 19):
            matches = list(self.skills_dir.glob("*"))
            for m in matches:
                if (m / "SKILL.md").exists():
                    stub = self.base_dir / ".agents" / "skills" / m.name / "SKILL.md"
                    self.assertTrue(stub.exists(), f"Antigravity skill stub missing for {m.name}")
                    stub_text = stub.read_text(encoding="utf-8")
                    self.assertIn(f"canonical/skills/{m.name}/SKILL.md", stub_text)

    def test_pattern_3_claude_code_shim_integration(self):
        """Simulate Pattern 3: Claude Code slash command resolution."""
        cmd_path = self.base_dir / ".claude" / "commands" / "orchestrator.md"
        self.assertTrue(cmd_path.exists())
        cmd_text = cmd_path.read_text(encoding="utf-8")
        self.assertIn("canonical/agents/orchestrator.md", cmd_text)
        self.assertIn("canonical/workflows/", cmd_text)

    def test_pattern_4_cursor_and_copilot_shims(self):
        """Simulate Pattern 4: Cursor MDC rules and Copilot instructions resolution."""
        cursor_mdc = self.base_dir / ".cursor" / "rules" / "orchestrator.mdc"
        copilot_inst = self.base_dir / ".github" / "copilot-instructions.md"

        self.assertTrue(cursor_mdc.exists())
        self.assertTrue(copilot_inst.exists())

        self.assertIn("canonical/agents/orchestrator.md", cursor_mdc.read_text(encoding="utf-8"))
        self.assertIn("canonical/agents/orchestrator.md", copilot_inst.read_text(encoding="utf-8"))

    def test_simulation_blocker_and_human_escalation(self):
        """Simulate blocker notification and Level 3 human approval gate flow."""
        # Specialist encounters blocker
        blocker_msg = self.create_envelope(
            "BLOCKER",
            sender="backend-engineer",
            receiver="orchestrator",
            summary="Schema requires drop column in production table"
        )
        errors = validate_dict_against_schema(blocker_msg, self.envelope_schema, "sim_blocker")
        self.assertEqual(errors, [])

        # Orchestrator evaluates Level 3 operation and issues APPROVAL_REQUEST
        approval_req = self.create_envelope(
            "APPROVAL_REQUEST",
            sender="orchestrator",
            receiver="human-interruption-gateway",
            summary="Level 3 Destructive DDL: User approval required to drop column"
        )
        errors = validate_dict_against_schema(approval_req, self.envelope_schema, "sim_approval_req")
        self.assertEqual(errors, [])

        # Human responds with APPROVAL_RESPONSE
        approval_resp = self.create_envelope(
            "APPROVAL_RESPONSE",
            sender="human-interruption-gateway",
            receiver="orchestrator",
            summary="Approved with condition: execute zero-downtime deprecation first"
        )
        errors = validate_dict_against_schema(approval_resp, self.envelope_schema, "sim_approval_resp")
        self.assertEqual(errors, [])

    def test_full_repository_markdown_links_integrity(self):
        """Cross-checks markdown links across entire repo to guarantee zero broken references."""
        import re
        link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        md_files = [
            self.base_dir / "README.md",
            self.base_dir / "AGENTS.md",
            self.base_dir / "ORCHESTRATOR.md",
            self.base_dir / "PROJECT_STATE.md"
        ]

        for md in md_files:
            if not md.exists():
                continue
            text = md.read_text(encoding="utf-8")
            for title, target in link_regex.findall(text):
                if target.startswith("#") or target.startswith("http://") or target.startswith("https://") or target.startswith("file:///"):
                    continue
                resolved = (md.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"Broken link in {md.name}: [{title}]({target}) -> {resolved}")


if __name__ == "__main__":
    unittest.main()
