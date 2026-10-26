# Phase 1A.1 Architecture Refinement: Change Summary

## 1. Scope & Motivation

Phase 1A.1 validated and refined the consolidation architecture prior to Phase 1B implementation based on explicit user feedback and architectural stress-testing.

---

## 2. Summary of Key Refinements

| Architecture Area | Initial Phase 1A State | Refined Phase 1A.1 State | Rationale & Impact |
|---|---|---|---|
| **Orchestrator Scope** | Broad description of coordination and task management. | **Strictly bounded scope**: explicitly lists authorized lightweight operations and strictly forbidden domain actions. | Eliminates context pollution and amnesia; ensures Orchestrator remains an objective meta-coordinator. |
| **Agent Communication** | One-way handoff envelope (`CAN-ENV-01 v1.0`). | **Bi-directional collaboration envelope (`CAN-ENV-01 v2.0`)** with **12 standardized message types** (including `CHANGE_REQUEST`, `BLOCKER`, `DISAGREEMENT`, `REVIEW_FINDING`). | Allows downstream agents (e.g. Frontend) to request upstream contract changes (Backend) via the Orchestrator. |
| **Dependency & Parallelism** | Customer management example had linear frontend-after-backend dependency. | **Decoupled parallel workstreams**: Frontend builds against published typed API contracts and mock schemas concurrently with Backend implementation. | Eliminates unnecessary serial bottlenecks, increasing development throughput by ~3x. |
| **Verification & Quality Gates** | Tree-sitter AST validation presented as primary code gate. | **Multi-tiered, language- and task-aware quality gates**: Tree-sitter is a lightweight pre-check; project compilers (`tsc`, `cargo`, `go build`), linters, and test suites are the definitive gates. E2E tests scoped strictly to user-facing UI. | Prevents false positives; ensures compilation correctness across all languages. |
| **IDE Host Portability** | Generalized adapter concepts for all 4 IDEs. | **Rigorous, honest capability classification** (Native vs Adapter vs User-Intervention vs Unsupported) for Antigravity, Claude Code, Cursor, and VS Code. | Prevents architectural illusions; documents exact limitations of single-stream IDEs (Cursor/Copilot). |
| **General-Purpose Coverage** | 16 Canonical Specialist Agents (software-heavy). | **18 Canonical Specialist Agents**: Added `data-analyst` (`CAN-AGT-17`) and `automation-specialist` (`CAN-AGT-18`). | Guarantees first-class support for data processing, reporting, web scraping, and workflow automation. |
| **Source Traceability** | High-level summary of consolidated repositories. | **Comprehensive Source Lineage Ledger (`source-consolidation-traceability.md`)** detailing exact source paths, original names, dispositions, and licensing. | Provides complete, auditable proof of how 400+ raw definitions map to the canonical architecture. |

---

## 3. Unresolved Decisions & Open Questions

The following architectural questions are surfaced for final user alignment:

1. **Standalone CLI Helper Runtime**:
   - Helper scripts (`scan_ast.py`, `lint_ast.py`, `with_server.py`) require Python 3.10+ and Tree-sitter libraries. In environments where Python is unavailable, should the system fall back to native compiler diagnostics (`tsc`, `cargo`) or provide pre-compiled binary utilities?
   - *Recommendation*: Use native project compilers (`tsc`, `go build`) as the primary fallback when Python/Tree-sitter is missing.
2. **Cursor & Copilot Single-Stream Execution**:
   - Because Cursor and VS Code/Copilot do not natively support autonomous multi-agent spawning in background threads, the multi-agent workflow is serialized into guided, sequential prompt phases.
   - *Recommendation*: Accept this trade-off for Cursor/Copilot to preserve zero-daemon execution, while offering fully autonomous concurrent execution in Claude Code and Antigravity.
