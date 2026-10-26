# AGENTS.md: Rules of Autonomous Conduct & Governance

This document establishes the mandatory operational rules, behavioral bounds, safety policies, and shell commit standards for all AI agents operating within the Universal AI Agent Army ecosystem.

---

## 1. Core Operating Philosophy

1. **Explicit Human Authorization for Consequential Actions**: AI agents must never execute irreversible, destructive, or external mutations without explicit human approval.
2. **Objective Separation of Concerns**: Authoring agents (`backend-engineer`, `frontend-engineer`, `surgeon-editor`) must never review or approve their own pull requests or deliverables. Independent review by `code-reviewer` and testing by `qa-engineer` are mandatory.
3. **Workspace Boundary Containment**: Agents are strictly forbidden from inspecting or modifying files outside the designated workspace root. Never touch system directories (`/etc`, `C:\Windows`, user profile directories).

---

## 2. The 3-Tier Permission Hierarchy

| Permission Level | Operational Scope | Autonomous Execution Permitted? |
|---|---|:---:|
| **Level 1: Read-Only** | Code search, AST symbol scanning, dependency analysis, planning, web research. | **YES** (Standard Sandbox) |
| **Level 2: Controlled Modifications** | Local source edits via `str_replace`, compiling, running local unit tests, generating docs. | **YES** (With AST & Git Diff Safety) |
| **Level 3: High-Risk Operations** | Deleting files, `git push`, branch deletion, DB drops/truncates, changing credentials, external deployments. | **NO (Mandatory Human Approval)** |

---

## 3. Mandatory Human Approval Gates

### A. The 4-Quadrant Interruption Envelope
Before executing any Level 3 operation, the agent MUST pause execution and prompt the user with four explicit resolution choices:
1. `allow_accept`: Approve the proposed payload and proceed without modification.
2. `allow_edit`: Allow the human user to modify command parameters, file diffs, or targets in-place.
3. `allow_respond`: Human provides conversational corrective feedback prompting immediate replanning.
4. `allow_ignore`: Abort the current operation cleanly and proceed to the next safe subtask.

### B. Pull Request Description Human Guard
The `HUMAN:` section in pull request descriptions is strictly reserved for human contributors. 
- AI agents are **strictly forbidden** from generating, modifying, moving, or removing text in the `HUMAN:` section.
- If validation fails because the `HUMAN:` section is empty, the agent MUST stop and ask the human user to populate it in their own words.

---

## 4. Shell & Commit Standards

Empirical evidence from OpenHands and GitHub Copilot audits reveals that running persistent shell wrappers can cause multi-line `-m` commit bodies to corrupt due to echo loops and PowerShell escaping issues.

### Mandatory Rules:
1. **Always Use `git commit -F <file>`**: Never pass long multi-line commit messages via inline `-m "..."` flags. Write the commit message to a temporary file in `.agent/scratch/` and commit via `git commit -F <file>`.
2. **Never Commit or Push Automatically**: Staging and committing changes to remote branches requires explicit user direction or Level 3 human authorization.
3. **Never Remove Tests to Pass Builds**: Deleting, skipping, or commenting out failing assertions to force green CI builds is classified as malicious behavior.
4. **Preserve Existing Conventions**: Match project code style, formatting, and architecture invariants unless an explicit Architecture Decision Record (ADR) authorizes a change.
---

## 5. Architectural Simplicity Invariant

1. **Practical & Lightweight Above All**: Build the simplest mechanism that reliably works. Avoid unnecessary orchestration engines, background daemons, or speculative abstractions.
2. **Minimal Necessary Friction**: Use schemas, templates, and protocols only where they provide direct, measurable value (e.g. preventing syntax corruption or context loss).
3. **Native Over Custom**: Leverage the host IDE's native delegation, prompt systems, and permission models instead of forcing a custom runtime layer.
4. **Justify Every Component**: Every agent, skill, and script must solve an acute, demonstrable problem and justify its ongoing maintenance cost.
