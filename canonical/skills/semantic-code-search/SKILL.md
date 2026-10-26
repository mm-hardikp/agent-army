---
id: "CAN-SKL-15"
name: "semantic-code-search"
version: "1.0.0"
category: "Code Intelligence"
description: >
  Discovers implementations, symbols, and concepts across codebases using multi-term keyword search and symbol cross-referencing.
trigger_patterns:
  - "semantic code search"
  - "find implementation"
  - "locate symbol"
  - "codebase search"
  - "find usages"
tools_required:
  - "grep_search"
  - "read_file"
tier_level: 2
instructions_path: "canonical/skills/semantic-code-search/SKILL.md"
---

# Skill: semantic-code-search

## 1. Purpose & Overview
Navigates and searches large codebases by combining natural language intent with ripgrep pattern matching and AST symbol cross-referencing.

When to use:
- Locating where a feature, route, or business logic is implemented.
- Finding all usages or callers of a particular function or class.
- Searching for configuration settings or constants across the project.

When NOT to use:
- Broad exploratory browsing when the target file is already known.
- Replacing code (use `surgical-code-editor`).

## 2. Step-by-Step Execution Workflow
1. **Query Formulation**: Decompose natural language request into specific identifiers, class names, function names, or regex patterns.
2. **Grep Search**: Execute `grep_search` with exact casing or regex flags across workspace files.
3. **Filter & Rank**: Exclude build outputs (`dist/`, `build/`, `.git/`, `node_modules/`).
4. **Context Read**: Use `read_file` with line range (`StartLine`, `EndLine`) on top search hits to inspect full context.
5. **Synthesize Findings**: Return exact file paths, line numbers, and symbol context to the requesting specialist.

## 3. Constraints & Guardrails
- Always include surrounding line context when reporting search results.
- Limit search results to relevant source extensions (`.py`, `.ts`, `.js`, `.go`, `.rs`, `.md`) to maintain performance.

## 4. Error Handling & Fallbacks
- If literal search yields zero matches, retry with case-insensitive search (`CaseInsensitive: true`) or partial keyword matching.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only search)**.
- Safe to execute autonomously in standard sandbox.
