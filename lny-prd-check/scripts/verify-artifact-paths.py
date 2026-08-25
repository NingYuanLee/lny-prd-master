#!/usr/bin/env python3
"""Report LNY-PRD artifacts written outside their canonical locations."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT_SPECS = {"main_spec.md", "ui_manifest.md", "api_spec.md", "feature_spec.md"}
FORBIDDEN_VERSION_DIRS = {"api", "feature", "ui"}
VERSION_PROTOTYPE_DIR = "prototypes"
LOOSE_DETAIL_RE = re.compile(r"^(?:API-[A-Z]+-\d{3}|EXT-\d{3}|FEATURE-\d{3}|PAGE-[A-Z]+-\d{3}|COMP-\d{3})\.md$")


def issue(code: str, path: Path, root: Path) -> str:
    return f"{code}: {path.relative_to(root).as_posix()}"


def scan(root: Path) -> list[str]:
    errors: list[str] = []
    if (root / "index.html").exists():
        errors.append(issue("ROOT_INDEX", root / "index.html", root))

    versions = root / "versions"
    if not versions.is_dir():
        return errors
    for version in sorted(path for path in versions.iterdir() if path.is_dir()):
        for name in sorted(ROOT_SPECS):
            path = version / name
            if path.exists():
                errors.append(issue("VERSION_SPEC_COPY", path, root))
        for name in sorted(FORBIDDEN_VERSION_DIRS):
            path = version / name
            if path.exists():
                errors.append(issue("VERSION_SPEC_TREE", path, root))
        prototype_tree = version / VERSION_PROTOTYPE_DIR
        if prototype_tree.exists():
            errors.append(issue("VERSION_PROTOTYPE_TREE", prototype_tree, root))
        index = version / "index.html"
        if index.exists():
            errors.append(issue("VERSION_ROOT_INDEX", index, root))
        for path in sorted(version.iterdir()):
            if path.is_file() and LOOSE_DETAIL_RE.fullmatch(path.name):
                errors.append(issue("VERSION_LOOSE_DETAIL", path, root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prd_root", type=Path)
    args = parser.parse_args()
    root = args.prd_root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"PRD root does not exist: {root}")
    errors = scan(root)
    if errors:
        print("artifact path validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("artifact path validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
