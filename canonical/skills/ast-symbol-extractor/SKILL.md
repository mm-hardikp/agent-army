---
id: "CAN-SKL-01"
name: "ast-symbol-extractor"
version: "1.0.0"
category: "Code Intelligence"
description: >
  Token-efficient AST symbol extractor and codebase discovery mechanism for rapid architectural mapping.
trigger_patterns:
  - "extract symbols"
  - "scan codebase"
  - "map code structure"
  - "find function definitions"
  - "code discovery"
tools_required:
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/ast-symbol-extractor/SKILL.md"
---

# Skill: ast-symbol-extractor

## 1. Purpose & Overview
Extracts high-level AST symbol tables (classes, functions, methods, parameters, and manifest ecosystems) from codebases with minimal token overhead. Invokes the standalone `tools/scan_ast.py` tool.

When to use:
- Initial project discovery and architectural mapping.
- Identifying available functions and class definitions without loading full source files.
- Locating package manifest files across multiple programming languages.

When NOT to use:
- Performing textual search for non-symbol keywords or comments (use `semantic-code-search` or `grep_search`).
- Modifying or editing code (use `surgical-code-editor`).

## 2. Step-by-Step Execution Workflow
1. **Target Identification**: Identify the directory or file path to inspect.
2. **Execution**: Run `tools/scan_ast.py` using `run_command`:
   ```bash
   python tools/scan_ast.py <target_path> --json --max-depth 3
   ```
3. **Parse Output**: Extract `symbol_index` and `manifests` from the JSON response.
4. **Handoff**: Provide the symbol inventory to the requesting specialist agent.

## 3. Constraints & Guardrails
- Automatically excludes large non-code directories (`node_modules`, `.git`, `dist`, `__pycache__`, `venv`).
- Does not modify any source files (strictly Level 1 Read-Only).
- Limits directory traversal depth via `--max-depth` to prevent performance bottlenecks.

## 4. Error Handling & Fallbacks
- If `tools/scan_ast.py` encounters unparseable syntax in a file, it logs the parse warning and continues scanning remaining files.
- If python execution fails, fall back to native ripgrep/grep symbol matching.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only)**.
- Safe to run autonomously in standard sandbox without human approval.
