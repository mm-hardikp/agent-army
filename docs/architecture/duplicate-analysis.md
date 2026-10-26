# Duplication & Overlap Analysis

## 1. Executive Summary

A critical reason for executing Phase 1A is that the open-source agent ecosystem suffers from severe prompt duplication, brand-based redundancy, and architectural copy-pasting.

Our analysis examined:
1. **Exact Text / Prompt Duplication** (verbatim copy-pasting across repositories).
2. **Conceptual / Functional Duplication** (different wording or framework bindings accomplishing the exact same technical objective).
3. **Role Bloat** (fragmenting a single professional role into dozens of hyper-narrow micro-prompts).

---

## 2. Quantified Duplication Breakdown

| Duplication Category | Approximate Instances in Raw 10 Repos | Root Cause | Army Consolidation Action |
|---|:---:|---|---|
| **Framework-Specific Dev Roles** | ~75 agents | Creating separate agents for every JS framework (`vue-dev`, `react-dev`, `svelte-dev`, `angular-dev`) and backend framework. | Consolidated into 2 canonical agents (`backend-engineer`, `frontend-engineer`) with on-demand skill guides. |
| **Generic "Code Review" Prompts** | ~40 agents/prompts | Every repository created its own variation of "review this code for bugs and style". | Consolidated into 1 canonical `code-reviewer` equipped with `code-review-standards` skill. |
| **"Documentation Writer" Prompts** | ~25 agents/prompts | Separate prompts for READMEs, API docs, release notes, and tutorials. | Consolidated into `docs-technical-writer` equipped with `doc-drift-synchronizer`. |
| **Database & SQL Optimizers** | ~18 agents/prompts | Separate agents for PostgreSQL, MySQL, SQLite, MongoDB, and Redis. | Consolidated into `database-specialist` supporting SQL/NoSQL schemas and migrations. |
| **Ad-Hoc File Search & Grep Loops** | ~60 skills/prompts | Repositories having agents run raw `find` and `grep` repeatedly, flooding context. | Replaced by `codebase-scanner` with Python AST symbol extractor (`scan.py`). |
| **Unsafe Edit & Overwrite Prompts** | ~50 tools/prompts | Agents attempting to overwrite entire 1,000-line files to change 2 lines. | Replaced by `surgeon-editor` using `str_replace` atomic replacement with tree-sitter validation. |

---

## 3. High-Impact Duplication Cases Resolved

### Case A: `surgeon-reviewer` vs `aci-editor` vs `custom-codereview-guide`
- **Heritage**: VoltAgent, OpenHands ACI, OpenHands Main.
- **Problem**: VoltAgent combined surgical editing and code review into a single prompt. OpenHands ACI implemented Python code for `str_replace` and Tree-sitter linting. OpenHands Main created code review guidelines.
- **Resolution**: We decoupled editing mechanics from review judgment. `surgeon-editor` executes atomic diffs; `syntax-verifier` checks ASTs; `code-reviewer` conducts independent review.

### Case B: MetaGPT SOP vs LangGraph Plan-and-Execute vs AutoGen Handoffs
- **Heritage**: MetaGPT (`REPO-006`), LangGraph (`REPO-008`), AutoGen (`REPO-009`).
- **Problem**: MetaGPT hardcoded a rigid waterfall sequence. LangGraph used code-heavy Pregel state graphs. AutoGen used conversational group chats with random speaker selection.
- **Resolution**: Consolidated into **Dynamic DAG Execution**:
  - The **Orchestrator** generates a dynamic task DAG (inspired by LangGraph).
  - Uses explicit **tool-based handoffs** (`transfer_to_<agent>`) inspired by AutoGen.
  - Enforces structured artifact deliverables (PRD, Architecture, Code, Tests) inspired by MetaGPT.
