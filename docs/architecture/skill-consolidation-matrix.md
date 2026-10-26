# Skill Consolidation Matrix

## 1. Executive Summary & Design Principle

In traditional prompt collections, skills are copied directly into agent instructions, causing massive token bloat, maintenance headaches, and drift. 

**Our Design Rule**: *Agents define WHO acts and WHAT their goals are; Skills define HOW specific technical capabilities are executed.*

A skill is an independent, reusable capability packaged in the `.agents/skills/<skill-name>/SKILL.md` format, equipped with executable helper scripts, templates, and progressive disclosure references (`references/guide.md`). Any canonical agent with appropriate tool permissions can invoke any applicable skill.

---

## 2. Reusable Core Skills Catalog (18 Canonical Skills)

| Canonical ID | Skill Name | Primary Purpose | Source Heritage & File Lineage | Consolidates / Replaces |
|---|---|---|---|---|
| **CAN-SKL-01** | **`codebase-scanner`** | AST symbol indexing, dependency graphing, architecture discovery without context flooding. | `github/awesome-copilot` (`skills/acquire-codebase-knowledge/scan.py`) | Ad-hoc grep loops, manual file reading. |
| **CAN-SKL-02** | **`str-replace-editor`** | Deterministic multiline search-and-replace file mutation with bounds checking. | `All-Hands-AI/openhands-aci` (`openhands_aci/editor/editor.py`) | Full-file overwrites, blind regex sed. |
| **CAN-SKL-03** | **`ast-syntax-verifier`** | Instant tree-sitter AST parsing across 14 languages to catch syntax errors post-edit. | `All-Hands-AI/openhands-aci` (`openhands_aci/editor/treesitter_linter.py`) | Post-commit CI failure discovery. |
| **CAN-SKL-04** | **`code-review-standards`**| Multi-pass code inspection (logic, security, typing, style, boundary enforcement). | `OpenHands/OpenHands` (`custom-codereview-guide.md`) & `VoltAgent` | Surface-level syntax commenting. |
| **CAN-SKL-05** | **`prd-generator`** | Structured PRD generation with user stories, acceptance criteria, and SPIDR splitting. | `FoundationAgents/MetaGPT` (`metagpt/actions/write_prd.py`) | Informal user requirement notes. |
| **CAN-SKL-06** | **`system-architecture-designer`** | Mermaid class/sequence diagramming, component topologies, data model contracts. | `FoundationAgents/MetaGPT` (`metagpt/actions/design_api.py`) | Unstructured architectural text. |
| **CAN-SKL-07** | **`adr-author`** | Architecture Decision Record generation with context, alternatives, and trade-offs. | `github/awesome-copilot` (`prompts/adr-generator.md`) | Undocumented architectural drift. |
| **CAN-SKL-08** | **`skill-eval-creator`** | Autonomous evaluation, benchmarking, and description optimization for new skills. | `anthropics/skills` (`skills/skill-creator/evals.py`) | Untested, uncalibrated agent skills. |
| **CAN-SKL-09** | **`web-app-testing-harness`** | Ephemeral local server lifecycle management and Playwright headless verification. | `anthropics/skills` (`skills/webapp-testing/with_server.py`) | Testing against dead or unstarted servers. |
| **CAN-SKL-10** | **`git-worktree-isolator`** | Concurrency isolation: spinning up git worktrees for parallel agent development. | `ruvnet/ruflo` (`claude-flow/worktree-isolator.sh`) | Branch conflicts and dirty workspace states. |
| **CAN-SKL-11** | **`episodic-memory-ledger`** | Persisting decisions, failed hypotheses, and lessons learned in `.agent/memory.json`. | `ruvnet/ruflo` (`skills/agentdb-memory.js`) | Context loss across agent session restarts. |
| **CAN-SKL-12** | **`progressive-disclosure-loader`** | 3-tier on-demand documentation loading (Metadata -> Core -> References). | `crewAIInc/crewAI` (`crewai/memory/`) | System prompt token blowup. |
| **CAN-SKL-13** | **`api-contract-validator`** | OpenAPI/JSON Schema enforcement, breaking change detection, type generation. | `OpenHands/OpenHands` (`.agents/skills/frontend-api-contracts/`) | Frontend/backend communication mismatches. |
| **CAN-SKL-14** | **`root-cause-diagnoser`** | Hypothesis generation, binary search log analysis, stack trace isolation. | `microsoft/autogen` & `langchain-ai/langgraph` (`reflexion.ipynb`) | Guess-and-check debugging. |
| **CAN-SKL-15** | **`security-vulnerability-scanner`** | SAST scanning, dependency vulnerability audit, hardcoded secret detection. | `ruvnet/ruflo` & `VoltAgent/security-auditor` | Manual security code review. |
| **CAN-SKL-16** | **`test-suite-builder`** | AAA pattern test generation, mock fixtures, edge cases, integration tests. | `FoundationAgents/MetaGPT` (`metagpt/actions/write_test.py`) | Happy-path only testing. |
| **CAN-SKL-17** | **`doc-drift-synchronizer`** | Automated audit comparing codebase reality against READMEs and technical docs. | `VoltAgent/awesome-claude-code-subagents` (`docs-drift-editor.md`) | Outdated, stale technical documentation. |
| **CAN-SKL-18** | **`terminal-safety-sanitizer`** | Pre-execution bash command inspection against safety envelopes and destructive flags. | `microsoft/autogen` (`UserProxyAgent`) & `ruvnet/ruflo` | Accidental data loss or rm -rf. |

---

## 3. Progressive Disclosure Architecture

Following the design validated in **CrewAI (`REPO-005`)** and **Anthropic Skills (`REPO-003`)**, each skill adheres to strict token budgeting:
1. **Tier 1 (Frontmatter Metadata - ~50 tokens)**: `name`, `description`, `trigger_patterns`. Loaded into agent memory so the agent knows the skill exists.
2. **Tier 2 (Core Instructions - ~500 tokens)**: `SKILL.md` body. Step-by-step methodology, constraints, tool requirements. Loaded only when triggered.
3. **Tier 3 (Deep Reference / Scripts - ~2,000+ tokens)**: `references/guide.md` and executable scripts (e.g. `scan.py`, `with_server.py`). Read on-demand or executed via CLI.
