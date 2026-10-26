import os
import sys
import json
import unittest
from pathlib import Path

base_dir = Path(__file__).parent.parent
sys.path.insert(0, str(base_dir / "scripts"))

from validate_canonical import parse_frontmatter, validate_dict_against_schema, validate_file


class TestCanonicalSchemas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas_dir = base_dir / "canonical" / "schemas"
        cls.templates_dir = base_dir / "canonical" / "templates"
        cls.skills_dir = base_dir / "canonical" / "skills"
        cls.agents_dir = base_dir / "canonical" / "agents"
        cls.agent_schema = json.loads((cls.schemas_dir / "agent.schema.json").read_text(encoding="utf-8"))
        cls.skill_schema = json.loads((cls.schemas_dir / "skill.schema.json").read_text(encoding="utf-8"))
        cls.envelope_schema = json.loads((cls.schemas_dir / "envelope.schema.json").read_text(encoding="utf-8"))

    def test_agent_template_validation(self):
        template_path = self.templates_dir / "agent-template.md"
        errors = validate_file(template_path, self.agent_schema)
        self.assertEqual(errors, [], f"Agent template failed schema validation: {errors}")

    def test_skill_template_validation(self):
        template_path = self.templates_dir / "skill-template.md"
        errors = validate_file(template_path, self.skill_schema)
        self.assertEqual(errors, [], f"Skill template failed schema validation: {errors}")

    def test_all_18_canonical_skills_validation(self):
        skill_files = list(self.skills_dir.glob("*/SKILL.md"))
        self.assertEqual(len(skill_files), 18, f"Expected 18 canonical skills, found {len(skill_files)}")

        seen_ids = set()
        seen_names = set()

        for sf in skill_files:
            errors = validate_file(sf, self.skill_schema)
            self.assertEqual(errors, [], f"Skill '{sf.parent.name}' failed validation: {errors}")

            data = parse_frontmatter(sf.read_text(encoding="utf-8"))
            skill_id = data.get("id")
            skill_name = data.get("name")

            self.assertNotIn(skill_id, seen_ids, f"Duplicate skill ID detected: {skill_id}")
            self.assertNotIn(skill_name, seen_names, f"Duplicate skill name detected: {skill_name}")
            seen_ids.add(skill_id)
            seen_names.add(skill_name)

        expected_ids = {f"CAN-SKL-{i:02d}" for i in range(1, 19)}
        self.assertEqual(seen_ids, expected_ids, f"Mismatch in canonical skill IDs: {expected_ids - seen_ids}")

    def test_all_18_canonical_agents_validation(self):
        agent_files = list(self.agents_dir.glob("*.md"))
        self.assertEqual(len(agent_files), 18, f"Expected 18 canonical agent definitions, found {len(agent_files)}")

        expected_agents = {
            "CAN-AGT-01": "orchestrator",
            "CAN-AGT-02": "product-analyst",
            "CAN-AGT-03": "system-architect",
            "CAN-AGT-04": "backend-engineer",
            "CAN-AGT-05": "frontend-engineer",
            "CAN-AGT-06": "database-specialist",
            "CAN-AGT-07": "fullstack-integrator",
            "CAN-AGT-08": "surgeon-editor",
            "CAN-AGT-09": "code-reviewer",
            "CAN-AGT-10": "syntax-verifier",
            "CAN-AGT-11": "qa-engineer",
            "CAN-AGT-12": "security-auditor",
            "CAN-AGT-13": "debugger-detective",
            "CAN-AGT-14": "devops-platform",
            "CAN-AGT-15": "docs-technical-writer",
            "CAN-AGT-16": "research-investigator",
            "CAN-AGT-17": "data-analyst",
            "CAN-AGT-18": "automation-specialist"
        }

        seen_ids = {}
        for af in agent_files:
            errors = validate_file(af, self.agent_schema)
            self.assertEqual(errors, [], f"Agent '{af.name}' failed schema validation: {errors}")

            data = parse_frontmatter(af.read_text(encoding="utf-8"))
            agent_id = data.get("id")
            agent_name = data.get("name")

            self.assertNotIn(agent_id, seen_ids, f"Duplicate agent ID detected: {agent_id}")
            seen_ids[agent_id] = agent_name

            # Verify referenced skills actually exist in canonical/skills/
            for skill_ref in data.get("skills_required", []):
                skill_path = self.skills_dir / skill_ref / "SKILL.md"
                self.assertTrue(skill_path.exists(), f"Agent '{agent_name}' references non-existent skill '{skill_ref}' at {skill_path}")

        # Assert IDs match the exact approved CAN-AGT-01 through CAN-AGT-18 roster
        self.assertEqual(seen_ids, expected_agents, "Mismatch in approved canonical agent roster IDs or names")

    def test_agent_schema_invalid_missing_field(self):
        invalid_data = {
            "id": "CAN-AGT-01",
            "name": "orchestrator",
            "version": "1.0.0"
        }
        errors = validate_dict_against_schema(invalid_data, self.agent_schema, "invalid_agent")
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("Missing required field: 'role'" in e for e in errors))

    def test_agent_schema_invalid_id_pattern(self):
        invalid_data = {
            "id": "INVALID-ID",
            "name": "orchestrator",
            "version": "1.0.0",
            "battalion": "Command & Control",
            "description": "Valid description length here",
            "role": "Orchestrator Lead",
            "goal": "Coordinate child agents efficiently",
            "backstory": "Experienced coordinator with high focus",
            "permission_level": 1,
            "tools_required": ["read_file"],
            "skills_required": [],
            "boundaries": {"authorized": ["planning"], "prohibited": ["coding"]}
        }
        errors = validate_dict_against_schema(invalid_data, self.agent_schema, "bad_id_agent")
        self.assertTrue(any("does not match pattern" in e for e in errors))

    def test_skill_schema_valid_and_invalid(self):
        valid_skill = {
            "id": "CAN-SKL-01",
            "name": "ast-scanner",
            "version": "1.0.0",
            "category": "Code Intelligence",
            "description": "Performs fast AST symbol scanning",
            "trigger_patterns": ["scan ast", "find symbols"],
            "tools_required": ["read_file"],
            "tier_level": 1
        }
        errors = validate_dict_against_schema(valid_skill, self.skill_schema, "valid_skill")
        self.assertEqual(errors, [])

        invalid_skill = dict(valid_skill)
        invalid_skill["tier_level"] = 99
        errors = validate_dict_against_schema(invalid_skill, self.skill_schema, "invalid_skill")
        self.assertTrue(any("invalid value '99'" in e for e in errors))

    def test_protocol_envelope_all_13_message_types(self):
        all_13_types = [
            "TASK_ASSIGNMENT",
            "TASK_ACCEPTANCE",
            "TASK_COMPLETION",
            "HANDOFF",
            "CLARIFICATION_REQUEST",
            "CHANGE_REQUEST",
            "REVIEW_FINDING",
            "BLOCKER",
            "DISAGREEMENT",
            "APPROVAL_REQUEST",
            "APPROVAL_RESPONSE",
            "TASK_REASSIGNMENT",
            "TASK_CANCELLATION"
        ]
        self.assertEqual(len(all_13_types), 13)

        base_envelope = {
            "version": "2.2.0",
            "message_id": "MSG-2026-0001",
            "correlation_id": "CORR-01",
            "task_id": "TASK-01",
            "timestamp": "2026-10-24T18:00:00Z",
            "sending_agent": "orchestrator",
            "receiving_agent": "backend-engineer",
            "status_summary": "Testing message types",
            "explicit_next_action": {
                "recommended_target": "backend-engineer",
                "required_action": "Execute task"
            }
        }

        for msg_type in all_13_types:
            envelope = dict(base_envelope)
            envelope["message_type"] = msg_type
            errors = validate_dict_against_schema(envelope, self.envelope_schema, f"envelope_{msg_type}")
            self.assertEqual(errors, [], f"Valid message_type '{msg_type}' failed validation: {errors}")

    def test_protocol_envelope_invalid_message_type(self):
        invalid_envelope = {
            "version": "2.2.0",
            "message_id": "MSG-2026-0001",
            "correlation_id": "CORR-01",
            "task_id": "TASK-01",
            "timestamp": "2026-10-24T18:00:00Z",
            "message_type": "NON_EXISTENT_TYPE",
            "sending_agent": "orchestrator",
            "receiving_agent": "backend-engineer",
            "status_summary": "Testing invalid type",
            "explicit_next_action": {
                "recommended_target": "backend-engineer",
                "required_action": "Execute task"
            }
        }
        errors = validate_dict_against_schema(invalid_envelope, self.envelope_schema, "invalid_envelope")
        self.assertTrue(any("invalid value 'NON_EXISTENT_TYPE'" in e for e in errors))

    def test_missing_frontmatter_delimiters(self):
        bad_md = "This markdown file has no frontmatter delimiters."
        with self.assertRaises(ValueError):
            parse_frontmatter(bad_md)


if __name__ == "__main__":
    unittest.main()
