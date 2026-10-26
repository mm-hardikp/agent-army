---
id: "CAN-SKL-08"
name: "security-secret-scanner"
version: "1.0.0"
category: "Ops & Safety"
description: >
  Scans source files and uncommitted diffs for hardcoded secrets, API tokens, passwords, and private keys.
trigger_patterns:
  - "scan secrets"
  - "check credentials"
  - "find leaked keys"
  - "pre-commit secret check"
  - "audit secrets"
tools_required:
  - "grep_search"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/security-secret-scanner/SKILL.md"
---

# Skill: security-secret-scanner

## 1. Purpose & Overview
Detects accidental inclusion of sensitive credentials, API keys, private keys, authentication tokens, and passwords in source code and configuration files.

When to use:
- Pre-commit check before staging any changes.
- Auditing configuration files (`.env`, `config.json`, `settings.py`).
- Onboarding new repositories to detect existing credential exposures.

When NOT to use:
- Full SAST security audits for complex application vulnerabilities (use specialized security tools).

## 2. Step-by-Step Execution Workflow
1. **Target Selection**: Identify unstaged or staged files in git working tree.
2. **Pattern Scanning**: Scan content using regex patterns for known secret formats:
   - AWS Keys (`AKIA[0-9A-Z]{16}`)
   - Private Keys (`-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----`)
   - Generic Tokens (`(api_key|secret|password|bearer|auth_token)\s*[:=]\s*['"][^'"]{8,}['"]`)
   - GitHub/GitLab Tokens (`ghp_[0-9A-Za-z]{36}`, `glpat-[0-9A-Za-z_-]{20}`)
3. **Evaluation**:
   - Zero findings: Proceed safely.
   - Findings detected: Flag file, line number, and redact secret value in alert.
4. **Escalation**: Block commit immediately. Prompt user via Level 3 human gate if a secret was committed historically.

## 3. Constraints & Guardrails
- Never output full plaintext secret values in logs or handoff messages; redact to first 4 characters followed by `****`.
- Exclude sample fixtures explicitly named `*.example`, `*.sample`, or test mocks containing dummy data (`test_secret_123`).

## 4. Error Handling & Fallbacks
- If regex scanning returns false positives on test mocks, verify whether file is under a `test/` or `mock/` directory.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 1 (Read-Only scanning)**.
- Remediation (removing secrets from git history) is **Level 3 (High-Risk)** and requires human approval.
