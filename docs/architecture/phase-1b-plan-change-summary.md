# Phase 1B Implementation Plan Refinement: Change Summary

## 1. Scope & Motivation

This document summarizes the refinements applied to `phase-1b-implementation-plan.md` based on architectural review and targeted user feedback.

---

## 2. Key Refinements Applied

| Architecture Area | Previous Plan Draft | Refined Plan Specification | Rationale & Benefit |
|---|---|---|---|
| **Implementation Sequence** | Tools and agents authored before formal schemas were codified. | **Strict "Standards-First" Sequence**: Schemas (`can-agt.schema.json`, `can-skl.schema.json`, `can-env-01.schema.json`) and templates are built in Milestone 2 *before* agents and skills are authored. | Guarantees 100% syntactic and structural consistency across all 18 agents and 18 skills; prevents rework. |
| **Tooling Scope Evaluation** | Proposed 3 full Python tools (`scan_ast.py`, `lint_ast.py`, `with_server.py`). | **Evaluated and streamlined**: Retained `scan_ast.py` (essential token reduction) and `lint_ast.py` (sub-second AST pre-check with compiler fallback). Replaced `with_server.py` with a minimal 40-line `ephemeral_server.py` script. | Avoids duplicating native build tools or project dev-servers while preserving essential AST capabilities. |
| **Repository Asset Classification** | Broad directory layout without ownership boundaries. | **Strict 3-Way Classification**: Formally categorized assets into: 1) Canonical Source of Truth (`canonical/`), 2) Generated Read-Only Adapter Outputs (`adapters/`), and 3) Gitignored Temporary Runtime Artifacts (`.agent/`, `.worktrees/`). | Clarifies build pipeline boundaries; prevents developers from editing generated adapter files directly. |
| **IDE Host Fidelity** | Generalized adapter concepts across all IDEs. | **Precise Platform Alignment**: Formally codified modular slash commands (`/plan`, `/implement`, `/review`, `/test`) for Cursor and VS Code/Copilot to reflect single-stream execution realities, while preserving autonomous subagent delegation in Claude Code and Antigravity. | Eliminates false assumptions about IDE autonomy; adheres to official configuration formats. |
| **Testing & Verification** | Claimed production readiness based on file existence. | **Empirical Validation Gates**: Defined explicit unit tests (`tests/test_*.py`), canonical linter execution (`validate_canonical.py`), and a synthetic DAG dry-run simulation (`simulate_orchestrator.py`). | Distinguishes planned tests from verified test runs; guarantees verifiable green builds. |
| **Parallel Concurrency Controls** | Uncontrolled parallelization of 18 agents and 18 skills. | **Partitioned Battalion Workstreams**: Mandated schema lockdown in Milestone 2 before parallel authoring; partitioned agents and skills into isolated directory batches. | Prevents merge conflicts and inconsistent prompt conventions. |
