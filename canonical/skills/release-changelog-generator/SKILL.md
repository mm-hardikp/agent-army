---
id: "CAN-SKL-17"
name: "release-changelog-generator"
version: "1.0.0"
category: "Reliability & Documentation"
description: >
  Generates Keep-a-Changelog compliant release notes categorized from git commit history and closed task handoffs.
trigger_patterns:
  - "generate changelog"
  - "create release notes"
  - "update changelog"
  - "summarize release"
  - "draft changelog"
tools_required:
  - "run_command"
  - "write_to_file"
tier_level: 2
instructions_path: "canonical/skills/release-changelog-generator/SKILL.md"
---

# Skill: release-changelog-generator

## 1. Purpose & Overview
Parses conventional git commit history, closed milestone deliverables, and handoff records to generate clear, structured release notes conforming to Keep a Changelog.

When to use:
- Tagging a new release version or milestone closure.
- Updating `CHANGELOG.md` following milestone completion.
- Summarizing changes for stakeholder and user review.

When NOT to use:
- Generating PR descriptions (use `pr-description-generator`).
- Publishing tags or releases to GitHub/GitLab (requires Level 3 approval).

## 2. Step-by-Step Execution Workflow
1. **Commit Range Extraction**: Query git log between target revisions or since last tag:
   ```bash
   git log <last_tag>..HEAD --oneline
   ```
2. **Category Classification**: Group commits according to Keep a Changelog standards:
   - **Added**: New features and capabilities.
   - **Changed**: Changes in existing functionality.
   - **Deprecated**: Soon-to-be removed features.
   - **Removed**: Removed features.
   - **Fixed**: Bug fixes.
   - **Security**: Vulnerability resolutions.
3. **Format Notes**: Structure entry under `## [Version] - YYYY-MM-DD`.
4. **Update Changelog**: Prepend new release block to `CHANGELOG.md` using `write_to_file`.

## 3. Constraints & Guardrails
- Never invent changes not present in git history or verified handoff records.
- Preserve existing historical changelog entries intact.

## 4. Error Handling & Fallbacks
- If no git tags exist, query the full git log history (`git log --oneline`).

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Modification)** for `CHANGELOG.md`.
- Creating remote git tags or release assets requires human authorization.
