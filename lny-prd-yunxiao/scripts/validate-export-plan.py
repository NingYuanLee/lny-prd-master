#!/usr/bin/env python3
"""Validate the structure and hierarchy of an LNY-PRD Yunxiao export plan."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MODULE_RE = re.compile(r"MODULE-\d{3}")
FEATURE_RE = re.compile(r"FEATURE-\d{3}")
TASK_RE = re.compile(r"FEATURE-\d{3}:[A-Z][A-Z0-9_-]{0,31}")
VERSION_RE = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
SOURCE_REF_RE = re.compile(r"(?:PAGE-[A-Z]+-\d{3}|API-[A-Z]+-\d{3}|EXT-\d{3})")
PAGE_REF_RE = re.compile(r"PAGE-[A-Z]+-\d{3}")
API_REF_RE = re.compile(r"API-[A-Z]+-\d{3}")
EXT_REF_RE = re.compile(r"EXT-\d{3}")
AC_RE = re.compile(r"AC-\d+")
FORBIDDEN_KEYS = {"yunxiaoid", "assignee", "status", "workitemid"}
OPERATIONS = {"upsert", "close"}


def validate(plan: Any, *, allow_legacy_empty_test: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["PLAN_ROOT: plan must be an object"]
    if plan.get("schemaVersion") != 1:
        errors.append("SCHEMA_VERSION: schemaVersion must be 1")
    if plan.get("adapter") != "lny-prd-yunxiao":
        errors.append("ADAPTER_ID: adapter must be lny-prd-yunxiao")
    if not isinstance(plan.get("sourceVersion"), str) or not VERSION_RE.fullmatch(plan["sourceVersion"]):
        errors.append("SOURCE_VERSION: sourceVersion must be vX.Y.Z")
    if not isinstance(plan.get("project"), str) or not plan["project"].strip():
        errors.append("PROJECT: project must be a non-empty string")
    items = plan.get("items")
    if not isinstance(items, list) or not items:
        errors.append("ITEMS: items must be a non-empty array")
        return errors
    forbidden_hits: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in FORBIDDEN_KEYS:
                    forbidden_hits.add(key)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(plan)
    if forbidden_hits:
        errors.append("FORBIDDEN_INSTANCE_FIELDS: " + ", ".join(sorted(forbidden_hits)))
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"ITEM_TYPE: items[{index}] must be an object")
            continue
        source_id = item.get("sourceId")
        item_type = item.get("workItemType")
        if not isinstance(source_id, str):
            errors.append(f"SOURCE_ID: items[{index}] has no string sourceId")
            continue
        if source_id in by_id:
            errors.append(f"DUPLICATE_SOURCE_ID: {source_id}")
        by_id[source_id] = item
        expected = {"product": MODULE_RE, "business": FEATURE_RE, "task": TASK_RE}.get(item_type)
        if expected is None or not expected.fullmatch(source_id):
            errors.append(f"SOURCE_SHAPE: {source_id} does not match type {item_type!r}")
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            errors.append(f"TITLE: {source_id} has no title")
        operation = item.get("operation", "upsert")
        if operation not in OPERATIONS:
            errors.append(f"OPERATION: {source_id} operation must be upsert or close")
        if item_type == "product" and operation == "close":
            errors.append(f"PRODUCT_CLOSE_UNSUPPORTED: {source_id} cannot be closed by a Feature delivery plan")
    for source_id, item in by_id.items():
        item_type = item.get("workItemType")
        parent_id = item.get("parentSourceId")
        if item_type == "product":
            if parent_id is not None:
                errors.append(f"PARENT: product {source_id} must have null parent")
            continue
        parent = by_id.get(parent_id)
        expected_parent = "product" if item_type == "business" else "business"
        if parent is None or parent.get("workItemType") != expected_parent:
            errors.append(f"PARENT: {source_id} must reference a {expected_parent} parent")
        elif parent.get("operation", "upsert") == "close" and item.get("operation", "upsert") != "close":
            errors.append(f"PARENT_OPERATION: {source_id} must close because parent {parent_id} closes")
        if item_type == "task":
            surface = item.get("deliverySurface")
            if source_id != f"{parent_id}:{surface}":
                errors.append(f"TASK_SURFACE: {source_id} does not match its parent and surface")
            refs = item.get("sourceRefs")
            dependencies = item.get("dependencyRefs", [])
            bindings = item.get("pageApiBindings", [])
            criteria = item.get("acceptanceCriteria")
            if not isinstance(refs, list) or not isinstance(criteria, list):
                errors.append(f"TASK_CONTENT: {source_id} needs sourceRefs and acceptanceCriteria arrays")
                continue
            if operation == "close":
                if dependencies != []:
                    errors.append(f"CLOSE_TASK_CONTENT: {source_id} dependencyRefs must be empty")
                if bindings != []:
                    errors.append(f"CLOSE_TASK_CONTENT: {source_id} pageApiBindings must be empty")
                if criteria != []:
                    errors.append(f"CLOSE_TASK_CONTENT: {source_id} acceptanceCriteria must be empty")
            if refs != sorted(set(refs)) or not all(isinstance(ref, str) and SOURCE_REF_RE.fullmatch(ref) for ref in refs):
                errors.append(f"SOURCE_REFS: {source_id} refs must be unique, sorted PRD source IDs")
            if not isinstance(dependencies, list) or dependencies != sorted(set(dependencies)) or not all(
                isinstance(ref, str) and (API_REF_RE.fullmatch(ref) or EXT_REF_RE.fullmatch(ref))
                for ref in dependencies
            ):
                errors.append(f"DEPENDENCY_REFS: {source_id} dependencies must be unique, sorted API/EXT IDs")
            if not isinstance(bindings, list):
                errors.append(f"PAGE_API_BINDINGS: {source_id} pageApiBindings must be an array")
                bindings = []
            ref_set = set(refs) if isinstance(refs, list) else set()
            dependency_set = set(dependencies) if isinstance(dependencies, list) else set()
            overlap = sorted(ref_set & dependency_set)
            if overlap:
                errors.append(
                    f"DEPENDENCY_OWNERSHIP_OVERLAP: {source_id} owns and depends on {', '.join(overlap)}"
                )
            binding_keys: list[tuple[str, str, str, str]] = []
            for binding in bindings:
                if not isinstance(binding, dict):
                    errors.append(f"PAGE_API_BINDING_SHAPE: {source_id} bindings must be objects")
                    continue
                page_ref = binding.get("pageRef")
                interface_ref = binding.get("interfaceRef")
                purpose = binding.get("purpose")
                trigger = binding.get("trigger")
                if not isinstance(page_ref, str) or not PAGE_REF_RE.fullmatch(page_ref):
                    errors.append(f"PAGE_API_BINDING_PAGE: {source_id} has an invalid pageRef")
                if not isinstance(interface_ref, str) or not (
                    API_REF_RE.fullmatch(interface_ref) or EXT_REF_RE.fullmatch(interface_ref)
                ):
                    errors.append(f"PAGE_API_BINDING_INTERFACE: {source_id} has an invalid interfaceRef")
                if isinstance(page_ref, str) and PAGE_REF_RE.fullmatch(page_ref) and page_ref not in ref_set:
                    errors.append(
                        f"PAGE_API_BINDING_PAGE_OWNERSHIP: {source_id} binding page {page_ref} is not in sourceRefs"
                    )
                if (
                    isinstance(interface_ref, str)
                    and (API_REF_RE.fullmatch(interface_ref) or EXT_REF_RE.fullmatch(interface_ref))
                    and interface_ref not in ref_set | dependency_set
                ):
                    errors.append(
                        f"PAGE_API_BINDING_INTERFACE_OWNERSHIP: {source_id} binding interface {interface_ref} "
                        "is neither owned nor depended on"
                    )
                for field, value in (("purpose", purpose), ("trigger", trigger)):
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"PAGE_API_BINDING_FIELD: {source_id} binding needs {field}")
                if all(isinstance(value, str) for value in (page_ref, interface_ref, purpose, trigger)):
                    binding_keys.append((page_ref, interface_ref, purpose, trigger))
            if binding_keys != sorted(set(binding_keys)):
                errors.append(f"PAGE_API_BINDING_ORDER: {source_id} bindings must be unique and sorted")
            seen_ac: set[str] = set()
            for criterion in criteria:
                if not isinstance(criterion, dict):
                    errors.append(f"AC_SHAPE: {source_id} acceptance criteria must be objects")
                    continue
                ac_id = criterion.get("id")
                if not isinstance(ac_id, str) or not AC_RE.fullmatch(ac_id):
                    errors.append(f"AC_ID: {source_id} has an invalid acceptance criterion ID")
                elif ac_id in seen_ac:
                    errors.append(f"AC_DUPLICATE: {source_id} repeats {ac_id}")
                else:
                    seen_ac.add(ac_id)
                for field in ("description", "verification"):
                    if not isinstance(criterion.get(field), str) or not criterion[field].strip():
                        errors.append(f"AC_FIELD: {source_id} {ac_id or 'unknown'} needs {field}")
                for field, pattern in (("pageRefs", PAGE_REF_RE), ("apiRefs", API_REF_RE), ("extRefs", EXT_REF_RE)):
                    values = criterion.get(field, [])
                    if not isinstance(values, list) or values != sorted(set(values)) or not all(
                        isinstance(value, str) and pattern.fullmatch(value) for value in values
                    ):
                        errors.append(f"AC_REFS: {source_id} {ac_id or 'unknown'} has invalid {field}")
    for item in items:
        if not isinstance(item, dict) or item.get("workItemType") != "business":
            continue
        if item.get("operation", "upsert") == "close":
            continue
        feature_id = item.get("sourceId")
        siblings = [
            candidate
            for candidate in items
            if isinstance(candidate, dict)
            and candidate.get("workItemType") == "task"
            and candidate.get("parentSourceId") == feature_id
            and candidate.get("operation", "upsert") == "upsert"
        ]
        test_items = [candidate for candidate in siblings if candidate.get("deliverySurface") == "TEST"]
        if not test_items:
            continue
        test_criteria = test_items[0].get("acceptanceCriteria", [])
        test_ids = {
            criterion.get("id")
            for criterion in test_criteria
            if isinstance(criterion, dict) and isinstance(criterion.get("id"), str)
        }
        sibling_ids = {
            criterion.get("id")
            for sibling in siblings
            for criterion in sibling.get("acceptanceCriteria", [])
            if isinstance(criterion, dict) and isinstance(criterion.get("id"), str)
        }
        if not allow_legacy_empty_test and (not test_ids or test_ids != sibling_ids):
            errors.append(f"TEST_AC_COVERAGE: {feature_id}:TEST must contain every sibling AC and at least one AC")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", help="JSON plan path or - for stdin")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
        plan = json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"error: cannot read plan: {exc}", file=sys.stderr)
        return 2
    errors = validate(plan)
    if errors:
        print(f"Yunxiao export plan invalid: {len(errors)} issue(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Yunxiao export plan ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
