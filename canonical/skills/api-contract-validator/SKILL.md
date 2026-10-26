---
id: "CAN-SKL-11"
name: "api-contract-validator"
version: "1.0.0"
category: "Quality Verification"
description: >
  Validates OpenAPI, JSON Schema, GraphQL, and Protobuf interface contracts for breaking changes and field integrity.
trigger_patterns:
  - "validate api contract"
  - "check schema compatibility"
  - "lint openapi"
  - "breaking change check"
  - "verify api schema"
tools_required:
  - "read_file"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/api-contract-validator/SKILL.md"
---

# Skill: api-contract-validator

## 1. Purpose & Overview
Audits API schemas (OpenAPI 3.x, JSON Schema, GraphQL SDL, Protobuf) for syntactic correctness, breaking interface changes, missing required fields, and type discrepancies.

When to use:
- Modifying backend API route schemas or client request models.
- Validating handoff contracts between frontend and backend specialist agents.
- Preventing breaking changes in public API contracts.

When NOT to use:
- Testing live HTTP endpoint responses (use API test runners or unit tests).

## 2. Step-by-Step Execution Workflow
1. **Schema Ingestion**: Read API schema files (`openapi.yaml`, `schema.graphql`, `*.schema.json`) using `read_file`.
2. **Schema Validation**:
   - For JSON Schema: Validate using `scripts/validate_canonical.py` or project validator.
   - For OpenAPI: Run project linter (e.g. `npx @redocly/cli lint` or spectral if present).
3. **Diff Analysis**: Compare modified schema against base branch to identify breaking changes:
   - Removed endpoints or fields.
   - Renamed request/response parameters.
   - Changed field nullability or types.
4. **Report**: Emit pass/fail status and explicit breaking change warnings.

## 3. Constraints & Guardrails
- Fail closed on breaking schema changes unless an explicit version bump (e.g. `/v2/`) is documented.
- Verify that required fields match canonical naming conventions (`snake_case` or `camelCase`).

## 4. Error Handling & Fallbacks
- If external linters are missing, validate structural JSON/YAML validity and required fields using `scripts/validate_canonical.py`.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only validation)**.
- Safe to run autonomously.
