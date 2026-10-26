---
id: "CAN-SKL-04"
name: "surgical-code-editor"
version: "1.0.0"
category: "Precision Mutation"
description: >
  Applies deterministic, minimal, and surgical code replacements avoiding destructive whole-file overwrites.
trigger_patterns:
  - "surgical edit"
  - "replace code block"
  - "deterministic edit"
  - "safe edit"
  - "targeted modification"
tools_required:
  - "read_file"
  - "replace_file_content"
tier_level: 2
instructions_path: "canonical/skills/surgical-code-editor/SKILL.md"
---

# Skill: surgical-code-editor

## 1. Purpose & Overview
Performs targeted, deterministic modifications to existing source files using localized search-and-replace primitives. Prevents the accidental erasure of comments, helper functions, or unrelated code that frequently occurs with blind whole-file rewrites.

When to use:
- Refactoring, bug fixes, or adding functions to existing files.
- Small-to-medium scoped code edits.

When NOT to use:
- Creating entirely new files from scratch (use `write_to_file`).
- Bulk formatting or sweeping lint autofixes across entire repositories.

## 2. Step-by-Step Execution Workflow
1. **Read & Locate**: Read target lines using `read_file` to capture exact context, line numbers, and indentation.
2. **Formulate Target & Replacement**:
   - Select a unique target snippet including 2-3 lines of surrounding context.
   - Ensure target content matches existing characters and whitespace exactly.
3. **Apply Mutation**: Use `replace_file_content` (or `multi_replace_file_content` for non-contiguous edits).
4. **Verification**: Run `ast-syntax-verifier` (`tools/lint_ast.py`) immediately following the edit.

## 3. Constraints & Guardrails
- Never overwrite an entire file when only a function or block needs changing.
- Preserve existing comments, docstrings, licensing headers, and indentation style.
- Only modify files within assigned specialist task scope.

## 4. Error Handling & Fallbacks
- If `TargetContent` is not found or matches multiple instances, re-read the target file with line range bounds and expand surrounding context until the match is strictly unique.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Modification)**.
- Monitored execution within assigned task files. Requires immediate post-edit verification.
