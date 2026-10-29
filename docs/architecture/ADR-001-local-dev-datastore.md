# ADR-001: Local Development Datastore Engine

## Status
**ACCEPTED** (Date: 2026-10-26, Decision Lead: `system-architect` [CAN-AGT-03], Approved by: `orchestrator` [CAN-AGT-01])

---

## 1. Context & Problem Framing

The **Universal AI Agent Army** is built upon a fundamental architectural axiom: **Zero-Daemon, Zero-Overhead Execution**. Developers must be able to clone the repository and run agents immediately in any IDE without spinning up Docker containers, background database services, or external cloud dependencies.

As the Agent Army expands into Phase 2 pilots (requiring local session persistence, run history caching, and task telemetry), we must establish an authoritative local data storage standard.

We evaluated two primary candidates:
1. **SQLite 3** (In-process, zero-configuration, embedded relational engine).
2. **PostgreSQL** (Client-server relational database management system).

---

## 2. Decision Matrix & Trade-Off Analysis

| Evaluation Criterion | SQLite 3 | PostgreSQL | Architectural Impact | Winner |
|---|---|---|---|:---:|
| **Installation & Daemon Overhead** | **Zero**. Built directly into standard Python runtime (`sqlite3`). No services or background processes. | **High**. Requires local service install (`pg_ctl`), Docker container, or external cloud instance. | Eliminates developer onboarding friction; conforms to Zero-Daemon philosophy. | **SQLite** |
| **Cross-Platform Portability** | **100% Native** across Windows, macOS, and Linux without OS-specific package managers. | Requires platform-specific service management, open ports, and permission configuration. | Repository runs identically on any workstation or air-gapped machine. | **SQLite** |
| **Startup & Execution Latency** | Sub-millisecond connection time (in-process memory or single local `.db` file). | TCP/Socket handshake latency; connection pooling required. | Speeds up test suites and sub-second tool verification. | **SQLite** |
| **Concurrency & Write Locks** | Single-writer with Write-Ahead Logging (`WAL` mode). High concurrent read throughput. | Multi-Version Concurrency Control (MVCC) with fine-grained row-level locking. | For local agent orchestration and task caching, single-writer WAL is more than adequate. | **PostgreSQL (High Concurrency)** |
| **Complex Types & Extensions** | JSON1 support, full-text search (`FTS5`), dynamic typing. | Advanced native types (`JSONB`, `UUID`, arrays), custom extensions (`pgvector`, `PostGIS`). | Advanced production features are not needed for local agent state management. | **PostgreSQL (Production)** |
| **CI/CD & Test Automation** | Instant in-memory (`:memory:`) or ephemeral file creation. Zero network setup. | Requires service containers (`services: postgres`) in GitHub Actions workflows. | Dramatically simplifies test runner harnesses (`tests/`). | **SQLite** |

---

## 3. Decision

We adopt **SQLite 3** as the **canonical local development datastore engine** for the Universal AI Agent Army.

### Implementation Standards:
1. **Zero External Drivers**: Utilize the standard library `sqlite3` module exclusively for local persistence. No `pip install psycopg2` or heavy ORM dependencies required.
2. **Write-Ahead Logging (WAL)**: All local SQLite connections must initialize with:
   ```sql
   PRAGMA journal_mode = WAL;
   PRAGMA synchronous = NORMAL;
   PRAGMA foreign_keys = ON;
   ```
   This guarantees safe concurrent readers while specialist agents log execution metrics.
3. **Pluggable Adapter Pattern**: If a downstream application built *by* the Agent Army requires production PostgreSQL, the **Database Specialist (`CAN-AGT-06`)** will generate dialect-agnostic migrations (e.g. standard SQL or Prisma/SQLAlchemy) supporting PostgreSQL as an external target without making it a prerequisite for running the Agent Army itself.

---

## 4. Consequences & Invariants

### Positive Consequences
- **Instant Developer Experience**: Cloning `agent-army` and running tests requires zero database configuration or port allocations.
- **Fast Test Execution**: Full unit and integration suites run in sub-second memory without database fixtures or teardown cleanup.
- **Single-File Portability**: All local run logs and state can be stored in a single `.agent/history.db` file (gitignored).

### Negative Consequences & Mitigations
- *Limitation*: SQLite does not support multiple simultaneous write transactions across distributed machines.
  - *Mitigation*: The Orchestrator enforces single-writer leases via CAN-ENV-01 two-phase file locking.
- *Limitation*: No native distributed clustering.
  - *Mitigation*: The Agent Army's local operational state is single-workspace bounded; distributed synchronization is out of scope for local IDE execution.

---

## 5. Participating Agent Verification Sign-off

- `CAN-AGT-16` (`research-investigator`): *Empirical benchmarking and dependency footprint audited.*
- `CAN-AGT-03` (`system-architect`): *ADR contract authored and aligned with Zero-Daemon architecture.*
- `CAN-AGT-01` (`orchestrator`): *Ratified into canonical architecture.*
