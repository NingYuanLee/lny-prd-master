# -*- coding: utf-8 -*-
"""Search icons: kit first, then iconfont.cn. No Cursor MCP required."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.iconfont.cn/api/icon/search.json"
KIT_JS = Path(__file__).resolve().parents[1] / "kit" / "md-icons.js"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def kit_index() -> tuple[list[str], dict[str, str]]:
    text = KIT_JS.read_text(encoding="utf-8")
    ids = re.findall(r'^\s+(?:([a-z][\w-]*)|"([\w-]+)"):\s*"M', text, flags=re.M)
    names = [a or b for a, b in ids]
    alias_block = text.split("var ALIAS = {", 1)
    aliases: dict[str, str] = {}
    if len(alias_block) == 2:
        body = alias_block[1].split("};", 1)[0]
        for zh, en in re.findall(r'"([^"]+)":\s*"([^"]+)"', body):
            aliases[zh] = en
    return names, aliases


def search_kit(query: str) -> list[dict]:
    names, aliases = kit_index()
    q = query.strip()
    hits: list[dict] = []
    if q in names:
        hits.append({"source": "kit", "id": q, "name": q})
    if q in aliases:
        hits.append({"source": "kit", "id": aliases[q], "name": q})
    for zh, en in aliases.items():
        if q and q in zh and {"source": "kit", "id": en, "name": zh} not in hits:
            hits.append({"source": "kit", "id": en, "name": zh})
    for n in names:
        if q and q in n and not any(h["id"] == n and h["source"] == "kit" for h in hits):
            hits.append({"source": "kit", "id": n, "name": n})
    return hits


def search_iconfont(query: str, page: int, page_size: int, fills: str) -> dict:
    payload = urllib.parse.urlencode(
        {
            "q": query,
            "sortType": "updated_at",
            "page": str(page),
            "pageSize": str(page_size),
            "sType": "",
            "fromCollection": "-1",
            "fills": fills,
            "t": str(int(time.time() * 1000)),
            "ctoken": "null",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=payload,
        method="POST",
        headers={
            "User-Agent": UA,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode("utf-8")
    data = json.loads(raw)
    if data.get("code") != 200:
        raise RuntimeError(data.get("message") or "iconfont search failed")
    icons = (data.get("data") or {}).get("icons") or []
    out = []
    for ic in icons:
        out.append(
            {
                "source": "iconfont",
                "id": str(ic.get("id")),
                "name": ic.get("name") or "",
                "fills": ic.get("fills"),
                "width": ic.get("width"),
                "height": ic.get("height"),
                "show_svg": ic.get("show_svg") or "",
            }
        )
    return {"total": len(out), "icons": out}


def parse_svg(svg: str) -> tuple[str, list[str]]:
    vb = re.search(r'viewBox="([^"]+)"', svg, flags=re.I)
    view_box = vb.group(1) if vb else "0 0 1024 1024"
    paths = re.findall(r'<path\b[^>]*\sd="([^"]+)"', svg, flags=re.I)
    if not paths:
        raise RuntimeError("no path in svg")
    return view_box, paths


def ascii_name(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip()).strip("-").lower()
    return s or "icon"


def upsert_extra(extra_js: Path, icon_id: str, spec: dict) -> None:
    extra_js.parent.mkdir(parents=True, exist_ok=True)
    old = extra_js.read_text(encoding="utf-8") if extra_js.is_file() else (
        "/* project icon extras; written by search-icons.py */\n"
    )
    old = re.sub(
        r"\n?if \(window\.ProtoIcons\) \{\s*ProtoIcons\.register\(\""
        + re.escape(icon_id)
        + r"\".*?\n\}\n?",
        "\n",
        old,
        flags=re.S,
    )
    alias = spec.get("alias") or ""
    alias_js = json.dumps(alias, ensure_ascii=False) if alias else "null"
    block = (
        "if (window.ProtoIcons) {\n"
        "  ProtoIcons.register("
        + json.dumps(icon_id, ensure_ascii=False)
        + ", { viewBox: "
        + json.dumps(spec["viewBox"])
        + ", paths: "
        + json.dumps(spec["paths"], ensure_ascii=False)
        + ", alias: "
        + alias_js
        + " });\n"
        "  ProtoIcons.mount();\n"
        "}\n"
    )
    extra_js.write_text(old.rstrip() + "\n" + block, encoding="utf-8", newline="\n")


def write_svg(path: Path, view_box: str, paths: list[str]) -> None:
    inner = "".join('<path d="' + d.replace('"', "'") + '"/>' for d in paths)
    text = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="'
        + view_box
        + '" class="md-icon" aria-hidden="true">'
        + inner
        + "</svg>\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    p = argparse.ArgumentParser(description="Search kit + iconfont.cn (no MCP)")
    p.add_argument("query", nargs="?", default="", help="keyword, e.g. 客服")
    p.add_argument("--list-kit", action="store_true")
    p.add_argument("--local-only", action="store_true")
    p.add_argument("--type", dest="icon_type", default="fill", help="fill|line|all")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=8)
    p.add_argument("--id", dest="icon_id", default="", help="iconfont numeric id to install")
    p.add_argument("--pick", type=int, default=-1, help="install Nth online result (0-based)")
    p.add_argument("--name", default="", help="ASCII id to register, e.g. kefu")
    p.add_argument("--out", default="", help="prototypes/{TERM}/assets")
    args = p.parse_args()

    if args.list_kit:
        names, aliases = kit_index()
        print(json.dumps({"ids": names, "aliases": aliases}, ensure_ascii=False, indent=2))
        return 0

    if not args.query and not args.icon_id:
        print("usage: search-icons.py <query> [--pick 0 --name kefu --out <assets>]", file=sys.stderr)
        return 2

    result: dict = {"kit": [], "iconfont": []}
    if args.query:
        result["kit"] = search_kit(args.query)

    fills = ""
    if args.icon_type == "fill":
        fills = "1"
    elif args.icon_type == "line":
        fills = "0"

    online: list[dict] = []
    online_error = ""
    need_online = (not args.local_only) and (
        args.icon_id or args.pick >= 0 or args.out or not result["kit"]
    )
    if need_online and args.query:
        try:
            packed = search_iconfont(args.query, args.page, min(args.size, 20), fills)
            online = packed["icons"]
            result["iconfont"] = [
                {k: v for k, v in ic.items() if k != "show_svg"} for ic in online
            ]
        except (OSError, TimeoutError, UnicodeError, json.JSONDecodeError, RuntimeError) as exc:
            online_error = str(exc)
            result["warning"] = "iconfont unavailable; use a semantically close kit icon"

    if online_error and (args.icon_id or args.pick >= 0):
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("online icon install unavailable: " + online_error, file=sys.stderr)
        return 1

    install = None
    if args.icon_id:
        for ic in online:
            if str(ic["id"]) == str(args.icon_id):
                install = ic
                break
        if install is None and args.query:
            try:
                packed = search_iconfont(args.query, 1, 20, fills)
                for ic in packed["icons"]:
                    if str(ic["id"]) == str(args.icon_id):
                        install = ic
                        break
            except (OSError, TimeoutError, UnicodeError, json.JSONDecodeError, RuntimeError) as exc:
                print("online icon install unavailable: " + str(exc), file=sys.stderr)
                return 1
        if install is None:
            print("icon id not in search results: " + args.icon_id, file=sys.stderr)
            return 1
    elif args.pick >= 0:
        if args.pick >= len(online):
            print("pick out of range", file=sys.stderr)
            return 1
        install = online[args.pick]

    if install and args.out:
        view_box, paths = parse_svg(install["show_svg"])
        icon_id = ascii_name(args.name or install["name"] or "icon")
        assets = Path(args.out).resolve()
        write_svg(assets / "icons" / (icon_id + ".svg"), view_box, paths)
        upsert_extra(
            assets / "icons-extra.js",
            icon_id,
            {
                "viewBox": view_box,
                "paths": paths,
                "alias": install.get("name") or "",
            },
        )
        result["installed"] = {
            "id": icon_id,
            "iconfont_id": install["id"],
            "data_icon": icon_id,
            "extra": str(assets / "icons-extra.js"),
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
