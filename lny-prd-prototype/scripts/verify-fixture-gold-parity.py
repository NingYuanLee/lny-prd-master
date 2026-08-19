# -*- coding: utf-8 -*-
"""Check mini-shop MP/AD fixture files exist and map to gold HTML on disk."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = ROOT / "lny-prd-prototype" / "gold"
MP_DIR = ROOT / "examples" / "mini-shop" / "prototypes" / "MP"
AD_DIR = ROOT / "examples" / "mini-shop" / "prototypes" / "AD"

MP_PAGE_TO_GOLD = {
    f"PAGE-MP-{i:03d}.html": gold
    for i, gold in [
        (1, "mobile-grid.html"),
        (2, "mobile-list.html"),
        (3, "mobile-detail.html"),
        (4, "mobile-form.html"),
        (5, "mobile-wizard.html"),
        (6, "mobile-settings.html"),
        (7, "mobile-buttons.html"),
        (8, "mobile-tree.html"),
        (9, "mobile-timeline.html"),
        (10, "mobile-menu.html"),
        (11, "mobile-pod.html"),
        (12, "mobile-fields.html"),
        (13, "mobile-locator.html"),
        (14, "mobile-order-list.html"),
    ]
}

AD_PAGE_TO_GOLD = {
    f"PAGE-AD-{i:03d}.html": gold
    for i, gold in [
        (1, "desktop-lists.html"),
        (2, "desktop-form.html"),
        (3, "desktop-wizard.html"),
        (4, "desktop-dashboard.html"),
        (5, "desktop-split.html"),
        (6, "desktop-settings.html"),
        (7, "desktop-timeline.html"),
        (8, "desktop-detail.html"),
        (9, "desktop-form.html"),
        (10, "desktop-menu.html"),
        (11, "desktop-pod.html"),
        (12, "desktop-fields.html"),
        (13, "desktop-locator.html"),
        (14, "desktop-layout.html"),
    ]
}

KIT_ASSETS = (
    "mui-kit.css",
    "proto-shell.css",
    "proto-page.js",
    "md-icons.js",
    "icons-extra.js",
)


def check_terminal(label: str, proto_dir: Path, mapping: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for page, gold in mapping.items():
        fixture = proto_dir / page
        gold_path = GOLD_DIR / gold
        if not fixture.is_file():
            errors.append(f"{label}: missing fixture {page}")
        if not gold_path.is_file():
            errors.append(f"{label}: missing gold {gold} (for {page})")
        assets = proto_dir / "assets"
        for name in KIT_ASSETS:
            if not (assets / name).is_file():
                errors.append(f"{label}: missing assets/{name} under {proto_dir.name}")
                break
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(check_terminal("MP", MP_DIR, MP_PAGE_TO_GOLD))
    errors.extend(check_terminal("AD", AD_DIR, AD_PAGE_TO_GOLD))
    mp_count = len(list(MP_DIR.glob("PAGE-MP-*.html")))
    ad_count = len(list(AD_DIR.glob("PAGE-AD-*.html")))
    if mp_count != len(MP_PAGE_TO_GOLD):
        errors.append(f"MP: expected {len(MP_PAGE_TO_GOLD)} fixtures, got {mp_count}")
    if ad_count != len(AD_PAGE_TO_GOLD):
        errors.append(f"AD: expected {len(AD_PAGE_TO_GOLD)} fixtures, got {ad_count}")
    gold_mobile = len(list(GOLD_DIR.glob("mobile-*.html")))
    gold_desktop = len(list(GOLD_DIR.glob("desktop-*.html")))
    if gold_mobile < 14:
        errors.append(f"gold: expected ≥14 mobile-*.html, got {gold_mobile}")
    if gold_desktop < 14:
        errors.append(f"gold: expected ≥14 desktop-*.html, got {gold_desktop}")
    if errors:
        for line in errors:
            print(line, file=sys.stderr)
        return 1
    print(
        f"parity ok: MP×{mp_count} AD×{ad_count} gold mobile×{gold_mobile} desktop×{gold_desktop}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
