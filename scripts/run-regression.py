#!/usr/bin/env python3
"""Run product-agnostic regression checks for the skill runtime."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ROOT = ROOT / "lny-prd" / "modules" / "lny-prd-check" / "scripts"
PROTO_ROOT = ROOT / "lny-prd" / "modules" / "lny-prd-prototype" / "scripts"


def run(command: list[str]) -> None:
    print("+", " ".join(str(part) for part in command))
    result = subprocess.run(command, cwd=ROOT, text=True)
    if result.returncode:
        raise SystemExit(result.returncode)


def audit_consistency_regression(temp_root: Path) -> None:
    project = temp_root / "fact-fixture"
    (project / "ui").mkdir(parents=True)
    (project / "pages_prd" / "MP").mkdir(parents=True)
    (project / "api").mkdir()
    (project / "feature").mkdir()
    manifest = "| 页面编号 | 页面名称 | 所属终端 | 明细路径 |\n|---|---|---|---|\n| PAGE-MP-001 | 首页 | 微信小程序 | ui/PAGE-MP-001.md |\n"
    detail = "| 属性 | 内容 |\n|---|---|\n| 页面编号 | PAGE-MP-001 |\n| 页面名称 | 首页 |\n| 所属终端 | 微信小程序 |\n"
    (project / "ui_manifest.md").write_text(manifest, encoding="utf-8")
    (project / "api_spec.md").write_text("# api\n", encoding="utf-8")
    (project / "feature_spec.md").write_text("# feature\n", encoding="utf-8")
    (project / "ui" / "PAGE-MP-001.md").write_text(detail, encoding="utf-8")
    (project / "pages_prd" / "MP" / "PAGE-MP-001.md").write_text(detail, encoding="utf-8")
    audit = CHECK_ROOT / "audit-fact-consistency.py"
    run([sys.executable, str(audit), str(project)])
    (project / "ui" / "PAGE-MP-001.md").write_text(detail.replace("| 页面名称 | 首页 |", "| 页面名称 | 错误 |"), encoding="utf-8")
    failed = subprocess.run([sys.executable, str(audit), str(project)], cwd=ROOT, text=True, capture_output=True)
    if failed.returncode == 0 or "FACT_DRIFT" not in failed.stdout:
        raise SystemExit("fact consistency regression failed")


def decision_walkthrough_regression(temp_root: Path) -> None:
    project = temp_root / "decision-fixture"
    project.mkdir()
    (project / "ui").mkdir()
    (project / "ui" / "PAGE-MP-001.md").write_text("# PAGE-MP-001 首页\n", encoding="utf-8")
    (project / "product_workspace.md").write_text(
        "状态：暂定\n产品目标：让用户快速浏览商品\n本次范围：PAGE-MP-001\n明确不做：支付\n成功标准：首屏能进入商品列表\n",
        encoding="utf-8",
    )
    audit = CHECK_ROOT / "audit-decision-walkthrough.py"
    run([sys.executable, str(audit), str(project)])
    (project / "product_workspace.md").write_text(
        "状态：暂定\n产品目标：让用户快速浏览商品\n本次范围：PAGE-MP-999\n明确不做：支付\n成功标准：首屏能进入商品列表\n",
        encoding="utf-8",
    )
    failed = subprocess.run([sys.executable, str(audit), str(project)], cwd=ROOT, text=True, capture_output=True)
    if failed.returncode == 0 or "missing artifact PAGE-MP-999" not in failed.stdout:
        raise SystemExit("decision walkthrough regression failed")


def main() -> int:
    probe = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "probe-host-capabilities.py"), "--json", "--self-check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if probe.returncode:
        raise SystemExit(probe.returncode)
    probe_data = json.loads(probe.stdout)
    if "codex" not in probe_data.get("hosts", {}) or "cursor" not in probe_data.get("hosts", {}):
        raise SystemExit("host capability probe regression failed")

    classification = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "classify-change.py"), "把首页标题左边距缩小", "--page-id", "PAGE-MP-001"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if classification.returncode:
        raise SystemExit(classification.returncode)
    if json.loads(classification.stdout).get("category") != "A":
        raise SystemExit("change classifier regression failed")

    with tempfile.TemporaryDirectory(prefix="lny-prd-kit-regression-") as temp:
        temp_root = Path(temp)
        audit_consistency_regression(temp_root)
        decision_walkthrough_regression(temp_root)
        feedback = temp_root / "feedback.md"
        feedback.write_text(
            "## FB-001 标题间距\n\n"
            "- 反馈原文：标题和筛选栏距离太大\n"
            "- 变更类别：A 视觉微调\n"
            "- 影响判断：不改变研发实现行为\n"
            "- 事实正本：无\n"
            "- 修改文件：prototypes/MP/PAGE-MP-001.html\n"
            "- 修改前截图：before.png\n"
            "- 修改后截图：after.png\n"
            "- 检查范围：目标页渲染和视觉自评\n"
            "- 结果：完成\n",
            encoding="utf-8",
        )
        run([sys.executable, str(PROTO_ROOT / "validate-feedback-record.py"), str(feedback)])
        html = temp_root / "utf8-check.html"
        html.write_text("<!doctype html><html lang=\"zh-CN\"><meta charset=\"utf-8\"><title>产品页面</title></html>", encoding="utf-8")
        run([sys.executable, str(PROTO_ROOT / "verify-prototype-utf8.py"), str(html)])

        destination = temp_root / "MP"
        run([sys.executable, str(PROTO_ROOT / "copy-kit.py"), str(destination)])
        expected = {
            "icons-extra.js",
            "md-icons.js",
            "mui-kit.css",
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
