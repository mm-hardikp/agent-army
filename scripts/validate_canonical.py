#!/usr/bin/env python3
"""validate_canonical.py - Lean validator for canonical frontmatter and envelopes."""
import os, sys, json, re
from pathlib import Path
from typing import Dict, Any, List

def strip_comment(line: str) -> str:
    in_q, qc = False, ''
    for i, ch in enumerate(line):
        if ch in ('"', "'"):
            if not in_q: in_q, qc = True, ch
            elif ch == qc: in_q = False
        elif ch == '#' and not in_q: return line[:i].rstrip()
    return line.rstrip()

def parse_val(v: str):
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")): return v[1:-1]
    return int(v) if v.isdigit() else (True if v.lower() == 'true' else (False if v.lower() == 'false' else v))

def parse_frontmatter(content: str) -> Dict[str, Any]:
    match = re.match(r'^---\s*\n(.*?)\n---\s*(\n|$)', content, re.DOTALL)
    if not match: raise ValueError("Missing or malformed '---' frontmatter delimiters.")
    cleaned = [(len(l) - len(l.lstrip()), l.strip()) for raw in match.group(1).splitlines() if (l := strip_comment(raw)).strip()]

    def parse_block(idx: int, base_indent: int):
        if idx >= len(cleaned): return {}, idx
        if cleaned[idx][1].startswith("- "):
            res = []
            while idx < len(cleaned) and cleaned[idx][0] == base_indent and cleaned[idx][1].startswith("- "):
                res.append(parse_val(cleaned[idx][1][2:].strip()))
                idx += 1
            return res, idx
        res = {}
        while idx < len(cleaned) and cleaned[idx][0] == base_indent:
            line = cleaned[idx][1]
            if ":" not in line: idx += 1; continue
            k, _, v = line.partition(":"); k, v = k.strip(), v.strip(); idx += 1
            if not v or v in (">", "|"):
                if idx < len(cleaned) and cleaned[idx][0] > base_indent:
                    c_ind = cleaned[idx][0]
                    if cleaned[idx][1].startswith("- ") or ":" in cleaned[idx][1]:
                        res[k], idx = parse_block(idx, c_ind)
                    else:
                        txt = []
                        while idx < len(cleaned) and cleaned[idx][0] >= c_ind and not cleaned[idx][1].startswith("- ") and ":" not in cleaned[idx][1]:
                            txt.append(cleaned[idx][1]); idx += 1
                        res[k] = " ".join(txt)
                else: res[k] = "" if v in (">", "|") else {}
            else: res[k] = parse_val(v)
        return res, idx
    return parse_block(0, 0)[0]

def validate_dict_against_schema(data: Dict[str, Any], schema: Dict[str, Any], ctx: str) -> List[str]:
    errors = [f"[{ctx}] Missing required field: '{r}'" for r in schema.get("required", []) if r not in data]
    props = schema.get("properties", {})
    type_map = {"string": str, "integer": int, "array": list, "object": dict, "boolean": bool}
    for k, v in data.items():
        if k not in props: continue
        rule = props[k]; exp = rule.get("type")
        if exp in type_map and not isinstance(v, type_map[exp]):
            errors.append(f"[{ctx}] Field '{k}' must be {exp}, got {type(v).__name__}")
        if "enum" in rule and v not in rule["enum"]:
            errors.append(f"[{ctx}] Field '{k}' invalid value '{v}'. Expected: {rule['enum']}")
        if "pattern" in rule and isinstance(v, str) and not re.match(rule["pattern"], v):
            errors.append(f"[{ctx}] Field '{k}' value '{v}' does not match pattern '{rule['pattern']}'")
        if exp == "object" and isinstance(v, dict) and "required" in rule:
            errors.extend([f"[{ctx}] Subfield '{k}.{sr}' is required" for sr in rule["required"] if sr not in v])
    return errors

def validate_file(file_path: Path, schema: Dict[str, Any]) -> List[str]:
    try:
        content = file_path.read_text(encoding="utf-8")
        data = json.loads(content) if file_path.suffix.lower() == ".json" else parse_frontmatter(content)
        return validate_dict_against_schema(data, schema, file_path.name)
    except Exception as e:
        return [f"[{file_path.name}] Parse error: {e}"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_canonical.py <schema_path> <file_to_validate>"); sys.exit(1)
    schema = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errs = validate_file(Path(sys.argv[2]), schema)
    if errs:
        for err in errs: print(f"ERROR: {err}")
        sys.exit(1)
    print(f"PASS: {Path(sys.argv[2]).name} conforms to {Path(sys.argv[1]).name}")
