# -*- coding: utf-8 -*-
"""Validate prototype HTML files are UTF-8, have charset/lang, and lack mojibake."""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPLACEMENT = "\ufffd"
MOJIBAKE_MARKERS = ("??", "锟", "烫烫烫")


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"{path}: invalid UTF-8 ({exc})"]

    if REPLACEMENT in text:
        errors.append(f"{path}: contains U+FFFD replacement character")

    lower = text.lower()
    if path.suffix.lower() in {".html", ".htm"}:
        if "charset" not in lower:
            errors.append(f"{path}: missing charset declaration")
        if not re.search(r"<html[^>]*\blang\s*=", text, flags=re.I):
            errors.append(f"{path}: missing html lang attribute")

    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            errors.append(f"{path}: possible mojibake marker {marker!r}")
            break

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: verify-prototype-utf8.py <file> [file ...]",
            file=sys.stderr,
        )
        return 1

    all_errors: list[str] = []
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            all_errors.append(f"{path}: file not found")
            continue
        all_errors.extend(check_file(path))

    if all_errors:
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
