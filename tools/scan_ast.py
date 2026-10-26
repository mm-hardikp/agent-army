#!/usr/bin/env python3
"""
scan_ast.py - Token-efficient AST symbol extractor and codebase discovery tool.
Origin: Derived from github/awesome-copilot (SKL-005 scan.py).
Zero external runtime dependencies (uses standard library ast, os, json, re, pathlib).

Usage:
    python scan_ast.py [PATH] [--json] [--max-depth DEPTH]
"""

import os
import sys
import ast
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt",
    "__pycache__", ".venv", "venv", ".tox", "target", "vendor",
    "coverage", ".cache", "bin", "obj", ".idea", ".vscode"
}

MANIFEST_FILES = {
    "package.json": "JavaScript/TypeScript (Node)",
    "requirements.txt": "Python (Pip)",
    "pyproject.toml": "Python (PEP 518/Poetry/Uv)",
    "Pipfile": "Python (Pipenv)",
    "go.mod": "Go Module",
    "Cargo.toml": "Rust (Cargo)",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java/Kotlin (Gradle)",
    "composer.json": "PHP (Composer)",
    "Gemfile": "Ruby (Bundler)"
}


class SymbolExtractor:
    @staticmethod
    def extract_python_symbols(file_path: Path) -> List[Dict[str, Any]]:
        symbols = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    symbols.append({
                        "kind": "function",
                        "name": node.name,
                        "line": node.lineno,
                        "args": args
                    })
                elif isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            methods.append(item.name)
                    symbols.append({
                        "kind": "class",
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods
                    })
        except Exception as e:
            symbols.append({"kind": "parse_error", "error": str(e)})
        return symbols

    @staticmethod
    def extract_js_ts_symbols(file_path: Path) -> List[Dict[str, Any]]:
        symbols = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            # Regex fallback extraction for JS/TS without requiring external node dependencies
            func_pattern = re.compile(r'^\s*(?:export\s+)?(?:async\s+)?function\s+([a-zA-Z0-9_$]+)\s*\(([^)]*)\)', re.MULTILINE)
            class_pattern = re.compile(r'^\s*(?:export\s+)?class\s+([a-zA-Z0-9_$]+)', re.MULTILINE)
            arrow_pattern = re.compile(r'^\s*(?:export\s+)?(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', re.MULTILINE)

            for match in func_pattern.finditer(content):
                line = content[:match.start()].count('\n') + 1
                symbols.append({"kind": "function", "name": match.group(1), "line": line})

            for match in class_pattern.finditer(content):
                line = content[:match.start()].count('\n') + 1
                symbols.append({"kind": "class", "name": match.group(1), "line": line})

            for match in arrow_pattern.finditer(content):
                line = content[:match.start()].count('\n') + 1
                symbols.append({"kind": "arrow_function", "name": match.group(1), "line": line})
        except Exception as e:
            symbols.append({"kind": "parse_error", "error": str(e)})
        return symbols


def scan_directory(root_path: Path, max_depth: int = 3) -> Dict[str, Any]:
    root_path = root_path.resolve()
    manifests_found = []
    symbol_index = {}
    file_count = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # In-place directory exclusion
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        rel_depth = len(Path(dirpath).relative_to(root_path).parts)
        if rel_depth > max_depth:
            continue

        for fname in filenames:
            file_count += 1
            fpath = Path(dirpath) / fname
            rel_path = str(fpath.relative_to(root_path))

            # Check manifests
            if fname in MANIFEST_FILES:
                manifests_found.append({
                    "file": rel_path,
                    "ecosystem": MANIFEST_FILES[fname]
                })

            # Check symbols for code files
            if fname.endswith(".py"):
                syms = SymbolExtractor.extract_python_symbols(fpath)
                if syms:
                    symbol_index[rel_path] = syms
            elif fname.endswith((".js", ".jsx", ".ts", ".tsx")):
                syms = SymbolExtractor.extract_js_ts_symbols(fpath)
                if syms:
                    symbol_index[rel_path] = syms

    return {
        "root": str(root_path),
        "total_files_scanned": file_count,
        "manifests": manifests_found,
        "symbol_index": symbol_index
    }


def main():
    parser = argparse.ArgumentParser(description="Extract AST symbols and manifest summary.")
    parser.add_argument("path", nargs="?", default=".", help="Root path to scan")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--max-depth", type=int, default=3, help="Max directory depth")
    args = parser.parse_args()

    results = scan_directory(Path(args.path), max_depth=args.max_depth)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"=== Codebase Discovery: {results['root']} ===")
        print(f"Total files scanned: {results['total_files_scanned']}")
        print("\n--- Manifests & Ecosystems ---")
        for m in results["manifests"]:
            print(f"  [{m['ecosystem']}] {m['file']}")
        print("\n--- Symbol Summary ---")
        for f, syms in list(results["symbol_index"].items())[:25]:
            print(f"  {f} ({len(syms)} symbols)")
            for s in syms[:5]:
                print(f"    - {s['kind']}: {s['name']} (line {s.get('line')})")


if __name__ == "__main__":
    main()
