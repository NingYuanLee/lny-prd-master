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
VISIBLE_IMPL_COPY_RE = re.compile(
    r"API-[A-Z]+-\d+|fitBounds|本页不含|不提供新建|无操作列|只读监控|只读台账|编号占位|模拟确认"
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
MOBILE_LIST_CARD_CLASSES = {"md-card--order", "md-card--row"}


def _extract_balanced(text: str, start: int, opening: str, closing: str) -> str | None:
    """Return a JS array/object including delimiters, ignoring quoted delimiters."""
    if start < 0 or start >= len(text) or text[start] != opening:
        return None
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def _top_level_objects(array_text: str) -> list[str]:
    objects: list[str] = []
    depth = 0
    start: int | None = None
    quote: str | None = None
    escaped = False
    for index, char in enumerate(array_text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'", "`"}:
            quote = char
        elif char == "{" and depth == 0:
            start = index
            depth = 1
        elif char == "{" and depth:
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(array_text[start : index + 1])
                start = None
    return objects


def _js_value(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
        value = raw[1:-1]
        return value.replace("\\n", "\n").replace("\\\"", '"').replace("\\'", "'")
    return raw


def parse_shell_page(index_text: str, page_id: str) -> dict | None:
    """Parse the small, deliberately data-only PROTO_SHELL object without eval."""
    pages_match = re.search(r"\bpages\s*:\s*\[", index_text)
    if not pages_match:
        return None
    pages_array = _extract_balanced(index_text, pages_match.end() - 1, "[", "]")
    if not pages_array:
        return None
    for page_object in _top_level_objects(pages_array[1:-1]):
        id_match = re.search(r"\bid\s*:\s*(['\"])(.*?)\1", page_object)
        if not id_match or id_match.group(2) != page_id:
            continue
        comps_match = re.search(r"\bcomps\s*:\s*\[", page_object)
        comps_array = (
            _extract_balanced(page_object, comps_match.end() - 1, "[", "]")
            if comps_match
            else "[]"
        )
        comps: list[dict] = []
        for comp_object in _top_level_objects((comps_array or "[]")[1:-1]):
            comp_id = re.search(r"\bid\s*:\s*(['\"])(.*?)\1", comp_object)
            if not comp_id:
                continue
            states_match = re.search(r"\bstates\s*:\s*\[", comp_object)
            states_array = (
                _extract_balanced(comp_object, states_match.end() - 1, "[", "]")
                if states_match
                else "[]"
            )
            states = [
                _js_value(match.group(0))
                for match in re.finditer(r"(['\"])(?:\\.|(?!\1).)*\1", (states_array or "[]"))
            ]
            comps.append({"id": comp_id.group(2), "states": states})
        state_demo = re.search(r"\bstateDemo\s*:\s*(true|false)", page_object)
        legacy = re.search(r"\btabBarExempt\s*:\s*(true|false)", page_object)
        return {
            "comps": comps,
            "stateDemo": None if state_demo is None else state_demo.group(1) == "true",
            "tabBarExempt": None if legacy is None else legacy.group(1) == "true",
        }
    return None


def parse_comp_states(text: str) -> list[str]:
    # Match the semantic heading so both legacy §5 and current §4 COMP files work.
    heading = re.search(r"^##\s*\d+\.\s*UI 状态矩阵.*$", text, flags=re.M)
    if not heading:
        return []
    tail = text[heading.end() :]
    next_heading = re.search(r"^##\s+", tail, flags=re.M)
    section = tail[: next_heading.start()] if next_heading else tail
    states: list[str] = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] in {"状态", "------", ""}:
            continue
        if set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0] not in states:
            states.append(cells[0])
    return states


def find_comp_doc(prd_root: Path, comp_id: str) -> Path | None:
    ui_root = prd_root / "ui"
    if not ui_root.is_dir():
        return None
    matches = list(ui_root.rglob(comp_id + ".md"))
    return matches[0] if matches else None


def find_page_ui(prd_root: Path, page_id: str) -> Path | None:
    ui_root = prd_root / "ui"
    if not ui_root.is_dir():
        return None
    matches = list(ui_root.rglob(page_id + ".md"))
    return matches[0] if matches else None


def terminal_of(page_id: str) -> str:
    parts = page_id.split("-")
    return parts[1] if len(parts) >= 3 else ""


def find_pages_prd(prd_root: Path, version: str, page_id: str) -> Path | None:
    """Find the canonical current page PRD; version snapshots are never authoring input."""
    base = prd_root / "pages_prd"
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
        self.stack: list[tuple[str, set[str], bool]] = []
        self.errors: list[str] = []
        self.text_parts: list[str] = []
        self.has_kit_css = False
        self.scripts: set[str] = set()
        self.hrefs: set[str] = set()
        self.comps: set[str] = set()
        self.empty_for: set[str] = set()
        self.in_thead = 0
        self.in_data_table = 0
        self.is_mobile = False
        self.is_desktop = False
        self.has_status_bar = False
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
        self.mobile_body_count = 0
        self.direct_mobile_sheet_count = 0
        self.direct_mobile_body_non_sheet: list[str] = []
        self.comp_states: dict[str, set[str]] = {}
        self.state_views: dict[str, set[str]] = {}
        self.skel_for: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        attr_names = {k for k, _ in attrs}
        classes = set((ad.get("class") or "").split())
        parent = self.stack[-1] if self.stack else None
        ancestors = [item_classes for _, item_classes, _ in self.stack]
        hidden_text = (
            tag in {"script", "style", "template", "noscript"}
            or "hidden" in attr_names
            or ad.get("aria-hidden", "").strip().lower() == "true"
            or "is-hidden" in classes
            or bool(parent and parent[2])
        )
        if "md-mobile-body" in classes:
            self.mobile_body_count += 1
        if parent and "md-mobile-body" in parent[1]:
            if "md-mobile-sheet" in classes:
                self.direct_mobile_sheet_count += 1
            else:
                self.direct_mobile_body_non_sheet.append(tag)
        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, classes, hidden_text))
        if classes & CARD_DENSITY_CONTEXT_CLASSES:
            self.has_card_density_context = True
        if "md-d1--list" in classes or "md-d1__list" in classes:
            self.has_dense_data_table = True
        if "md-list-toolbar" in classes:
            self.has_list_toolbar = True
        if "md-mobile-page" in classes:
            self.is_mobile = True
        if "md-d1" in classes:
            self.is_desktop = True
        if "md-status-bar" in classes:
            self.has_status_bar = True
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
            state = ad.get("data-state")
            if state:
                self.comp_states.setdefault(comp, set()).add(state)
        state_for = ad.get("data-state-for")
        state_view = ad.get("data-state")
        if state_for and state_view:
            self.state_views.setdefault(state_for, set()).add(state_view)
        empty_for = ad.get("data-empty-for")
        if empty_for:
            self.empty_for.add(empty_for)
        skel_for = ad.get("data-skel-for")
        if skel_for:
            self.skel_for.add(skel_for)
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
        if tag == "thead" and self.in_thead:
            self.in_thead -= 1
        if tag == "table" and self.in_data_table:
            self.in_data_table -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if (
            self.stack
            and any(tag == "body" for tag, _, _ in self.stack)
            and not self.stack[-1][2]
        ):
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
    for match in dict.fromkeys(VISIBLE_IMPL_COPY_RE.findall(visible)):
        errors.append(
            str(path)
            + ": visible body copy exposes implementation/meta text: "
            + match
        )
    if parser.bare_media:
        errors.append(str(path) + ": md-media-ph without --1..--6 variant")
    errors.extend(check_density(path, parser))
    if parser.is_mobile and "proto-page.js" not in parser.scripts:
        errors.append(str(path) + ": mobile page missing proto-page.js (injects fixed status bar)")
    if parser.is_mobile:
        if parser.mobile_body_count == 0:
            errors.append(str(path) + ": mobile page missing md-mobile-body")
        elif parser.mobile_body_count > 1:
            errors.append(
                str(path)
                + ": mobile page has multiple md-mobile-body elements (got "
                + str(parser.mobile_body_count)
                + ")"
            )
        if parser.direct_mobile_sheet_count == 0:
            errors.append(
                str(path)
                + ": mobile page missing direct md-mobile-sheet child of md-mobile-body"
            )
        elif parser.direct_mobile_sheet_count > 1:
            errors.append(
                str(path)
                + ": mobile page has multiple direct md-mobile-sheet children of md-mobile-body (got "
                + str(parser.direct_mobile_sheet_count)
                + ")"
            )
        if parser.direct_mobile_body_non_sheet:
            errors.append(
                str(path)
                + ": md-mobile-body has direct non-sheet child: "
                + ", ".join(parser.direct_mobile_body_non_sheet)
                + " (put L3 inside md-mobile-sheet and fixed L1 outside md-mobile-body)"
            )
    if parser.is_desktop and not parser.has_breadcrumb:
        errors.append(str(path) + ": desktop page missing md-breadcrumb")
    errors.extend(check_visual_floor(path, page_id, text, parser, fixture=fixture))
    return errors


def check_state_contract(
    prd_root: Path,
    version: str,
    page_id: str,
    expected_comps: set[str] | None,
    path: Path,
) -> list[str]:
    """Keep the shell state machine, COMP matrix, and page visuals in lockstep."""
    errors: list[str] = []
    terminal = terminal_of(page_id)
    index_path = prd_root / "prototypes" / terminal / "index.html"
    if not index_path.is_file():
        return [str(index_path) + ": missing terminal shell for state contract"]
    try:
        index_text = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [str(index_path) + ": cannot read terminal shell: " + str(exc)]
    shell_page = parse_shell_page(index_text, page_id)
    if shell_page is None:
        return [str(index_path) + ": PROTO_SHELL missing page " + page_id]

    shell_comps = {comp["id"] for comp in shell_page["comps"]}
    if expected_comps is not None and shell_comps != expected_comps:
        errors.append(
            str(index_path)
            + ": shell comps "
            + repr(sorted(shell_comps))
            + " do not match PAGE components "
            + repr(sorted(expected_comps))
        )
    if shell_page["tabBarExempt"] is True and shell_comps and shell_page["stateDemo"] is None:
        errors.append(
            str(index_path)
            + ": tabBarExempt cannot hide a page with components; use explicit stateDemo:false only"
        )

    parser = PageParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        return errors + [str(path) + ": cannot read page for state contract: " + str(exc)]

    for comp in shell_page["comps"]:
        comp_id = comp["id"]
        shell_states = comp["states"]
        if not shell_states:
            errors.append(str(index_path) + ": " + comp_id + " has no states")
            continue
        if len(shell_states) != len(set(shell_states)):
            errors.append(str(index_path) + ": " + comp_id + " has duplicate states")
        doc = find_comp_doc(prd_root, comp_id)
        if doc is None:
            errors.append(str(index_path) + ": missing ui/" + comp_id + ".md for state source")
            continue
        matrix_states = parse_comp_states(doc.read_text(encoding="utf-8"))
        if not matrix_states:
            errors.append(str(doc) + ": UI state matrix is missing or empty")
        elif shell_states != matrix_states:
            errors.append(
                str(index_path)
                + ": "
                + comp_id
                + " states "
                + repr(shell_states)
                + " do not exactly match "
                + str(doc)
                + " states "
                + repr(matrix_states)
            )
        if comp_id not in parser.comps:
            errors.append(str(path) + ": missing data-comp=" + comp_id + " for shell component")
        for state in shell_states:
            if state == "loading" and comp_id not in parser.skel_for:
                errors.append(str(path) + ": " + comp_id + " loading state missing data-skel-for")
            elif state in {"empty", "error"} and comp_id not in parser.empty_for:
                errors.append(str(path) + ": " + comp_id + " " + state + " state missing data-empty-for")
            elif state not in {"loading", "empty", "error", "default"} and state not in parser.state_views.get(comp_id, set()):
                errors.append(
                    str(path)
                    + ": "
                    + comp_id
                    + " custom state "
                    + state
                    + " missing data-state-for visual"
                )
        undeclared_views = parser.state_views.get(comp_id, set()) - set(shell_states)
        if undeclared_views:
            errors.append(
                str(path)
                + ": "
                + comp_id
                + " has undeclared visual states "
                + repr(sorted(undeclared_views))
            )
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
        comps: set[str] | None = None
        jumps: set[str] = set()
        quotes: list[str] = []
        if prd is None:
            if not ui_direct:
                all_errors.append(page_id + ": pages_prd missing (not ui直出)")
            else:
                ui_page = find_page_ui(prd_root, page_id)
                if ui_page is not None:
                    comps = set(COMP_RE.findall(ui_page.read_text(encoding="utf-8")))
                else:
                    comps = None
        else:
            text = prd.read_text(encoding="utf-8")
            comps, jumps, quotes = parse_prd(text)
            jumps.discard("无")
        page_path = html_path(prd_root, page_id)
        all_errors.extend(
            check_html(
                page_path,
                page_id,
                comps or set(),
                jumps,
                quotes,
                fixture=page_id in fixture_pages,
            )
        )
        all_errors.extend(check_state_contract(prd_root, version, page_id, comps, page_path))

    if all_errors:
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1
    print("coverage ok: " + str(len(pages)) + " page(s), version " + version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
