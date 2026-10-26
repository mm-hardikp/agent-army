# Capability Gap Analysis

## 1. Executive Summary

While the 10 audited repositories contained impressive isolated inventions, **none of them provided a complete, production-grade, IDE-portable agent architecture**. Every repository had critical blind spots that caused agent failure when deployed in real-world software engineering environments.

Phase 1A explicitly identifies these capability gaps and designs the missing components into our Universal AI Agent Army architecture.

---

## 2. Matrix of Discovered Gaps & Bespoke Solutions

| Gap ID | Identified Capability Gap | Where Existing Repos Failed | Universal Agent Army Solution |
|---|---|---|---|
| **GAP-01** | **No Native IDE File-Mediated State Machine** | Repos either required a continuous Docker/Python daemon (OpenHands, LangGraph, AutoGen) or had zero state persistence between prompt calls (Awesome-Copilot, VoltAgent). | **File-Mediated State Ledger**: We design a zero-daemon `.agent/state.json` ledger maintained by the Orchestrator, allowing any native IDE agent to resume state cleanly across turns. |
| **GAP-02** | **Lack of Pre-Commit Syntax Validation** | 9 out of 10 repos allowed agents to write invalid syntax directly to source files, only catching errors when external compiler/linter tasks failed later. | **`CAN-SKL-03 (ast-syntax-verifier)`**: Borrowed from OpenHands ACI, our army mandates local AST tree-sitter validation immediately after every file modification, rejecting edits before git staging. |
| **GAP-03** | **Uncontrolled Parallel File Collisions** | Multi-agent swarms (Ruflo, AutoGen) attempted concurrent edits on the same source files, leading to git conflicts and overwritten logic. | **Worktree Concurrency Envelope**: Adopted from Ruflo (`WFL-006`) combined with a strict file-reservation lock in the Orchestrator's execution plan. |
| **GAP-04** | **Unstructured Inter-Agent Handoffs** | Agents exchanged unstructured conversational chit-chat ("I have finished the backend, you can do frontend now"), omitting API parameters, file paths, and decisions. | **Standardized Handoff Contract (`CAN-ENV-01`)**: Mandatory structured envelope containing Task ID, modified files, exported interfaces, test status, and remaining work. |
| **GAP-05** | **Absence of Independent Quality Verification** | In most repos (VoltAgent, Awesome-Copilot), the developer agent evaluated its own work, always reporting 100% success despite broken code. | **Mandatory Dual-Gate Protocol**: Code review and QA are strictly decoupled from authoring agents. An author agent cannot self-certify completion. |
| **GAP-06** | **Shell Persistent Wrapper Message Corruption** | Discovered empirically in OpenHands `AGENTS.md`: running `git commit -m "multi-line"` in persistent IDE shell terminals frequently corrupts commit bodies due to echo loops. | **Mandatory `git commit -F <file>` Standard**: All commit and complex shell operations write to temporary files first, eliminating shell escaping bugs. |
| **GAP-07** | **No Universal Human-in-the-Loop Contract** | Human interaction was either completely absent (unsupervised runs) or clunky console input prompts (`input()`) that crash non-interactive IDEs. | **4-Quadrant Interruption Envelope**: Standardized `allow_accept`, `allow_edit`, `allow_respond`, and `allow_ignore` prompts natively compatible with IDE approval modals. |
