# -*- coding: utf-8 -*-
"""Copy kit CSS/JS into prototypes/{terminal}/assets/."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

KIT_FILES = (
    "mui-kit.css",
    "proto-shell.css",
    "proto-shell.js",
    "proto-page.js",
    "proto-map.js",
    "md-icons.js",
)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: copy-kit.py <prdRoot>/prototypes/{TERM} [...more dests]")
        print("       also: copy-kit.py <skillDir>/gold   # preview assets for gold HTML")
        return 2
    kit_dir = Path(__file__).resolve().parents[1] / "kit"
    missing = [n for n in KIT_FILES if not (kit_dir / n).is_file()]
    if missing:
        print("missing kit files: " + ", ".join(missing), file=sys.stderr)
        return 1
    for dest_root in sys.argv[1:]:
        assets = Path(dest_root).resolve() / "assets"
        assets.mkdir(parents=True, exist_ok=True)
        for name in KIT_FILES:
            shutil.copy2(kit_dir / name, assets / name)
        extra = assets / "icons-extra.js"
        if not extra.is_file():
            extra.write_text(
                "/* project icon extras; written by search-icons.py */\n",
                encoding="utf-8",
                newline="\n",
            )
        print("copied " + str(len(KIT_FILES)) + " kit files -> " + str(assets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
