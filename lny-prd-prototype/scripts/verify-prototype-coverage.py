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
FENCED_BLOCK_RE = re.compile(
    r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$",
    re.M | re.S,
)
STYLE_THEME_RE = re.compile(
    r"\b(background|color|font|border(-color|-radius)?)\s*:",
    re.I,
)
SKIP_QUOTES = {"无", "是", "否"}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
CARD_DENSITY_CONTEXT_CLASSES = {"md-grid-2", "md-list-toolbar", "md-timeline"}
LIST_MODULE_CLASSES = {
    "md-card--cover",
    "md-card--tile",
    "md-card--row",
    "md-card--order",
    "md-grid-2",
    "md-comment-list",
    "md-group-list",
}
FUNC_AREA_CLASSES = {"md-king", "md-svc-strip", "md-set-pair", "md-set-group"}
MOBILE_SECTION_HEAD_OPTIONAL_CLASSES = {
    "md-card--order",
    "md-chapter-list",
    "md-form-page",
    "md-group-list",
    "md-set-page",
    "md-tree-page",
}
MOBILE_LIST_CARD_CLASSES = {"md-card--order", "md-card--row"}


def terminal_of(page_id: str) -> str:
    parts = page_id.split("-")
    return parts[1] if len(parts) >= 3 else ""


def find_pages_prd(prd_root: Path, version: str, page_id: str) -> Path | None:
    base = prd_root / "versions" / version / "pages_prd"
    if not base.is_dir():
        return None
    matches = list(base.rglob(page_id + ".md"))
    return matches[0] if matches else None


def html_path(prd_root: Path, page_id: str) -> Path:
    term = terminal_of(page_id)
    return prd_root / "prototypes" / term / (page_id + ".html")


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
    # ASCII wireframes describe layout and may use illustrative copy. Only prose/table
    # requirements are label contracts for the prototype coverage check.
    label_contract = FENCED_BLOCK_RE.sub("", sec3)
    for q in QUOTE_RE.findall(label_contract):
        q = q.strip()
        if q and q not in SKIP_QUOTES and q not in quotes:
            quotes.append(q)
    return comps, jumps, quotes


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, set[str]]] = []
        self.errors: list[str] = []
        self.text_parts: list[str] = []
        self.has_kit_css = False
        self.scripts: set[str] = set()
        self.hrefs: set[str] = set()
        self.comps: set[str] = set()
        self.empty_for: set[str] = set()
        self.in_style = False
        self.in_thead = 0
        self.in_data_table = 0
        self.is_mobile = False
        self.is_desktop = False
        self.has_status_bar = False
        self.has_section_head = False
        self.has_breadcrumb = False
        self.has_tabbar = False
        self.has_mobile_appbar = False
        self.has_center_appbar = False
        self.card_count = 0
        self.unsupported_list_card_count = 0
        self.table_rows = 0
        self.bare_media = 0
        self.has_card_density_context = False
        self.has_dense_data_table = False
        self.has_list_toolbar = False
        self.has_list_module = False
        self.has_func_area = False
        self.classes_seen: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        classes = set((ad.get("class") or "").split())
        self.classes_seen.update(classes)
        ancestors = [item_classes for _, item_classes in self.stack]
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, classes))
        if classes & CARD_DENSITY_CONTEXT_CLASSES:
            self.has_card_density_context = True
        if "md-d1--list" in classes or "md-d1__list" in classes:
            self.has_dense_data_table = True
        if "md-list-toolbar" in classes:
            self.has_list_toolbar = True
        if classes & LIST_MODULE_CLASSES:
            self.has_list_module = True
        if classes & FUNC_AREA_CLASSES:
            self.has_func_area = True
        if "md-mobile-page" in classes:
            self.is_mobile = True
        if "md-d1" in classes:
            self.is_desktop = True
        if "md-status-bar" in classes:
            self.has_status_bar = True
        if "md-section-head" in classes:
            self.has_section_head = True
        if "md-breadcrumb" in classes:
            self.has_breadcrumb = True
        if "md-tabbar" in classes:
            self.has_tabbar = True
        if "md-appbar--center" in classes:
            self.has_center_appbar = True
        if "md-appbar--mobile" in classes or (
            tag in {"header"} and "md-appbar" in classes
        ):
            self.has_mobile_appbar = True
        if "md-card" in classes:
            self.card_count += 1
            if not classes & MOBILE_LIST_CARD_CLASSES:
                self.unsupported_list_card_count += 1
        if "md-media-ph" in classes:
            if not any(re.match(r"md-media-ph--\d+", c) for c in classes):
                self.bare_media += 1
        if tag == "table":
            if "md-table" in classes:
                self.in_data_table += 1
            elif "md-article__table" not in classes:
                self.errors.append(
                    "<table> without md-table or md-article__table"
                )
        if tag == "thead":
            self.in_thead += 1
        if tag == "tr" and self.in_data_table and self.in_thead == 0:
            self.table_rows += 1
        if tag == "style":
            self.in_style = True
            self.errors.append("page <style> is forbidden; use kit classes")
        if tag == "link" and "mui-kit.css" in ad.get("href", ""):
            self.has_kit_css = True
        if tag == "script":
            src = ad.get("src", "")
            if src:
                self.scripts.add(Path(re.split(r"[?#]", src, maxsplit=1)[0]).name)
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
            in_toggle = any("md-toggle" in prev for prev in ancestors)
            if not allowed and not in_toggle:
                self.errors.append(
                    "naked <button> without md-* class at "
                    + str(self.getpos())
                    + " (browser chrome; use md-btn / md-icon-btn / md-tab)"
                )
        if tag in {"input", "select", "textarea"}:
            if ad.get("type") == "hidden":
                return
            in_field = any(
                {
                    "md-field",
                    "md-check",
                    "md-radio",
                    "md-set-pick",
                    "md-slider",
                    "md-switch",
                    "md-upload",
                    "md-upload-grid__add",
                    "md-combo",
                }
                & prev
                for prev in ancestors
            )
            self_ok = any(c.startswith("md-") for c in classes)
            if not in_field and not self_ok:
                self.errors.append(
                    "naked <"
                    + tag
                    + "> without md-field / md-* at "
                    + str(self.getpos())
                )
    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self.in_style = False
        if tag == "thead" and self.in_thead:
            self.in_thead -= 1
        if tag == "table" and self.in_data_table:
            self.in_data_table -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.in_style:
            self.text_parts.append(data)


def check_html(
    path: Path,
    page_id: str,
    comps: set[str],
    jumps: set[str],
    quotes: list[str],
    *,
    fixture: bool = False,
) -> list[str]:
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
    errors.extend(check_density(path, parser))
    if parser.is_mobile and "proto-page.js" not in parser.scripts:
        errors.append(str(path) + ": mobile page missing proto-page.js (injects fixed status bar)")
    if mobile_section_head_required(parser) and not parser.has_section_head:
        errors.append(str(path) + ": mobile page missing md-section-head")
    if parser.is_desktop and not parser.has_breadcrumb:
        errors.append(str(path) + ": desktop page missing md-breadcrumb")
    errors.extend(check_visual_floor(path, page_id, text, parser, fixture=fixture))
    return errors


BOX_DRAW_RE = re.compile(r"[┌┐└┘├┤┬┴┼│─]|[+][-]{2,}")
NATIVE_DATE_RE = re.compile(r"""type\s*=\s*["']date["']""", re.I)


def check_density(path: Path, parser: PageParser) -> list[str]:
    """Enforce repeated-content density only for explicit list/grid contexts."""
    errors: list[str] = []
    if parser.has_card_density_context and 0 < parser.card_count < 4:
        errors.append(
            str(path)
            + ": need ≥4 cards in list/grid default state (got "
            + str(parser.card_count)
            + ")"
        )
    if parser.has_dense_data_table and 0 < parser.table_rows < 4:
        errors.append(
            str(path)
            + ": need ≥4 table rows in D1-1 default state (got "
            + str(parser.table_rows)
            + ")"
        )
    return errors


def mobile_section_head_required(parser: PageParser) -> bool:
    """Require section headings only on page types where they carry structure."""
    if not parser.is_mobile:
        return False
    if parser.classes_seen & MOBILE_SECTION_HEAD_OPTIONAL_CLASSES:
        return False
    if parser.has_func_area and not parser.has_list_module:
        return False
    return True


DIALOG_ID_RE = re.compile(
    r'<div\b[^>]*\bid="([^"]+)"[^>]*\bclass="[^"]*\bmd-dialog\b',
    re.I,
)


def check_dialog_backdrop(path: Path, text: str) -> list[str]:
    """D5 dialog must pair md-backdrop to block click-through."""
    errors: list[str] = []
    prefix = str(path) + ": "
    for m in DIALOG_ID_RE.finditer(text):
        dlg_id = m.group(1)
        if dlg_id == "mdConfirmDlg":
            continue
        backdrop_id = dlg_id + "Backdrop"
        if not re.search(
            r'<div\b[^>]*\bid="' + re.escape(backdrop_id) + r'"[^>]*\bclass="[^"]*\bmd-backdrop\b',
            text,
            re.I,
        ):
            errors.append(
                prefix
                + "md-dialog #"
                + dlg_id
                + " missing md-backdrop #"
                + backdrop_id
                + " (semi-transparent mask blocks click-through)"
            )
    return errors


DRAWER_ID_RE = re.compile(
    r'<(?:aside|div)\b[^>]*\bid="([^"]+)"[^>]*\bclass="[^"]*\bmd-drawer\b',
    re.I,
)


def check_drawer_backdrop(path: Path, text: str) -> list[str]:
    """Drawer/sheet must pair md-backdrop to block click-through."""
    errors: list[str] = []
    prefix = str(path) + ": "
    for m in DRAWER_ID_RE.finditer(text):
        drawer_id = m.group(1)
        backdrop_id = drawer_id + "Backdrop"
        if not re.search(
            r'<div\b[^>]*\bid="' + re.escape(backdrop_id) + r'"[^>]*\bclass="[^"]*\bmd-backdrop\b',
            text,
            re.I,
        ):
            errors.append(
                prefix
                + "md-drawer #"
                + drawer_id
                + " missing md-backdrop #"
                + backdrop_id
                + " (semi-transparent mask blocks click-through)"
            )
    return errors


DIALOG_TAG_RE = re.compile(
    r"<div\b[^>]*\bclass=\"[^\"]*\bmd-dialog\b[^\"]*\"[^>]*>",
    re.I,
)
DIALOG_SURFACE_STRIP_RE = re.compile(
    r"border-radius\s*:\s*0|box-shadow\s*:\s*none",
    re.I,
)


def check_dialog_surface(path: Path, text: str) -> list[str]:
    """D5 dialog panel must keep kit rounded surface + unified elevation."""
    errors: list[str] = []
    prefix = str(path) + ": "
    for tag in DIALOG_TAG_RE.findall(text):
        if "style=" in tag and DIALOG_SURFACE_STRIP_RE.search(tag):
            errors.append(
                prefix
                + "md-dialog must not strip border-radius/box-shadow via inline style; use md-dialog class"
            )
    return errors


def check_wizard_nav(
    path: Path, page_id: str, text: str, *, fixture: bool = False
) -> list[str]:
    """PT-STATE-FLOW: one wizard nav type per business page; no gold tab-demo on business pages."""
    errors: list[str] = []
    prefix = str(path) + ": "
    demo = fixture

    if "data-wizard-panel" in text and not demo:
        errors.append(
            prefix
            + "business page must not copy gold wizard md-tabs demo (data-wizard-panel)"
        )

    if demo:
        return errors

    kinds: list[str] = []
    if re.search(r"\bmd-stepper\b", text):
        kinds.append("md-stepper")
    if re.search(r"\bmd-advance\b", text):
        kinds.append("md-advance")
    if re.search(r"\bmd-progress--lg\b", text):
        kinds.append("md-progress--lg")

    if len(kinds) < 2:
        return errors

    wizardish = (
        "md-form-page" in text
        or "md-stepper" in text
        or "data-wizard-host" in text
        or ("md-d1__form" in text and "md-stepper" in text)
    )
    if not wizardish:
        return errors

    errors.append(
        prefix
        + "wizard nav must pick one of stepper/advance/progress-lg (PT-STATE-FLOW), got: "
        + "+".join(kinds)
    )
    return errors


def check_visual_floor(
    path: Path,
    page_id: str,
    text: str,
    parser: PageParser,
    *,
    fixture: bool = False,
) -> list[str]:
    """Block wireframe-like HTML that still passes quote/count checks."""
    errors: list[str] = []
    prefix = str(path) + ": "
    errors.extend(check_wizard_nav(path, page_id, text, fixture=fixture))
    errors.extend(check_dialog_backdrop(path, text))
    errors.extend(check_drawer_backdrop(path, text))
    errors.extend(check_dialog_surface(path, text))
    if BOX_DRAW_RE.search(text):
        errors.append(prefix + "ASCII wireframe leaked into HTML")
    if not parser.is_mobile and not parser.is_desktop:
        errors.append(prefix + "missing md-mobile-page or md-d1 root")
    if NATIVE_DATE_RE.search(text):
        errors.append(prefix + "use md-field--date + type=text, not type=date")
    if parser.is_desktop and parser.table_rows:
        if "md-chip" not in text and "md-thumb" not in text and "md-row-goods" not in text:
            errors.append(prefix + "desktop table missing md-chip/md-thumb/md-row-goods")
    if parser.is_desktop and "md-d1__form" in text and "md-field--sm" not in text:
        errors.append(prefix + "form fields must use md-field--sm")
    if parser.is_mobile and parser.has_list_toolbar and parser.unsupported_list_card_count:
        errors.append(
            prefix
            + "mobile list cards must use md-card--row or md-card--order"
        )
    if parser.is_mobile and "md-tabbar" in text and "data-icon" not in text:
        errors.append(prefix + "tabbar missing data-icon")
    if parser.has_tabbar and parser.has_mobile_appbar and not parser.has_center_appbar:
        errors.append(
            prefix
            + "tabbar page: only L2 md-appbar--center allowed (not L3/L5/L6 return or overlay appbar)"
        )
    if parser.is_mobile and "viewport-fit=cover" not in text:
        errors.append(prefix + "mobile page missing viewport-fit=cover")
    if parser.is_mobile and "md-immersive" not in text and "md-sink" not in text and "md-standard" not in text:
        errors.append(prefix + "mobile page must declare md-immersive or md-standard")
    if "md-d1__list" in text:
        if "md-d1--list" not in text:
            errors.append(prefix + "D1-1 list must use md-d1--list compact density")
        if not any(
            cls in text
            for cls in (
                "md-col-name",
                "md-col-price",
                "md-col-status",
                "md-col-date",
                "md-col-id",
                "md-col-num",
            )
        ):
            errors.append(prefix + "D1-1 columns must use semantic md-col-* (not equal widths)")
        if "md-empty" not in text:
            errors.append(prefix + "list page missing md-empty (hidden empty state)")
        if "md-skel-host" not in text and "md-skeleton" not in text:
            errors.append(prefix + "list page missing skeleton (md-skel-host / md-skeleton)")
    if "md-comment" in text:
        if "md-comment__time" not in text:
            errors.append(prefix + "comments must include md-comment__time")
        if "md-comment__photos" not in text:
            errors.append(prefix + "comments must include md-comment__photos (max 5 per row)")
    if "data-menu" in text and "md-menu--fixed" not in text:
        errors.append(prefix + "data-menu requires md-menu--fixed (keep gold more-menu behavior)")
    if "md-tabs--page" in text and "data-panel" not in text:
        errors.append(prefix + "md-tabs--page requires data-panel (keep gold tab switching)")
    if "data-wheel" in text and "proto-page.js" not in parser.scripts:
        errors.append(prefix + "data-wheel requires proto-page.js (keep gold picker behavior)")
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
    parser.add_argument(
        "--fixture",
        action="append",
        default=[],
        help="PAGE id intentionally containing a gold/demo comparison",
    )
    args = parser.parse_args(argv[1:])
    prd_root = Path(args.prd_root).resolve()
    version = resolve_version(prd_root, args.version)
    pages = args.page or list_pages(prd_root)
    fixture_pages = set(args.fixture)
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
        all_errors.extend(
            check_html(
                html_path(prd_root, page_id),
                page_id,
                comps,
                jumps,
                quotes,
                fixture=page_id in fixture_pages,
            )
        )

    if all_errors:
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1
    print("coverage ok: " + str(len(pages)) + " page(s), version " + version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
