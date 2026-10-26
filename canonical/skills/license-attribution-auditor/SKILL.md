---
id: "CAN-SKL-14"
name: "license-attribution-auditor"
version: "1.0.0"
category: "Ops & Safety"
description: >
  Audits repository dependencies and source files for open-source license compliance, copyleft risks, and attributions.
trigger_patterns:
  - "audit licenses"
  - "check license compatibility"
  - "verify attribution"
  - "scan gpl risk"
  - "license check"
tools_required:
  - "read_file"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/license-attribution-auditor/SKILL.md"
---

# Skill: license-attribution-auditor

## 1. Purpose & Overview
Audits third-party dependencies, harvested code, and vendored packages for open-source license compliance. Flags copyleft contamination (GPL, AGPL) and verifies required attribution notices.

When to use:
- Evaluating new external libraries before adoption.
- Auditing project dependencies prior to release.
- Verifying compliance with MIT, Apache 2.0, BSD, and proprietary license boundaries.

When NOT to use:
- Legal advice (provides technical compliance heuristics, not formal legal counsel).

## 2. Step-by-Step Execution Workflow
1. **Manifest & Lockfile Scan**: Inspect dependencies via `read_file` on `package.json`, `Cargo.lock`, `requirements.txt`.
2. **License Resolution**:
   - Check declared `license` field in manifests.
   - Run project license tool if available (e.g. `npx license-checker`, `pip-licenses`).
3. **Classification**:
   - **Permissive**: MIT, Apache 2.0, BSD-2/3-Clause, ISC.
   - **Weak Copyleft**: LGPL, MPL 2.0.
   - **Strong Copyleft**: GPLv2/v3, AGPLv3.
   - **Restricted/Non-Commercial**: CC-BY-NC, PolyForm Noncommercial, BSL.
4. **Report & Attribution**: Flag strong copyleft risks and ensure copyright notices are added to `THIRD_PARTY_LICENSES` or notice files.

## 3. Constraints & Guardrails
- Permissive licenses (MIT, Apache 2.0) are preferred.
- Strongly flag AGPL or commercial restriction risks before any code integration.

## 4. Error Handling & Fallbacks
- If license metadata is missing in the manifest, read the raw package repository `LICENSE` file.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only auditing)**.
- Safe to run autonomously.
