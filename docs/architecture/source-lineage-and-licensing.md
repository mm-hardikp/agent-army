# Source Lineage & Licensing Ledger

## 1. Compliance Statement

The Universal AI Agent Army project honors open-source licensing, copyright attribution, and redistribution requirements. Every capability, prompt structure, or helper script harvested from the 10 audited repositories is documented below with its exact originating commit SHA and license terms.

---

## 2. Lineage & Attribution Matrix

| Harvested Component | Canonical ID | Originating Repository | Source Commit SHA | Source File Path | Upstream License | Attribution Obligation |
|---|---|---|:---:|---|---|---|
| **`scan.py` AST Symbol Scanner** | `CAN-SKL-01` | `github/awesome-copilot` | `d85f762` | `skills/acquire-codebase-knowledge/scan.py` | MIT | Include Copyright (c) GitHub, Inc. |
| **`str_replace` Mutation Engine**| `CAN-SKL-02` | `All-Hands-AI/openhands-aci` | `a8d8d23` | `openhands_aci/editor/editor.py` | MIT | Include Copyright (c) All-Hands-AI |
| **Tree-sitter AST Syntax Linter**| `CAN-SKL-03` | `All-Hands-AI/openhands-aci` | `a8d8d23` | `openhands_aci/editor/treesitter_linter.py`| MIT | Include Copyright (c) All-Hands-AI |
| **Code Review Standards** | `CAN-SKL-04` | `OpenHands/OpenHands` | `fee10e3` | `.agents/skills/custom-codereview-guide.md`| MIT | Include Copyright (c) 2025 OpenHands contributors |
| **PRD Generator Action** | `CAN-SKL-05` | `FoundationAgents/MetaGPT` | `11cdf46` | `metagpt/actions/write_prd.py` | MIT | Include Copyright (c) 2023 DeepWisdom |
| **System Architecture Design** | `CAN-SKL-06` | `FoundationAgents/MetaGPT` | `11cdf46` | `metagpt/actions/design_api.py` | MIT | Include Copyright (c) 2023 DeepWisdom |
| **ADR Generator Prompt** | `CAN-SKL-07` | `github/awesome-copilot` | `d85f762` | `prompts/adr-generator.md` | MIT | Include Copyright (c) GitHub, Inc. |
| **`evals.py` & Description Tuner**| `CAN-SKL-08` | `anthropics/skills` | `dbd4588` | `skills/skill-creator/evals.py` | Apache 2.0 | Include Apache 2.0 License Notice & Anthropic Attribution |
| **`with_server.py` Test Harness** | `CAN-SKL-09` | `anthropics/skills` | `dbd4588` | `skills/webapp-testing/with_server.py` | Apache 2.0 | Include Apache 2.0 License Notice & Anthropic Attribution |
| **Git Worktree Swarm Protocol** | `CAN-SKL-10` | `ruvnet/ruflo` | `533e17e` | `claude-flow/worktree-isolator.sh` | MIT | Include Copyright (c) 2025 Ruvnet |
| **Episodic Memory Ledger** | `CAN-SKL-11` | `ruvnet/ruflo` | `533e17e` | `skills/agentdb-memory.js` | MIT | Include Copyright (c) 2025 Ruvnet |
| **Role-Goal-Backstory Schema** | `ADR-001` | `crewAIInc/crewAI` | `38db11e` | `crewai/agents/agent_builder/base_agent.py`| MIT | Include Copyright (c) CrewAI, Inc. |
| **Plan-and-Execute Loop** | `CAN-WFL-01` | `langchain-ai/langgraph` | `4c52e12` | `examples/plan-and-execute/` | MIT | Include Copyright (c) 2024 LangChain, Inc. |
| **Human Interruption Protocol** | `CAN-ENV-01` | `langchain-ai/langgraph` | `4c52e12` | `libs/prebuilt/langgraph/prebuilt/interrupt.py`| MIT | Include Copyright (c) 2024 LangChain, Inc. |
| **Dynamic Tool Handoffs** | `CAN-WFL-11` | `microsoft/autogen` | `004749e` | `python/packages/autogen-agentchat/src/autogen_agentchat/base/_handoff.py`| MIT | Include Copyright (c) Microsoft Corporation |
| **Society of Mind Encapsulation**| `CAN-AGT-01` | `microsoft/autogen` | `004749e` | `python/packages/autogen-agentchat/src/autogen_agentchat/agents/_society_of_mind_agent.py`| MIT | Include Copyright (c) Microsoft Corporation |
| **`AGENTS.md` Contributor Rules**| `CAN-POL-01` | `OpenHands/OpenHands` | `fee10e3` | `AGENTS.md` | MIT | Include Copyright (c) 2025 OpenHands contributors |
| **`surgeon-reviewer` Mechanics** | `CAN-AGT-08` | `VoltAgent/awesome-claude-code-subagents`| `408d3c9` | `agents/surgeon-reviewer.md` | MIT | Include Copyright (c) 2025 VoltAgent |

---

## 3. Rejected Proprietary Assets

In accordance with our Phase 0 findings, all proprietary-licensed skills from `anthropics/skills` (specifically `skills/document-processing/` and internal Claude models) were **strictly rejected and excluded** from the Army to ensure 100% legal compliance and commercial usability.
