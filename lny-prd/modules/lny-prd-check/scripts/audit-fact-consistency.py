#!/usr/bin/env python3
"""Audit duplicated identity facts across LNY-PRD project documents."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


ID_RE = re.compile(r"(?:PAGE-[A-Z]+-\d{3}|API-[A-Z]+-\d{3}|EXT-\d{3}|FEATURE-\d{3})")


def cells(line: str) -> list[str]:
    return [value.strip() for value in line.strip().strip("|").split("|")]


def is_separator(values: list[str]) -> bool:
    return bool(values) and all(re.fullmatch(r":?-{3,}:?", value.replace(" ", "")) for value in values)


def tables(text: str) -> list[list[dict[str, str]]]:
    lines = text.splitlines()
    result: list[list[dict[str, str]]] = []
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith("|"):
            index += 1
            continue
        block: list[str] = []
        while index < len(lines) and lines[index].lstrip().startswith("|"):
            block.append(lines[index])
            index += 1
        if len(block) < 2:
            continue
        headers = cells(block[0])
        separator = cells(block[1])
        if len(headers) != len(separator) or not is_separator(separator):
            continue
        rows: list[dict[str, str]] = []
        for line in block[2:]:
            values = cells(line)
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
        result.append(rows)
    return result


def first_table(text: str, required: set[str]) -> list[dict[str, str]]:
    for table in tables(text):
        if table and required <= set(table[0]):
            return table
    return []


def facts(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for table in tables(text):
        for row in table:
            if len(row) != 2:
                continue
            key_column = "属性" if "属性" in row else "项目" if "项目" in row else None
            if key_column is None or "内容" not in row:
                continue
            result.setdefault(row[key_column].strip(), row["内容"].strip().strip("`"))
    return result


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`"))


def compare(errors: list[str], source: Path, target: Path, field: str, source_value: str, target_value: str) -> None:
    if normalize(source_value) != normalize(target_value):
        errors.append(
            f"FACT_DRIFT: {source.as_posix()} {field}={source_value!r}; "
            f"{target.as_posix()} {field}={target_value!r}"
        )


def audit(root: Path) -> list[str]:
    errors: list[str] = []
    ui_path = root / "ui_manifest.md"
    api_path = root / "api_spec.md"
    feature_path = root / "feature_spec.md"
    if not all(path.is_file() for path in (ui_path, api_path, feature_path)):
        return [f"FACT_SOURCE_MISSING: {path.as_posix()}" for path in (ui_path, api_path, feature_path) if not path.is_file()]

    ui_text = ui_path.read_text(encoding="utf-8")
    page_rows: dict[str, tuple[Path, dict[str, str]]] = {}
    for table in tables(ui_text):
        if not table or not {"页面编号", "页面名称", "所属终端", "明细路径"} <= set(table[0]):
            continue
        for row in table:
            page_id = row.get("页面编号", "").strip()
            detail = (root / row.get("明细路径", "")).resolve()
            if page_id and detail.is_file():
                page_rows[page_id] = (detail, row)
    for page_id, (detail_path, row) in sorted(page_rows.items()):
        detail = facts(detail_path.read_text(encoding="utf-8"))
        for field in ("页面编号", "页面名称", "所属终端"):
            if field in detail:
                compare(errors, ui_path, detail_path, field, row[field], detail[field])
        terminal_match = re.fullmatch(r"PAGE-([A-Z]+)-\d{3}", page_id)
        terminal = terminal_match.group(1) if terminal_match else ""
        page_prd = root / "pages_prd" / terminal / f"{page_id}.md"
        if page_prd.is_file():
            page_facts = facts(page_prd.read_text(encoding="utf-8"))
            for field in ("页面编号", "页面名称", "所属终端"):
                if field in page_facts:
                    compare(errors, ui_path, page_prd, field, row[field], page_facts[field])

    for source_path, id_field, name_field, directory in (
        (api_path, "接口编号", "接口名称", "api"),
        (feature_path, "功能编号", "功能名称", "feature"),
    ):
        source_text = source_path.read_text(encoding="utf-8")
        for table in tables(source_text):
            if not table or not {id_field, name_field, "明细路径"} <= set(table[0]):
                continue
            for row in table:
                item_id = row.get(id_field, "").strip()
                detail_path = (root / row.get("明细路径", "")).resolve()
                if not item_id or not detail_path.is_file():
                    continue
                detail = facts(detail_path.read_text(encoding="utf-8"))
                for field in (id_field, name_field):
                    if field in detail:
                        compare(errors, source_path, detail_path, field, row[field], detail[field])
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prd_root", type=Path)
    args = parser.parse_args()
    root = args.prd_root.expanduser().resolve()
    errors = audit(root)
    if errors:
        print("fact consistency audit failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("fact consistency audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
