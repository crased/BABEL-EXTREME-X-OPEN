"""
Pre-flight check for Babel-Extreme apprentice submissions.

Usage:
    python tools/eval_runner.py outputs/

Walks the given directory looking for any *.json file, validates each against
contracts/schema.json, and prints population statistics. Exits non-zero if
validation fails on any file.

Run this before submitting. If it fails, your submission will score 0 on
schema validity per RUBRIC.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(
        "jsonschema is required. Install it:\n"
        "    pip install jsonschema\n"
        "(Or include it in your requirements.txt.)",
        file=sys.stderr,
    )
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "contracts" / "schema.json"

TEXT_BEARING = {
    "text_block", "heading", "caption", "formula",
    "header", "footer", "list_item",
}


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_outputs(target: Path) -> list[Path]:
    if target.is_file() and target.suffix == ".json":
        return [target]
    if target.is_dir():
        return sorted(target.rglob("*.json"))
    return []


def validate_one(path: Path, validator: Draft202012Validator) -> tuple[bool, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, [f"invalid JSON: {e}"]
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    return (not errors), [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors]


def stats(data: dict[str, Any]) -> dict[str, Any]:
    pages = data.get("pages", [])
    out = {
        "page_count": len(pages),
        "elements_total": 0,
        "text_bearing_total": 0,
        "text_bearing_with_content": 0,
        "tables_total": 0,
        "tables_with_cells": 0,
        "figures_total": 0,
        "figures_with_path": 0,
        "needs_review_count": 0,
        "bbox_invalid_count": 0,
        "reading_order_misses": 0,
    }
    for page in pages:
        elements = page.get("elements", [])
        ids = {e.get("id") for e in elements}
        for el in elements:
            out["elements_total"] += 1
            if el.get("needs_review"):
                out["needs_review_count"] += 1
            t = el.get("type")
            bb = el.get("bbox") or {}
            if not (
                bb.get("x2", 0) > bb.get("x1", 0)
                and bb.get("y2", 0) > bb.get("y1", 0)
                and 0 <= bb.get("x1", 0) <= page.get("width", 0)
                and 0 <= bb.get("y1", 0) <= page.get("height", 0)
                and bb.get("x2", 0) <= page.get("width", 0)
                and bb.get("y2", 0) <= page.get("height", 0)
            ):
                out["bbox_invalid_count"] += 1
            if t in TEXT_BEARING:
                out["text_bearing_total"] += 1
                if (el.get("content") or "").strip():
                    out["text_bearing_with_content"] += 1
            if t == "table":
                out["tables_total"] += 1
                if (el.get("table") or {}).get("cells"):
                    out["tables_with_cells"] += 1
            if t == "figure":
                out["figures_total"] += 1
                if el.get("figure_path"):
                    out["figures_with_path"] += 1
        for rid in page.get("reading_order", []):
            if rid not in ids:
                out["reading_order_misses"] += 1
    return out


def fmt_pct(num: int, denom: int) -> str:
    if denom == 0:
        return "n/a"
    return f"{100.0 * num / denom:.0f}%"


def report(path: Path, ok: bool, errors: list[str], data: dict[str, Any] | None) -> bool:
    print(f"\n=== {path} ===")
    print(f"  schema:       {'OK' if ok else 'FAIL'}")
    if errors:
        for e in errors[:10]:
            print(f"    - {e}")
        if len(errors) > 10:
            print(f"    - ... and {len(errors) - 10} more")
    if not data:
        return ok

    s = stats(data)
    text_pct = fmt_pct(s["text_bearing_with_content"], s["text_bearing_total"])
    print(f"  pages:        {s['page_count']}")
    print(f"  elements:     {s['elements_total']}")
    print(
        "  text-bearing: "
        f"{s['text_bearing_with_content']}/{s['text_bearing_total']} populated ({text_pct})"
    )
    print(f"  tables:       {s['tables_with_cells']}/{s['tables_total']} with cells")
    print(f"  figures:      {s['figures_with_path']}/{s['figures_total']} with path")
    print(f"  needs_review: {s['needs_review_count']}")
    print(f"  bbox issues:  {s['bbox_invalid_count']}")
    print(f"  read-order misses: {s['reading_order_misses']}")

    floor_pct = (
        100.0 * s["text_bearing_with_content"] / s["text_bearing_total"]
        if s["text_bearing_total"]
        else 0.0
    )
    if s["text_bearing_total"] >= 5 and floor_pct < 60.0:
        print(f"  -> WARN: 60% floor on populated text-bearing elements; you are at {floor_pct:.0f}%.")
    return ok


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/eval_runner.py <output-file-or-dir>", file=sys.stderr)
        return 2

    target = Path(argv[1]).resolve()
    if not target.exists():
        print(f"path does not exist: {target}", file=sys.stderr)
        return 2

    schema = load_schema()
    validator = Draft202012Validator(schema)
    paths = find_outputs(target)
    if not paths:
        print(f"no .json files found at {target}", file=sys.stderr)
        return 2

    all_ok = True
    for p in paths:
        ok, errors = validate_one(p, validator)
        data = None
        if ok:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                data = None
        report(p, ok, errors, data)
        all_ok = all_ok and ok

    print("\n" + ("ALL OK" if all_ok else "FAILED — fix the above before submitting."))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
