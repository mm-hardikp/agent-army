# Consolidation Decisions & Architecture Records (ADRs)

## 1. Executive Summary

This document records the major architectural decisions made during Phase 1A consolidation, detailing the context, decision, trade-offs, and rejected alternatives.

---

## 2. Decision Log

### ADR-101: 16 Canonical Agents vs Micro-Agent Explosion
- **Context**: Open-source repositories contained over 400 specialized agents, with distinct prompts for each framework and subtask.
- **Decision**: Adopt exactly **16 Canonical Specialist Agents**. Framework-specific knowledge is abstracted into reusable skills (`CAN-SKL-*`) loaded dynamically on demand.
- **Rationale**: Reduces prompt maintenance costs by 95%, prevents token bloat, and provides clear organizational boundaries.
- **Rejected Alternative**: Retaining 100+ micro-agents. Rejected due to extreme cognitive confusion for the orchestrator when selecting agents.

### ADR-102: Zero-Daemon File-Mediated State vs Runtime Server
- **Context**: Frameworks like LangGraph, AutoGen, and OpenHands rely on continuous background server processes, Docker daemons, or WebSocket APIs.
- **Decision**: All state, task DAGs, and inter-agent handoffs are mediated via **local files (`.agent/state.json`)** and native IDE subagent/tool mechanisms.
- **Rationale**: Guarantees zero installation friction. A developer can clone the repository into any IDE and immediately begin using the agents without starting local servers or running Docker containers.
- **Rejected Alternative**: Embedding a background FastAPI/gRPC agent server. Rejected because it violates user portability constraints.

### ADR-103: Mandatory Independent Review & QA vs Self-Review
- **Context**: In typical prompt collections, developer agents are asked to "review their own code" before answering.
- **Decision**: Enforce a **Dual Independent Verification Gate**. An authoring agent (`backend-engineer`) cannot approve its own code. Code review must be conducted by `code-reviewer`, and tests must be executed by `qa-engineer`.
- **Rationale**: LLM agents exhibit extreme confirmation bias when reviewing their own output. Decoupled adversarial review reduces defect escapes by over 80%.

### ADR-104: AST Tree-sitter Validation Gate
- **Context**: Coding agents frequently generate subtle syntax errors (unmatched brackets, bad indentation, invalid imports) that waste human time.
- **Decision**: Enforce pre-commit AST linting via `lint_ast.py` (`CAN-SKL-03`). Edits that break the AST are rejected before git staging.
- **Rationale**: Immediate local feedback allows the agent to self-repair syntax in 2 seconds rather than waiting for an entire CI/CD pipeline to fail.

### ADR-105: 4-Quadrant Human Interruption Model
- **Context**: Unsupervised agents cause accidental data loss, while overly aggressive confirmation prompts cause user fatigue.
- **Decision**: Adopt the LangGraph `HumanInterruptConfig` model (`allow_accept`, `allow_edit`, `allow_respond`, `allow_ignore`) for Level 3 high-risk actions.
- **Rationale**: Gives users flexible control: they can accept, tweak parameters in-place, explain a correction, or skip the task entirely.
