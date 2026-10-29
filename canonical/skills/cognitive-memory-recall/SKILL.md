---
id: "CAN-SKL-19"
name: "cognitive-memory-recall"
version: "1.0.0"
category: "Reliability & Documentation"
description: >
  Synthesizes, catalogs, and retrieves persistent project memory snapshots, architectural rationales, and historical task summaries using the memory vault.
trigger_patterns:
  - "store task memory"
  - "recall past task"
  - "search memory vault"
  - "what did we do for"
  - "why did we choose"
  - "summarize milestone memory"
tools_required:
  - "read_file"
  - "write_to_file"
  - "run_command"
tier_level: 2
instructions_path: "canonical/skills/cognitive-memory-recall/SKILL.md"
---

# Skill: cognitive-memory-recall (CAN-SKL-19)

## 1. Purpose & Overview
Maintains persistent, long-term memory across multiple sessions, tasks, and repositories. Enables agents to capture high-level task summaries, architectural rationales (why decisions were made), and key files, and later perform conversational recall when a user or agent queries past work.

When to use:
- At the end of every completed feature, milestone, or technical investigation.
- When recording an architectural decision, technology trade-off, or complex bug fix.
- When a user asks: "Did we build something like this before?", "Why did we choose X?", or "Where did we write that logic?".
- Across multi-project workflows where learnings from one codebase apply to another.

When NOT to use:
- Ephemeral scratch notes or minute-by-minute commit logs (use git history).
- Large binary blobs or code dumps (store file pointers and summary snippets instead).

## 2. Vault Architecture & Storage Standard
By default, the vault is maintained in a central machine directory:
- **Default Path**: `C:\Agent-Memory` (or `~/.agent-memory` on non-Windows/restricted hosts, or custom path via `--vault` or `AGENT_MEMORY_PATH`).
- **Structure**:
  ```text
  C:\Agent-Memory\
  ├── config.json                     # Vault metadata, user preferences, created_at
  ├── index.json                      # Inverted search index with tags, summaries, and paths
  └── projects\
      └── <project-slug>\
          └── <YYYY-MM-DD>_<title-slug>.md  # Rich Markdown memory card
  ```

## 3. Step-by-Step Execution Workflow

### Step 1: Vault Initialization & First-Run Check
1. On first activation, check if `C:\Agent-Memory` exists using `python tools/memory_vault.py init`.
2. If first initializing for a user, confirm the storage location:
   *"Memory vault active at `C:\Agent-Memory`. All task summaries and architectural decisions will be cataloged here."*

### Step 2: Milestone & Task Memory Capture
At the conclusion of a milestone or feature:
1. Synthesize four essential pillars:
   - **WHAT**: High-level problem statement and solution implemented.
   - **WHY**: Architectural rationale, trade-offs evaluated, alternatives rejected (ADR summary).
   - **WHERE**: Key files, functions, and models modified.
   - **LEARNINGS**: Gotchas, edge cases resolved, configuration caveats.
2. Execute the CLI command:
   ```bash
   python tools/memory_vault.py store \
     --project "<project-name>" \
     --title "<descriptive-title>" \
     --what "<summary-of-what-was-done>" \
     --why "<why-this-solution-was-chosen>" \
     --where "<key-files-and-endpoints>" \
     --learnings "<gotchas-or-lessons>" \
     --tags "<tag1,tag2,tag3>" \
     --workflow "<workflow-id>"
   ```

### Step 3: Conversational Recall & Querying
When the user or another agent asks about past work:
1. Query the vault using `search`:
   ```bash
   python tools/memory_vault.py search "<user-query-keywords>" --json
   ```
2. If a specific memory ID is identified, retrieve full context:
   ```bash
   python tools/memory_vault.py get "<memory-id>" --json
   ```
3. Formulate a crisp, conversational answer highlighting:
   - When and in what project the work took place.
   - What was implemented and the specific file paths.
   - The architectural "why" behind the choice.

## 4. Guardrails & Boundaries
- Never store plaintext secrets, API keys, or private credentials in memory cards.
- Keep summaries high-level and dense with insight rather than dumping raw code.
- Always include explicit `tags` for domain keywords (e.g. `sqlite`, `fastapi`, `revenue`, `auth`).\n