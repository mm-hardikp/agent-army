---
id: "CAN-SKL-07"
name: "pr-description-generator"
version: "1.0.0"
category: "Reliability & Documentation"
description: >
  Generates structured pull request descriptions with change summaries, testing evidence, and preserved human review sections.
trigger_patterns:
  - "generate pr description"
  - "create pr summary"
  - "draft pull request"
  - "pr description"
tools_required:
  - "run_command"
  - "write_to_file"
tier_level: 2
instructions_path: "canonical/skills/pr-description-generator/SKILL.md"
---

# Skill: pr-description-generator

## 1. Purpose & Overview
Generates comprehensive, professional Pull Request (PR) descriptions based on actual git diffs and test results. Strictly preserves human review validation checkpoints.

When to use:
- Preparing completed task branches for code review and PR submission.
- Summarizing multi-file changes across milestone deliverables.

When NOT to use:
- Directly creating remote PRs or merging PRs (requires human gate).

## 2. Step-by-Step Execution Workflow
1. **Extract Diff Summary**: Run git diff against base branch:
   ```bash
   git diff --stat origin/main...HEAD
   ```
2. **Collect Evidence**: Gather test run results and lint reports from completed task handoffs.
3. **Format PR Body**:
   - Title: Semantic PR title (`feat: ...`, `fix: ...`).
   - Summary: Problem solved and architectural approach.
   - Changes: Bulleted list of modified modules and rationale.
   - Verification: Exact test commands and empirical outputs.
   - Preserved `HUMAN:` Section: Explicit placeholder for human reviewer sign-off.
4. **Output**: Save PR draft to `.pr_description.md` or present in task report.

## 3. Constraints & Guardrails
- **Human Section Invariant**: Agents must NEVER generate text inside or modify the `HUMAN:` verification checkpoint of PR descriptions.
- Accurate diff statistics: Never invent modified files or fake test passes.

## 4. Error Handling & Fallbacks
- If base branch is not fetched, diff against `HEAD~1` or local base branch.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1/2 (Draft generation)**.
- Publishing or merging PRs requires human approval.
