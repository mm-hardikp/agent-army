#!/usr/bin/env python3
"""test_workflows.py - Comprehensive test suite for Canonical Cognitive Workflows (Milestone 5)."""

import unittest
import re
from pathlib import Path
import sys

# Ensure scripts directory is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "scripts"))

from validate_canonical import parse_frontmatter


class TestCanonicalWorkflows(unittest.TestCase):
    """Validates the 10 canonical workflows, unique IDs, agent/skill references, and structure."""

    @classmethod
    def setUpClass(cls):
        cls.base_dir = BASE_DIR
        cls.workflows_dir = cls.base_dir / "canonical" / "workflows"
        cls.agents_dir = cls.base_dir / "canonical" / "agents"
        cls.skills_dir = cls.base_dir / "canonical" / "skills"

        # Expected 10 workflows baseline from Phase 1A architecture
        cls.expected_workflows = {
            "CAN-WFL-01": "full-cycle-feature-development",
            "CAN-WFL-02": "surgical-bug-investigation-and-fix",
            "CAN-WFL-03": "independent-adversarial-code-review",
            "CAN-WFL-04": "technical-research-and-spike",
            "CAN-WFL-05": "architecture-decision-and-system-design",
            "CAN-WFL-06": "database-schema-and-migration-lifecycle",
            "CAN-WFL-07": "documentation-and-drift-remediation",
            "CAN-WFL-08": "application-security-and-vulnerability-audit",
            "CAN-WFL-09": "automated-test-suite-expansion",
            "CAN-WFL-10": "parallel-multi-agent-worktree-swarm",
        }

    def test_all_10_workflow_files_exist(self):
        """Verify exactly 10 workflow files exist with canonical filenames."""
        workflow_files = list(self.workflows_dir.glob("*.md"))
        self.assertEqual(
            len(workflow_files),
            10,
            f"Expected 10 canonical workflows, found {len(workflow_files)}: {[f.name for f in workflow_files]}"
        )

        for expected_name in self.expected_workflows.values():
            expected_path = self.workflows_dir / f"{expected_name}.md"
            self.assertTrue(
                expected_path.exists(),
                f"Missing expected canonical workflow file: {expected_path.name}"
            )

    def test_unique_workflow_ids_and_names(self):
        """Verify all workflow IDs and names are unique and match Phase 1A baseline."""
        seen_ids = {}
        for wf_file in self.workflows_dir.glob("*.md"):
            content = wf_file.read_text(encoding="utf-8")
            data = parse_frontmatter(content)
            wf_id = data.get("id")
            wf_name = data.get("name")

            self.assertIsNotNone(wf_id, f"Missing 'id' frontmatter in {wf_file.name}")
            self.assertIsNotNone(wf_name, f"Missing 'name' frontmatter in {wf_file.name}")
            self.assertNotIn(wf_id, seen_ids, f"Duplicate workflow ID '{wf_id}' found in {wf_file.name}")
            seen_ids[wf_id] = wf_name

        self.assertEqual(
            seen_ids,
            self.expected_workflows,
            "Workflow IDs and names mismatch against Phase 1A architecture baseline"
        )

    def test_workflow_participating_agents_validity(self):
        """Verify every participating agent exists in canonical/agents/ and orchestrator is included."""
        existing_agents = {f.stem for f in self.agents_dir.glob("*.md")}

        for wf_file in self.workflows_dir.glob("*.md"):
            data = parse_frontmatter(wf_file.read_text(encoding="utf-8"))
            agents = data.get("participating_agents", [])
            self.assertTrue(isinstance(agents, list), f"'participating_agents' must be a list in {wf_file.name}")
            self.assertGreater(len(agents), 0, f"'participating_agents' cannot be empty in {wf_file.name}")

            # Orchestrator CAN-AGT-01 must coordinate every workflow
            self.assertIn("orchestrator", agents, f"'orchestrator' (CAN-AGT-01) must be in participating_agents of {wf_file.name}")

            for agent in agents:
                self.assertIn(
                    agent,
                    existing_agents,
                    f"Workflow {wf_file.name} references non-existent agent '{agent}'"
                )

    def test_workflow_required_skills_validity(self):
        """Verify every required skill exists in canonical/skills/."""
        existing_skills = {d.name for d in self.skills_dir.iterdir() if d.is_dir()}

        for wf_file in self.workflows_dir.glob("*.md"):
            data = parse_frontmatter(wf_file.read_text(encoding="utf-8"))
            skills = data.get("required_skills", [])
            self.assertTrue(isinstance(skills, list), f"'required_skills' must be a list in {wf_file.name}")
            self.assertGreater(len(skills), 0, f"'required_skills' cannot be empty in {wf_file.name}")

            for skill in skills:
                self.assertIn(
                    skill,
                    existing_skills,
                    f"Workflow {wf_file.name} references non-existent skill '{skill}'"
                )

    def test_workflow_required_structure_and_sections(self):
        """Verify each workflow defines all required sections per Milestone 5 constraints."""
        required_sections = [
            (r"## 1\.\s+Purpose\s+&\s+Applicable\s+Scenarios", "Purpose & Applicable Scenarios"),
            (r"## 2\.\s+Entry\s+Conditions\s+&\s+Required\s+Inputs", "Entry Conditions & Required Inputs"),
            (r"## 3\.\s+Participating\s+Agents", "Participating Agents"),
            (r"## 4\.\s+Execution\s+Stages\s+&\s+Dependency\s+Graph", "Execution Stages & Dependency Graph"),
            (r"## 5\.\s+Parallel\s+Execution\s+Opportunities", "Parallel Execution Opportunities"),
            (r"## 6\.\s+Handoffs", "Handoffs, Blockers & Escalation Pathways"),
            (r"## 7\.\s+Applicable\s+Conditional\s+Quality\s+Gates", "Applicable Conditional Quality Gates"),
            (r"## 8\.\s+Expected\s+Outputs\s+&\s+Completion\s+Criteria", "Expected Outputs & Completion Criteria"),
        ]

        for wf_file in self.workflows_dir.glob("*.md"):
            content = wf_file.read_text(encoding="utf-8")

            # Check required markdown sections
            for pattern, name in required_sections:
                self.assertTrue(
                    re.search(pattern, content, re.IGNORECASE),
                    f"Workflow {wf_file.name} missing required section: '{name}'"
                )

            # Check Mermaid dependency graph existence
            self.assertIn("```mermaid", content, f"Workflow {wf_file.name} must include a Mermaid dependency graph")

            # Check explicit Mandatory vs Conditional labeling
            self.assertIn("Mandatory", content, f"Workflow {wf_file.name} must explicitly identify Mandatory stages")
            self.assertIn("Conditional", content, f"Workflow {wf_file.name} must explicitly identify Conditional stages")

            # Check routing through CAN-AGT-01
            has_routing = ("CAN-AGT-01" in content or "orchestrator" in content) and "CAN-ENV-01" in content
            self.assertTrue(has_routing, f"Workflow {wf_file.name} must explicitly specify CAN-ENV-01 routing through CAN-AGT-01")

    def test_markdown_links_integrity(self):
        """Verify all local markdown links in workflow files resolve correctly."""
        link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

        for wf_file in self.workflows_dir.glob("*.md"):
            content = wf_file.read_text(encoding="utf-8")
            links = link_regex.findall(content)
            for title, target in links:
                if target.startswith("#") or target.startswith("http://") or target.startswith("https://"):
                    continue
                target_path = (wf_file.parent / target).resolve()
                self.assertTrue(
                    target_path.exists(),
                    f"Broken markdown link in {wf_file.name}: [{title}]({target}) -> {target_path}"
                )


if __name__ == "__main__":
    unittest.main()
