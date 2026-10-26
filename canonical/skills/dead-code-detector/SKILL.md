---
id: "CAN-SKL-13"
name: "dead-code-detector"
version: "1.0.0"
category: "Code Intelligence"
description: >
  Identifies unreachable functions, abandoned exports, dead routes, and orphan test fixtures across the workspace.
trigger_patterns:
  - "find dead code"
  - "detect unused exports"
  - "check orphaned files"
  - "audit unused functions"
  - "clean dead code"
tools_required:
  - "run_command"
  - "grep_search"
  - "read_file"
tier_level: 2
instructions_path: "canonical/skills/dead-code-detector/SKILL.md"
---

# Skill: dead-code-detector

## 1. Purpose & Overview
Discovers unreferenced exports, obsolete functions, orphaned files, and abandoned test fixtures to keep codebases lean and maintainable.

When to use:
- Post-refactoring cleanups.
- Auditing legacy codebases during initial onboarding.
- Identifying dead code candidates before major architectural changes.

When NOT to use:
- Blindly deleting code without human review (deletions are Level 3 operations).
- Auditing public library exports that are meant for external consumers.

## 2. Step-by-Step Execution Workflow
1. **Symbol Inventory**: Extract declared symbols using `tools/scan_ast.py`.
2. **Reference Cross-Check**: For exported functions and classes, perform codebase-wide reference searches using `grep_search`.
3. **Filter Legitimate Exports**: Exclude public entry points (`main`, `index.js`, `api routes`, framework lifecycle hooks).
4. **Candidate Reporting**: Group candidates by file with line numbers and usage counts (0 references).
5. **Human Gate**: Present deletion candidate list to human reviewer before removing any code.

## 3. Constraints & Guardrails
- Never delete identified dead code automatically. Always prompt the human reviewer.
- Check dynamic imports, reflection, and string references before classifying code as dead.

## 4. Error Handling & Fallbacks
- If project tooling provides a native dead-code tool (e.g. `ts-prune`, `vulture`, `cargo-deadlinks`), invoke that tool first.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Detection)**.
- Deleting files or code blocks is **Level 2/3** and requires human confirmation.
