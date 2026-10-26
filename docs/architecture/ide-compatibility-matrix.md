# IDE Compatibility Matrix & Adapter Architecture (Refined Phase 1A.1)

## 1. Executive Summary & Reality Check

Our Universal AI Agent Army targets four primary IDE environments: **Antigravity**, **Claude Code**, **Cursor**, and **VS Code with GitHub Copilot**.

### Confirmed Architectural Decisions:
1. **Cursor & VS Code/Copilot Adapters (Option A Accepted)**:
   - Generate **modular slash command files** (`/plan`, `/implement`, `/review`, `/test`).
   - Strictly maintain **guided sequential execution** where autonomous delegation is unsupported.
2. **Helper Tool Distribution (Option A Accepted)**:
   - Distribute helper tools as **portable Python scripts** (`scan_ast.py`, `lint_ast.py`, `with_server.py`) with native project tooling fallbacks (`tsc`, `cargo`, `go build`). Do not introduce compiled binary bloat.

---

## 2. Granular IDE Capability Matrix

| Capability Dimension | Claude Code | Antigravity | Cursor | VS Code / Copilot |
|---|:---:|:---:|:---:|:---:|
| **Central Orchestration Model** | **A (Native)**: CLI subagent delegation via Task tools. | **A (Native)**: Subagent tool calling & multi-agent execution. | **B (Adapter-Guided)**: Modular slash commands (`/plan`, `/implement`, `/review`, `/test`). | **C (User-Triggered)**: Modular slash commands (`/plan`, `/implement`, `/review`, `/test`). |
| **Subagent Delegation** | **A (Native)**: Coordinator summons subagents autonomously. | **A (Native)**: Built-in subagent tool calling. | **B (Adapter-Guided)**: User-guided sequential persona adoption. | **C (User-Triggered)**: User directs agent `@workspace /role`. |
| **Structured Message Handoffs** | **A (Native)**: Tool call payload returns JSON envelope. | **A (Native)**: Ingests & emits structured `.agent/handoffs/`. | **B (Adapter)**: Reads & writes `.agent/state.json` file. | **B (Adapter)**: Reads & writes `.agent/state.json` file. |
| **Parallel Execution** | **A (Native)**: Spawns parallel background tasks. | **A (Native)**: Background tasks & subagents. | **D (Unsupported)**: Composer is single active stream. | **D (Unsupported)**: Copilot chat is single conversational stream. |
| **Concurrent File Isolation** | **B (Adapter)**: Git worktree isolator (`CAN-WFL-10`). | **B (Adapter)**: Git worktree isolator (`CAN-WFL-10`). | **D (Unsupported)**: Shared active workspace only. | **D (Unsupported)**: Shared active workspace only. |
| **Sandboxing & Permissions** | **A (Native)**: Native bash/command approval gates. | **A (Native)**: Built-in Sandbox (`BypassSandbox: true/false`). | **C (User-Intervention)**: IDE-level tool confirmation toggles. | **C (User-Intervention)**: Extension approval prompts. |
| **Zero-Daemon Compliance** | **Yes** (Pure CLI) | **Yes** (Native IDE runtime) | **Yes** (No daemon required) | **Yes** (No daemon required) |

---

## 3. Host-Specific Adapter Strategy

### 1. Claude Code
- **Adapter Output**: `.claude/agents/<agent-name>.md`
- **Orchestration**: Fully autonomous. The Orchestrator calls specialist subagents natively using Claude's internal subagent tools, passing `CAN-ENV-01` handoffs in tool parameters.

### 2. Antigravity
- **Adapter Output**: `.agents/skills/<skill-name>/SKILL.md` and customization rules.
- **Orchestration**: Fully autonomous. Leverages native subagent delegation and the local workspace `.agent/state.json` ledger. Sandboxing maps cleanly to `BypassSandbox: false` (Level 1/2) and `BypassSandbox: true` (Level 3).

### 3. Cursor
- **Adapter Output**: `.cursor/rules/<agent-name>.mdc` and modular prompt commands.
- **Orchestration**: Guided Sequential (Option A). Cursor Composer acts as the single active executor. Modular slash commands (`/plan`, `/implement`, `/review`, `/test`) guide the developer step-by-step, reading and updating `.agent/state.json`.

### 4. VS Code with GitHub Copilot
- **Adapter Output**: `.github/copilot-instructions.md` and modular slash command templates.
- **Orchestration**: Guided Sequential (Option A). Copilot does not autonomously spawn child subagents. The adapter generates structured slash commands (`/plan`, `/implement`, `/review`, `/test`) that guide the developer through the multi-agent lifecycle step-by-step.
