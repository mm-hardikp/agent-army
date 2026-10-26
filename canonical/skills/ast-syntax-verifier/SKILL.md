---
id: "CAN-SKL-03"
name: "ast-syntax-verifier"
version: "1.0.0"
category: "Quality Verification"
description: >
  Fast AST syntax verification gate with fallback to native project compilers before and after file modifications.
trigger_patterns:
  - "verify syntax"
  - "lint ast"
  - "check parse errors"
  - "pre-edit check"
  - "post-edit check"
tools_required:
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/ast-syntax-verifier/SKILL.md"
---

# Skill: ast-syntax-verifier

## 1. Purpose & Overview
Provides instant, sub-second syntax verification on source files before and after modifications to catch parse errors, unbalanced braces, and invalid syntax. Invokes `tools/lint_ast.py`.

When to use:
- Pre-mutation baseline verification: Confirm file is syntactically valid before editing.
- Post-mutation gate: Verify edits did not introduce syntax or parse errors before handing off.

When NOT to use:
- Running comprehensive unit or integration test suites (use dedicated test runners).
- Semantic type-checking across large projects (use native project compilers `tsc`, `cargo check`, etc.).

## 2. Step-by-Step Execution Workflow
1. **Pre-Check**: Run `tools/lint_ast.py <file>` to verify current syntax validity:
   ```bash
   python tools/lint_ast.py path/to/file.py
   ```
2. **Execute Edit**: Specialist agent performs surgical edit.
3. **Post-Check**: Re-run `tools/lint_ast.py <file>` to verify syntax after mutation.
4. **Gate Evaluation**:
   - Exit Code 0 (`[AST LINT PASS]`): Proceed to next task.
   - Exit Code 1 (`[AST LINT FAIL]`): Revert or correct the syntax error immediately.

## 3. Constraints & Guardrails
- Uses Python native `ast` for instant zero-dependency checks on Python files.
- Uses `tree_sitter` or project compiler fallbacks (`tsc --noEmit`, `cargo check`, `go build`) when available.
- Fails closed on syntax errors; agents must not proceed if syntax verification fails.

## 4. Error Handling & Fallbacks
- If a language compiler or tree-sitter is unavailable, the tool outputs a bypass warning and exits cleanly without blocking execution.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only verification)**.
- Safe to execute autonomously in standard sandbox.
