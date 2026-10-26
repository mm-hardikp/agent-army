# Governance Policy: Human Approval & Safety Boundaries

This policy establishes the operational permission boundaries, safety rules, and human approval protocols for all autonomous agents in the Universal AI Agent Army.

---

## 1. Permission Levels & Operational Scopes

| Level | Classification | Description & Allowed Scope | Autonomous Execution? |
|:---:|---|---|:---:|
| **Level 1** | **Read-Only** | Code search, AST symbol scanning (`tools/scan_ast.py`), dependency tree inspection, architecture planning, documentation reading. | **YES** (Standard Sandbox) |
| **Level 2** | **Controlled Modification** | Modifying local files within assigned domain scope, creating test files, running local unit tests, compiling code, local AST linting (`tools/lint_ast.py`). | **YES** (Monitored with pre/post checks) |
| **Level 3** | **High-Risk Operations** | Deleting files, modifying credentials/secrets, `git push`, branch deletion, DB drops/truncates, infrastructure provisioning. | **NO (Mandatory Human Approval)** |

---

## 2. The 4-Quadrant Human Interruption Model

Whenever an agent encounters a Level 3 operation or unresolvable architectural conflict, it MUST halt execution and present the user with four explicit options:

1. **`allow_accept`**: Human approves the proposed operation and parameters exactly as specified.
2. **`allow_edit`**: Human modifies the parameters, target file paths, or command string before execution.
3. **`allow_respond`**: Human provides conversational feedback or corrective guidance prompting the Orchestrator to replan.
4. **`allow_ignore`**: Human aborts the proposed operation cleanly, allowing the agent to proceed to the next safe subtask.

---

## 3. Workspace & File Safety Rules

1. **Workspace Boundary Containment**: Agents must never read or modify files outside the active workspace directory. Touching OS directories (`C:\Windows`, `/etc`, `/var`, user profile roots) is strictly prohibited.
2. **Atomic File Modifications**: File modifications should be surgical and deterministic (using `replace_file_content` or `str_replace`), avoiding destructive blind full-file overwrites.
3. **Safe Lock Lease Surrender**: File write leases must be surrendered immediately upon task completion, cancellation, or blocker escalation.

---

## 4. Commit & Remote Push Restrictions

1. **Mandatory `git commit -F <file>`**: To prevent shell wrapper echo loops from corrupting multi-line commit messages, all commit messages must be written to a temporary file first and committed using `-F <file>`.
2. **Zero Automatic Push**: Agents may stage commits locally in task branches, but executing `git push` to remote repositories strictly requires Level 3 human authorization.
3. **Never Falsify Review / Human Sections**: Agents are strictly forbidden from modifying or generating text inside the `HUMAN:` validation section of PR descriptions.
