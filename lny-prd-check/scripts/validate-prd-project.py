#!/usr/bin/env python3
"""Validate semantic consistency across an LNY-PRD project."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PAGE_RE = re.compile(r"PAGE-([A-Z]+)-(\d{3})")
API_RE = re.compile(r"API-([A-Z]+)-(\d{3})")
EXT_RE = re.compile(r"EXT-(\d{3})")
FEATURE_RE = re.compile(r"FEATURE-(\d{3})")
COMP_RE = re.compile(r"COMP-(\d{3})")
MODULE_RE = re.compile(r"MODULE-(\d{3})")
STORY_RE = re.compile(r"STORY-(\d{3})")
VERSION_RE = re.compile(r"^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")
FEATURE_STATUSES = {"draft", "active", "deprecated"}
REVIEW_STATUSES = {"pending", "reviewing", "approved", "blocked"}
STORY_TYPES = {"用户价值", "运营", "合规", "迁移", "技术使能"}
MODULE_REQUIRED_FIELDS = {
    "模块名称",
    "领域职责",
    "核心业务对象",
    "范围内",
    "范围外",
    "对外提供能力",
    "依赖模块",
    "跨模块交互",
}
SCOPE_REVIEW_CONCLUSIONS = {"通过", "附条件通过", "退回补充", "不进入本期"}
SCOPE_INCLUSIONS = {"本期开发", "本期下线", "待确认"}
AC_DELIVERY_ROLE_RE = re.compile(r"(?<![A-Z0-9_-])(?:FE|BE|MP|AD|PC|APP|H5|TEST)(?![A-Z0-9_-])")


@dataclass(frozen=True)
class Issue:
    code: str
    path: Path
    message: str

    def format(self, root: Path) -> str:
        try:
            display = self.path.relative_to(root).as_posix()
        except ValueError:
            display = self.path.as_posix()
        return f"{self.code}: {display}: {self.message}"


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def tables(text: str) -> list[list[dict[str, str]]]:
    """Parse ordinary pipe tables; complex cells containing pipes are unsupported."""
    lines = text.splitlines()
    parsed: list[list[dict[str, str]]] = []
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
        rows: list[dict[str, str]] = []
        for line in block[2:]:
            values = cells(line)
            if len(values) != len(header):
                continue
            rows.append(dict(zip(header, values)))
        parsed.append(rows)
    return parsed


def matching_tables(text: str, required: set[str]) -> list[list[dict[str, str]]]:
    return [table for table in tables(text) if table and required <= set(table[0])]


def id_set(pattern: re.Pattern[str], value: str) -> set[str]:
    return {match.group(0) for match in pattern.finditer(value)}


def first_int(value: str) -> int | None:
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def nonnegative_int(value: str) -> int | None:
    stripped = value.strip()
    return int(stripped) if re.fullmatch(r"\d+", stripped) else None


def key_values(text: str) -> dict[str, str]:
    for table in matching_tables(text, {"属性", "内容"}):
        return {row["属性"]: row["内容"] for row in table}
    for table in matching_tables(text, {"项目", "内容"}):
        return {row["项目"]: row["内容"] for row in table}
    return {}


def add(issues: list[Issue], code: str, path: Path, message: str) -> None:
    issues.append(Issue(code, path, message))


def read_required(root: Path, name: str, issues: list[Issue]) -> tuple[Path, str]:
    path = root / name
    if not path.is_file():
        add(issues, "MISSING_ROOT_SPEC", path, "required root specification is missing")
        return path, ""
    text = read_utf8(path, issues)
    return path, text or ""


def read_utf8(path: Path, issues: list[Issue]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        add(issues, "INVALID_UTF8", path, str(exc))
    except OSError as exc:
        add(issues, "READ_ERROR", path, str(exc))
    return None


def collect_index(
    text: str,
    required: set[str],
    id_column: str,
    pattern: re.Pattern[str],
    path: Path,
    issues: list[Issue],
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for table in matching_tables(text, required):
        for row in table:
            found = id_set(pattern, row.get(id_column, ""))
            if not found:
                continue
            item_id = sorted(found)[0]
            if item_id in result:
                add(issues, "DUPLICATE_INDEX_ID", path, f"{item_id} appears more than once")
            result[item_id] = row
    return result


def detail_path(root: Path, row: dict[str, str], column: str, fallback: Path) -> Path:
    raw = row.get(column, "").strip().strip("`")
    if raw and raw != "无":
        return root.joinpath(*re.split(r"[\\/]+", raw))
    return fallback


def collect_details(
    root: Path,
    index: dict[str, dict[str, str]],
    *,
    id_field: str,
    pattern: re.Pattern[str],
    fallback_dir: str,
    missing_code: str,
    identity_code: str,
    issues: list[Issue],
    cache: dict[Path, str | None],
) -> dict[str, tuple[Path, str, dict[str, str]]]:
    result: dict[str, tuple[Path, str, dict[str, str]]] = {}
    for item_id, row in index.items():
        path = detail_path(root, row, "明细路径", root / fallback_dir / f"{item_id}.md")
        if not path.is_file():
            add(issues, missing_code, path, f"indexed {item_id} has no detail file")
            continue
        if path not in cache:
            cache[path] = read_utf8(path, issues)
        text = cache[path]
        if text is None:
            continue
        facts = key_values(text)
        actual_ids = id_set(pattern, facts.get(id_field, ""))
        if actual_ids != {item_id}:
            actual = ", ".join(sorted(actual_ids)) if actual_ids else "missing"
            add(issues, identity_code, path, f"expected {id_field} {item_id}, got {actual}")
        result[item_id] = (path, text, facts)
    return result


def validate_project(root: Path, *, allow_fixture_status: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    main_path, main = read_required(root, "main_spec.md", issues)
    ui_path, ui = read_required(root, "ui_manifest.md", issues)
    api_path, api = read_required(root, "api_spec.md", issues)
    feature_path, feature = read_required(root, "feature_spec.md", issues)
    if not all((main, ui, api, feature)):
        return issues

    stories = collect_index(
        main,
        {"故事编号"},
        "故事编号",
        STORY_RE,
        main_path,
        issues,
    )

    pages = collect_index(
        ui,
        {"页面编号", "明细路径"},
        "页面编号",
        PAGE_RE,
        ui_path,
        issues,
    )
    for page_id, row in pages.items():
        status = row.get("状态", "active").strip().lower() or "active"
        allowed = {"active", "deprecated"}
        if allow_fixture_status:
            allowed.add("fixture")
        if status not in allowed:
            add(
                issues,
                "INVALID_PAGE_STATUS",
                ui_path,
                f"{page_id} status={status!r}; allowed: {', '.join(sorted(allowed))}",
            )
    indexed_active_pages = {
        page_id
        for page_id, row in pages.items()
        if row.get("状态", "active").strip().lower() not in {"deprecated", "fixture"}
    }
    comps = collect_index(
        ui,
        {"组件编号", "明细路径"},
        "组件编号",
        COMP_RE,
        ui_path,
        issues,
    )
    apis = collect_index(
        api,
        {"接口编号", "明细路径"},
        "接口编号",
        API_RE,
        api_path,
        issues,
    )
    exts = collect_index(
        api,
        {"接口编号", "明细路径"},
        "接口编号",
        EXT_RE,
        api_path,
        issues,
    )
    features = collect_index(
        feature,
        {"功能编号", "明细路径"},
        "功能编号",
        FEATURE_RE,
        feature_path,
        issues,
    )
    delivery_scopes = sorted((root / "versions").glob("v*/delivery_scope.md"))
    versioned_delivery_scopes = [
        (tuple(int(value) for value in match.groups()), path)
        for path in delivery_scopes
        if (match := VERSION_RE.fullmatch(path.parent.name))
    ]
    current_delivery_scope = max(
        versioned_delivery_scopes,
        default=((), None),
    )[1]
    module_tables = []
    for table in matching_tables(feature, {"属性", "内容"}):
        facts = {row["属性"]: row["内容"] for row in table}
        if "模块编号" in facts:
            module_tables.append(facts)
    legacy_module_tables = matching_tables(main, {"模块编号", "模块名称"})
    module_contract_enabled = bool(delivery_scopes) or bool(module_tables) or bool(legacy_module_tables)
    modules: dict[str, str] = {}
    module_dependencies: dict[str, set[str]] = {}
    for facts in module_tables:
        module_ids = id_set(MODULE_RE, facts.get("模块编号", ""))
        module_name = facts.get("模块名称", "").strip()
        if len(module_ids) != 1 or not module_name:
            add(issues, "INVALID_MODULE_DEFINITION", feature_path, f"invalid module definition: {facts}")
            continue
        module_id = sorted(module_ids)[0]
        if module_id in modules:
            add(issues, "DUPLICATE_MODULE_ID", feature_path, f"{module_id} appears more than once")
        modules[module_id] = module_name
        missing_fields = sorted(
            field for field in MODULE_REQUIRED_FIELDS if not facts.get(field, "").strip()
        )
        if missing_fields:
            add(
                issues,
                "INCOMPLETE_MODULE_BOUNDARY",
                feature_path,
                f"{module_id} missing: {', '.join(missing_fields)}",
            )
        module_dependencies[module_id] = id_set(MODULE_RE, facts.get("依赖模块", ""))
    if not module_tables:
        # Read-only compatibility for pre-migration projects. New and modified
        # projects define full Module boundaries in feature_spec.md.
        for table in legacy_module_tables:
            for row in table:
                module_ids = id_set(MODULE_RE, row.get("模块编号", ""))
                module_name = row.get("模块名称", "").strip()
                if len(module_ids) != 1 or not module_name:
                    add(issues, "INVALID_LEGACY_MODULE_ROW", main_path, f"invalid module row: {row}")
                    continue
                module_id = sorted(module_ids)[0]
                if module_id in modules:
                    add(issues, "DUPLICATE_MODULE_ID", main_path, f"{module_id} appears more than once")
                modules[module_id] = module_name
    if module_contract_enabled and not modules:
        add(issues, "MODULE_DEFINITION_MISSING", feature_path, "delivery contract requires MODULE definitions")
    for module_id, dependencies in module_dependencies.items():
        if module_id in dependencies:
            add(issues, "MODULE_SELF_DEPENDENCY", feature_path, f"{module_id} depends on itself")
        for dependency in sorted(dependencies - set(modules)):
            add(issues, "UNDEFINED_MODULE_DEPENDENCY", feature_path, f"{module_id} depends on {dependency}")

    detail_cache: dict[Path, str | None] = {}
    page_details = collect_details(
        root,
        pages,
        id_field="页面编号",
        pattern=PAGE_RE,
        fallback_dir="ui",
        missing_code="MISSING_PAGE_DETAIL",
        identity_code="PAGE_DETAIL_ID",
        issues=issues,
        cache=detail_cache,
    )
    collect_details(
        root,
        comps,
        id_field="组件编号",
        pattern=COMP_RE,
        fallback_dir="ui",
        missing_code="MISSING_COMP_DETAIL",
        identity_code="COMP_DETAIL_ID",
        issues=issues,
        cache=detail_cache,
    )
    collect_details(
        root,
        apis,
        id_field="接口编号",
        pattern=API_RE,
        fallback_dir="api",
        missing_code="MISSING_API_DETAIL",
        identity_code="API_DETAIL_ID",
        issues=issues,
        cache=detail_cache,
    )
    collect_details(
        root,
        exts,
        id_field="接口编号",
        pattern=EXT_RE,
        fallback_dir="api",
        missing_code="MISSING_API_DETAIL",
        identity_code="EXT_DETAIL_ID",
        issues=issues,
        cache=detail_cache,
    )
    feature_details = collect_details(
        root,
        features,
        id_field="功能编号",
        pattern=FEATURE_RE,
        fallback_dir="feature",
        missing_code="MISSING_FEATURE_DETAIL",
        identity_code="FEATURE_DETAIL_ID",
        issues=issues,
        cache=detail_cache,
    )

    active_pages: set[str] = set()
    active_feature_count = 0
    feature_facts: dict[str, tuple[int | None, int]] = {}
    feature_statuses: dict[str, str] = {}
    feature_page_acs: dict[tuple[str, str], set[str]] = {}
    feature_ac_ids: dict[str, set[str]] = {}
    feature_story_refs: dict[str, set[str]] = {}
    story_fact_contract_enabled = any("故事类型" in row for row in stories.values())
    story_mapping_contract_enabled = story_fact_contract_enabled or any(
        "关联 STORY" in detail[2] for detail in feature_details.values()
    )
    if story_fact_contract_enabled:
        for story_id, row in stories.items():
            story_type = row.get("故事类型", "").strip()
            if story_type not in STORY_TYPES:
                add(
                    issues,
                    "INVALID_STORY_TYPE",
                    main_path,
                    f"{story_id} type={story_type or 'missing'}; allowed: {', '.join(sorted(STORY_TYPES))}",
                )
            missing = [
                field
                for field in ("角色 / 利益相关方", "画像 / 背景", "需求故事")
                if not row.get(field, "").strip()
            ]
            if missing:
                add(issues, "STORY_FACT_MISSING", main_path, f"{story_id} missing: {', '.join(missing)}")
    for feature_id in features:
        detail = feature_details.get(feature_id)
        if detail is None:
            continue
        path, text, facts = detail
        detail_status = facts.get("状态", "").strip().lower()
        feature_statuses[feature_id] = detail_status
        if detail_status not in FEATURE_STATUSES:
            add(
                issues,
                "INVALID_FEATURE_STATUS",
                path,
                f"{feature_id} status={detail_status!r}; allowed: {', '.join(sorted(FEATURE_STATUSES))}",
            )
        detail_review = facts.get("评审状态", "").strip().lower()
        detail_modules = id_set(MODULE_RE, facts.get("模块编号", ""))
        detail_stories = id_set(STORY_RE, facts.get("关联 STORY", ""))
        feature_story_refs[feature_id] = detail_stories
        if story_mapping_contract_enabled:
            if not detail_stories:
                add(
                    issues,
                    "FEATURE_STORY_MISSING",
                    path,
                    f"{feature_id} must reference at least one STORY; '无/框架承接' is not allowed",
                )
            for story_id in sorted(detail_stories - set(stories)):
                add(issues, "UNDEFINED_STORY_REF", path, f"{feature_id} references {story_id}")
        feature_contract_enabled = module_contract_enabled or bool(detail_review or detail_modules)
        if feature_contract_enabled:
            if detail_review not in REVIEW_STATUSES:
                add(
                    issues,
                    "INVALID_FEATURE_REVIEW_STATUS",
                    path,
                    f"{feature_id} review={detail_review or 'missing'}; allowed: {', '.join(sorted(REVIEW_STATUSES))}",
                )
            if len(detail_modules) != 1:
                add(
                    issues,
                    "INVALID_FEATURE_MODULE",
                    path,
                    f"{feature_id} detail must contain exactly one MODULE ID",
                )
            elif sorted(detail_modules)[0] not in modules:
                add(
                    issues,
                    "UNDEFINED_MODULE_REF",
                    path,
                    f"{feature_id} references {sorted(detail_modules)[0]}",
                )
        detail_branch = first_int(facts.get("分支数", ""))
        if detail_branch is None or detail_branch < 1:
            add(
                issues,
                "INVALID_FEATURE_BRANCH_COUNT",
                path,
                f"{feature_id} branch count must be a positive integer",
            )
        detail_pages = set()
        detail_apis = set()
        detail_exts = set()
        for line in text.splitlines():
            if line.lstrip().startswith("- 关联页面："):
                detail_pages |= id_set(PAGE_RE, line)
            elif line.lstrip().startswith("- 关联接口："):
                detail_apis |= id_set(API_RE, line)
            elif line.lstrip().startswith("- 关联第三方接口："):
                detail_exts |= id_set(EXT_RE, line)
        for page_id in sorted(detail_pages - set(pages)):
            add(issues, "UNDEFINED_PAGE_REF", path, f"{feature_id} references {page_id}")
        for api_id in sorted(detail_apis - set(apis)):
            add(issues, "UNDEFINED_API_REF", path, f"{feature_id} references {api_id}")
        for ext_id in sorted(detail_exts - set(exts)):
            add(issues, "UNDEFINED_EXT_REF", path, f"{feature_id} references {ext_id}")
        ac_tables = matching_tables(text, {"AC 编号", "验收描述（可验证）"})
        ac_rows = [ac_row for table in ac_tables for ac_row in table]
        seen_ac_ids: set[str] = set()
        for ac_row in ac_rows:
            ac_id = ac_row.get("AC 编号", "").strip()
            if not re.fullmatch(r"AC-\d+", ac_id):
                add(issues, "INVALID_AC_ID", path, f"{feature_id} has invalid AC ID {ac_id or 'missing'}")
                continue
            duplicate_ac = ac_id in seen_ac_ids
            if duplicate_ac:
                add(issues, "DUPLICATE_AC_ID", path, f"{feature_id} repeats {ac_id}")
            else:
                seen_ac_ids.add(ac_id)
            description = ac_row.get("验收描述（可验证）", "").strip()
            verification = ac_row.get("验证方式", "").strip()
            if not description:
                add(issues, "AC_DESCRIPTION_MISSING", path, f"{feature_id} {ac_id} needs a verifiable description")
            if not verification:
                add(issues, "AC_VERIFICATION_MISSING", path, f"{feature_id} {ac_id} needs a verification method")
            leaked_roles = sorted(set(AC_DELIVERY_ROLE_RE.findall(verification)))
            if leaked_roles:
                add(
                    issues,
                    "AC_VERIFICATION_ROLE_LEAK",
                    path,
                    f"{feature_id} {ac_id} verification contains delivery roles: {', '.join(leaked_roles)}",
                )
            ac_pages = id_set(PAGE_RE, ac_row.get("关联页面", ""))
            ac_apis = id_set(API_RE, ac_row.get("关联接口", ""))
            ac_exts = id_set(EXT_RE, ac_row.get("关联接口", ""))
            for page_id in sorted(ac_pages - detail_pages):
                add(issues, "AC_PAGE_OUTSIDE_FEATURE", path, f"{feature_id} {ac_id} references {page_id}")
            for api_id in sorted(ac_apis - detail_apis):
                add(issues, "AC_API_OUTSIDE_FEATURE", path, f"{feature_id} {ac_id} references {api_id}")
            for ext_id in sorted(ac_exts - detail_exts):
                add(issues, "AC_EXT_OUTSIDE_FEATURE", path, f"{feature_id} {ac_id} references {ext_id}")
            for page_id in ac_pages:
                feature_page_acs.setdefault((feature_id, page_id), set()).add(ac_id)
        if detail_status == "active" and not seen_ac_ids:
            add(issues, "FEATURE_AC_MISSING", path, f"{feature_id} needs at least one valid AC")
        feature_ac_ids[feature_id] = seen_ac_ids
        ac_count = len(seen_ac_ids)
        feature_facts[feature_id] = (detail_branch, ac_count)
        if detail_status == "active":
            active_feature_count += 1
            active_pages |= detail_pages

    if story_mapping_contract_enabled:
        covered_stories = set().union(*feature_story_refs.values()) if feature_story_refs else set()
        for story_id in sorted(set(stories) - covered_stories):
            add(issues, "STORY_WITHOUT_FEATURE", main_path, f"{story_id} is not referenced by any Feature detail")

    page_prd_by_id: dict[str, Path] = {}
    version_dirs = sorted(
        (
            (tuple(int(value) for value in match.groups()), path)
            for path in (root / "versions").glob("v*")
            if path.is_dir() and (match := VERSION_RE.fullmatch(path.name))
        ),
        reverse=True,
    )
    for _, version_dir in version_dirs:
        page_root = version_dir / "pages_prd"
        if not page_root.is_dir():
            continue
        for page_path in sorted(page_root.rglob("PAGE-*.md")):
            page_ids = id_set(PAGE_RE, page_path.stem)
            if len(page_ids) == 1:
                page_prd_by_id.setdefault(sorted(page_ids)[0], page_path)
    for page_id, page_path in page_prd_by_id.items():
        page_text = read_utf8(page_path, issues)
        if page_text is None:
            continue
        reverse_tables = matching_tables(page_text, {"Feature编号", "关联AC"})
        if not reverse_tables:
            continue
        reverse: dict[str, set[str]] = {}
        for table in reverse_tables:
            for row in table:
                row_features = id_set(FEATURE_RE, row.get("Feature编号", ""))
                row_acs = id_set(re.compile(r"AC-\d+"), row.get("关联AC", ""))
                for feature_id in row_features:
                    reverse.setdefault(feature_id, set()).update(row_acs)
                    if feature_id not in features:
                        add(issues, "PAGE_AC_UNKNOWN_FEATURE", page_path, f"{page_id} references {feature_id}")
                    for ac_id in sorted(row_acs - feature_ac_ids.get(feature_id, set())):
                        add(issues, "PAGE_AC_UNKNOWN_AC", page_path, f"{page_id} references {feature_id} {ac_id}")
        related_features = {
            feature_id
            for (feature_id, related_page), ac_ids in feature_page_acs.items()
            if related_page == page_id and ac_ids
        } | set(reverse)
        for feature_id in sorted(related_features):
            expected = feature_page_acs.get((feature_id, page_id), set())
            actual = reverse.get(feature_id, set())
            if expected != actual:
                add(
                    issues,
                    "PAGE_AC_DRIFT",
                    page_path,
                    f"{page_id} {feature_id} Feature ACs={sorted(expected)}, PAGE ACs={sorted(actual)}",
                )

    for feature_id in sorted(id_set(FEATURE_RE, main) - set(features)):
        add(issues, "UNDEFINED_FEATURE_REF", main_path, f"main_spec references {feature_id}")

    if active_pages != indexed_active_pages:
        missing_from_features = sorted(indexed_active_pages - active_pages)
        missing_from_index = sorted(active_pages - indexed_active_pages)
        detail = []
        if missing_from_features:
            detail.append("active pages without active Feature: " + ", ".join(missing_from_features))
        if missing_from_index:
            detail.append("active Feature pages not active in manifest: " + ", ".join(missing_from_index))
        add(issues, "ACTIVE_PAGE_FEATURE_DRIFT", ui_path, "; ".join(detail))

    for report in sorted((root / "versions").glob("v*/sp_report.md")):
        report_text = read_utf8(report, issues)
        if report_text is None:
            continue
        for table in matching_tables(report_text, {"FEATURE编号", "分支数", "AC条数（只审计）"}):
            for row in table:
                feature_ids = id_set(FEATURE_RE, row.get("FEATURE编号", ""))
                if not feature_ids:
                    continue
                feature_id = sorted(feature_ids)[0]
                expected = feature_facts.get(feature_id)
                if expected is None:
                    add(issues, "SP_UNKNOWN_FEATURE", report, f"report contains undefined {feature_id}")
                    continue
                branch, ac_count = expected
                report_branch = first_int(row["分支数"])
                report_ac = first_int(row["AC条数（只审计）"])
                if (report_branch, report_ac) != (branch, ac_count):
                    add(
                        issues,
                        "SP_FEATURE_INPUT_DRIFT",
                        report,
                        f"{feature_id} report=({report_branch}, {report_ac}), source=({branch}, {ac_count})",
                    )

    for scope_path in delivery_scopes:
        scope_text = read_utf8(scope_path, issues)
        if scope_text is None:
            continue
        scope_facts = key_values(scope_text)
        expected_version = scope_path.parent.name
        if scope_facts.get("版本号", "").strip() != expected_version:
            add(
                issues,
                "DELIVERY_SCOPE_VERSION_DRIFT",
                scope_path,
                f"expected {expected_version}, got {scope_facts.get('版本号', 'missing')}",
            )
        scope_review = scope_facts.get("评审状态", "").strip().lower()
        if scope_review not in REVIEW_STATUSES:
            add(
                issues,
                "INVALID_SCOPE_REVIEW_STATUS",
                scope_path,
                f"review={scope_review or 'missing'}; allowed: {', '.join(sorted(REVIEW_STATUSES))}",
            )
        scope_conclusion = scope_facts.get("评审结论", "").strip()
        if scope_conclusion and scope_conclusion not in SCOPE_REVIEW_CONCLUSIONS:
            add(
                issues,
                "INVALID_SCOPE_REVIEW_CONCLUSION",
                scope_path,
                f"conclusion={scope_conclusion}; allowed: {', '.join(sorted(SCOPE_REVIEW_CONCLUSIONS))}",
            )
        confirmation_count = nonnegative_int(scope_facts.get("产品确认项", ""))
        if confirmation_count is None:
            add(issues, "INVALID_SCOPE_CONFIRMATION_COUNT", scope_path, "产品确认项 must be a non-negative integer")
        scope_tables = matching_tables(scope_text, {"Feature", "纳入方式", "评审状态", "阻塞决策"})
        if not scope_tables:
            add(issues, "DELIVERY_SCOPE_FEATURE_TABLE_MISSING", scope_path, "Feature scope table is missing")
        seen_scope_features: set[str] = set()
        for table in scope_tables:
            for row in table:
                feature_ids = id_set(FEATURE_RE, row.get("Feature", ""))
                if not feature_ids:
                    continue
                feature_id = sorted(feature_ids)[0]
                if feature_id in seen_scope_features:
                    add(issues, "DUPLICATE_SCOPE_FEATURE", scope_path, f"{feature_id} appears more than once")
                seen_scope_features.add(feature_id)
                if feature_id not in features:
                    add(issues, "SCOPE_UNKNOWN_FEATURE", scope_path, f"references undefined {feature_id}")
                inclusion = row.get("纳入方式", "").strip()
                if inclusion not in SCOPE_INCLUSIONS:
                    add(
                        issues,
                        "INVALID_SCOPE_INCLUSION",
                        scope_path,
                        f"{feature_id} 纳入方式={inclusion or 'missing'}; allowed: 本期开发, 本期下线, 待确认",
                    )
                elif (
                    scope_path == current_delivery_scope
                    and feature_id in features
                    and inclusion in {"本期开发", "本期下线"}
                ):
                    expected_status = "active" if inclusion == "本期开发" else "deprecated"
                    actual_status = feature_statuses.get(feature_id, "")
                    if actual_status != expected_status:
                        add(
                            issues,
                            "SCOPE_FEATURE_LIFECYCLE_MISMATCH",
                            scope_path,
                            f"{feature_id} {inclusion} requires status={expected_status}, got {actual_status or 'missing'}",
                        )
                row_review = row.get("评审状态", "").strip().lower()
                if row_review not in REVIEW_STATUSES:
                    add(issues, "INVALID_SCOPE_FEATURE_REVIEW", scope_path, f"{feature_id} review={row_review or 'missing'}")
                if nonnegative_int(row.get("阻塞决策", "")) is None:
                    add(issues, "INVALID_SCOPE_BLOCKER_COUNT", scope_path, f"{feature_id} 阻塞决策 must be a non-negative integer")
        for table in matching_tables(scope_text, {"决策编号", "状态", "问题", "影响对象"}):
            for row in table:
                decision_id = row.get("决策编号", "").strip()
                if decision_id in {"", "无", "—", "-"}:
                    continue
                if row.get("状态", "").strip().lower() not in {"open", "closed"}:
                    add(issues, "INVALID_DECISION_STATUS", scope_path, f"{decision_id} status must be open or closed")

    defined_ids = set(pages) | set(apis) | set(exts) | set(features) | set(comps)
    for directory in (root / "ui", root / "api", root / "feature"):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if path not in detail_cache:
                detail_cache[path] = read_utf8(path, issues)
            text = detail_cache[path]
            if text is None:
                continue
            for pattern, label in ((PAGE_RE, "PAGE"), (API_RE, "API"), (EXT_RE, "EXT"), (FEATURE_RE, "FEATURE"), (COMP_RE, "COMP")):
                for item_id in sorted(id_set(pattern, text) - defined_ids):
                    add(issues, f"UNDEFINED_{label}_REF", path, f"references {item_id}")

    return issues


# 机器可读「下一步建议」路由：issue 码 → 建议委派的技能短名（① master 消费）。
# 短名与 /lny-prd-* 对应；master 指 ① 总控（根规格、Story 与可读性）。
NEXT_ROUTE: dict[str, str] = {
    "MISSING_ROOT_SPEC": "master",
    "INVALID_UTF8": "master",
    "READ_ERROR": "master",
    "DUPLICATE_INDEX_ID": "master",
    "INVALID_STORY_TYPE": "master",
    "STORY_FACT_MISSING": "master",
    "UNDEFINED_STORY_REF": "master",

    "MODULE_DEFINITION_MISSING": "feature",
    "INVALID_LEGACY_MODULE_ROW": "feature",
    "INVALID_MODULE_DEFINITION": "feature",
    "INCOMPLETE_MODULE_BOUNDARY": "feature",
    "DUPLICATE_MODULE_ID": "feature",
    "MODULE_SELF_DEPENDENCY": "feature",
    "UNDEFINED_MODULE_DEPENDENCY": "feature",
    "UNDEFINED_MODULE_REF": "feature",
    "FEATURE_STORY_MISSING": "feature",
    "STORY_WITHOUT_FEATURE": "feature",
    "INVALID_FEATURE_BRANCH_COUNT": "feature",
    "INVALID_FEATURE_MODULE": "feature",
    "INVALID_FEATURE_STATUS": "feature",
    "INVALID_FEATURE_REVIEW_STATUS": "feature",
    "INVALID_AC_ID": "feature",
    "DUPLICATE_AC_ID": "feature",
    "AC_DESCRIPTION_MISSING": "feature",
    "AC_VERIFICATION_MISSING": "feature",
    "AC_VERIFICATION_ROLE_LEAK": "feature",
    "FEATURE_AC_MISSING": "feature",
    "AC_PAGE_OUTSIDE_FEATURE": "feature",
    "AC_API_OUTSIDE_FEATURE": "feature",
    "AC_EXT_OUTSIDE_FEATURE": "feature",
    "UNDEFINED_FEATURE_REF": "feature",
    "MISSING_FEATURE_DETAIL": "feature",
    "FEATURE_DETAIL_ID": "feature",

    "UNDEFINED_PAGE_REF": "page",
    "PAGE_AC_UNKNOWN_FEATURE": "page",
    "PAGE_AC_UNKNOWN_AC": "page",
    "PAGE_AC_DRIFT": "page",

    "ACTIVE_PAGE_FEATURE_DRIFT": "ui",
    "INVALID_PAGE_STATUS": "ui",
    "MISSING_PAGE_DETAIL": "ui",
    "MISSING_COMP_DETAIL": "ui",
    "PAGE_DETAIL_ID": "ui",
    "COMP_DETAIL_ID": "ui",
    "UNDEFINED_COMP_REF": "ui",

    "UNDEFINED_API_REF": "api",
    "UNDEFINED_EXT_REF": "api",
    "MISSING_API_DETAIL": "api",
    "API_DETAIL_ID": "api",
    "EXT_DETAIL_ID": "api",

    "DELIVERY_SCOPE_VERSION_DRIFT": "review",
    "DELIVERY_SCOPE_FEATURE_TABLE_MISSING": "review",
    "DUPLICATE_SCOPE_FEATURE": "review",
    "SCOPE_UNKNOWN_FEATURE": "review",
    "SCOPE_FEATURE_LIFECYCLE_MISMATCH": "review",
    "INVALID_SCOPE_INCLUSION": "review",
    "INVALID_SCOPE_REVIEW_STATUS": "review",
    "INVALID_SCOPE_REVIEW_CONCLUSION": "review",
    "INVALID_SCOPE_FEATURE_REVIEW": "review",
    "INVALID_SCOPE_BLOCKER_COUNT": "review",
    "INVALID_SCOPE_CONFIRMATION_COUNT": "review",
    "INVALID_DECISION_STATUS": "review",

    "SP_UNKNOWN_FEATURE": "sp",
    "SP_FEATURE_INPUT_DRIFT": "sp",
}


def suggested_routes(issues: list[Issue]) -> list[str]:
    routes = {NEXT_ROUTE.get(issue.code) for issue in issues}
    routes.discard(None)
    return sorted(routes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prd_root", type=Path)
    parser.add_argument(
        "--allow-fixture-status",
        action="store_true",
        help="allow the repository-only fixture page status",
    )
    args = parser.parse_args(argv)
    root = args.prd_root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"PRD root does not exist: {root}")
    issues = validate_project(root, allow_fixture_status=args.allow_fixture_status)
    routes = suggested_routes(issues)
    print("NEXT_STEP_ROUTE: " + (",".join(routes) if routes else "none"))
    if issues:
        print(f"PRD semantic validation failed: {len(issues)} issue(s)", file=sys.stderr)
        for issue in issues:
            print(f"- {issue.format(root)}", file=sys.stderr)
        return 1
    print("PRD semantic validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
