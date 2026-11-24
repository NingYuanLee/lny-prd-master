#!/usr/bin/env python3
"""Validate one evidence-backed visual self-review record."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


DIMENSIONS = (
    "首屏任务", "信息层级", "间距留白", "布局与对齐", "UI 组件",
    "文字与素材", "风格语言", "视觉锚点", "状态与反馈", "跨视口表现",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    path = args.review.resolve()
    if not path.is_file():
        print(f"review file not found: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if any(token in text for token in ("{位置与现象}", "{动作或理由}", "{首屏路径}", "{操作后路径}", "{修改前截图路径}", "{修改后截图路径}")):
        errors.append("review still contains template placeholders")
    if re.search(r"\|[^\n|]+\|\s*(?:清楚|合理|不错|ok|OK)\s*\|", text):
        errors.append("review uses a vague score without observable evidence")
    if "## 视觉自评" not in text:
        errors.append("missing visual self-review heading")
    if not re.search(r"实际查看：\s*是", text):
        errors.append("actual screenshot inspection is not confirmed")
    if not re.search(r"截图证据：\s*[^\n；]+；[^\n；]+；[^\n]+", text):
        errors.append("three screenshot evidence paths are required")
    if "修改前后对照：" in text and re.search(r"修改前后对照：\s*(?:无|待|未)", text):
        errors.append("before and after comparison is empty")
    if "修改前后对照：" in text and not re.search(r"修改前后对照：\s*[^→]+→[^；]+；变化区域：\s*[^\n]+", text):
        errors.append("before and after comparison needs two paths and a changed area")
    scores: dict[str, int] = {}
    for dimension in DIMENSIONS:
        match = re.search(rf"\|\s*{re.escape(dimension)}\s*\|\s*([0-2])\s*\|", text)
        if not match:
            errors.append(f"missing score for {dimension}")
        else:
            scores[dimension] = int(match.group(1))
    if len(scores) == len(DIMENSIONS):
        total = sum(scores.values())
        if total < 16:
            errors.append(f"score {total}/20 is below the 16/20 threshold")
        for critical in ("首屏任务", "信息层级", "布局与对齐", "UI 组件", "状态与反馈"):
            if scores[critical] == 0:
                errors.append(f"critical dimension {critical} cannot score 0")
    if not re.search(r"结论：\s*(通过|继续返修)", text):
        errors.append("missing explicit conclusion")
    if errors:
        print("visual self-review validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("visual self-review validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
