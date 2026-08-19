# -*- coding: utf-8 -*-
"""Align mini-shop MP fixtures and gold mobile headers with sheet DOM rules."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLD_DIR = ROOT / "lny-prd-prototype" / "gold"
KIT_SCRIPT = ROOT / "lny-prd-prototype" / "scripts" / "copy-kit.py"
MP_DIR = ROOT / "examples" / "mini-shop" / "prototypes" / "MP"
VER_DIR = ROOT / "examples" / "mini-shop" / "versions" / "v1.0.0" / "prototypes" / "MP"
AD_DIR = ROOT / "examples" / "mini-shop" / "prototypes" / "AD"
AD_VER_DIR = ROOT / "examples" / "mini-shop" / "versions" / "v1.0.0" / "prototypes" / "AD"

GOLD_DOM = {
    "mobile-grid.html": "DOM：md-hero 与 body 并列；body > md-mobile-sheet（默认 safe-x）。",
    "mobile-list.html": "DOM：md-list-toolbar 在 body 外；body > md-mobile-sheet（默认 safe-x）。",
    "mobile-detail.html": "DOM：body > md-mobile-sheet--flush-x + md-detail-content。",
    "mobile-fields.html": "DOM：body > md-mobile-sheet（默认 safe-x）+ md-group-list。",
    "mobile-form.html": "DOM：body > md-mobile-sheet（md-form-page 自动 lr0）。",
    "mobile-wizard.html": "DOM：body > md-mobile-sheet（md-form-page 自动 lr0）。",
    "mobile-settings.html": "DOM：body > md-mobile-sheet（md-set-page 自动 lr0）。",
    "mobile-buttons.html": "DOM：body > md-mobile-sheet（默认 safe-x）。",
    "mobile-timeline.html": "DOM：body > md-mobile-sheet（默认 safe-x）。",
    "mobile-menu.html": "DOM：body > md-mobile-sheet（md-set-page 自动 lr0）。",
    "mobile-tree.html": "DOM：body > md-mobile-sheet--flush-x（全幅 split）。",
    "mobile-locator.html": "DOM：body > md-mobile-sheet--flush-x（全幅 split）。",
    "mobile-order-list.html": "DOM：md-list-toolbar 在 body 外；body > md-mobile-sheet（默认 safe-x）。",
    "mobile-pod.html": "DOM：md-hero 与 body 并列；body > md-mobile-sheet（默认 safe-x）；md-pod 在页根。",
}

PAGE_TO_GOLD = {
    "PAGE-MP-001.html": "mobile-grid.html",
    "PAGE-MP-002.html": "mobile-list.html",
    "PAGE-MP-003.html": "mobile-detail.html",
    "PAGE-MP-004.html": "mobile-form.html",
    "PAGE-MP-005.html": "mobile-wizard.html",
    "PAGE-MP-006.html": "mobile-settings.html",
    "PAGE-MP-007.html": "mobile-buttons.html",
    "PAGE-MP-008.html": "mobile-tree.html",
    "PAGE-MP-009.html": "mobile-timeline.html",
    "PAGE-MP-010.html": "mobile-menu.html",
    "PAGE-MP-011.html": "mobile-pod.html",
    "PAGE-MP-012.html": "mobile-fields.html",
    "PAGE-MP-013.html": "mobile-locator.html",
    "PAGE-MP-014.html": "mobile-order-list.html",
}

FIXTURE_INTRO = {
    "PAGE-MP-001.html": "夹具：对标 mobile-grid.html。",
    "PAGE-MP-002.html": "夹具：对标 mobile-list.html。",
    "PAGE-MP-003.html": "夹具：对标 mobile-detail.html。",
    "PAGE-MP-004.html": "夹具：对标 mobile-form.html。",
    "PAGE-MP-005.html": "夹具：对标 mobile-wizard.html。",
    "PAGE-MP-006.html": "夹具：对标 mobile-settings.html。",
    "PAGE-MP-007.html": "夹具：对标 mobile-buttons.html。",
    "PAGE-MP-008.html": "夹具：对标 mobile-tree.html。商品·分类树；左多级树右图文介绍。禁止当横卡列表、禁止当定位导航。",
    "PAGE-MP-009.html": "夹具：对标 mobile-timeline.html。订单·物流时间轴；节点按时间倒序。",
    "PAGE-MP-010.html": "夹具：对标 mobile-menu.html。",
    "PAGE-MP-011.html": "夹具：对标 mobile-pod.html。",
    "PAGE-MP-012.html": "夹具：对标 mobile-fields.html。商品·字段列表；单商品多维度按组。禁止当图文、禁止当表单。",
    "PAGE-MP-013.html": "夹具：对标 mobile-locator.html。商品·分类导航；左一级分组右分组横卡，滚动联动。禁止当树。",
    "PAGE-MP-014.html": "夹具：对标 mobile-order-list.html。订单·订单列表。",
}


def normalize_comment_spacing(text: str) -> str:
    return re.sub(r"<!--\s{2,}", "<!-- ", text)


def patch_gold_headers() -> None:
    for fname, dom in GOLD_DOM.items():
        path = GOLD_DIR / fname
        text = normalize_comment_spacing(path.read_text(encoding="utf-8"))
        # strip any existing DOM suffix then re-append
        text = re.sub(r"\s*DOM：[^。]+。", "", text, count=0)
        match = re.match(r"(<!-- LNY-PRD gold: .*? -->)", text, re.S)
        if not match:
            print("SKIP no comment", fname)
            continue
        old = match.group(1)
        inner = old[4:-3].strip()
        if not inner.endswith("。"):
            inner += "。"
        new = f"<!-- {inner} {dom} -->"
        path.write_text(normalize_comment_spacing(text.replace(old, new, 1)), encoding="utf-8", newline="\n")
        print("gold", fname)


def fix_split_flush_x(directory: Path) -> None:
    for page in ("PAGE-MP-008.html", "PAGE-MP-013.html"):
        path = directory / page
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        needle = '<div class="md-mobile-sheet">'
        repl = '<div class="md-mobile-sheet md-mobile-sheet--flush-x">'
        if needle in text and repl not in text:
            path.write_text(text.replace(needle, repl, 1), encoding="utf-8", newline="\n")
            print("flush-x", path)


def patch_fixture_comments() -> None:
    for page, gold_file in PAGE_TO_GOLD.items():
        path = MP_DIR / page
        if not path.exists():
            continue
        intro = FIXTURE_INTRO[page]
        dom = GOLD_DOM[gold_file]
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"<!-- .*? -->", f"<!-- LNY-PRD gold: {intro} {dom} -->", text, count=1, flags=re.S)
        path.write_text(normalize_comment_spacing(text), encoding="utf-8", newline="\n")
        print("fixture", page)


def mirror_mp_to_version() -> None:
    VER_DIR.mkdir(parents=True, exist_ok=True)
    for src in sorted(MP_DIR.glob("PAGE-MP-*.html")):
        dst = VER_DIR / src.name
        dst.write_bytes(src.read_bytes())
        print("mirror", src.name)


def copy_kit_to_fixtures() -> None:
    import subprocess
    import sys

    targets = [MP_DIR, VER_DIR, AD_DIR, AD_VER_DIR, GOLD_DIR]
    for target in targets:
        if not target.exists():
            continue
        subprocess.run(
            [sys.executable, str(KIT_SCRIPT), str(target)],
            check=True,
            cwd=str(ROOT),
        )
        print("copy-kit", target.relative_to(ROOT))


def main() -> None:
    copy_kit_to_fixtures()
    patch_gold_headers()
    fix_split_flush_x(MP_DIR)
    patch_fixture_comments()
    mirror_mp_to_version()
    fix_split_flush_x(VER_DIR)


if __name__ == "__main__":
    main()
