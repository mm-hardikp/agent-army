---
id: "CAN-SKL-10"
name: "headless-browser-runner"
version: "1.0.0"
category: "Quality Verification"
description: >
  Executes automated headless browser tests, visual assertions, and DOM snapshots using Playwright or native runners.
trigger_patterns:
  - "run browser test"
  - "headless test"
  - "playwright test"
  - "ui verification"
  - "e2e browser test"
tools_required:
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/headless-browser-runner/SKILL.md"
---

# Skill: headless-browser-runner

## 1. Purpose & Overview
Executes end-to-end browser automation, visual assertions, and regression checks in headless browser environments. Pairs with `ephemeral-test-server` for local full-stack test execution.

When to use:
- Validating UI components, client-side routing, and DOM rendering.
- Capturing screenshots and video recordings of web application workflows.
- Verifying web application responsiveness and accessibility.

When NOT to use:
- Backend-only unit tests that do not render HTML/CSS/JS.
- Scraping public web pages (use HTTP client tools or web search).

## 2. Step-by-Step Execution Workflow
1. **Prerequisites Check**: Verify browser automation framework (Playwright, Puppeteer, or IDE native browser agent) is available.
2. **Launch Server Harness**: If testing a local app, launch via `ephemeral-test-server`:
   ```bash
   python tools/ephemeral_server.py --server "npm run dev" --port 3000 -- npx playwright test
   ```
3. **Inspect Output**: Review test reports, failed assertion traces, and DOM snapshots.
4. **Handoff**: Provide test results and failure logs to requesting agent.

## 3. Constraints & Guardrails
- Must run in headless mode (`--headless`) to prevent unwanted window popups on the host desktop.
- Set strict navigation timeouts (e.g. 15-30s) to avoid hanging on slow network requests.

## 4. Error Handling & Fallbacks
- If Playwright browsers are not installed, run `npx playwright install --with-deps chromium` or fall back to HTTP status code verification.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Execution)**.
- Safe to run locally against workspace applications.
