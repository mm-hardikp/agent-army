---
id: "CAN-SKL-18"
name: "human-interruption-gateway"
version: "1.0.0"
category: "Ops & Safety"
description: >
  Enforces human-in-the-loop approval gates for Level 3 high-risk actions using the 4-quadrant decision model.
trigger_patterns:
  - "request human approval"
  - "human gate"
  - "prompt user decision"
  - "level 3 confirmation"
  - "interrupt for approval"
tools_required:
  - "write_to_file"
tier_level: 2
instructions_path: "canonical/skills/human-interruption-gateway/SKILL.md"
---

# Skill: human-interruption-gateway

## 1. Purpose & Overview
Enforces the mandatory human approval gate whenever any agent encounters a Level 3 High-Risk operation (destructive deletes, remote pushes, credential modifications, irreversible DDL) or unresolvable architectural conflict. Implements the 4-quadrant decision model.

When to use:
- Before executing any Level 3 High-Risk action (`git push`, `rm -rf`, file deletion, branch deletion, live DB migration).
- Escalating unresolvable contract disputes or architectural disagreements.
- Halting execution when an agent detects contradictory requirements.

When NOT to use:
- Routine Level 1 read operations or Level 2 local edits within assigned workspace files.

## 2. Step-by-Step Execution Workflow
1. **Halt Execution**: Stop autonomous execution immediately upon identifying a Level 3 trigger.
2. **Construct Interruption Record**: Detail exact proposed action, target files/commands, and risk classification.
3. **Present 4-Quadrant Options**:
   - `allow_accept`: Human approves the action and exact parameters.
   - `allow_edit`: Human modifies command, parameters, or target paths before execution.
   - `allow_respond`: Human provides conversational corrective guidance prompting replanning.
   - `allow_ignore`: Human aborts the proposed action cleanly; agent skips to next safe subtask.
4. **Gate Evaluation**:
   - Await explicit user response.
   - Proceed only if `allow_accept` or `allow_edit` is received.
   - If `allow_ignore`, record skipped action and surrender write locks.

## 3. Constraints & Guardrails
- **Zero Bypass**: Agents are strictly prohibited from self-approving Level 3 operations.
- Must present all 4 decision options clearly with context and risk impact.

## 4. Error Handling & Fallbacks
- If user input is ambiguous, treat as `allow_respond` and ask for clarification.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 3 (Human Interruption Authority)**.
- Foundation of the Agent Army's safety and governance framework.
