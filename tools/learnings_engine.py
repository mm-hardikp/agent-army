#!/usr/bin/env python3
r"""
learnings_engine.py - SQLite-powered self-learning memory engine for AI Agent Army.
Learns from user corrections, preferences, and instructions on this machine.
Default location: C:\Agent-Memory\learnings.db

Usage:
    python learnings_engine.py init [--db PATH]
    python learnings_engine.py add --instruction TEXT [--category CAT] [--context CTX] [--reason TEXT]
    python learnings_engine.py recall [QUERY] [--context CTX] [--limit N] [--json]
    python learnings_engine.py list [--all] [--json]
    python learnings_engine.py prompt [QUERY]
    python learnings_engine.py delete RULE_ID
"""

import os
import sys
import sqlite3
import json
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

DEFAULT_DB_WIN = Path("C:/Agent-Memory/learnings.db")
DEFAULT_DB_FALLBACK = Path.home() / ".agent-memory" / "learnings.db"


def resolve_db_path(custom_path: Optional[str] = None) -> Path:
    """Resolves the active SQLite learnings database path."""
    if custom_path:
        p = Path(custom_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    env_path = os.environ.get("AGENT_LEARNINGS_DB")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    if os.name == "nt":
        try:
            DEFAULT_DB_WIN.parent.mkdir(parents=True, exist_ok=True)
            return DEFAULT_DB_WIN
        except (PermissionError, OSError):
            DEFAULT_DB_FALLBACK.parent.mkdir(parents=True, exist_ok=True)
            return DEFAULT_DB_FALLBACK
    DEFAULT_DB_FALLBACK.parent.mkdir(parents=True, exist_ok=True)
    return DEFAULT_DB_FALLBACK


class LearningsEngine:
    """SQLite database manager for personal user learnings, habits, and corrections."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_db()

    from contextlib import contextmanager

    @contextmanager
    def get_connection(self):
        """Yields SQLite connection and closes it cleanly on exit."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """Initializes database schema and tables."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learned_rules (
                    rule_id TEXT PRIMARY KEY,
                    category TEXT NOT NULL,          -- 'preference', 'correction', 'style', 'environment', 'general'
                    trigger_context TEXT NOT NULL,   -- e.g. 'shell commands', 'python', 'formatting', 'general'
                    instruction TEXT NOT NULL UNIQUE,-- The learned rule to follow
                    reason TEXT,                     -- Why this rule was established
                    source TEXT DEFAULT 'user',      -- 'user_explicit' or 'user_correction'
                    times_applied INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    active INTEGER DEFAULT 1         -- 1 = active, 0 = disabled
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_context ON learned_rules(trigger_context, active);
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_rules_category ON learned_rules(category, active);
            """)
            conn.commit()

    def add_rule(
        self,
        instruction: str,
        category: str = "general",
        trigger_context: str = "general",
        reason: Optional[str] = None,
        source: str = "user_explicit"
    ) -> Dict[str, Any]:
        """Adds or updates a learned rule."""
        inst = instruction.strip()
        if not inst:
            raise ValueError("Instruction cannot be empty")

        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        # Deterministic ID based on instruction
        rule_hash = hashlib.sha256(inst.lower().encode("utf-8")).hexdigest()[:8].upper()
        rule_id = f"LRN-{category[:3].upper()}-{rule_hash}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO learned_rules 
                (rule_id, category, trigger_context, instruction, reason, source, times_applied, created_at, updated_at, active)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, 1)
                ON CONFLICT(instruction) DO UPDATE SET
                    category = excluded.category,
                    trigger_context = excluded.trigger_context,
                    reason = COALESCE(excluded.reason, learned_rules.reason),
                    source = excluded.source,
                    updated_at = excluded.updated_at,
                    active = 1
            """, (rule_id, category.lower(), trigger_context.lower(), inst, reason, source, now_iso, now_iso))
            conn.commit()

        return {
            "status": "saved",
            "rule_id": rule_id,
            "category": category,
            "trigger_context": trigger_context,
            "instruction": inst,
            "reason": reason or ""
        }

    def recall_rules(self, query: Optional[str] = None, context: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Recalls active rules matching query tokens or context."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if not query and not context:
                cursor.execute("""
                    SELECT * FROM learned_rules 
                    WHERE active = 1 
                    ORDER BY times_applied DESC, updated_at DESC 
                    LIMIT ?
                """, (limit,))
            else:
                tokens = [t.lower() for t in (query or "").split() if len(t) > 2]
                where_clauses = ["active = 1"]
                params: List[Any] = []

                if context:
                    where_clauses.append("(trigger_context LIKE ? OR category LIKE ?)")
                    params.extend([f"%{context.lower()}%", f"%{context.lower()}%"])

                if tokens:
                    token_conditions = []
                    for tok in tokens:
                        token_conditions.append("(instruction LIKE ? OR trigger_context LIKE ? OR reason LIKE ?)")
                        params.extend([f"%{tok}%", f"%{tok}%", f"%{tok}%"])
                    where_clauses.append(f"({' OR '.join(token_conditions)})")

                where_sql = " AND ".join(where_clauses)
                sql = f"SELECT * FROM learned_rules WHERE {where_sql} ORDER BY times_applied DESC, updated_at DESC LIMIT ?"
                params.append(limit)
                cursor.execute(sql, params)

            rows = cursor.fetchall()
            results = [dict(r) for r in rows]

            # Increment usage counter
            if results:
                ids = [r["rule_id"] for r in results]
                placeholders = ",".join(["?"] * len(ids))
                now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                cursor.execute(f"""
                    UPDATE learned_rules 
                    SET times_applied = times_applied + 1, updated_at = ?
                    WHERE rule_id IN ({placeholders})
                """, [now_iso] + ids)
                conn.commit()
                for r in results:
                    r["times_applied"] = r.get("times_applied", 0) + 1

            return results

    def list_rules(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Lists all learned rules."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if active_only:
                cursor.execute("SELECT * FROM learned_rules WHERE active = 1 ORDER BY updated_at DESC")
            else:
                cursor.execute("SELECT * FROM learned_rules ORDER BY updated_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    def delete_rule(self, rule_id: str) -> bool:
        """Deactivates a rule by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE learned_rules SET active = 0 WHERE rule_id = ?", (rule_id,))
            conn.commit()
            return cursor.rowcount > 0

    def format_prompt_context(self, query: Optional[str] = None, context: Optional[str] = None) -> str:
        """Generates a high-impact prompt injection containing learned user rules."""
        rules = self.recall_rules(query=query, context=context, limit=8)
        if not rules:
            return ""

        lines = [
            "<!-- USER-LEARNED INSTRUCTION SET -->",
            "[USER PREFERENCES & LEARNED RULES]",
            "The following rules were learned directly from user interactions on this machine and must be strictly followed:"
        ]
        for r in rules:
            cat = r.get("category", "general").capitalize()
            inst = r.get("instruction", "")
            reason = f" (Reason: {r['reason']})" if r.get("reason") else ""
            lines.append(f"- [{cat}]: {inst}{reason}")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="learnings_engine.py - Self-learning memory for AI Agent Army.")
    parser.add_argument("--db", help="Custom SQLite database path")
    subparsers = parser.add_subparsers(dest="subcommand", help="Learnings action")

    # init
    subparsers.add_parser("init", help="Initialize database")

    # add
    add_p = subparsers.add_parser("add", help="Add or update a learned rule")
    add_p.add_argument("--instruction", required=True, help="Exact learned rule/instruction")
    add_p.add_argument("--category", default="general", help="Category: preference, style, correction, environment, general")
    add_p.add_argument("--context", default="general", help="Trigger context domain (e.g. 'shell commands', 'python')")
    add_p.add_argument("--reason", help="Why this rule was established")
    add_p.add_argument("--source", default="user_explicit", help="Source: user_explicit or user_correction")

    # recall
    rec_p = subparsers.add_parser("recall", help="Recall matching rules for a task")
    rec_p.add_argument("query", nargs="?", default="", help="Task keywords to match")
    rec_p.add_argument("--context", help="Filter by context domain")
    rec_p.add_argument("--limit", type=int, default=10, help="Max rules")
    rec_p.add_argument("--json", action="store_true", help="Output JSON")

    # list
    list_p = subparsers.add_parser("list", help="List all rules")
    list_p.add_argument("--all", action="store_true", help="Include inactive rules")
    list_p.add_argument("--json", action="store_true", help="Output JSON")

    # prompt
    prompt_p = subparsers.add_parser("prompt", help="Format prompt injection string")
    prompt_p.add_argument("query", nargs="?", default="", help="Task keywords to match")
    prompt_p.add_argument("--context", help="Filter by context domain")

    # delete
    del_p = subparsers.add_parser("delete", help="Deactivate a rule by ID")
    del_p.add_argument("rule_id", help="Rule ID (e.g. LRN-PRE-12345678)")

    args = parser.parse_args()
    db_path = resolve_db_path(args.db)
    engine = LearningsEngine(db_path)

    if args.subcommand == "init":
        print(f"Learnings database initialized at: {db_path}")
    elif args.subcommand == "add":
        res = engine.add_rule(
            instruction=args.instruction,
            category=args.category,
            trigger_context=args.context,
            reason=args.reason,
            source=args.source
        )
        print(json.dumps(res, indent=2))
    elif args.subcommand == "recall":
        res = engine.recall_rules(query=args.query, context=args.context, limit=args.limit)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Recalled {len(res)} matching learned rules:\n")
            for r in res:
                print(f"[{r['rule_id']}] ({r['category'].upper()} | {r['trigger_context']})")
                print(f"  Rule:   {r['instruction']}")
                if r.get("reason"):
                    print(f"  Reason: {r['reason']}")
                print(f"  Used:   {r['times_applied']} times\n")
    elif args.subcommand == "list":
        res = engine.list_rules(active_only=not args.all)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Total active learned rules: {len(res)}\n")
            for r in res:
                print(f"[{r['rule_id']}] ({r['category'].upper()} | {r['trigger_context']})")
                print(f"  Rule: {r['instruction']}\n")
    elif args.subcommand == "prompt":
        output = engine.format_prompt_context(query=args.query, context=args.context)
        print(output if output else "No learned rules applicable.")
    elif args.subcommand == "delete":
        ok = engine.delete_rule(args.rule_id)
        if ok:
            print(f"Rule '{args.rule_id}' deactivated.")
        else:
            print(f"Rule '{args.rule_id}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
