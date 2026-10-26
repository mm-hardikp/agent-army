# Target Repository Structure

## 1. Executive Summary & Design Vision

The final Universal AI Agent Army repository must be clean, modular, self-documenting, and easy to maintain. It separates **canonical specifications** from **generated IDE adapters** and **shared executable tools**.

---

## 2. Proposed Target Repository Layout

```
Agent-Army/
├── README.md                        # Master project documentation, quickstart, philosophy
├── LICENSE                          # MIT License
├── AGENTS.md                        # Strict agent contributor rules & safety constraints
├── Makefile / package.json          # Build & validation automation scripts
│
├── canonical/                       # CANONICAL SOURCE OF TRUTH (Pure Markdown & YAML)
│   ├── agents/                      # 16 Canonical Agent Specifications (CAN-AGT-SPEC)
│   │   ├── orchestrator.md
│   │   ├── product-analyst.md
│   │   ├── system-architect.md
│   │   ├── backend-engineer.md
│   │   ├── frontend-engineer.md
│   │   ├── database-specialist.md
│   │   ├── surgeon-editor.md
│   │   ├── code-reviewer.md
│   │   ├── syntax-verifier.md
│   │   ├── qa-engineer.md
│   │   ├── security-auditor.md
│   │   ├── debugger-detective.md
│   │   ├── devops-platform.md
│   │   ├── docs-technical-writer.md
│   │   └── research-investigator.md
│   ├── skills/                      # 18 Canonical Skills (SKILL.md + references/)
│   │   ├── codebase-scanner/
│   │   ├── str-replace-editor/
│   │   ├── ast-syntax-verifier/
│   │   ├── code-review-standards/
│   │   ├── prd-generator/
│   │   ├── system-architecture-designer/
│   │   ├── adr-author/
│   │   ├── skill-eval-creator/
│   │   ├── web-app-testing-harness/
│   │   ├── git-worktree-isolator/
│   │   ├── episodic-memory-ledger/
│   │   ├── progressive-disclosure-loader/
│   │   ├── api-contract-validator/
│   │   ├── root-cause-diagnoser/
│   │   ├── security-vulnerability-scanner/
│   │   ├── test-suite-builder/
│   │   ├── doc-drift-synchronizer/
│   │   └── terminal-safety-sanitizer/
│   ├── workflows/                   # 10 Reusable Cognitive Workflows (CAN-WFL-*)
│   │   ├── feature-development.md
│   │   ├── bug-investigation-fix.md
│   │   ├── independent-code-review.md
│   │   ├── technical-research-spike.md
│   │   ├── system-architecture-design.md
│   │   ├── database-lifecycle.md
│   │   ├── documentation-synchronization.md
│   │   ├── security-vulnerability-audit.md
│   │   ├── test-suite-expansion.md
│   │   └── parallel-worktree-swarm.md
│   ├── protocols/                   # Schemas & contracts (CAN-ENV-01 handoffs)
│   │   ├── handoff-envelope.schema.json
│   │   └── state-ledger.schema.json
│   └── policies/                    # Governance & safety policies
│       ├── permission-hierarchy.md
│       └── human-approval-rules.md
│
├── tools/                           # Standalone Executable CLI Helpers (Zero-Daemon)
│   ├── scan_ast.py                  # Python AST symbol scanner (SKL-01)
│   ├── lint_ast.py                  # Tree-sitter multi-language syntax linter (SKL-03)
│   ├── with_server.py               # Ephemeral test server harness (SKL-09)
│   └── isolate_worktree.sh          # Git worktree concurrency isolator (SKL-10)
│
├── adapters/                        # IDE Adapters (Compiled from canonical definitions)
│   ├── claude-code/                 # Output: .claude/agents/*.md
│   ├── antigravity/                 # Output: .agents/skills/ & rules/
│   ├── cursor/                      # Output: .cursor/rules/*.mdc
│   └── copilot/                     # Output: .github/copilot-instructions/
│
├── scripts/                         # Build & validation pipelines
│   ├── compile_adapters.py          # Transpiles canonical/ into adapters/
│   ├── validate_canonical.py        # Schema validation & broken link checks
│   └── run_evals.py                 # Skill & prompt benchmark runner
│
└── tests/                           # Test fixtures & unit tests for tools & adapters
    ├── test_lint_ast.py
    ├── test_scan_ast.py
    └── test_adapter_compilation.py
```

---

## 3. Directory Responsibility Analysis

- **`canonical/`**: The immutable core. Any new capability, prompt improvement, or boundary constraint is authored here first. Never edit compiled adapter files directly.
- **`tools/`**: Self-contained, portable Python/Bash scripts that agents invoke to perform deterministic tasks (scanning, AST parsing, worktree management). These scripts require no continuous server or database.
- **`adapters/`**: Houses the generated assets tailored for each IDE target. If a developer uses Cursor, they copy or symlink `adapters/cursor/`; if they use Antigravity, they mount `adapters/antigravity/`.
- **`scripts/`**: CI/CD automation that guarantees canonical definitions compile cleanly and pass all validation gates.
