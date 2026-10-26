---
id: "CAN-SKL-12"
name: "database-migration-linter"
version: "1.0.0"
category: "Quality Verification"
description: >
  Lints SQL and ORM database migration scripts for table locks, irreversible drops, and missing rollback paths.
trigger_patterns:
  - "lint migration"
  - "check database migration"
  - "safe migration check"
  - "audit sql migration"
  - "verify rollback"
tools_required:
  - "read_file"
  - "grep_search"
tier_level: 2
instructions_path: "canonical/skills/database-migration-linter/SKILL.md"
---

# Skill: database-migration-linter

## 1. Purpose & Overview
Lints database migration files (Flyway, Alembic, Prisma, Django, Knex, Liquibase) for dangerous DDL operations, table lock risks, and missing reversibility/rollback functions.

When to use:
- Creating or editing database schema migrations.
- Auditing pull requests containing database structural changes.

When NOT to use:
- Executing migrations against live production databases (Level 3 High-Risk).
- Running routine SQL read queries.

## 2. Step-by-Step Execution Workflow
1. **Locate Migration Files**: Find new or modified migration files under `migrations/` or `prisma/`.
2. **Syntax & Operation Audit**: Scan for high-risk DDL patterns:
   - Adding non-nullable column without a default value (`NOT NULL` lock risk).
   - Adding unindexed foreign keys on high-volume tables.
   - Dropping columns or tables without backward-compatible deprecation.
   - Renaming columns directly rather than dual-writing.
3. **Reversibility Check**: Verify that a valid rollback (`down()` or `downgrade()`) function is implemented.
4. **Report**: Flag dangerous patterns and suggest safe alternatives (e.g. add column as nullable first, backfill, then set not-null).

## 3. Constraints & Guardrails
- Strictly static analysis. Never execute `DROP TABLE` or destructive DDL on real databases without explicit Level 3 authorization.
- Every migration must have a tested or explicitly justified rollback path.

## 4. Error Handling & Fallbacks
- If migration uses raw SQL strings inside ORM methods, scan SQL strings using regex patterns for DDL hazards.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only auditing)**.
- Applying migrations to live databases is **Level 3 (Mandatory Human Approval)**.
