# Phase 1B: Canonical Foundation Implementation Plan (Refined)

## 1. Executive Summary & Design Mission

Phase 1B executes the construction of the canonical **Universal AI Agent Army** based on the approved Phase 1A.1 architectural specifications.

### Core Architectural Axioms:
1. **Standards Before Content**: Machine-validatable JSON schemas, canonical specification standards (`CAN-AGT-SPEC`, `CAN-SKL-SPEC`), and communication contracts (`CAN-ENV-01 v2.2`) are established and tested *first*, before authoring any of the 18 agents, 18 skills, or 10 workflows.
2. **Lean Tooling Scope**: Tooling is strictly limited to capabilities that cannot be provided natively by IDEs or project build tools.
3. **Canonical vs. Generated Separation**: Canonical files (`canonical/`) are the sole human-authored source of truth; IDE adapters (`adapters/`) are read-only generated outputs transpiled by automated build scripts.
4. **Honest Host Capability Alignment**: Adapters adhere to official platform specifications (Claude Code `.claude/agents/`, Antigravity `.agents/skills/`, Cursor `.cursor/rules/*.mdc`, VS Code Copilot modular instructions), explicitly reflecting single-stream vs. multi-agent execution realities.

---

## 2. Re-evaluated Tooling Scope

We critically re-evaluated the three standalone helper tools proposed in early drafts to avoid duplicating native host capabilities:

| Candidate Tool | Evaluation vs. Native IDE / Compiler Capabilities | Final Decision | Justification |
|---|---|:---:|---|
| **`scan_ast.py`** | IDEs have built-in file search and grep, but lack token-efficient AST symbol extraction. LLMs reading entire repos cause context overflow. | **RETAIN** (Essential) | Extracted from `REPO-002` (`scan.py`). Parses AST symbols (classes, functions, signatures) in Python/TS/JS into compact index summaries (~80% token savings). |
| **`lint_ast.py`** | Compilers (`tsc`, `cargo`, `go build`) validate syntax, but only after files are written to disk and whole projects are built (slow). Linters catch subtle syntax errors instantly. | **RETAIN with Fallback** (Essential) | Extracted from `REPO-007` (`openhands-aci`). Provides sub-second AST pre-commit checks across 14 languages. Includes automatic fallback to native project compiler (`tsc`, `cargo`) if Python Tree-sitter bindings are absent. |
| **`with_server.py`** | Node/Python projects already provide `concurrently`, `start-server-and-test`, or background bash jobs (`npm run dev &`). | **SIMPLIFY TO LIGHTWEIGHT SCRIPT** | Heavy Python wrapper rejected. Replaced by a minimal, portable 40-line script (`tools/ephemeral_server.py`) used strictly for headless Playwright test harnesses (`CAN-SKL-09`). |

---

## 3. Strict Classification of Repository Assets

The target repository structure at `C:\Agent-Army\agent-army\` strictly classifies assets into three mutually exclusive categories:

```
agent-army/
├── [CANONICAL SOURCE OF TRUTH] - (Human-authored, tracked in git)
│   ├── README.md, LICENSE, AGENTS.md
│   ├── canonical/
│   │   ├── schemas/                 # JSON Schemas: agent.schema.json, skill.schema.json, env-01.schema.json
│   │   ├── templates/               # Standard markdown templates for agents and skills
│   │   ├── agents/                  # 18 Canonical Agent Markdown Specs (CAN-AGT-SPEC)
│   │   ├── skills/                  # 18 Canonical Skills (SKILL.md + references/guide.md)
│   │   ├── workflows/               # 10 Reusable Cognitive Workflows (CAN-WFL-*)
│   │   ├── protocols/               # CAN-ENV-01 v2.2 schemas & state machine contracts
│   │   └── policies/                # 3-tier permission hierarchy & human approval rules
│   ├── tools/                       # Lean, standalone helper CLI scripts (scan_ast.py, lint_ast.py)
│   ├── scripts/                     # Build, validation & compiler scripts (compile_adapters.py, validate_canonical.py)
│   └── tests/                       # Automated unit tests for tools, schemas & compilers
│
├── [GENERATED ADAPTER OUTPUTS] - (Machine-compiled from canonical/, read-only build outputs)
│   └── adapters/
│       ├── claude-code/             # .claude/agents/*.md
│       ├── antigravity/             # .agents/skills/ & rules/
│       ├── cursor/                  # .cursor/rules/*.mdc & modular slash prompts
│       └── copilot/                 # .github/copilot-instructions/ & slash prompts
│
└── [TEMPORARY BUILD ARTIFACTS] - (Gitignored, regenerated on build)
    ├── .agent/                      # Local runtime state (state.json, locks.json, messages.json)
    ├── .worktrees/                  # Ephemeral concurrency worktrees (CAN-WFL-10)
    └── build/                       # Compilation caches and validation reports
```

---

## 4. Reordered Implementation Sequence (Standards First)

The milestone sequence has been reordered to guarantee that **standards, schemas, and templates are implemented and validated before generating content**:

```mermaid
graph TD
    M1[Milestone 1: Repository Skeleton, Governance & Standalone Tools] --> M2[Milestone 2: Protocol Schemas, Agent/Skill Standards & Validation Engine]
    M2 --> M3[Milestone 3: Canonical Skills Repository (18 Skills)]
    M2 --> M4[Milestone 4: Command Core & Orchestrator (CAN-AGT-01 to 03)]
    M3 --> M5[Milestone 5: Specialist Engineering Battalions (CAN-AGT-04 to 18)]
    M4 --> M5
    M5 --> M6[Milestone 6: Standardized Cognitive Workflows (10 Workflows)]
    M6 --> M7[Milestone 7: Compiler Pipeline & Multi-IDE Adapters]
    M7 --> M8[Milestone 8: Automated Verification & Integration Simulation]
```

### Milestone 1: Repository Skeleton, Governance & Lean Standalone Tools
- **Objective**: Establish the physical repository foundation, root contributor governance, and lean helper utilities.
- **Tasks**:
  1. Initialize directory layout under `C:\Agent-Army\agent-army\`.
  2. Author root governance files: `README.md`, `LICENSE` (MIT), and `AGENTS.md` (codifying human review gates, commit standards via `git commit -F`, and boundary rules).
  3. Implement lean standalone helper tools in `tools/`:
     - `scan_ast.py` (AST symbol parser).
     - `lint_ast.py` (Tree-sitter syntax validator with native compiler fallback).
     - `ephemeral_server.py` (lightweight test server wrapper).
  4. Author unit tests in `tests/`: `test_scan_ast.py`, `test_lint_ast.py`.
- **Validation Criteria**: Unit tests pass 100% locally with `pytest`.

### Milestone 2: Protocol Schemas, Agent/Skill Standards & Validation Engine
- **Objective**: Establish machine-validatable JSON schemas, markdown templates, and automated linter scripts *before* content authoring begins.
- **Tasks**:
  1. Author JSON schemas in `canonical/schemas/`:
     - `can-agt.schema.json` (validates agent YAML frontmatter, role, goal, backstory, tools, boundaries).
     - `can-skl.schema.json` (validates skill metadata, progressive disclosure tiers, triggers).
     - `can-env-01.schema.json` (validates all 13 CAN-ENV-01 v2.2 message types, correlation IDs, idempotency keys, and cancellation payloads).
     - `state-ledger.schema.json` (validates `.agent/state.json` FSM transitions).
     - `lock-registry.schema.json` (validates atomic two-phase write locks in `.agent/locks.json`).
  2. Create standard authoring templates in `canonical/templates/`: `agent-template.md`, `skill-template.md`.
  3. Author `canonical/policies/permission-hierarchy.md` and `human-approval-rules.md`.
  4. Implement `scripts/validate_canonical.py` to automatically validate all canonical markdown files against schemas.
- **Validation Criteria**: `validate_canonical.py` executes cleanly against templates; `tests/test_protocol_schemas.py` passes 100%.

### Milestone 3: Canonical Skills Repository (18 Skills)
- **Objective**: Build the shared technical capabilities that agents will invoke.
- **Tasks**:
  - Author all 18 `SKILL.md` packages in `canonical/skills/` adhering to the 3-tier progressive disclosure model:
    - *Tier 1 (Metadata)*: `name`, `description`, `trigger_patterns`.
    - *Tier 2 (Core)*: Step-by-step instructions, constraints, tool requirements.
    - *Tier 3 (Deep Reference)*: `references/guide.md` and executable scripts.
- **Parallel Execution**: Safe to author in 4 parallel domain batches (Code Intelligence, Precision Mutation, Testing/QA, Ops/Security).
- **Validation Criteria**: `python scripts/validate_canonical.py --skills` passes 100% against `can-skl.schema.json`.

### Milestone 4: Canonical Agent Definitions (18 Approved Agents)
- **Objective**: Author all 18 canonical agent definitions strictly adhering to the approved Phase 1A / Phase 1A.1 roster, `agent-template.md`, and `agent.schema.json`.

#### 1. Core Architecture & Orchestrator Principle
- **Single Central Coordinator**: The Orchestrator (`CAN-AGT-01`) manages specialist child agents based on their specific skills and responsibilities.
- **No Direct Domain Implementation**: The Orchestrator plans DAGs, selects necessary child agents, delegates tasks, coordinates handoffs, and compiles final reports; it does not write application code directly.
- **Lightweight & Native**: Uses native IDE capabilities and direct CLI tools without introducing unnecessary frameworks, daemons, or enterprise bloat.

#### 2. Conditional Quality-Gate Architecture
Quality gates are applied conditionally based on task type, complexity, and risk rather than imposing a blanket review/test pipeline on every task:
- **Documentation Tasks** (e.g. README, ADRs, user guides, changelogs):
  - *Applicable Gates*: Markdown syntax verification, link checks, documentation drift verification (`docs-technical-writer` / `documentation-synthesizer`).
  - *Skipped Gates*: Code review pipeline, QA test runners, browser test harnesses, migration linters.
- **Code Modification Tasks** (e.g. backend endpoints, UI components, bug fixes, refactoring):
  - *Gate 1 (Syntax)*: AST syntax verification (`syntax-verifier` / `ast-syntax-verifier`).
  - *Gate 2 (Review)*: Independent adversarial review (`code-reviewer`) for non-trivial modifications.
  - *Gate 3 (Tests)*: Task-proportional automated unit and integration tests (`qa-engineer`).
- **Database Migration Tasks**:
  - *Applicable Gates*: Migration safety & table lock linting (`database-migration-linter`), rollback verification, adversarial code review.
- **Security-Sensitive / Auth / Infrastructure Tasks**:
  - *Applicable Gates*: SAST and secret scanning (`security-auditor` / `security-secret-scanner`), adversarial code review, and mandatory Level 3 human approval gate before deployment or remote push.
- **Research & Data Analysis Tasks**:
  - *Applicable Gates*: Schema and evidence verification. Skipped: Full test harness.

#### 3. Individual Agent Boundaries & Collaboration Requirements
Every agent definition explicitly documents:
1. Primary responsibilities.
2. What the agent must NOT do (prohibited actions).
3. Responsibilities that belong to other specialists (handoff boundaries).
4. When to escalate to the Orchestrator (contract changes, blockers, ambiguity, Level 3 operations).
5. Collaboration partners, expected inputs, expected outputs, and handoff triggers.

#### 4. Permission Verification
Strictly aligns with `canonical/policies/approval-rules.md`:
- **Level 1 (Read-Only)**: `orchestrator`, `product-analyst`, `code-reviewer`, `syntax-verifier`, `security-auditor`, `research-investigator`.
- **Level 2 (Controlled Modification)**: `system-architect` (docs/ADRs), `backend-engineer`, `frontend-engineer`, `database-specialist`, `fullstack-integrator`, `surgeon-editor`, `qa-engineer`, `debugger-detective`, `devops-platform`, `docs-technical-writer`, `data-analyst`, `automation-specialist`.
- **Level 3 (Mandatory Human Approval)**: Any file deletion, credential modification, `git push`, branch deletion, live DB drops/truncates, or cloud provisioning triggered by any agent MUST halt and present the 4-quadrant human approval gate (`allow_accept`, `allow_edit`, `allow_respond`, `allow_ignore`).

- **Validation Criteria**: `python scripts/validate_canonical.py canonical/schemas/agent.schema.json canonical/agents/*.md` passes 100% across all 18 agents, verified by automated unit tests in `tests/test_schemas.py`.

### Milestone 6: Standardized Cognitive Workflows (10 Workflows)
- **Objective**: Codify the multi-agent collaboration patterns.
- **Tasks**:
  - Author all 10 workflow definitions in `canonical/workflows/`, specifying DAG topologies, role handoffs, and task-conditional quality gates.
- **Validation Criteria**: Workflows cross-reference existing canonical agents and skills without broken links.

### Milestone 7: Compiler Pipeline & Multi-IDE Adapters
- **Objective**: Build the transpiler generating native configurations for all 4 target IDEs.
- **Tasks**:
  1. Implement `scripts/compile_adapters.py`:
     - **Claude Code**: Transpiles canonical agents into `.claude/agents/*.md` with native tool bindings.
     - **Antigravity**: Symlinks/copies canonical skills into `.agents/skills/` and exports IDE rules.
     - **Cursor**: Generates `.cursor/rules/*.mdc` and modular prompt commands (`/plan`, `/implement`, `/review`, `/test`).
     - **VS Code/Copilot**: Generates `.github/copilot-instructions.md` and modular slash command templates.
  2. Author `tests/test_adapter_compilation.py` to verify adapter generation integrity.
- **Validation Criteria**: Compiler executes without warnings; generated adapter files pass structural syntax checks.

### Milestone 8: Automated Verification & Integration Simulation
- **Objective**: Validate the complete ecosystem through automated simulation.
- **Tasks**:
  1. Implement `scripts/simulate_orchestrator.py`: Dry-runs the Customer Management DAG, testing two-way `CHANGE_REQUEST`, dynamic two-phase locking, and `TASK_CANCELLATION`.
  2. Execute complete test suite (`pytest tests/`).
  3. Generate final Phase 1B Verification Report.
- **Validation Criteria**: All unit tests, canonical linters, and synthetic DAG simulations report green.

---

## 5. Parallel Execution & Concurrency Governance

To prevent inconsistent definitions and conflicting edits during parallel authoring:
1. **Schema Lockdown First**: Milestones 1 and 2 must be 100% completed and committed before any parallel authoring in Milestones 3, 4, or 5 begins.
2. **Battalion Partitioning**:
   - Agent authoring is partitioned by directory and persona ID; no two parallel authoring tasks touch the same file.
   - Skill authoring is isolated by folder (`canonical/skills/<skill-name>/`).
3. **Automated Pre-Commit Validation**: Every authored file must pass `scripts/validate_canonical.py` before being committed to git.

---

## 6. Implementation Risks & Mitigations

| Identified Risk | Severity | Mitigation Strategy |
|---|:---:|---|
| **Tree-sitter Binding Compilation Failure** | Medium | `lint_ast.py` includes automatic fallback to native project compilers (`tsc`, `cargo`, `go build`). |
| **Token Bloat in Agent Prompts** | High | Strict adherence to the 3-tier progressive disclosure model; reference documentation is kept in external `references/` files. |
| **Adapter Drift Across IDEs** | Medium | Single source of truth in `canonical/`; adapter files are read-only build outputs generated by `compile_adapters.py`. |
| **Persistent Shell Quoting Bugs** | Low | Mandatory enforcement of `git commit -F <file>` in `AGENTS.md` and helper scripts. |

---

## 7. Next Step

Awaiting your review and explicit approval of this refined implementation plan before initiating **Milestone 1**.
