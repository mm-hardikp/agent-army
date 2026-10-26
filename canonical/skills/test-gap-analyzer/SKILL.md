---
id: "CAN-SKL-16"
name: "test-gap-analyzer"
version: "1.0.0"
category: "Quality Verification"
description: >
  Audits test coverage metrics and code changes to identify untested execution branches and missing edge cases.
trigger_patterns:
  - "analyze test gaps"
  - "check test coverage"
  - "find untested code"
  - "missing unit tests"
  - "coverage gap analysis"
tools_required:
  - "read_file"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/test-gap-analyzer/SKILL.md"
---

# Skill: test-gap-analyzer

## 1. Purpose & Overview
Identifies untested execution branches, unverified edge cases, and test coverage gaps on newly created or modified code before release.

When to use:
- QA and test engineering reviews following feature implementation.
- Auditing test suite completeness against acceptance criteria.
- Identifying missing unit or integration tests for high-risk logic.

When NOT to use:
- Writing the test implementations directly (use test-specialist agents).
- Running routine test suites when coverage metrics are not needed.

## 2. Step-by-Step Execution Workflow
1. **Diff Identification**: Identify files and functions modified in the current branch.
2. **Coverage Data Ingestion**: Read coverage reports (`coverage.xml`, `lcov.info`, `.coverage`, or json coverage) using `read_file`.
3. **Gap Detection**:
   - Compare modified lines against uncovered lines in the coverage report.
   - Inspect conditional branches (`if/else`, error handlers, exception blocks) lacking test coverage.
4. **Gap Prioritization**: Classify gaps by risk:
   - High Risk: Unchecked error handlers, auth checks, financial/data mutations.
   - Medium Risk: Optional parameter branches, edge-case fallbacks.
5. **Recommendations**: Generate a concrete list of recommended test cases.

## 3. Constraints & Guardrails
- Prioritize behavioral edge-case coverage over arbitrary 100% line coverage metrics.
- Report specific file paths, function names, and missing test scenarios.

## 4. Error Handling & Fallbacks
- If no coverage engine is configured, inspect test files directly against source files to identify functions lacking corresponding test functions.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only analysis)**.
- Safe to run autonomously.
