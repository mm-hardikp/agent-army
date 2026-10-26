---
id: "CAN-SKL-05"
name: "documentation-synthesizer"
version: "1.0.0"
category: "Reliability & Documentation"
description: >
  Synthesizes and updates architectural documentation, API contracts, ADRs, and READMEs verified against active code.
trigger_patterns:
  - "update documentation"
  - "generate docs"
  - "write adr"
  - "document api"
  - "update readme"
tools_required:
  - "read_file"
  - "write_to_file"
tier_level: 2
instructions_path: "canonical/skills/documentation-synthesizer/SKILL.md"
---

# Skill: documentation-synthesizer

## 1. Purpose & Overview
Creates and updates clear, accurate, code-verified technical documentation, Architecture Decision Records (ADRs), API guides, and README files.

When to use:
- Updating project documentation after implementing features or refactorings.
- Documenting architectural decisions in standard ADR format.
- Documenting public API interfaces, CLI flags, or schema definitions.

When NOT to use:
- Speculative design documents without ground-truth code verification.
- Writing marketing copy or unverified assumptions.

## 2. Step-by-Step Execution Workflow
1. **Source Verification**: Read source code and schemas directly to verify actual parameters, return types, and behaviors before drafting documentation.
2. **Structure Selection**:
   - ADR: Title, Status, Context, Decision, Consequences.
   - API Reference: Endpoint/Function, Parameters, Returns, Example, Errors.
   - README: Project Overview, Quickstart, Architecture, License.
3. **Draft Documentation**: Write clear, concise Markdown adhering to GitHub Flavored Markdown.
4. **Link Verification**: Ensure all referenced file paths use valid clickable relative or absolute links.

## 3. Constraints & Guardrails
- Every documented feature or parameter must correspond to active, verified code.
- Keep documentation concise and scannable; avoid verbose redundancy.

## 4. Error Handling & Fallbacks
- If code behavior is ambiguous, verify by inspecting tests or running AST symbol extraction before writing the documentation.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Modification)** for documentation files.
- Modifying documentation files within workspace does not require Level 3 approval.
