# -*- coding: utf-8 -*-
"""对照 pages_prd 验收原型 PAGE：跳转、COMP、套件类名、禁止裸控件。"""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE_RE = re.compile(r"PAGE-[A-Z]+-\d+")
COMP_RE = re.compile(r"COMP-\d+")
QUOTE_RE = re.compile(r"「([^」]+)」")
STYLE_THEME_RE = re.compile(
    r"\b(background|color|font|border(-color|-radius)?)\s*:",
    re.I,
)
SKIP_QUOTES = {"无", "是", "否"}


def terminal_of(page_id: str) -> str:
    parts = page_id.split("-")
    return parts[1] if len(parts) >= 3 else ""


def find_pages_prd(prd_root: Path, version: str, page_id: str) -> Path | None:
    base = prd_root / "versions" / version / "pages_prd"
    if not base.is_dir():
        return None
    matches = list(base.rglob(page_id + ".md"))
    return matches[0] if matches else None


def html_paths(prd_root: Path, version: str, page_id: str) -> list[Path]:
    term = terminal_of(page_id)
    paths = [prd_root / "prototypes" / term / (page_id + ".html")]
    mirror_root = prd_root / "versions" / version / "prototypes"
    if mirror_root.is_dir():
        paths.append(mirror_root / term / (page_id + ".html"))
    return paths


def parse_prd(text: str) -> tuple[set[str], set[str], list[str]]:
    sec3 = ""
    sec4 = ""
    m3 = re.search(r"^## 3\..*$", text, flags=re.M)
    m4 = re.search(r"^## 4\..*$", text, flags=re.M)
    m5 = re.search(r"^## 5\..*$", text, flags=re.M)
    if m3 and m4:
        sec3 = text[m3.start() : m4.start()]
    elif m3:
        sec3 = text[m3.start() :]
    if m4 and m5:
        sec4 = text[m4.start() : m5.start()]
    elif m4:
        sec4 = text[m4.start() :]

    comps = set(COMP_RE.findall(sec3 + sec4))
    jumps: set[str] = set()
    for pid in PAGE_RE.findall(sec4):
        if pid:
            jumps.add(pid)
    quotes: list[str] = []
    for q in QUOTE_RE.findall(sec3):
        q = q.strip()
        if q and q not in SKIP_QUOTES and q not in quotes:
            quotes.append(q)
    return comps, jumps, quotes


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[set[str]] = []
        self.errors: list[str] = []
        self.text_parts: list[str] = []
        self.has_kit_css = False
        self.scripts: set[str] = set()
        self.hrefs: set[str] = set()
        self.comps: set[str] = set()
        self.empty_for: set[str] = set()
        self.in_style = False
        self.in_thead = 0
        self.is_mobile = False
        self.is_desktop = False
        self.has_status_bar = False
        self.has_section_head = False
        self.has_page_head = False
        self.card_count = 0
        self.table_rows = 0
        self.bare_media = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        classes = set((ad.get("class") or "").split())
        self.stack.append(classes)
        if "md-mobile-page" in classes:
            self.is_mobile = True
        if "md-d1" in classes:
            self.is_desktop = True
        if "md-status-bar" in classes:
            self.has_status_bar = True
        if "md-section-head" in classes:
            self.has_section_head = True
        if "md-page-head" in classes:
            self.has_page_head = True
        if "md-card" in classes:
            self.card_count += 1
        if "md-media-ph" in classes:
            if not any(re.match(r"md-media-ph--\d+", c) for c in classes):
                self.bare_media += 1
        if tag == "thead":
            self.in_thead += 1
        if tag == "tr" and self.in_thead == 0:
            self.table_rows += 1
        if tag == "style":
            self.in_style = True
            self.errors.append("page <style> is forbidden; use kit classes")
        if tag == "link" and "mui-kit.css" in ad.get("href", ""):
            self.has_kit_css = True
        if tag == "script":
            src = ad.get("src", "")
            if src:
                self.scripts.add(Path(src).name)
        if tag == "a" and ad.get("href"):
            self.hrefs.add(ad["href"])
        comp = ad.get("data-comp")
        if comp:
            self.comps.add(comp)
        empty_for = ad.get("data-empty-for")
        if empty_for:
            self.empty_for.add(empty_for)
        style = ad.get("style") or ""
        if style and STYLE_THEME_RE.search(style):
            self.errors.append("inline theme style: " + style[:80])
        if tag == "button":
            allowed = any(c.startswith("md-") or c.startswith("proto-") for c in classes)
            in_toggle = any("md-toggle" in prev for prev in self.stack[:-1])
            if not allowed and not in_toggle:
                self.errors.append("naked <button> without md-* class")
        if tag in {"input", "select", "textarea"}:
            if ad.get("type") == "hidden":
                return
            in_field = any(
                {
                    "md-field",
                    "md-check",
                    "md-radio",
                    "md-switch",
                    "md-upload",
                }
                & prev
                for prev in self.stack
            )
            self_ok = any(c.startswith("md-") for c in classes)
            if not in_field and not self_ok:
                self.errors.append("naked <" + tag + "> without md-field / md-*")
        if tag == "table" and "md-table" not in classes:
            self.errors.append("<table> without md-table")

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False
        if tag == "thead" and self.in_thead:
            self.in_thead -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if not self.in_style:
            self.text_parts.append(data)


def check_html(path: Path, page_id: str, comps: set[str], jumps: set[str], quotes: list[str]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [str(path) + ": file not found"]
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [str(path) + ": invalid UTF-8 (" + str(exc) + ")"]

    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:  # noqa: BLE001
        return [str(path) + ": HTML parse error (" + str(exc) + ")"]
    errors.extend(str(path) + ": " + e for e in parser.errors)
    if not parser.has_kit_css:
        errors.append(str(path) + ": missing assets/mui-kit.css")
    for name in ("md-icons.js", "icons-extra.js", "proto-page.js"):
        if name not in parser.scripts:
            errors.append(str(path) + ": missing script " + name)
    assets = path.parent / "assets"
    for name in ("mui-kit.css", "md-icons.js", "icons-extra.js", "proto-page.js"):
        if not (assets / name).is_file():
            errors.append(str(path) + ": assets/" + name + " not on disk")
    visible = "".join(parser.text_parts)
    for comp in sorted(comps):
        if comp not in parser.comps:
            errors.append(str(path) + ": missing data-comp=" + comp)
        if comp not in parser.empty_for:
            errors.append(str(path) + ": missing data-empty-for=" + comp)
    for jump in sorted(jumps):
        if jump == page_id:
            continue
        needle = jump + ".html"
        if not any(needle in href for href in parser.hrefs):
            errors.append(str(path) + ": missing href to " + needle)
    for q in quotes:
        if q not in visible and q not in text:
            errors.append(str(path) + ": missing quoted label 「" + q + "」")
    low_fi = re.search(
        r"示例商品|示例用户|测试数据|商品\s*[AB]|Item\s*\d|lorem ipsum|\bxxx\b",
        visible,
        flags=re.I,
    )
    if low_fi:
        errors.append(str(path) + ": low-fidelity fixture " + low_fi.group(0))
    if parser.bare_media:
        errors.append(str(path) + ": md-media-ph without --1..--6 variant")
    if parser.card_count and parser.card_count < 4:
        errors.append(str(path) + ": need ≥4 cards in default state (got " + str(parser.card_count) + ")")
    if parser.table_rows and parser.table_rows < 4:
        errors.append(str(path) + ": need ≥4 table rows (got " + str(parser.table_rows) + ")")
    if parser.is_mobile and not parser.has_status_bar:
        errors.append(str(path) + ": mobile page missing md-status-bar")
    if parser.is_mobile and not parser.has_section_head:
        errors.append(str(path) + ": mobile page missing md-section-head")
    if parser.is_desktop and not parser.has_page_head:
        errors.append(str(path) + ": desktop page missing md-page-head")
    return errors


def resolve_version(prd_root: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    versions = prd_root / "versions"
    if not versions.is_dir():
        raise SystemExit("versions/ not found: " + str(prd_root))
    names = sorted(
        (p.name for p in versions.iterdir() if p.is_dir() and p.name.startswith("v")),
        key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"[^\d]+", s) if x],
    )
    if not names:
        raise SystemExit("no version directory under " + str(versions))
    return names[-1]


def list_pages(prd_root: Path) -> list[str]:
    proto = prd_root / "prototypes"
    found: list[str] = []
    if proto.is_dir():
        for p in proto.rglob("PAGE-*.html"):
            found.append(p.stem)
    return sorted(set(found))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prd_root")
    parser.add_argument("--version", default=None)
    parser.add_argument("--page", action="append", default=[])
    args = parser.parse_args(argv[1:])
    prd_root = Path(args.prd_root).resolve()
    version = resolve_version(prd_root, args.version)
    pages = args.page or list_pages(prd_root)
    if not pages:
        print("no PAGE-*.html under prototypes/", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    ui_direct = False
    notes = prd_root / "versions" / version
    for marker in notes.glob("*.md"):
        try:
            if "ui直出" in marker.read_text(encoding="utf-8"):
                ui_direct = True
                break
        except OSError:
            continue

    for page_id in pages:
        prd = find_pages_prd(prd_root, version, page_id)
        comps: set[str] = set()
        jumps: set[str] = set()
        quotes: list[str] = []
        if prd is None:
            if not ui_direct:
                all_errors.append(page_id + ": pages_prd missing (not ui直出)")
        else:
            text = prd.read_text(encoding="utf-8")
            comps, jumps, quotes = parse_prd(text)
            jumps.discard("无")
        for html in html_paths(prd_root, version, page_id):
            all_errors.extend(check_html(html, page_id, comps, jumps, quotes))

    if all_errors:
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1
    print("coverage ok: " + str(len(pages)) + " page(s), version " + version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
