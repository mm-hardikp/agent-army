---
id: "CAN-SKL-09"
name: "ephemeral-test-server"
version: "1.0.0"
category: "Quality Verification"
description: >
  Spawns and manages ephemeral local test servers with automated readiness polling and guaranteed process cleanup.
trigger_patterns:
  - "run test server"
  - "start ephemeral server"
  - "test with server"
  - "headless test harness"
  - "server lifecycle"
tools_required:
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/ephemeral-test-server/SKILL.md"
---

# Skill: ephemeral-test-server

## 1. Purpose & Overview
Wraps test execution around a temporary local background server (e.g. dev server, mock API, test HTTP backend). Automatically polls for port binding readiness, executes the test suite, and guarantees process group termination without leaving orphaned zombie processes. Invokes `tools/ephemeral_server.py`.

When to use:
- Running integration tests or browser tests that require a live local server (`npm run dev`, `uvicorn main:app`, `python -m http.server`).
- Executing Playwright or Cypress test suites against local web apps.

When NOT to use:
- Pure unit tests that do not require network socket binding.
- Managing persistent production or staging servers.

## 2. Step-by-Step Execution Workflow
1. **Identify Server & Port**: Determine startup command (e.g. `npm run dev`) and target listening port (e.g. `5173`).
2. **Execute Wrapper**:
   ```bash
   python tools/ephemeral_server.py --server "npm run dev" --port 5173 --timeout 30 -- python -m pytest tests/e2e/
   ```
3. **Readiness Verification**: Wrapper polls port readiness via socket connection before test execution begins.
4. **Teardown**: Upon test completion or failure, wrapper terminates the server process group and closes all file pipes cleanly.

## 3. Constraints & Guardrails
- Zero daemon persistence: Processes are strictly killed when tests complete.
- Cross-platform process termination: Uses `taskkill /F /T` on Windows and `os.killpg` on Unix.
- Fail-safe timeout: Aborts cleanly if server fails to bind within the specified timeout.

## 4. Error Handling & Fallbacks
- If server fails to start due to port collision, identify free port and pass `--port <FREE_PORT>`.

## 5. Security & Permission Boundaries
- **Permission Level**: **Level 2 (Controlled Execution)**.
- Restricted to local loopback ports (`127.0.0.1` / `localhost`).
