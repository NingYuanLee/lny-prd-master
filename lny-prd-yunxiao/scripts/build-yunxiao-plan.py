#!/usr/bin/env python3
"""Validate LNY-PRD delivery scope and build a read-only Yunxiao export plan."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MODULE_RE = re.compile(r"MODULE-\d{3}")
FEATURE_RE = re.compile(r"FEATURE-\d{3}")
PAGE_RE = re.compile(r"PAGE-([A-Z]+)-\d{3}")
API_RE = re.compile(r"API-[A-Z]+-\d{3}")
EXT_RE = re.compile(r"EXT-\d{3}")
AC_RE = re.compile(r"AC-\d+")
SEMVER_DIR_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
FEATURE_REVIEW_STATES = {"pending", "reviewing", "approved", "blocked"}
SCOPE_OPERATIONS = {"本期开发": "upsert", "本期下线": "close"}
SURFACE_RE = re.compile(r"^[A-Z][A-Z0-9_-]{0,31}$")
ALLOWED_DELIVERY_SURFACES = {"BE", "MP"}

DEFAULT_POLICY: dict[str, Any] = {
    "schemaVersion": 1,
    "apiSurface": "BE",
    "externalApiSurface": "BE",
    "pageTerminalSurfaces": {
        "MP": "MP",
        "APP": "MP",
        "H5": "MP",
        "PC": "MP",
        "AD": "BE",
    },
    "includeTestTask": True,
    "surfaceOrder": ["BE", "MP", "TEST"],
}
POLICY_FIELDS = set(DEFAULT_POLICY)


@dataclass(frozen=True)
class Diagnostic:
    code: str
    path: Path
    message: str

    def format(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root).as_posix()
        except ValueError:
            display = self.path.as_posix()
        return f"{self.code}: {display}: {self.message}"


@dataclass
class Feature:
    source_id: str
    title: str
    module_id: str
    module_name: str
    status: str
    review_status: str
    operation: str
    pages: list[str]
    apis: list[str]
    exts: list[str]
    acceptance_criteria: list[dict[str, Any]]
    close_tasks: list[dict[str, Any]]


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def tables(text: str) -> list[tuple[list[str], list[dict[str, str]]]]:
    result: list[tuple[list[str], list[dict[str, str]]]] = []
    lines = text.splitlines()
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
        header = cells(block[0])
        separator = cells(block[1])
        if len(header) != len(separator) or not all(
            TABLE_SEPARATOR_RE.fullmatch(value.replace(" ", "")) for value in separator
        ):
            continue
        rows = []
        for line in block[2:]:
            values = cells(line)
            if len(values) == len(header):
                rows.append(dict(zip(header, values)))
        result.append((header, rows))
    return result


def find_table(text: str, required: set[str]) -> list[dict[str, str]]:
    for header, rows in tables(text):
        if required <= set(header):
            return rows
    return []


def find_table_with_header(
    text: str,
    required: set[str],
) -> tuple[list[str], list[dict[str, str]]] | None:
    for header, rows in tables(text):
        if required <= set(header):
            return header, rows
    return None


def key_values(text: str) -> dict[str, str]:
    rows = find_table(text, {"属性", "内容"}) or find_table(text, {"项目", "内容"})
    return {row["属性"]: row["内容"] for row in rows} if rows and "属性" in rows[0] else {
        row["项目"]: row["内容"] for row in rows
    }


def ids(pattern: re.Pattern[str], value: str) -> list[str]:
    return sorted(set(match.group(0) for match in pattern.finditer(value)))


def nonnegative_int(value: str) -> int | None:
    stripped = value.strip()
    return int(stripped) if re.fullmatch(r"\d+", stripped) else None


def read_text(path: Path, diagnostics: list[Diagnostic], code: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        diagnostics.append(Diagnostic(code, path, "required input is missing"))
    except (OSError, UnicodeDecodeError) as exc:
        diagnostics.append(Diagnostic(code, path, str(exc)))
    return ""


def resolve_version(root: Path, requested: str | None) -> str:
    if requested:
        if not SEMVER_DIR_RE.fullmatch(requested):
            raise ValueError("--version must be vX.Y.Z")
        if not (root / "versions" / requested).is_dir():
            raise ValueError(f"version directory does not exist: versions/{requested}")
        return requested
    versions = []
    directory = root / "versions"
    if directory.is_dir():
        for path in directory.iterdir():
            match = SEMVER_DIR_RE.fullmatch(path.name)
            if path.is_dir() and match:
                versions.append((tuple(int(value) for value in match.groups()), path.name))
    if not versions:
        raise ValueError("no versions/vX.Y.Z directory found")
    return max(versions)[1]


def load_policy(path: Path | None) -> dict[str, Any]:
    policy = json.loads(json.dumps(DEFAULT_POLICY))
    if path is not None:
        try:
            override = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot read policy JSON: {exc}") from exc
        if not isinstance(override, dict):
            raise ValueError("policy root must be an object")
        unknown = set(override) - POLICY_FIELDS
        if unknown:
            raise ValueError("unknown policy fields: " + ", ".join(sorted(unknown)))
        policy.update(override)
    if policy.get("schemaVersion") != 1:
        raise ValueError("policy schemaVersion must be 1")
    page_mapping = policy.get("pageTerminalSurfaces")
    if not isinstance(page_mapping, dict) or not all(
        isinstance(key, str) and isinstance(value, str) and SURFACE_RE.fullmatch(value)
        for key, value in page_mapping.items()
    ):
        raise ValueError("pageTerminalSurfaces must map terminal strings to surface strings")
    unsupported_pages = set(page_mapping.values()) - ALLOWED_DELIVERY_SURFACES
    if unsupported_pages:
        raise ValueError("unsupported page delivery surfaces: " + ", ".join(sorted(unsupported_pages)))
    for field in ("apiSurface", "externalApiSurface"):
        value = policy.get(field)
        if not isinstance(value, str) or not SURFACE_RE.fullmatch(value):
            raise ValueError(f"{field} must be a non-empty uppercase surface")
        if value != "BE":
            raise ValueError(f"{field} must be BE for the company delivery contract")
    if not isinstance(policy.get("includeTestTask"), bool):
        raise ValueError("includeTestTask must be boolean")
    order = policy.get("surfaceOrder")
    if (
        not isinstance(order, list)
        or not order
        or len(order) != len(set(order))
        or not all(isinstance(value, str) and SURFACE_RE.fullmatch(value) for value in order)
    ):
        raise ValueError("surfaceOrder must contain unique uppercase surfaces")
    unsupported_order = set(order) - ALLOWED_DELIVERY_SURFACES - {"TEST"}
    if unsupported_order:
        raise ValueError("surfaceOrder contains unsupported surfaces: " + ", ".join(sorted(unsupported_order)))
    configured = set(page_mapping.values()) | {policy["apiSurface"], policy["externalApiSurface"]}
    if policy["includeTestTask"]:
        configured.add("TEST")
    missing = configured - set(order)
    if missing:
        raise ValueError("surfaceOrder is missing configured surfaces: " + ", ".join(sorted(missing)))
    return policy


def run_core_validation(root: Path, diagnostics: list[Diagnostic], *, allow_fixture_status: bool) -> None:
    validator_path = Path(__file__).resolve().parents[2] / "lny-prd-check" / "scripts" / "validate-prd-project.py"
    if not validator_path.is_file():
        diagnostics.append(Diagnostic("CORE_VALIDATOR_MISSING", validator_path, "install the complete LNY-PRD bundle"))
        return
    spec = importlib.util.spec_from_file_location("lny_prd_project_validator", validator_path)
    if spec is None or spec.loader is None:
        diagnostics.append(Diagnostic("CORE_VALIDATOR_LOAD", validator_path, "cannot load validator"))
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    for issue in module.validate_project(root, allow_fixture_status=allow_fixture_status):
        diagnostics.append(Diagnostic("CORE_" + issue.code, issue.path, issue.message))


def parse_modules(main_path: Path, text: str, diagnostics: list[Diagnostic]) -> dict[str, str]:
    rows = find_table(text, {"模块编号", "模块名称"})
    modules: dict[str, str] = {}
    if not rows:
        diagnostics.append(Diagnostic("MODULE_REGISTRY_MISSING", main_path, "add a 模块编号/模块名称 registry"))
        return modules
    for row in rows:
        found = ids(MODULE_RE, row.get("模块编号", ""))
        name = row.get("模块名称", "").strip()
        if len(found) != 1 or not name:
            diagnostics.append(Diagnostic("INVALID_MODULE_ROW", main_path, f"invalid module row: {row}"))
            continue
        module_id = found[0]
        if module_id in modules:
            diagnostics.append(Diagnostic("DUPLICATE_MODULE", main_path, f"{module_id} appears more than once"))
        modules[module_id] = name
    return modules


def parse_feature_index(path: Path, text: str, diagnostics: list[Diagnostic]) -> dict[str, dict[str, str]]:
    required = {"功能编号", "功能名称", "模块编号", "所属模块", "状态", "评审状态", "明细路径"}
    rows = find_table(text, required)
    if not rows:
        diagnostics.append(Diagnostic("FEATURE_GATE_COLUMNS_MISSING", path, "Feature index needs 模块编号 and 评审状态 columns"))
        return {}
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        found = ids(FEATURE_RE, row.get("功能编号", ""))
        if len(found) != 1:
            diagnostics.append(Diagnostic("INVALID_FEATURE_ROW", path, f"invalid Feature row: {row}"))
            continue
        feature_id = found[0]
        if feature_id in result:
            diagnostics.append(Diagnostic("DUPLICATE_FEATURE", path, f"{feature_id} appears more than once"))
        result[feature_id] = row
    return result


def parse_selected_scope(
    root: Path,
    version: str,
    explicit: list[str],
    diagnostics: list[Diagnostic],
) -> dict[str, str]:
    scope_path = root / "versions" / version / "delivery_scope.md"
    if not scope_path.is_file():
        if explicit:
            return {feature_id: "upsert" for feature_id in sorted(set(explicit))}
        diagnostics.append(Diagnostic("DELIVERY_SCOPE_MISSING", scope_path, "add delivery_scope.md or pass explicit --feature values"))
        return {}
    text = read_text(scope_path, diagnostics, "DELIVERY_SCOPE_READ")
    facts = key_values(text)
    if facts.get("版本号", "").strip() != version:
        diagnostics.append(Diagnostic("SCOPE_VERSION_DRIFT", scope_path, f"expected {version}, got {facts.get('版本号', 'missing')}"))
    if facts.get("评审状态", "").strip().lower() != "approved":
        diagnostics.append(Diagnostic("SCOPE_NOT_APPROVED", scope_path, "range review status must be approved"))
    if nonnegative_int(facts.get("产品确认项", "")) != 0:
        diagnostics.append(Diagnostic("OPEN_PRODUCT_CONFIRMATIONS", scope_path, "产品确认项 must be 0"))
    rows = find_table(text, {"Feature", "纳入方式", "评审状态", "阻塞决策"})
    if not rows:
        diagnostics.append(Diagnostic("SCOPE_FEATURE_TABLE_MISSING", scope_path, "Feature scope table is missing"))
        return {}
    included: dict[str, tuple[dict[str, str], str]] = {}
    for row in rows:
        found = ids(FEATURE_RE, row.get("Feature", ""))
        if len(found) != 1:
            continue
        feature_id = found[0]
        inclusion = row.get("纳入方式", "").strip()
        operation = SCOPE_OPERATIONS.get(inclusion)
        if operation:
            included[feature_id] = (row, operation)
            if row.get("评审状态", "").strip().lower() != "approved":
                diagnostics.append(Diagnostic("SCOPE_FEATURE_NOT_APPROVED", scope_path, f"{feature_id} is not approved"))
            if nonnegative_int(row.get("阻塞决策", "")) != 0:
                diagnostics.append(Diagnostic("SCOPE_FEATURE_BLOCKED", scope_path, f"{feature_id} has blocking decisions"))
    decision_rows = find_table(text, {"决策编号", "状态", "问题", "影响对象"})
    for row in decision_rows:
        decision_id = row.get("决策编号", "").strip()
        if decision_id not in {"", "无", "—", "-"} and row.get("状态", "").strip().lower() != "closed":
            diagnostics.append(Diagnostic("OPEN_SCOPE_DECISION", scope_path, f"{decision_id} is not closed"))
    selected = (
        {feature_id: included[feature_id][1] for feature_id in sorted(set(explicit)) if feature_id in included}
        if explicit
        else {feature_id: included[feature_id][1] for feature_id in sorted(included)}
    )
    if explicit:
        for feature_id in sorted(set(explicit)):
            if feature_id not in included:
                diagnostics.append(Diagnostic("FEATURE_OUTSIDE_SCOPE", scope_path, f"{feature_id} is not an approved 本期开发/本期下线 row"))
    if not selected:
        diagnostics.append(Diagnostic("EMPTY_DELIVERY_SCOPE", scope_path, "no Feature selected for development or shutdown"))
    return selected


def parse_feature(
    root: Path,
    feature_id: str,
    row: dict[str, str],
    modules: dict[str, str],
    operation: str,
    diagnostics: list[Diagnostic],
) -> Feature | None:
    raw_path = row.get("明细路径", "").strip().strip("`")
    detail_path = root.joinpath(*re.split(r"[\\/]", raw_path)) if raw_path else root / "feature" / f"{feature_id}.md"
    text = read_text(detail_path, diagnostics, "FEATURE_DETAIL_MISSING")
    if not text:
        return None
    facts = key_values(text)
    index_status = row.get("状态", "").strip().lower()
    index_review = row.get("评审状态", "").strip().lower() or "pending"
    detail_status = facts.get("状态", "").strip().lower()
    detail_review = facts.get("评审状态", "").strip().lower() or "pending"
    index_module = (ids(MODULE_RE, row.get("模块编号", "")) or [""])[0]
    detail_module = (ids(MODULE_RE, facts.get("模块编号", "")) or [""])[0]
    module_name = row.get("所属模块", "").strip()
    expected_status = "deprecated" if operation == "close" else "active"
    if index_status != expected_status:
        code = "FEATURE_NOT_DEPRECATED" if operation == "close" else "FEATURE_NOT_ACTIVE"
        diagnostics.append(Diagnostic(code, detail_path, f"{feature_id} status={index_status or 'missing'}; expected {expected_status}"))
    if index_review not in FEATURE_REVIEW_STATES:
        diagnostics.append(Diagnostic("INVALID_FEATURE_REVIEW", root / "feature_spec.md", f"{feature_id} review={index_review!r}"))
    if index_review != "approved":
        diagnostics.append(Diagnostic("FEATURE_NOT_APPROVED", detail_path, f"{feature_id} review={index_review}"))
    if detail_status != index_status or detail_review != index_review:
        diagnostics.append(Diagnostic("FEATURE_GATE_DRIFT", detail_path, f"{feature_id} index/detail gate facts differ"))
    if not index_module or index_module != detail_module:
        diagnostics.append(Diagnostic("FEATURE_MODULE_DRIFT", detail_path, f"{feature_id} index/detail module IDs differ"))
    if index_module not in modules:
        diagnostics.append(Diagnostic("UNDEFINED_MODULE", detail_path, f"{feature_id} references {index_module or 'no MODULE ID'}"))
    elif module_name != modules[index_module] or facts.get("所属模块", "").strip() != module_name:
        diagnostics.append(Diagnostic("MODULE_NAME_DRIFT", detail_path, f"{feature_id} module name differs from {index_module}"))
    page_lines, api_lines, ext_lines = [], [], []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("- 关联页面："):
            page_lines.extend(ids(PAGE_RE, line))
        elif stripped.startswith("- 关联接口："):
            api_lines.extend(ids(API_RE, line))
        elif stripped.startswith("- 关联第三方接口："):
            ext_lines.extend(ids(EXT_RE, line))
    acs = []
    seen_ac_ids: set[str] = set()
    for ac_row in find_table(text, {"AC 编号", "验收描述（可验证）"}):
        ac_ids = ids(AC_RE, ac_row.get("AC 编号", ""))
        raw_ac_id = ac_row.get("AC 编号", "").strip()
        if len(ac_ids) != 1 or ac_ids[0] != raw_ac_id:
            diagnostics.append(Diagnostic("INVALID_AC_ID", detail_path, f"invalid AC row: {raw_ac_id or 'missing'}"))
            continue
        ac_id = ac_ids[0]
        duplicate_ac = ac_id in seen_ac_ids
        if duplicate_ac:
            diagnostics.append(Diagnostic("DUPLICATE_AC_ID", detail_path, f"{ac_id} appears more than once"))
        else:
            seen_ac_ids.add(ac_id)
        description = ac_row.get("验收描述（可验证）", "").strip()
        verification = ac_row.get("验证方式", "").strip()
        if not description:
            diagnostics.append(Diagnostic("AC_DESCRIPTION_MISSING", detail_path, f"{ac_id} needs a verifiable description"))
        if not verification:
            diagnostics.append(Diagnostic("AC_VERIFICATION_MISSING", detail_path, f"{ac_id} needs a verification method"))
        if ac_ids:
            page_refs = ids(PAGE_RE, ac_row.get("关联页面", ""))
            interface_value = ac_row.get("关联接口", "")
            api_refs = ids(API_RE, interface_value)
            ext_refs = ids(EXT_RE, interface_value)
            for page_ref in sorted(set(page_refs) - set(page_lines)):
                diagnostics.append(Diagnostic("AC_PAGE_OUTSIDE_FEATURE", detail_path, f"{ac_ids[0]} references {page_ref}"))
            for api_ref in sorted(set(api_refs) - set(api_lines)):
                diagnostics.append(Diagnostic("AC_API_OUTSIDE_FEATURE", detail_path, f"{ac_ids[0]} references {api_ref}"))
            for ext_ref in sorted(set(ext_refs) - set(ext_lines)):
                diagnostics.append(Diagnostic("AC_EXT_OUTSIDE_FEATURE", detail_path, f"{ac_ids[0]} references {ext_ref}"))
            if not duplicate_ac:
                acs.append({
                    "id": ac_id,
                    "description": description,
                    "verification": verification,
                    "pageRefs": page_refs,
                    "apiRefs": api_refs,
                    "extRefs": ext_refs,
                })
    if operation == "upsert" and not acs:
        diagnostics.append(Diagnostic("FEATURE_AC_MISSING", detail_path, f"{feature_id} needs at least one AC for delivery"))
    return Feature(
        feature_id,
        row.get("功能名称", "").strip() or facts.get("功能名称", "").strip(),
        index_module,
        module_name,
        index_status,
        index_review,
        operation,
        sorted(set(page_lines)),
        sorted(set(api_lines)),
        sorted(set(ext_lines)),
        sorted(acs, key=lambda item: int(item["id"].split("-")[1])),
        [],
    )


def load_page_api_bindings(
    root: Path,
    version: str,
    features: list[Feature],
    diagnostics: list[Diagnostic],
) -> dict[str, list[dict[str, str]]]:
    page_root = root / "versions" / version / "pages_prd"
    result: dict[str, list[dict[str, str]]] = {}
    for page_id in sorted({page_id for feature in features for page_id in feature.pages}):
        matches = sorted(path for path in page_root.rglob(f"{page_id}.md") if path.is_file()) if page_root.is_dir() else []
        if len(matches) > 1:
            diagnostics.append(Diagnostic("DUPLICATE_PAGE_PRD", page_root, f"{page_id} has {len(matches)} page PRDs"))
            continue
        candidates: list[tuple[Path, str]] = []
        if matches:
            candidates.append((matches[0], "PAGE_PRD_READ"))
        root_page = root / "ui" / f"{page_id}.md"
        if root_page.is_file():
            candidates.append((root_page, "PAGE_DETAIL_READ"))
        if not candidates:
            diagnostics.append(
                Diagnostic(
                    "PAGE_API_BINDING_SOURCE_MISSING",
                    page_root,
                    f"{page_id} has neither a current page PRD nor a root UI detail",
                )
            )
            result[page_id] = []
            continue
        page_path, read_code = candidates[0]
        text = read_text(page_path, diagnostics, read_code)
        table = find_table_with_header(text, {"接口编号", "触发时机"})
        if table is None and len(candidates) > 1:
            page_path, read_code = candidates[1]
            text = read_text(page_path, diagnostics, read_code)
            table = find_table_with_header(text, {"接口编号", "触发时机"})
        if table is None:
            diagnostics.append(
                Diagnostic(
                    "PAGE_API_BINDING_TABLE_MISSING",
                    page_path,
                    f"{page_id} needs an API binding table with 接口编号 and 触发时机",
                )
            )
            result[page_id] = []
            continue
        bindings: list[dict[str, str]] = []
        _, rows = table
        for row in rows:
            interface_value = row.get("接口编号", "")
            purpose = next((value.strip() for key, value in row.items() if "用途" in key), "")
            trigger = row.get("触发时机", "").strip()
            for interface_ref in ids(API_RE, interface_value) + ids(EXT_RE, interface_value):
                bindings.append({
                    "pageRef": page_id,
                    "interfaceRef": interface_ref,
                    "purpose": purpose or "未指定",
                    "trigger": trigger or "未指定",
                })
        result[page_id] = sorted(
            bindings,
            key=lambda item: (item["pageRef"], item["interfaceRef"], item["purpose"], item["trigger"]),
        )
    return result


def load_previous_close_tasks(
    root: Path,
    version: str,
    features: list[Feature],
    diagnostics: list[Diagnostic],
) -> None:
    close_features = [feature for feature in features if feature.operation == "close"]
    if not close_features:
        return
    requested_match = SEMVER_DIR_RE.fullmatch(version)
    requested_key = tuple(int(value) for value in requested_match.groups()) if requested_match else ()
    candidates: list[tuple[tuple[int, int, int], Path]] = []
    versions_root = root / "versions"
    if versions_root.is_dir():
        for version_dir in versions_root.iterdir():
            match = SEMVER_DIR_RE.fullmatch(version_dir.name)
            plan_path = version_dir / "yunxiao-plan.json"
            if match and plan_path.is_file():
                key = tuple(int(value) for value in match.groups())
                if key < requested_key:
                    candidates.append((key, plan_path))
    if not candidates:
        diagnostics.append(
            Diagnostic(
                "PREVIOUS_PLAN_MISSING",
                versions_root / version / "yunxiao-plan.json",
                "close operations require the nearest earlier versions/{v}/yunxiao-plan.json snapshot",
            )
        )
        return
    previous_path = max(candidates, key=lambda item: item[0])[1]
    try:
        previous = json.loads(previous_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        diagnostics.append(Diagnostic("PREVIOUS_PLAN_READ", previous_path, str(exc)))
        return
    previous_errors = validate_plan_structure(previous, allow_legacy_empty_test=True)
    if previous_errors:
        diagnostics.append(
            Diagnostic(
                "PREVIOUS_PLAN_INVALID",
                previous_path,
                f"snapshot has {len(previous_errors)} issue(s): {previous_errors[0]}",
            )
        )
        return
    items = previous.get("items") if isinstance(previous, dict) else None
    if not isinstance(items, list):
        diagnostics.append(Diagnostic("PREVIOUS_PLAN_INVALID", previous_path, "items must be an array"))
        return
    item_by_id = {
        item.get("sourceId"): item
        for item in items
        if isinstance(item, dict) and isinstance(item.get("sourceId"), str)
    }
    for feature in close_features:
        prior_business = item_by_id.get(feature.source_id)
        if not isinstance(prior_business, dict) or prior_business.get("workItemType") != "business":
            diagnostics.append(
                Diagnostic("PREVIOUS_PLAN_FEATURE_MISSING", previous_path, f"{feature.source_id} was not exported by the previous plan")
            )
            continue
        if prior_business.get("operation", "upsert") == "close":
            diagnostics.append(
                Diagnostic("PREVIOUS_PLAN_ALREADY_CLOSED", previous_path, f"{feature.source_id} was already closed")
            )
            continue
        if prior_business.get("parentSourceId") != feature.module_id:
            diagnostics.append(
                Diagnostic(
                    "PREVIOUS_PLAN_MODULE_DRIFT",
                    previous_path,
                    f"{feature.source_id} previously belonged to {prior_business.get('parentSourceId')}, now {feature.module_id}",
                )
            )
        prefix = feature.source_id + ":"
        prior_tasks = [
            item
            for item in items
            if isinstance(item, dict)
            and item.get("workItemType") == "task"
            and item.get("parentSourceId") == feature.source_id
            and isinstance(item.get("sourceId"), str)
            and item["sourceId"].startswith(prefix)
        ]
        feature.close_tasks = sorted(prior_tasks, key=lambda item: item["sourceId"])


def validate_inputs(
    root: Path,
    version: str,
    explicit: list[str],
    policy: dict[str, Any],
    *,
    allow_fixture_status: bool = False,
) -> tuple[list[Diagnostic], dict[str, str], list[Feature], dict[str, list[dict[str, str]]], str]:
    diagnostics: list[Diagnostic] = []
    run_core_validation(root, diagnostics, allow_fixture_status=allow_fixture_status)
    main_path = root / "main_spec.md"
    feature_index_path = root / "feature_spec.md"
    main = read_text(main_path, diagnostics, "MAIN_SPEC_MISSING")
    feature_spec = read_text(feature_index_path, diagnostics, "FEATURE_SPEC_MISSING")
    modules = parse_modules(main_path, main, diagnostics) if main else {}
    index = parse_feature_index(feature_index_path, feature_spec, diagnostics) if feature_spec else {}
    selected = parse_selected_scope(root, version, explicit, diagnostics)
    for feature_id in explicit:
        if not FEATURE_RE.fullmatch(feature_id):
            diagnostics.append(Diagnostic("INVALID_FEATURE_ID", root, feature_id))
    features = []
    for feature_id, operation in selected.items():
        row = index.get(feature_id)
        if row is None:
            diagnostics.append(Diagnostic("UNDEFINED_FEATURE", feature_index_path, f"{feature_id} is not indexed"))
            continue
        parsed = parse_feature(root, feature_id, row, modules, operation, diagnostics)
        if parsed is not None:
            features.append(parsed)
    page_mapping = policy["pageTerminalSurfaces"]
    for feature in features:
        for page_id in feature.pages:
            terminal_match = PAGE_RE.fullmatch(page_id)
            terminal = terminal_match.group(1) if terminal_match else ""
            if terminal not in page_mapping:
                diagnostics.append(
                    Diagnostic(
                        "UNMAPPED_PAGE_TERMINAL",
                        root / "feature" / f"{feature.source_id}.md",
                        f"{page_id} terminal {terminal or 'missing'} has no mapping policy",
                    )
                )
        if feature.operation == "upsert" and not (feature.pages or feature.apis or feature.exts):
            diagnostics.append(
                Diagnostic(
                    "NO_IMPLEMENTATION_SURFACE",
                    root / "feature" / f"{feature.source_id}.md",
                    f"{feature.source_id} has no PAGE/API/EXT source refs",
                )
            )
    page_bindings = load_page_api_bindings(
        root,
        version,
        [feature for feature in features if feature.operation == "upsert"],
        diagnostics,
    )
    for page_id, bindings in page_bindings.items():
        for binding in bindings:
            interface_ref = binding["interfaceRef"]
            owners = [
                feature_id
                for feature_id, row in index.items()
                if page_id in ids(PAGE_RE, row.get("关联页面", ""))
                and interface_ref in (ids(API_RE, row.get("关联接口", "")) + ids(EXT_RE, row.get("关联接口", "")))
            ]
            if not owners:
                diagnostics.append(
                    Diagnostic(
                        "PAGE_API_OUTSIDE_FEATURE",
                        root / "ui" / f"{page_id}.md",
                        f"{page_id} binds {interface_ref}, but no associated Feature includes both refs",
                    )
                )
    load_previous_close_tasks(root, version, features, diagnostics)
    title_match = re.search(r"^#\s+产品规格说明书\s*-\s*(.+?)\s*$", main, re.MULTILINE)
    project = title_match.group(1).strip() if title_match else root.name
    return diagnostics, modules, sorted(features, key=lambda item: item.source_id), page_bindings, project


def surface_sort_key(surface: str, policy: dict[str, Any]) -> tuple[int, str]:
    order = policy["surfaceOrder"]
    return (order.index(surface), surface) if surface in order else (len(order), surface)


def page_surface(page_id: str, policy: dict[str, Any]) -> str | None:
    terminal_match = PAGE_RE.fullmatch(page_id)
    terminal = terminal_match.group(1) if terminal_match else ""
    return policy["pageTerminalSurfaces"].get(terminal)


def criterion_surfaces(
    feature: Feature,
    criterion: dict[str, Any],
    page_bindings: dict[str, list[dict[str, str]]],
    policy: dict[str, Any],
) -> set[str]:
    surfaces = {surface for page_id in criterion["pageRefs"] if (surface := page_surface(page_id, policy))}
    interface_refs = set(criterion["apiRefs"] + criterion["extRefs"])
    if interface_refs:
        surfaces.add("BE")
    if not criterion["pageRefs"] and interface_refs:
        for page_id in feature.pages:
            bound_refs = {binding["interfaceRef"] for binding in page_bindings.get(page_id, [])}
            if interface_refs & bound_refs:
                surface = page_surface(page_id, policy)
                if surface:
                    surfaces.add(surface)
    return surfaces


def build_plan(
    version: str,
    project: str,
    modules: dict[str, str],
    features: list[Feature],
    page_bindings: dict[str, list[dict[str, str]]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    selected_modules = sorted({feature.module_id for feature in features})
    for module_id in selected_modules:
        items.append({
            "sourceId": module_id,
            "parentSourceId": None,
            "workItemType": "product",
            "title": modules[module_id],
        })
    for feature in features:
        business_item = {
            "sourceId": feature.source_id,
            "parentSourceId": feature.module_id,
            "workItemType": "business",
            "title": feature.title,
        }
        if feature.operation == "close":
            business_item["operation"] = "close"
        items.append(business_item)
        refs_by_surface: dict[str, set[str]] = {}
        if feature.apis:
            refs_by_surface.setdefault(policy["apiSurface"], set()).update(feature.apis)
        if feature.exts:
            refs_by_surface.setdefault(policy["externalApiSurface"], set()).update(feature.exts)
        for page_id in feature.pages:
            surface = page_surface(page_id, policy)
            if surface:
                refs_by_surface.setdefault(surface, set()).add(page_id)
        if policy["includeTestTask"]:
            refs_by_surface.setdefault("TEST", set()).update(feature.pages + feature.apis + feature.exts)
        if feature.operation == "close":
            for previous_task in feature.close_tasks:
                surface = previous_task.get("deliverySurface")
                if not isinstance(surface, str) or previous_task.get("sourceId") != f"{feature.source_id}:{surface}":
                    continue
                items.append({
                    "sourceId": f"{feature.source_id}:{surface}",
                    "parentSourceId": feature.source_id,
                    "workItemType": "task",
                    "title": f"[{surface}] {feature.title}",
                    "operation": "close",
                    "deliverySurface": surface,
                    "sourceRefs": sorted(set(previous_task.get("sourceRefs", []))),
                    "dependencyRefs": [],
                    "pageApiBindings": [],
                    "acceptanceCriteria": [],
                })
            continue
        feature_interfaces = set(feature.apis + feature.exts)
        bindings_by_surface: dict[str, list[dict[str, str]]] = {}
        for page_id in feature.pages:
            surface = page_surface(page_id, policy)
            if not surface:
                continue
            for binding in page_bindings.get(page_id, []):
                if binding["interfaceRef"] in feature_interfaces:
                    bindings_by_surface.setdefault(surface, []).append(binding)
                    if policy["includeTestTask"]:
                        bindings_by_surface.setdefault("TEST", []).append(binding)
        criteria_by_surface: dict[str, list[dict[str, Any]]] = {"TEST": feature.acceptance_criteria}
        for criterion in feature.acceptance_criteria:
            for surface in criterion_surfaces(feature, criterion, page_bindings, policy):
                criteria_by_surface.setdefault(surface, []).append(criterion)
        for surface in sorted(refs_by_surface, key=lambda value: surface_sort_key(value, policy)):
            surface_bindings = sorted(
                bindings_by_surface.get(surface, []),
                key=lambda item: (item["pageRef"], item["interfaceRef"], item["purpose"], item["trigger"]),
            )
            dependencies = {
                binding["interfaceRef"]
                for binding in surface_bindings
                if surface not in {"BE", "TEST"}
            }
            if surface not in {"BE", "TEST"}:
                for criterion in criteria_by_surface.get(surface, []):
                    dependencies.update(criterion["apiRefs"] + criterion["extRefs"])
            items.append({
                "sourceId": f"{feature.source_id}:{surface}",
                "parentSourceId": feature.source_id,
                "workItemType": "task",
                "title": f"[{surface}] {feature.title}",
                "deliverySurface": surface,
                "sourceRefs": sorted(refs_by_surface[surface]),
                "dependencyRefs": sorted(dependencies),
                "pageApiBindings": surface_bindings,
                "acceptanceCriteria": criteria_by_surface.get(surface, []),
            })
    return {
        "schemaVersion": 1,
        "adapter": "lny-prd-yunxiao",
        "sourceVersion": version,
        "project": project,
        "items": items,
    }


def validate_plan_structure(plan: Any, *, allow_legacy_empty_test: bool = False) -> list[str]:
    validator_path = Path(__file__).with_name("validate-export-plan.py")
    spec = importlib.util.spec_from_file_location("lny_prd_yunxiao_plan_validator", validator_path)
    if spec is None or spec.loader is None:
        return ["PLAN_VALIDATOR_LOAD: cannot load validate-export-plan.py"]
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return list(module.validate(plan, allow_legacy_empty_test=allow_legacy_empty_test))


def validate_built_plan(
    plan: dict[str, Any],
    features: list[Feature],
    policy: dict[str, Any],
) -> list[str]:
    errors = validate_plan_structure(plan)
    by_id = {item.get("sourceId"): item for item in plan.get("items", []) if isinstance(item, dict)}
    for feature in features:
        if feature.operation != "upsert":
            continue
        if not policy["includeTestTask"]:
            continue
        test_item = by_id.get(f"{feature.source_id}:TEST")
        if not isinstance(test_item, dict):
            errors.append(f"TEST_AC_COVERAGE: {feature.source_id} has no TEST task")
            continue
        expected = feature.acceptance_criteria
        if test_item.get("acceptanceCriteria") != expected:
            errors.append(f"TEST_AC_COVERAGE: {feature.source_id}:TEST does not contain the complete Feature AC set")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prd_root", type=Path)
    parser.add_argument("--mode", choices=("validate", "plan"), default="plan")
    parser.add_argument("--version")
    parser.add_argument("--feature", action="append", default=[], help="explicit FEATURE-###; repeatable")
    parser.add_argument("--policy", type=Path, help="optional organization mapping policy JSON")
    parser.add_argument("--allow-fixture-status", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = args.prd_root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"PRD root does not exist: {root}")
    try:
        version = resolve_version(root, args.version)
        policy = load_policy(args.policy.expanduser().resolve() if args.policy else None)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    diagnostics, modules, features, page_bindings, project = validate_inputs(
        root,
        version,
        args.feature,
        policy,
        allow_fixture_status=args.allow_fixture_status,
    )
    if diagnostics:
        print(f"Yunxiao export validation failed: {len(diagnostics)} issue(s)", file=sys.stderr)
        for diagnostic in diagnostics:
            print(f"- {diagnostic.format(root)}", file=sys.stderr)
        return 1
    plan = build_plan(version, project, modules, features, page_bindings, policy)
    plan_errors = validate_built_plan(plan, features, policy)
    if plan_errors:
        print(f"Yunxiao export validation failed: {len(plan_errors)} issue(s)", file=sys.stderr)
        for error in plan_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.mode == "validate":
        print(json.dumps({
            "valid": True,
            "sourceVersion": version,
            "selectedFeatures": [feature.source_id for feature in features],
            "featureOperations": {feature.source_id: feature.operation for feature in features},
        }, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
