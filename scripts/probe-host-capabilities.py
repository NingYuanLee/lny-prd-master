#!/usr/bin/env python3
"""Probe host capabilities without treating unavailable signals as proof of absence."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


KNOWN_HOSTS = {
    "codex": ("Codex / ChatGPT", ("codex", "chatgpt", "openai codex")),
    "claude-code": ("Claude Code", ("claude", "claude code")),
    "cursor": ("Cursor", ("cursor",)),
    "deepseek-harness": ("DeepSeek Harness", ("dsh", "deepseek harness", "deepseek")),
    "workbuddy": ("WorkBuddy", ("workbuddy", "腾讯 workbuddy")),
    "doubao-work": ("豆包工作", ("doubao", "豆包工作")),
    "qwen-work": ("千问办公", ("qwen", "千问办公", "tongyi")),
    "trae": ("Trae", ("trae", "traework", "trae work")),
}


def command_version(command: str) -> str | None:
    executable = shutil.which(command)
    if not executable:
        return None
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=3)
    except (OSError, subprocess.SubprocessError):
        return "available"
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else "available"


def load_declared_capabilities(path: str | None) -> dict:
    raw = path or os.environ.get("LNY_PRD_HOST_CAPABILITIES")
    if not raw:
        return {}
    try:
        if Path(raw).is_file():
            return json.loads(Path(raw).read_text(encoding="utf-8"))
        return json.loads(raw)
    except (OSError, json.JSONDecodeError):
        return {"_invalid_declaration": raw}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capabilities", help="JSON string or file supplied by the host integration")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    declared = load_declared_capabilities(args.capabilities)
    commands = {}
    for command in ("python", "node", "npm", "git", "pwsh", "playwright", "chromium", "google-chrome", "msedge"):
        version = command_version(command)
        commands[command] = {"status": "available" if version else "unknown", "version": version}

    hosts = {}
    declared_hosts = declared.get("hosts", {}) if isinstance(declared, dict) else {}
    for key, (label, aliases) in KNOWN_HOSTS.items():
        supplied = declared_hosts.get(key) if isinstance(declared_hosts, dict) else None
        if supplied is not None:
            hosts[key] = {"label": label, "status": "declared", "capabilities": supplied}
        else:
            hosts[key] = {"label": label, "status": "unknown", "aliases": list(aliases)}

    result = {
        "commands": commands,
        "hosts": hosts,
        "declared_capabilities": declared,
        "policy": "unknown means not detected by this probe, not unavailable",
        "next_action": "use the host-provided tool inventory before requesting installation",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Host capability probe")
        for command, item in commands.items():
            print(f"- command {command}: {item['status']}" + (f" ({item['version']})" if item["version"] else ""))
        for key, item in hosts.items():
            print(f"- host {item['label']}: {item['status']}")
        print("- policy: unknown means not detected by this probe, not unavailable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
