#!/usr/bin/env python3
r"""
memory_vault.py - Zero-dependency persistent memory engine and recall indexer.
Maintains persistent task snapshots, architectural decisions (ADRs), and cross-project learnings.
Default location: C:\Agent-Memory (configurable via --vault or AGENT_MEMORY_PATH).

Usage:
    python memory_vault.py init [--vault PATH] [--user USERNAME]
    python memory_vault.py store --project SLUG --title TITLE --what TEXT --why TEXT [--where FILES] [--learnings TEXT] [--tags TAG1,TAG2] [--vault PATH]
    python memory_vault.py search QUERY [--project SLUG] [--tag TAG] [--vault PATH] [--json]
    python memory_vault.py list [--project SLUG] [--vault PATH] [--json]
    python memory_vault.py get MEMORY_ID [--vault PATH] [--json]
"""

import os
import sys
import json
import re
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

DEFAULT_VAULT_WIN = Path("C:/Agent-Memory")
DEFAULT_VAULT_FALLBACK = Path.home() / ".agent-memory"


def resolve_vault_path(custom_path: Optional[str] = None) -> Path:
    """Resolves the active memory vault directory."""
    if custom_path:
        return Path(custom_path).expanduser().resolve()
    env_path = os.environ.get("AGENT_MEMORY_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()
    if os.name == "nt":
        try:
            DEFAULT_VAULT_WIN.mkdir(parents=True, exist_ok=True)
            return DEFAULT_VAULT_WIN
        except (PermissionError, OSError):
            return DEFAULT_VAULT_FALLBACK
    return DEFAULT_VAULT_FALLBACK


def slugify(text: str) -> str:
    """Converts a string to a safe kebab-case slug."""
    text = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.lower()).strip("-")
    return text[:40] or "task"


class MemoryVault:
    """Manages the persistent multi-project memory vault and search index."""

    def __init__(self, vault_dir: Path):
        self.vault_dir = vault_dir
        self.config_file = self.vault_dir / "config.json"
        self.index_file = self.vault_dir / "index.json"
        self.projects_dir = self.vault_dir / "projects"

    def init_vault(self, username: Optional[str] = None) -> Dict[str, Any]:
        """Initializes the memory vault directory structure and index."""
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            cfg = {
                "version": "1.0.0",
                "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "default_user": username or os.environ.get("USERNAME", "developer"),
                "vault_path": str(self.vault_dir)
            }
            self.config_file.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

        if not self.index_file.exists():
            initial_index = {
                "version": "1.0.0",
                "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "entries": []
            }
            self.index_file.write_text(json.dumps(initial_index, indent=2), encoding="utf-8")

        return {
            "status": "initialized",
            "vault_path": str(self.vault_dir),
            "config": json.loads(self.config_file.read_text(encoding="utf-8")),
            "total_entries": len(self.load_index().get("entries", []))
        }

    def load_index(self) -> Dict[str, Any]:
        """Loads index.json or returns default empty index."""
        if not self.index_file.exists():
            return {"version": "1.0.0", "updated_at": "", "entries": []}
        try:
            return json.loads(self.index_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"version": "1.0.0", "updated_at": "", "entries": []}

    def save_index(self, index_data: Dict[str, Any]) -> None:
        """Saves updated index data."""
        index_data["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.index_file.write_text(json.dumps(index_data, indent=2), encoding="utf-8")

    def store_memory(
        self,
        project: str,
        title: str,
        what: str,
        why: str,
        where_files: Optional[str] = None,
        learnings: Optional[str] = None,
        tags: Optional[List[str]] = None,
        workflow: Optional[str] = None,
        author: Optional[str] = None
    ) -> Dict[str, Any]:
        """Stores a new memory entry and updates the search index."""
        self.init_vault()

        proj_slug = slugify(project)
        title_slug = slugify(title)
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        time_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Stable unique memory ID
        seed = f"{proj_slug}:{title}:{time_iso}"
        hash_suffix = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
        memory_id = f"MEM-{proj_slug.upper()}-{now.strftime('%Y%m%d')}-{hash_suffix}"

        project_dir = self.projects_dir / proj_slug
        project_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{date_str}_{title_slug}.md"
        file_path = project_dir / filename
        counter = 1
        while file_path.exists():
            filename = f"{date_str}_{title_slug}_{counter}.md"
            file_path = project_dir / filename
            counter += 1

        tag_list = [t.strip().lower() for t in (tags or []) if t.strip()]

        # Generate markdown card
        where_section = where_files.strip() if where_files else "None explicitly listed."
        learnings_section = learnings.strip() if learnings else "None documented."
        workflow_tag = workflow or "Unspecified"

        md_content = f"""# Memory Snapshot: {title}
<!-- Memory ID: {memory_id} -->
- **Memory ID**: `{memory_id}`
- **Date**: {date_str}
- **Project**: `{project}`
- **Workflow**: `{workflow_tag}`
- **Author/Agent**: `{author or 'memory-keeper'}`
- **Tags**: {", ".join([f"`{t}`" for t in tag_list]) or "None"}

---

## 1. What Was Done
{what.strip()}

---

## 2. Why This Approach Was Chosen (Architectural Rationale)
{why.strip()}

---

## 3. Key Files & Components (Where)
{where_section}

---

## 4. Learnings, Gotchas & Caveats
{learnings_section}
"""
        file_path.write_text(md_content.strip() + "\\n", encoding="utf-8")

        # Update index
        index_data = self.load_index()
        rel_path = f"projects/{proj_slug}/{filename}"

        entry_record = {
            "id": memory_id,
            "project": project,
            "project_slug": proj_slug,
            "date": date_str,
            "timestamp": time_iso,
            "title": title,
            "what_summary": what[:200] + ("..." if len(what) > 200 else ""),
            "why_summary": why[:200] + ("..." if len(why) > 200 else ""),
            "tags": tag_list,
            "workflow": workflow_tag,
            "relative_path": rel_path
        }

        index_data["entries"].insert(0, entry_record)
        self.save_index(index_data)

        return {
            "status": "stored",
            "memory_id": memory_id,
            "project": project,
            "title": title,
            "file_path": str(file_path),
            "relative_path": rel_path,
            "tags": tag_list
        }

    def search_memories(
        self,
        query: str,
        project: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Searches indexed memories by keyword matching and scoring."""
        index_data = self.load_index()
        entries = index_data.get("entries", [])
        if not entries:
            return []

        query_tokens = [tok.lower() for tok in re.split(r"[\\s,._-]+", query) if tok]
        project_filter = project.lower() if project else None
        tag_filter = tag.lower() if tag else None

        results = []
        for e in entries:
            if project_filter and project_filter not in e.get("project_slug", "") and project_filter not in e.get("project", "").lower():
                continue
            if tag_filter and tag_filter not in [t.lower() for t in e.get("tags", [])]:
                continue

            score = 0
            searchable_text = (
                f"{e.get('title', '')} {e.get('project', '')} "
                f"{e.get('what_summary', '')} {e.get('why_summary', '')} "
                f"{' '.join(e.get('tags', []))}"
            ).lower()

            for tok in query_tokens:
                if tok in e.get("title", "").lower():
                    score += 5
                if any(tok == t.lower() for t in e.get("tags", [])):
                    score += 4
                if tok in e.get("what_summary", "").lower():
                    score += 2
                if tok in e.get("why_summary", "").lower():
                    score += 2
                if tok in searchable_text:
                    score += 1

            if score > 0 or not query_tokens:
                results.append((score, e))

        results.sort(key=lambda x: (x[0], x[1].get("timestamp", "")), reverse=True)
        return [item[1] for item in results[:limit]]

    def list_memories(self, project: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Lists stored memories chronologically."""
        index_data = self.load_index()
        entries = index_data.get("entries", [])
        if project:
            proj_low = project.lower()
            entries = [e for e in entries if proj_low in e.get("project", "").lower() or proj_low in e.get("project_slug", "")]
        return entries[:limit]

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a memory entry and its full markdown content."""
        index_data = self.load_index()
        for e in index_data.get("entries", []):
            if e.get("id") == memory_id:
                rel_path = e.get("relative_path")
                full_path = self.vault_dir / rel_path
                content = full_path.read_text(encoding="utf-8") if full_path.exists() else ""
                result = dict(e)
                result["content"] = content
                result["full_path"] = str(full_path)
                return result
        return None


def main():
    parser = argparse.ArgumentParser(description="memory_vault.py - Persistent memory engine for AI Agent Army.")
    parser.add_argument("--vault", help="Custom memory vault directory path")
    subparsers = parser.add_subparsers(dest="subcommand", help="Vault action")

    # init
    init_p = subparsers.add_parser("init", help="Initialize memory vault")
    init_p.add_argument("--user", help="Default username")

    # store
    store_p = subparsers.add_parser("store", help="Store a new memory snapshot")
    store_p.add_argument("--project", required=True, help="Project name or slug")
    store_p.add_argument("--title", required=True, help="Short descriptive title of the task")
    store_p.add_argument("--what", required=True, help="What was done / problem and solution")
    store_p.add_argument("--why", required=True, help="Why this approach was chosen (decision rationale)")
    store_p.add_argument("--where", help="Key files created or modified")
    store_p.add_argument("--learnings", help="Gotchas, trade-offs, or lessons learned")
    store_p.add_argument("--tags", help="Comma-separated tags (e.g. 'sqlite,auth,api')")
    store_p.add_argument("--workflow", help="Cognitive workflow ID (e.g. CAN-WFL-01)")
    store_p.add_argument("--author", help="Author or agent name")

    # search
    search_p = subparsers.add_parser("search", help="Search memory vault")
    search_p.add_argument("query", help="Keywords or question to search")
    search_p.add_argument("--project", help="Filter by project")
    search_p.add_argument("--tag", help="Filter by tag")
    search_p.add_argument("--limit", type=int, default=10, help="Max results")
    search_p.add_argument("--json", action="store_true", help="Output JSON")

    # list
    list_p = subparsers.add_parser("list", help="List all stored memories")
    list_p.add_argument("--project", help="Filter by project")
    list_p.add_argument("--limit", type=int, default=25, help="Max results")
    list_p.add_argument("--json", action="store_true", help="Output JSON")

    # get
    get_p = subparsers.add_parser("get", help="Retrieve full memory card")
    get_p.add_argument("memory_id", help="Memory entry ID")
    get_p.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()
    vault_dir = resolve_vault_path(args.vault)
    vault = MemoryVault(vault_dir)

    if args.subcommand == "init":
        res = vault.init_vault(args.user)
        print(json.dumps(res, indent=2))
    elif args.subcommand == "store":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        res = vault.store_memory(
            project=args.project,
            title=args.title,
            what=args.what,
            why=args.why,
            where_files=args.where,
            learnings=args.learnings,
            tags=tags,
            workflow=args.workflow,
            author=args.author
        )
        print(json.dumps(res, indent=2))
    elif args.subcommand == "search":
        res = vault.search_memories(args.query, project=args.project, tag=args.tag, limit=args.limit)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Found {len(res)} memories matching '{args.query}':\\n")
            for r in res:
                tags = ", ".join(r.get("tags", []))
                print(f"[{r.get('id')}] ({r.get('date')}) {r.get('project')}: {r.get('title')}")
                print(f"  What: {r.get('what_summary')}")
                print(f"  Why:  {r.get('why_summary')}")
                if tags:
                    print(f"  Tags: {tags}")
                print(f"  File: {r.get('relative_path')}\\n")
    elif args.subcommand == "list":
        res = vault.list_memories(project=args.project, limit=args.limit)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Total memories: {len(res)}\\n")
            for r in res:
                print(f"[{r.get('id')}] ({r.get('date')}) {r.get('project')}: {r.get('title')}")
                print(f"  File: {r.get('relative_path')}")
    elif args.subcommand == "get":
        res = vault.get_memory(args.memory_id)
        if not res:
            print(f"Error: Memory ID '{args.memory_id}' not found.", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(res.get("content", ""))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
