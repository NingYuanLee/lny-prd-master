#!/usr/bin/env python3
"""Run product-agnostic regression checks for the skill runtime."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ROOT = ROOT / "lny-prd" / "modules" / "lny-prd-check" / "scripts"
PROTO_ROOT = ROOT / "lny-prd" / "modules" / "lny-prd-prototype" / "scripts"


def run(command: list[str]) -> None:
    print("+", " ".join(str(part) for part in command))
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="lny-prd-kit-regression-") as temp:
        temp_root = Path(temp)
        html = temp_root / "utf8-check.html"
        html.write_text("<!doctype html><html lang=\"zh-CN\"><meta charset=\"utf-8\"><title>产品页面</title></html>", encoding="utf-8")
        run([sys.executable, str(PROTO_ROOT / "verify-prototype-utf8.py"), str(html)])

        destination = temp_root / "MP"
        run([sys.executable, str(PROTO_ROOT / "copy-kit.py"), str(destination)])
        expected = {
            "icons-extra.js",
            "md-icons.js",
            "mui-kit.css",
            "proto-map.js",
            "proto-page.js",
            "proto-shell.css",
            "proto-shell.js",
        }
        actual = {path.name for path in (destination / "assets").iterdir()}
        if actual != expected:
            raise SystemExit(f"kit copy mismatch: expected {sorted(expected)}, got {sorted(actual)}")

        run([sys.executable, str(CHECK_ROOT / "verify-artifact-paths.py"), str(temp_root)])

    print("LNY PRD Workflow runtime regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
