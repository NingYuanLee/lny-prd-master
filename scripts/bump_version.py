#!/usr/bin/env python3
"""Bump the LNY-PRD bundle version across all synchronized locations.

skill-bundle.json is the source of truth; this script keeps it aligned with
the README version marker and prepends a CHANGELOG.md section, so a version
release is one command instead of three hand edits.

Usage:
    python scripts/bump_version.py 2.15.0
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
README_MARKER_RE = re.compile(r"\*\*工具包版本：[^*]+\*\*")


def semver_tuple(value: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in value.split("."))  # type: ignore[return-value]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not SEMVER_RE.fullmatch(argv[1]):
        print("Usage: python scripts/bump_version.py <X.Y.Z>", file=sys.stderr)
        return 2
    version = argv[1]

    bundle_path = ROOT / "skill-bundle.json"
    manifest = json.loads(bundle_path.read_text(encoding="utf-8"))
    current = manifest.get("bundle_version")
    if not isinstance(current, str) or not SEMVER_RE.fullmatch(current):
        print(f"skill-bundle.json has invalid bundle_version: {current!r}", file=sys.stderr)
        return 1
    if version == current:
        print(f"already at {version}; nothing to do", file=sys.stderr)
        return 1
    if semver_tuple(version) <= semver_tuple(current):
        print(f"refusing to bump {current} -> {version}: new version must be larger", file=sys.stderr)
        return 1

    manifest["bundle_version"] = version
    bundle_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    marker = README_MARKER_RE.search(readme)
    if marker is None:
        print("README.md version marker '**工具包版本：…**' missing", file=sys.stderr)
        return 1
    readme_path.write_text(readme.replace(marker.group(0), f"**工具包版本：{version}**", 1), encoding="utf-8")

    changelog_path = ROOT / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    section = f"## {version} - {datetime.date.today().isoformat()}\n\n- （待补充：本版本变更摘要）\n"
    insert_at = -1
    for heading in re.finditer(r"\n## [^\n]*", changelog):
        if re.match(r"## \d+\.\d+\.\d+\b", heading.group(0)[1:]):
            insert_at = heading.start()
            break
    if insert_at == -1:
        changelog = changelog.rstrip("\n") + "\n\n" + section
    else:
        changelog = changelog[: insert_at + 1] + section + "\n" + changelog[insert_at + 1 :]
    changelog_path.write_text(changelog, encoding="utf-8")

    print(f"bumped {current} -> {version}: skill-bundle.json, README.md, CHANGELOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
