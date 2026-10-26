---
id: "CAN-SKL-06"
name: "git-atomic-committer"
version: "1.0.0"
category: "Ops & Safety"
description: >
  Executes atomic, focused git commits using temporary file commit messages with zero automatic remote pushes.
trigger_patterns:
  - "atomic commit"
  - "git commit"
  - "stage task commit"
  - "safe commit"
  - "record commit"
tools_required:
  - "run_command"
  - "write_to_file"
tier_level: 2
instructions_path: "canonical/skills/git-atomic-committer/SKILL.md"
---

# Skill: git-atomic-committer

## 1. Purpose & Overview
Creates clean, single-purpose git commits corresponding to completed task milestones. Uses temporary file commit messages (`git commit -F <file>`) to prevent multi-line shell escaping corruption.

When to use:
- Recording completed, verified subtasks in local task branches.
- Committing validated changes before handoff or task completion.

When NOT to use:
- Committing failing code or unverified changes.
- Pushing to remote repositories (`git push` is Level 3 and strictly requires human approval).

## 2. Step-by-Step Execution Workflow
1. **Status & Diff Review**: Inspect modified files:
   ```bash
   git status --short
   git diff --stat
   ```
2. **Stage Specific Files**: Stage only the files modified for the current task:
   ```bash
   git add path/to/file1 path/to/file2
   ```
3. **Write Commit Message**: Write commit message adhering to Conventional Commits format to a temporary file:
   - Example: `feat(api): add healthcheck endpoint`
4. **Commit with -F**: Execute commit referencing message file:
   ```bash
   git commit -F .git_msg_tmp.txt
   ```
5. **Cleanup**: Remove temporary message file.

## 3. Constraints & Guardrails
- **Mandatory `-F <file>`**: Never use inline `git commit -m "multi\nline"` in PowerShell/bash due to shell corruption risks.
- **Zero Auto-Push**: Never execute `git push` autonomously.
- **Atomic Commits**: One commit per completed task milestone. Never bundle unrelated changes.

## 4. Error Handling & Fallbacks
- If pre-commit hooks fail, review the hook errors, correct the files, and re-stage before retrying commit.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Modification)** for local git commits.
- **Level 3 (High-Risk)** for `git push`, branch deletion, or force commits (`--force`), which strictly require explicit human authorization.
