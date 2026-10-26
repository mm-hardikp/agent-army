# Agent Communication & Handoff Protocol (CAN-ENV-01 v2.2)

## 1. Executive Summary & Design Principle

Multi-agent coordination collapses when communication is informal, lossy, or uncoordinated. 

The **CAN-ENV-01 v2.2 Protocol** defines a unified, bi-directional, stateful communication envelope supporting real-world asynchronous collaboration, change requests, blocker escalations, message acknowledgements, deduplication, running-task cancellation with clean resource reclamation, and review feedback across all specialist agents and the central Orchestrator.

---

## 2. Standardized Message Types & Routing Topology

### Centralized Hub-and-Spoke Invariant:
*Agents NEVER send unmediated peer-to-peer messages.*
All communication flows through the **Orchestrator as the Authoritative State Owner**. This guarantees:
1. Every state mutation, change request, blocker, and cancellation is recorded in `.agent/state.json`.
2. No hidden side-channel agreements or unmonitored locks occur between agents.
3. The Orchestrator retains 100% complete visibility over task progress, active leases, and history.

| Message Type | Direction | Routing & Owner | Semantic Purpose |
|---|---|---|---|
| **`TASK_ASSIGNMENT`** | Orchestrator $	o$ Agent | Dispatched by Orchestrator | Assigns atomic task, scope, inputs, tools, skills, and acceptance criteria. |
| **`TASK_ACCEPTANCE`** | Agent $	o$ Orchestrator | Emitted by Assigned Agent | Confirms receipt, acknowledges prerequisite availability, and transitions task to `IN_PROGRESS`. |
| **`TASK_COMPLETION`** | Agent $	o$ Orchestrator | Emitted by Assigned Agent | Declares task complete, provides artifact list, test proofs, and handoff payload. |
| **`HANDOFF`** | Agent $	o$ Orchestrator $	o$ Consumer | Routed by Orchestrator | Transmits completed contract, schema, or asset payload to downstream consumer. |
| **`CLARIFICATION_REQUEST`**| Agent $	o$ Orchestrator $	o$ User | Routed to User / Product Analyst | Requests missing requirements, business rules, or design decisions. |
| **`CHANGE_REQUEST`** | Downstream Agent $	o$ Orch $	o$ Upstream | Evaluated by Orchestrator | Requests modification to an upstream interface, contract, or dependent implementation. |
| **`REVIEW_FINDING`** | Code Reviewer $	o$ Orch $	o$ Author | Validated by Orchestrator | Reports security, logic, or architectural defects with line citations and remediation instructions. |
| **`BLOCKER`** | Agent $	o$ Orchestrator | Evaluated by Orchestrator | Declares execution halted due to external failure, missing dependency, or environment bug. |
| **`DISAGREEMENT`** | Agent $	o$ Orch $	o$ Architect | Arbitrated by System Architect | Formal notice of conflicting technical approaches; results in binding ADR. |
| **`APPROVAL_REQUEST`** | Agent $	o$ Orchestrator $	o$ User | Decided by Human User | Solicits human authorization for Level 3 high-risk actions (deploy, delete, push). |
| **`APPROVAL_RESPONSE`** | User $	o$ Orchestrator $	o$ Agent | Relayed by Orchestrator | Relays human decision (`allow_accept`, `allow_edit`, `allow_respond`, `allow_ignore`). |
| **`TASK_REASSIGNMENT`** | Orchestrator $	o$ Agent | Dispatched by Orchestrator | Cancels stalled/failed agent attempt; reassigns task to alternate specialist or resets context. |
| **`TASK_CANCELLATION`** | Orchestrator $	o$ Agent (and Ack) | Managed by Orchestrator | Orders immediate termination of in-progress task; triggers safe workspace cleanup and lock release. |

---

## 3. CAN-ENV-01 v2.2 Specification Schema

All messages conform to the following structured schema (serialized as JSON or YAML):

```yaml
envelope:
  version: "2.2.0"
  message_id: "MSG-2026-1042"
  correlation_id: "CORR-FEATURE-CUST-MGT"
  task_id: "TASK-FE-003"
  idempotency_key: "IDEM-FE-003-ATTEMPT-1" # Deduplication key
  timestamp: "2026-10-24T17:28:00Z"
  message_type: "CHANGE_REQUEST" # One of 13 standard types
  sending_agent: "frontend-engineer"
  receiving_agent: "orchestrator"
  target_specialist: "backend-engineer" # Destination specialist routed via Orchestrator
  attempt_number: 1
  requires_ack: true
  
  status_summary: >
    Frontend integration blocked: GET /api/v1/customers response contract is missing
    the 'loyalty_tier' field required by acceptance criterion AC-04.

  acceptance_criteria_status:
    - id: "AC-01"
      description: "Render responsive customer list table"
      status: "MET"
    - id: "AC-04"
      description: "Display customer loyalty tier badge"
      status: "BLOCKED_ON_CONTRACT"

  change_request_details:
    target_interface: "REST_API: GET /api/v1/customers"
    nature_of_change: "SCHEMA_EXTENSION"
    proposed_field: "loyalty_tier: enum ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']"
    rationale: "Required to render customer status badges without secondary round-trips."

  artifacts_and_evidence:
    - type: "UI_COMPONENT"
      path: "src/components/CustomerTable.tsx"
    - type: "MOCK_SCHEMA"
      path: "tests/mocks/customer-mock.json"

  blocker_info:
    is_hard_blocker: false
    can_proceed_with_mocks: true
    workaround_in_use: "Using temporary hardcoded mock enum in tests."

  review_findings: [] # Populated during REVIEW_FINDING messages

  cancellation_details: # Populated during TASK_CANCELLATION messages
    reason: ""
    rollback_target_checkpoint: ""
    locks_to_release: []
    cleanup_actions_completed: []

  handoff_history:
    - turn: 1
      agent: "system-architect"
      action: "Published initial OpenAPI spec (v1.0.0)"
    - turn: 2
      agent: "frontend-engineer"
      action: "Identified missing loyalty_tier in AC-04 verification"

  explicit_next_action:
    recommended_target: "backend-engineer"
    required_action: "Update Pydantic model and OpenAPI schema to include loyalty_tier."
```

---

## 4. Formal Protocol: TASK_CANCELLATION & Safe Cleanup

When an upstream dependency fails permanently, a task times out, or the human user aborts a workstream, the Orchestrator initiates the formal `TASK_CANCELLATION` protocol:

```mermaid
sequenceDiagram
    autonumber
    actor Orch as Central Orchestrator
    actor Worker as In-Progress Specialist Agent
    participant LockReg as .agent/locks.json
    participant StateReg as .agent/state.json

    Note over Orch: Upstream failure / User abort / Timeout
    Orch->>Worker: CAN-ENV-01 (TASK_CANCELLATION: Reason, target_checkpoint)
    Note over Worker: Halts active generation / tool calls
    Note over Worker: Reverts uncommitted changes / discards temp files
    Worker->>LockReg: Surrenders all leased file locks
    Worker->>Orch: CAN-ENV-01 (TASK_CANCELLATION acknowledgement: Cleaned files, released locks)
    Note over Orch: Validates workspace cleanliness (git status check)
    Orch->>StateReg: Transitions task status to CANCELLED; records audit trail
```

### Invariants of Safe Cancellation:
1. **Running Task Interruption**: The agent immediately ceases further tool invocations or edits upon receiving `TASK_CANCELLATION`.
2. **Deterministic Workspace Rollback**: The agent or Orchestrator reverts any dirty uncommitted changes in the agent's worktree/workspace back to the last clean checkpoint (`target_checkpoint`), leaving no corrupted partial edits.
3. **Guaranteed Lock Surrender**: All active leases held in `.agent/locks.json` by the cancelled task are revoked and immediately made available to other queued tasks.
4. **Cancellation Acknowledgement**: The agent returns an acknowledgement payload detailing the reverted files and released locks. The Orchestrator validates workspace cleanliness before updating `.agent/state.json`.
