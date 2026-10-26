---
id: "CAN-SKL-XX"
name: "reusable-skill-name"
version: "1.0.0"
category: "Code Intelligence" # Code Intelligence, Precision Mutation, Quality Verification, Ops & Safety
description: >
  Concise explanation of the reusable capability provided by this skill.
trigger_patterns:
  - "trigger phrase 1"
  - "trigger phrase 2"
tools_required:
  - "read_file"
tier_level: 2 # 1: Metadata (always loaded), 2: Core SKILL.md, 3: Deep references/guide.md
instructions_path: "canonical/skills/reusable-skill-name/SKILL.md"
references_path: "canonical/skills/reusable-skill-name/references/guide.md"
---

# Skill: reusable-skill-name

## 1. Purpose & Overview
Brief explanation of when and why any specialist agent should invoke this capability.

## 2. Step-by-Step Execution Workflow
1. **Preparation**: Identify target files, parameters, and prerequisites.
2. **Execution**: Run the specific command or apply the deterministic pattern.
3. **Validation**: Verify that the expected outcome is achieved cleanly.

## 3. Constraints & Guardrails
- Explicit boundaries on what this skill must not do (e.g. no destructive file overwrites).
- Safe fallbacks when tools or dependencies are missing.
