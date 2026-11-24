#!/usr/bin/env python3
"""Audit a PRD decision contract against referenced project artifacts."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


ID_PATTERNS = (
    re.compile(r"PAGE-[A-Z]+-\d{3}"),
    re.compile(r"API-[A-Z]+-\d{3}"),
    re.compile(r"EXT-\d{3}"),
    re.compile(r"FEATURE-\d{3}"),
)
REQUIRED_FIELDS = ("状态", "产品目标", "本次范围", "明确不做", "成功标准")


def find_contract(root: Path, explicit: str | None) -> Path | None:
    if explicit:
        path = (root / explicit).resolve()
        return path if path.is_file() else None
    for relative in ("decision_contract.md", "product_workspace.md"):
        path = root / relative
        if path.is_file():
            return path
    return None


def field_value(text: str, field: str) -> str:
    match = re.search(rf"^\s*(?:[-*]\s*)?{re.escape(field)}\s*[:：]\s*(.+?)\s*$", text, re.M)
    return match.group(1).strip() if match else ""


def referenced_ids(text: str) -> set[str]:
    found: set[str] = set()
    for pattern in ID_PATTERNS:
        found.update(pattern.findall(text))
    return found


def existing_ids(root: Path, excluded: Path) -> set[str]:
    found: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html"}:
            continue
        if path.resolve() == excluded.resolve():
            continue
        if any(part in {".git", "node_modules", ".visual-review"} for part in path.parts):
            continue
        found.update(referenced_ids(path.read_text(encoding="utf-8", errors="replace")))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prd_root", type=Path)
    parser.add_argument("--decision-file", default=None)
    args = parser.parse_args()
    root = args.prd_root.expanduser().resolve()
    contract = find_contract(root, args.decision_file)
    if contract is None:
        print("DECISION_WALKTHROUGH: skipped (no decision_contract.md or product_workspace.md)")
        return 2

    text = contract.read_text(encoding="utf-8")
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        value = field_value(text, field)
        if not value or value in {"-", "待填写", "TODO", "{...}"}:
            errors.append(f"{contract.name}: missing decision field {field}")

    status = field_value(text, "状态")
    if status and status not in {"暂定", "已确认", "provisional", "approved"}:
        errors.append(f"{contract.name}: 状态 must be 暂定/已确认")

    ids = referenced_ids(text)
    available = existing_ids(root, contract)
    for item_id in sorted(ids - available):
        errors.append(f"{contract.name}: decision references missing artifact {item_id}")

    if errors:
        print("DECISION_WALKTHROUGH: failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"DECISION_WALKTHROUGH: passed ({contract.relative_to(root).as_posix()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
