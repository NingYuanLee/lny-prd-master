#!/usr/bin/env python3
"""Validate the unified LNY PRD Workflow package without third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "lny-prd"
MODULE_ROOT = SKILL_ROOT / "modules"
EXPECTED_MODULES = {
    "lny-prd-master",
    "lny-prd-discovery",
    "lny-prd-learning",
    "lny-prd-ui",
    "lny-prd-api",
    "lny-prd-feature",
    "lny-prd-page",
    "lny-prd-prototype",
    "lny-prd-check",
    "lny-prd-review",
    "lny-prd-sp",
    "lny-prd-iter",
}
REQUIRED_RUNTIME_FILES = (
    "modules/lny-prd-check/scripts/validate-prd-project.py",
    "modules/lny-prd-check/scripts/verify-artifact-paths.py",
    "modules/lny-prd-check/scripts/audit-fact-consistency.py",
    "modules/lny-prd-check/scripts/audit-decision-walkthrough.py",
    "modules/lny-prd-prototype/scripts/copy-kit.py",
    "modules/lny-prd-prototype/scripts/verify-prototype-utf8.py",
    "modules/lny-prd-prototype/scripts/verify-prototype-coverage.py",
    "modules/lny-prd-prototype/scripts/verify-prototype-browser.mjs",
    "modules/lny-prd-prototype/scripts/validate-visual-review.py",
    "modules/lny-prd-prototype/scripts/validate-feedback-record.py",
)
REQUIRED_REPO_TOOLS = ("scripts/classify-change.py", "scripts/run-regression.py")
PROJECT_ARTIFACTS = {
    "main_spec.md",
    "ui_manifest.md",
    "api_spec.md",
    "feature_spec.md",
}
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PATH_RE = re.compile(r"(?:<skillDir>|\bmodules)/[^\s)`>]+")
LEGACY_PATH_RE = re.compile(
    r"(?<!\.\./)(?<!modules/)(?<!/)`?lny-prd-"
    r"(?:master|ui|api|feature|page|prototype|check|review|sp|iter)/"
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(errors, f"{path}: cannot read: {exc}")
        return ""


def check_bundle(errors: list[str]) -> None:
    path = ROOT / "skill-bundle.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{path}: invalid JSON: {exc}")
        return
    expected = {
        "schema_version": 2,
        "bundle_id": "lny-prd",
        "skills": ["lny-prd"],
        "source_dir": "lny-prd",
        "install_contract": "junction",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(errors, f"{path}: {key} must be {value!r}")
    version = data.get("bundle_version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(errors, f"{path}: bundle_version must use X.Y.Z")


def check_frontmatter(errors: list[str]) -> None:
    path = SKILL_ROOT / "SKILL.md"
    text = read(path, errors)
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(errors, f"{path}: missing or malformed frontmatter")
        return
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("'\"")
    if fields.get("name") != "lny-prd":
        fail(errors, f"{path}: frontmatter name must be lny-prd")
    if not fields.get("description"):
        fail(errors, f"{path}: description must be non-empty")


def check_agent(errors: list[str]) -> None:
    path = SKILL_ROOT / "agents" / "openai.yaml"
    text = read(path, errors)
    for field in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf"^\s+{field}:\s*\".+\"\s*$", text, re.M):
            fail(errors, f"{path}: interface.{field} must be a quoted non-empty value")
    if "$lny-prd" not in text:
        fail(errors, f"{path}: default_prompt must mention $lny-prd")
    if "allow_implicit_invocation: true" not in text:
        fail(errors, f"{path}: implicit invocation must remain enabled")


def check_modules(errors: list[str]) -> None:
    actual = {path.name for path in MODULE_ROOT.iterdir() if path.is_dir()}
    if actual != EXPECTED_MODULES:
        fail(errors, f"{MODULE_ROOT}: modules mismatch, got {sorted(actual)}")
    for name in sorted(EXPECTED_MODULES):
        path = MODULE_ROOT / name / "SKILL.md"
        text = read(path, errors)
        if not text.strip():
            continue
        if "lny-prd-master" not in text and name != "lny-prd-master":
            fail(errors, f"{path}: missing reference to the shared master rules")
    for relative in REQUIRED_RUNTIME_FILES:
        if not (SKILL_ROOT / relative).is_file():
            fail(errors, f"missing required runtime file: {relative}")


def check_markdown_links(errors: list[str]) -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        text = read(path, errors)
        for match in LINK_RE.finditer(text):
            raw = match.group(1).split("#", 1)[0].strip()
            if not raw or re.match(r"^(?:https?://|mailto:)", raw):
                continue
            if Path(raw).name in PROJECT_ARTIFACTS and raw.startswith("./"):
                continue
            target = (path.parent / raw).resolve()
            if not target.exists():
                fail(errors, f"{path}: broken local link {raw}")


def check_declared_scripts(errors: list[str]) -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        text = read(path, errors)
        for match in PATH_RE.finditer(text):
            raw = match.group(0)
            if raw.startswith("<skillDir>"):
                raw = raw.replace("<skillDir>/", "", 1)
                target = SKILL_ROOT / raw
            else:
                target = SKILL_ROOT / raw
            if any(char in raw for char in "…{}"):
                continue
            if ("scripts/" in raw or raw.endswith(".py") or raw.endswith(".mjs")) and not target.exists():
                fail(errors, f"{path}: declared path does not exist {match.group(0)}")


def check_legacy_paths(errors: list[str]) -> None:
    for path in SKILL_ROOT.rglob("*.md"):
        text = read(path, errors)
        if LEGACY_PATH_RE.search(text):
            fail(errors, f"{path}: contains a legacy top-level module path")


def check_regression_runner(errors: list[str]) -> None:
    for relative in REQUIRED_REPO_TOOLS:
        path = ROOT / relative
        if not path.is_file():
            fail(errors, f"missing repository tool: {path}")


def main() -> int:
    errors: list[str] = []
    for check in (
        check_bundle,
        check_frontmatter,
        check_agent,
        check_modules,
        check_markdown_links,
        check_declared_scripts,
        check_legacy_paths,
        check_regression_runner,
    ):
        check(errors)
    if errors:
        print("LNY PRD Workflow package validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("LNY PRD Workflow package validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
