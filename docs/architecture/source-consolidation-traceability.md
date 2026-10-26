# Source Consolidation Traceability & Mapping Ledger

## 1. Executive Summary & Methodology

Across the 10 audited repositories, over 400 agent and prompt files were catalogued. To provide complete, unambiguous traceability from raw open-source assets to our canonical architecture, this ledger maps each source archetype to its final disposition in the Universal AI Agent Army.

### Final Disposition Categories:
- **`ADOPT`**: Preserved and integrated into a Canonical Specialist Agent or Skill with attribution.
- **`CONSOLIDATE`**: Merged with similar/overlapping roles into a single Canonical Agent (e.g., merging 35 framework roles into `backend-engineer`).
- **`SPLIT`**: Conflated responsibilities decoupled into separate distinct roles (e.g., splitting `surgeon-reviewer` into `surgeon-editor`, `syntax-verifier`, and `code-reviewer`).
- **`REJECT`**: Excluded due to proprietary licensing, hyper-narrow boilerplate, or external daemon dependencies.

---

## 2. Comprehensive Traceability Matrix

| Source Repository | Source Path / Archetype | Original Agent / Tool Name | Final Disposition | Canonical Target ID & Name | Rationale & Licensing Notes |
|---|---|---|:---:|---|---|
| **VoltAgent** (`REPO-001`) | `agents/surgeon-reviewer.md` | `surgeon-reviewer` | **SPLIT** | `CAN-AGT-08 (surgeon-editor)` & `CAN-AGT-09 (code-reviewer)` | Author cannot be critic. Split atomic file editing from adversarial code review. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/docs-drift-editor.md` | `docs-drift-editor` | **ADOPT** | `CAN-AGT-15 (docs-technical-writer)` & `CAN-SKL-17` | High-value drift comparison between code and documentation. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/frontend/*.md` (40 files) | `react-dev`, `vue-dev`, `nextjs-pro`, `svelte-specialist`, etc. | **CONSOLIDATE** | `CAN-AGT-05 (frontend-engineer)` | 90% instruction overlap. Framework specifics moved to skills and guides. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/backend/*.md` (35 files) | `fastapi-expert`, `django-dev`, `express-dev`, `go-dev`, `rust-pro`, etc. | **CONSOLIDATE** | `CAN-AGT-04 (backend-engineer)` | Redundant boilerplate. Consolidated into universal backend specialist. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/database-engineer.md` | `database-engineer`, `sql-optimizer` | **CONSOLIDATE** | `CAN-AGT-06 (database-specialist)` | Unifies relational and NoSQL schema design, indexing, and migrations. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/security-auditor.md` | `security-auditor` | **ADOPT** | `CAN-AGT-12 (security-auditor)` | Static security analysis, secret leak detection, and OWASP review. (MIT) |
| **VoltAgent** (`REPO-001`) | `agents/devops-engineer.md` | `devops-engineer`, `docker-specialist` | **CONSOLIDATE** | `CAN-AGT-14 (devops-platform)` | Merges Docker, CI/CD pipelines, and environment management. (MIT) |
| **Awesome-Copilot** (`REPO-002`) | `skills/acquire-codebase-knowledge/scan.py` | `scan.py` AST scanner | **ADOPT** | `CAN-SKL-01 (codebase-scanner)` | High-efficiency Python AST symbol extraction without context flooding. (MIT) |
| **Awesome-Copilot** (`REPO-002`) | `prompts/adr-generator.md` | `adr-generator` | **ADOPT** | `CAN-SKL-07 (adr-author)` | Lightweight, standardized Architectural Decision Record authoring. (MIT) |
| **Awesome-Copilot** (`REPO-002`) | `skills/agent-governance/` | `agent-governance` | **CONSOLIDATE** | `CAN-POL-01 (safety-and-approval-policy)` | Consolidated with OpenHands contributor rules into master safety policy. (MIT) |
| **Awesome-Copilot** (`REPO-002`) | `prompts/data-analyst.md` | `data-analyst` | **ADOPT** | `CAN-AGT-17 (data-analyst)` | General-purpose tabular data analysis and reporting. (MIT) |
| **Anthropic Skills** (`REPO-003`) | `skills/skill-creator/evals.py` | `skill-creator` | **ADOPT** | `CAN-SKL-08 (skill-eval-creator)` | Automated benchmarking and prompt description optimization. (Apache 2.0) |
| **Anthropic Skills** (`REPO-003`) | `skills/webapp-testing/with_server.py` | `with_server.py` test harness | **ADOPT** | `CAN-SKL-09 (web-app-testing-harness)` | Spawns ephemeral test server, runs tests, guarantees clean teardown. (Apache 2.0) |
| **Anthropic Skills** (`REPO-003`) | `skills/document-processing/` | Document processing tools | **REJECT** | *None* | Excluded due to proprietary licensing terms. |
| **Ruflo** (`REPO-004`) | `claude-flow/worktree-isolator.sh` | Git Worktree Isolator | **ADOPT** | `CAN-SKL-10 (git-worktree-isolator)` | Clean filesystem isolation for concurrent agent execution. (MIT) |
| **Ruflo** (`REPO-004`) | `skills/agentdb-memory.js` | AgentDB episodic memory | **ADOPT** | `CAN-SKL-11 (episodic-memory-ledger)` | Persisting decisions and lessons learned in `.agent/memory.json`. (MIT) |
| **CrewAI** (`REPO-005`) | `crewai/agents/agent_builder/base_agent.py`| BaseAgent Persona Engine | **ADOPT** | `ADR-001 (Role-Goal-Backstory Schema)` | Industry-standard persona formulation adopted across all canonical agents. (MIT) |
| **CrewAI** (`REPO-005`) | `crewai/memory/` | Progressive disclosure loader | **ADOPT** | `CAN-SKL-12 (progressive-disclosure-loader)` | 3-tier memory management preventing system prompt token bloat. (MIT) |
| **MetaGPT** (`REPO-006`) | `metagpt/roles/product_manager.py` | `ProductManager` | **ADOPT** | `CAN-AGT-02 (product-analyst)` & `CAN-SKL-05` | Rigorous PRD authoring with SPIDR user stories. (MIT) |
| **MetaGPT** (`REPO-006`) | `metagpt/roles/architect.py` | `Architect` | **ADOPT** | `CAN-AGT-03 (system-architect)` & `CAN-SKL-06` | System design with Mermaid classDiagram and sequenceDiagram. (MIT) |
| **MetaGPT** (`REPO-006`) | `metagpt/roles/qa_engineer.py` | `QaEngineer` | **ADOPT** | `CAN-AGT-11 (qa-engineer)` & `CAN-SKL-16` | Automated test suite builder using Arrange-Act-Assert pattern. (MIT) |
| **OpenHands ACI** (`REPO-007`) | `openhands_aci/editor/editor.py` | `aci-editor` | **ADOPT** | `CAN-AGT-08 (surgeon-editor)` & `CAN-SKL-02` | `str_replace` atomic file editing primitive with bounds checking. (MIT) |
| **OpenHands ACI** (`REPO-007`) | `openhands_aci/editor/treesitter_linter.py`| `TreesitterBasicLinter` | **ADOPT** | `CAN-AGT-10 (syntax-verifier)` & `CAN-SKL-03` | Instant pre-commit Tree-sitter AST validation across 14 languages. (MIT) |
| **LangGraph** (`REPO-008`) | `examples/plan-and-execute/` | Plan-and-Execute Loop | **ADOPT** | `CAN-AGT-01 (orchestrator)` & `CAN-WFL-01` | Decouples dynamic planning from execution with auto-replanning. (MIT) |
| **LangGraph** (`REPO-008`) | `libs/prebuilt/langgraph/prebuilt/interrupt.py`| `HumanInterruptConfig` | **ADOPT** | `CAN-POL-01 (4-Quadrant Interruption Gate)` | Standardizes user interruption (`accept`, `edit`, `respond`, `ignore`). (MIT) |
| **AutoGen** (`REPO-009`) | `autogen_agentchat/base/_handoff.py` | Dynamic Tool Handoffs | **ADOPT** | `CAN-ENV-01 (Handoff Protocol)` | Synthetic handoff tool generation (`transfer_to_<agent>`). (MIT) |
| **AutoGen** (`REPO-009`) | `autogen_agentchat/agents/_society_of_mind_agent.py`| `SocietyOfMindAgent` | **ADOPT** | `CAN-AGT-01 (Orchestration Pattern)` | Hierarchical swarm encapsulation into a single virtual agent interface. (MIT) |
| **OpenHands Main** (`REPO-010`) | `AGENTS.md` | Contributor Guidelines | **ADOPT** | `CAN-POL-01 (Code of Conduct)` | Strict rules for AI contributors and shell wrapper commit safety (`git commit -F`). (MIT) |
| **OpenHands Main** (`REPO-010`) | `.agents/skills/custom-codereview-guide.md`| Code Review Guide | **ADOPT** | `CAN-SKL-04 (code-review-standards)` | Boundary-aware code review checklist enforcing layer separation. (MIT) |
