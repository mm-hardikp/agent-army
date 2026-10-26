# Agent Consolidation Matrix (Refined Phase 1A.1)

## 1. General-Purpose Capability Review

The Phase 0 vision mandates an agent army that is **general-purpose**, capable of handling software development, research, documentation, data analysis, automation, and technical investigation.

### Gap Assessment of Initial 16 Canonical Agents:
Upon rigorous review against non-software workflows, two important responsibilities were missing distinct canonical ownership:
1. **Data Analysis & Processing**: Handling CSV/Parquet data munging, SQL querying, statistics, and chart generation. While `database-specialist` manages schemas and migrations, it is NOT calibrated for data science or reporting.
2. **Workflow Automation & Scripting**: Managing scheduled cron tasks, web scrapers, ETL pipelines, and repetitive API integrations. While `devops-platform` handles infrastructure, it is not calibrated for application-level task scripts.

### Refined Battalion Structure: Exactly 18 Canonical Agents
To achieve comprehensive general-purpose coverage without prompt bloat, we introduce two new canonical agents:
- **`CAN-AGT-17 (data-analyst)`**
- **`CAN-AGT-18 (automation-specialist)`**

---

## 2. Refined Master Catalog of 18 Canonical Specialist Agents

| Canonical ID | Canonical Agent Name | Battalion / Category | Primary Responsibility | Replaced / Consolidated Roles |
|---|---|---|---|---|
| **CAN-AGT-01** | **`orchestrator`** | Command & Control | Intent deconstruction, DAG planning, delegation, handoff routing, quality gate enforcement. | AutoGen `GroupChatManager`, LangGraph `PlanAndExecute`, Ruflo `SwarmCoordinator`. |
| **CAN-AGT-02** | **`product-analyst`** | Strategy & Discovery | User stories, acceptance criteria, PRD generation, SPIDR feature decomposition. | MetaGPT `ProductManager`, Copilot `requirements-analyst`, VoltAgent `product-owner`. |
| **CAN-AGT-03** | **`system-architect`** | Strategy & Discovery | System topology, Mermaid class/sequence diagrams, data contracts, ADR authoring. | MetaGPT `Architect`, Copilot `adr-generator`, VoltAgent `software-architect`. |
| **CAN-AGT-04** | **`backend-engineer`** | Core Engineering | Server business logic, REST/gRPC/GraphQL APIs, microservices, algorithmic correctness. | 35+ framework agents (`fastapi-expert`, `node-dev`, `django-dev`, `go-dev`, `spring-boot`). |
| **CAN-AGT-05** | **`frontend-engineer`** | Core Engineering | UI/UX component engineering, responsive CSS, state management, client performance. | 40+ UI agents (`react-pro`, `nextjs-dev`, `vue-master`, `tailwind-expert`, Anthropic design). |
| **CAN-AGT-06** | **`database-specialist`**| Core Engineering | Relational/NoSQL DDL schemas, migration scripts, index optimization, rollback plans. | Copilot `database-engineer`, VoltAgent `sql-optimizer`, `postgres-pro`. |
| **CAN-AGT-07** | **`fullstack-integrator`**| Core Engineering | Glue code, client-server integration, mock replacement, BFF layers, full-stack prototypes.| VoltAgent `fullstack-developer`, MetaGPT `Engineer`. |
| **CAN-AGT-08** | **`surgeon-editor`** | Precision Mutation | Atomic multiline code modifications via `str_replace`, zero line-drift, bounds checking. | OpenHands `aci-editor`, VoltAgent `surgeon-reviewer` (editing half). |
| **CAN-AGT-09** | **`code-reviewer`** | Quality Verification | Independent multi-pass adversarial PR review, boundary enforcement, code smell detection. | VoltAgent `surgeon-reviewer`, OpenHands `custom-codereview-guide`, CrewAI `CodeReviewer`. |
| **CAN-AGT-10** | **`syntax-verifier`** | Quality Verification | Pre-commit AST validation across 14 languages; instant syntax error diagnosis. | OpenHands `TreesitterBasicLinter`, `ast-syntax-verifier`. |
| **CAN-AGT-11** | **`qa-engineer`** | Quality Verification | Unit, integration, and E2E test suites; test harness execution; edge case verification. | MetaGPT `QaEngineer`, OpenHands `e2e-testing`, VoltAgent `test-automator`. |
| **CAN-AGT-12** | **`security-auditor`** | Quality Verification | Static application security testing (SAST), CVE audit, secret leakage detection, OWASP Top 10. | VoltAgent `security-auditor`, Copilot `appsec-reviewer`, Ruflo `sec-guard`. |
| **CAN-AGT-13** | **`debugger-detective`** | Reliability & Ops | Root-cause analysis, stack trace isolation, hypothesis generation, binary log search. | VoltAgent `debugger`, Copilot `troubleshooter`, LangGraph `Reflexion`. |
| **CAN-AGT-14** | **`devops-platform`** | Reliability & Ops | CI/CD pipelines, Dockerfiles, Kubernetes manifests, environment configuration, dependency locks.| VoltAgent `devops-engineer`, `docker-specialist`, OpenHands `local-stack-runtime`. |
| **CAN-AGT-15** | **`docs-technical-writer`**| Documentation | Architecture documentation, README synchronization, API docs, changelogs, drift detection.| VoltAgent `docs-drift-editor`, Copilot `tech-writer`, MetaGPT `TechnicalWriter`. |
| **CAN-AGT-16** | **`research-investigator`**| Research & Intelligence| Web research, academic paper investigation, competitor tech benchmarking, codebase scanning.| Anthropics `skill-creator` eval, Copilot `acquire-codebase-knowledge`, Ruflo `researcher`. |
| **CAN-AGT-17** | **`data-analyst`** | Data & Insights | Tabular data munging (Pandas/Polars), statistical analysis, analytical SQL, report charts. | Awesome-Copilot data prompts, LangGraph data extraction agents. |
| **CAN-AGT-18** | **`automation-specialist`**| Automation & Scripting | Workflow automation, web scraping, cron utilities, headless browser tasks, webhook scripts. | OpenHands `automation` machinery, Ruflo swarm tools. |

---

## 3. General-Purpose Domain Coverage Matrix

| Domain | Primary Canonical Agents | Supporting Skills | Primary Deliverable |
|---|---|---|---|
| **Software Development** | `product-analyst`, `system-architect`, `backend-engineer`, `frontend-engineer`, `database-specialist` | `api-contract-validator`, `str-replace-editor`, `ast-syntax-verifier` | Verified, tested, and reviewed source code |
| **Research & Exploration** | `research-investigator`, `system-architect` | `codebase-scanner`, `progressive-disclosure-loader` | Research dossier, benchmark comparison, ADR |
| **Documentation & Sync** | `docs-technical-writer`, `research-investigator` | `doc-drift-synchronizer`, `codebase-scanner` | Accurate READMEs, API specs, architecture guides |
| **Data Analysis & Insights**| `data-analyst`, `database-specialist` | `codebase-scanner`, `root-cause-diagnoser` | Data summaries, analytical SQL, trend charts |
| **Workflow Automation** | `automation-specialist`, `devops-platform` | `web-app-testing-harness`, `terminal-safety-sanitizer` | Python/bash automation scripts, cron jobs |
| **Technical Investigation**| `debugger-detective`, `surgeon-editor` | `root-cause-diagnoser`, `ast-syntax-verifier` | Reproduction test, root-cause report, patch |
| **Planning & Governance** | `orchestrator`, `product-analyst` | `prd-generator`, `adr-author`, `episodic-memory-ledger` | Dynamic execution DAG, acceptance criteria, ADRs |
