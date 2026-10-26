# Universal AI Agent Army — Orchestrator Entry Point

Welcome to the **Universal AI Agent Army**. This repository contains a fully autonomous, lightweight multi-agent engineering organization coordinated by a central Orchestrator agent (`CAN-AGT-01`).

---

## Quick Start: How to Run in Any IDE

To launch the Agent Army, open this repository in your preferred AI-enabled IDE (Google Antigravity, Claude Code, Cursor, or VS Code with GitHub Copilot) and paste this prompt into the AI chat:

```markdown
Act as our project Orchestrator following canonical/agents/orchestrator.md and AGENTS.md.
Review PROJECT_STATE.md to understand the current project status, then recommend and execute the next task using canonical/workflows/.
```

That's it! The IDE's AI agent will assume the Orchestrator persona, inspect the persistent roadmap ledger, select specialist agents from `canonical/agents/`, provision skills from `canonical/skills/`, and coordinate execution using the IDE's native tools.

---

## Core Architecture Principles

1. **One Central Orchestrator**: `CAN-AGT-01` coordinates all activities, delegates atomic tasks, tracks dependencies, resolves blockers, and presents delivery reports. It **never** writes domain feature code directly.
2. **Specialist Domain Agents**: 17 domain specialists (Backend, Frontend, Database, QA, Security, Code Review, etc.) execute specific implementation tasks under non-overlapping file reservations.
3. **No Heavy Infrastructure**: Operates directly on standard markdown files, schemas, and native IDE tool calls. No daemon services or background servers required.
4. **Conditional Quality Gates**: Quality checks are applied proportionally (e.g. documentation updates skip full QA runners; code changes require syntax linting and adversarial review).
5. **Persistent State**: Current milestone status, verified evidence, and next recommended actions are maintained in [PROJECT_STATE.md](PROJECT_STATE.md).

---

## Available Cognitive Workflows

When directing the Orchestrator, you can invoke any of the 10 approved canonical workflows:

| Workflow ID | Workflow Name | When to Use |
|:---:|---|---|
| `CAN-WFL-01` | [full-cycle-feature-development.md](canonical/workflows/full-cycle-feature-development.md) | Multi-tier feature delivery from requirements to QA |
| `CAN-WFL-02` | [surgical-bug-investigation-and-fix.md](canonical/workflows/surgical-bug-investigation-and-fix.md) | Hypothesis-driven bug triage, minimal reproduction, surgical patch |
| `CAN-WFL-03` | [independent-adversarial-code-review.md](canonical/workflows/independent-adversarial-code-review.md) | Multi-pass adversarial code review on git diffs |
| `CAN-WFL-04` | [technical-research-and-spike.md](canonical/workflows/technical-research-and-spike.md) | Exploratory research, library benchmarking, feasibility spikes |
| `CAN-WFL-05` | [architecture-decision-and-system-design.md](canonical/workflows/architecture-decision-and-system-design.md) | Subsystem design, contract specification, and ADR authoring |
| `CAN-WFL-06` | [database-schema-and-migration-lifecycle.md](canonical/workflows/database-schema-and-migration-lifecycle.md) | Zero-downtime database migrations, index optimization, rollback checks |
| `CAN-WFL-07` | [documentation-and-drift-remediation.md](canonical/workflows/documentation-and-drift-remediation.md) | AST-based code inspection and documentation synchronization |
| `CAN-WFL-08` | [application-security-and-vulnerability-audit.md](canonical/workflows/application-security-and-vulnerability-audit.md) | Secret scanning, license compliance, SAST vulnerability review |
| `CAN-WFL-09` | [automated-test-suite-expansion.md](canonical/workflows/automated-test-suite-expansion.md) | Test coverage gap discovery, unit/integration test authoring |
| `CAN-WFL-10` | [parallel-multi-agent-worktree-swarm.md](canonical/workflows/parallel-multi-agent-worktree-swarm.md) | High-throughput concurrent execution across disjoint workstreams |

---

## Optional: IDE Adapter Compilation

While this repository works immediately without any build step, you can optionally generate native IDE configuration shims (for automatic prompt injection or slash commands) by running:

```bash
# Generate native shims for all IDEs
python adapters/compile.py --target all

# Or target a specific IDE:
python adapters/compile.py --target cursor
python adapters/compile.py --target claude
python adapters/compile.py --target antigravity
python adapters/compile.py --target copilot

# To remove generated shims at any time:
python adapters/compile.py --clean
```

All generated files are thin pointers referencing `canonical/`. Your canonical assets remain the single source of truth.
