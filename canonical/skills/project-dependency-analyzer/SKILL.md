---
id: "CAN-SKL-02"
name: "project-dependency-analyzer"
version: "1.0.0"
category: "Code Intelligence"
description: >
  Analyzes project manifests, lockfiles, and dependency graphs to identify ecosystems, versions, and constraints.
trigger_patterns:
  - "analyze dependencies"
  - "check manifest"
  - "inspect package.json"
  - "check requirements.txt"
  - "audit packages"
tools_required:
  - "read_file"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/project-dependency-analyzer/SKILL.md"
---

# Skill: project-dependency-analyzer

## 1. Purpose & Overview
Inspects project manifests and lockfiles to determine dependencies, runtime constraints, library versions, and potential version conflicts.

When to use:
- Analyzing tech stacks and package ecosystems upon repository onboarding.
- Checking whether a required library or utility is already present before proposing new dependencies.
- Investigating dependency compatibility issues or major version upgrades.

When NOT to use:
- Installing or upgrading packages (requires Level 2/3 modification approval).
- Security vulnerability auditing of dependencies (use `license-attribution-auditor` or external vulnerability scanners).

## 2. Step-by-Step Execution Workflow
1. **Manifest Detection**: Inspect project root for manifest files (`package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`).
2. **File Inspection**: Read manifest content using `read_file`.
3. **Tree Inspection (Optional)**: If a lockfile exists and CLI tooling is present, run read-only dependency tree commands:
   - Node: `npm list --depth=0` or `pnpm list`
   - Python: `pip list` or `poetry show --tree`
   - Rust: `cargo tree --depth 1`
   - Go: `go list -m all`
4. **Summary Generation**: Report production dependencies, dev dependencies, and version constraints.

## 3. Constraints & Guardrails
- Read-only execution. Never run mutating package commands like `npm install`, `pip install`, or `cargo add`.
- Do not read deeply nested `node_modules` or `.venv` source files directly.

## 4. Error Handling & Fallbacks
- If CLI package tools are not installed in the environment, fall back strictly to parsing static manifest files (`package.json`, `pyproject.toml`) via `read_file`.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only)**.
- Safe to run autonomously.
