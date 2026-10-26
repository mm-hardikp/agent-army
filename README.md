# Universal AI Agent Army

## 1. Project Philosophy & Vision

The **Universal AI Agent Army** is an independent, general-purpose multi-agent architecture designed to operate natively inside modern AI-powered developer environments (Claude Code, Antigravity, Cursor, and VS Code with GitHub Copilot).

### Core Architectural Principles:
1. **One Canonical Library, Multiple Adapters**: We author canonical agent, skill, and workflow definitions once in machine-validatable YAML/Markdown (`canonical/`). Automated compiler scripts transpile these into native IDE configurations (`adapters/`).
2. **Zero-Daemon Execution**: No mandatory external orchestration servers, Docker daemons, or cloud gateways are required. The ecosystem is fully portable and runs directly in the developer's local IDE workspace.
3. **Strict Division of Responsibility**: The central Orchestrator coordinates tasks, dependency DAGs, and two-way handoffs (`CAN-ENV-01 v2.2`), but *never performs domain implementation work directly*, preserving its context window for high-level decision making.
4. **Independent Quality Verification**: Authoring agents cannot act as their own code reviewer or QA tester. Verification is decoupled, multi-staged, and strictly conditional on the task type (software, research, documentation).
5. **Human-in-the-Loop Safety**: Consequential or destructive operations (deployments, git push, database drops, file deletions) are strictly gated by a 4-quadrant human interruption envelope (`allow_accept`, `allow_edit`, `allow_respond`, `allow_ignore`).

---

## 2. Directory Index & Asset Classification

The repository enforces a strict three-way asset classification:

```
agent-army/
├── [CANONICAL SOURCE OF TRUTH] - (Human-authored, tracked in git)
│   ├── README.md                    # Master documentation & philosophy
│   ├── LICENSE                      # MIT License
│   ├── AGENTS.md                    # Agent conduct rules, human approval sections, commit safety
│   ├── canonical/
│   │   ├── schemas/                 # Machine-validatable JSON schemas (agent, skill, protocol)
│   │   ├── templates/               # Standard authoring templates
│   │   ├── agents/                  # 18 Canonical Agent Specifications (CAN-AGT-SPEC)
│   │   ├── skills/                  # 18 Reusable Skills (SKILL.md + references/guide.md)
│   │   ├── workflows/               # 10 Reusable Cognitive Workflows (CAN-WFL-*)
│   │   ├── protocols/               # CAN-ENV-01 v2.2 schemas & state machine contracts
│   │   └── policies/                # 3-tier permission hierarchy & human approval rules
│   ├── tools/                       # Standalone portable helper CLI tools (scan_ast, lint_ast)
│   ├── scripts/                     # Build, validation & compiler scripts (compile_adapters.py)
│   └── tests/                       # Automated unit tests for tools, schemas & compilers
│
├── [GENERATED ADAPTER OUTPUTS] - (Machine-compiled from canonical/, read-only build outputs)
│   └── adapters/
│       ├── claude-code/             # .claude/agents/*.md
│       ├── antigravity/             # .agents/skills/ & rules/
│       ├── cursor/                  # .cursor/rules/*.mdc & modular slash commands
│       └── copilot/                 # .github/copilot-instructions/ & slash commands
│
└── [TEMPORARY BUILD ARTIFACTS] - (Gitignored, regenerated on build)
    ├── .agent/                      # Local runtime state (state.json, locks.json)
    └── .worktrees/                  # Ephemeral concurrency worktrees (CAN-WFL-10)
```

---

## 3. Operational Battalions (18 Canonical Agents)

1. **Command & Control**: `orchestrator`
2. **Strategy & Discovery**: `product-analyst`, `system-architect`
3. **Core Engineering**: `backend-engineer`, `frontend-engineer`, `database-specialist`, `fullstack-integrator`
4. **Precision Mutation & Quality**: `surgeon-editor`, `code-reviewer`, `syntax-verifier`, `qa-engineer`, `security-auditor`
5. **Reliability & Documentation**: `debugger-detective`, `devops-platform`, `docs-technical-writer`, `research-investigator`
6. **Data & Automation**: `data-analyst`, `automation-specialist`

---

## 4. Governance & Safety Summary

All autonomous agents operating in this repository must strictly adhere to [`AGENTS.md`](AGENTS.md). Level 3 high-risk actions require explicit human authorization.
