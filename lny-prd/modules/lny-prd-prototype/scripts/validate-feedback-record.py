#!/usr/bin/env python3
"""Validate one lightweight prototype feedback record."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = ("反馈原文：", "变更类别：", "影响判断：", "事实正本：", "修改文件：", "修改前截图：", "修改后截图：", "检查范围：", "结果：")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    path = args.record.resolve()
    if not path.is_file():
        print(f"feedback record not found: {path}")
        return 1
    text = path.read_text(encoding="utf-8")
    errors = [f"missing field {field}" for field in REQUIRED if field not in text]
    if re.search(r"修改前截图：\s*(?:无|待|未)", text) or re.search(r"修改后截图：\s*(?:无|待|未)", text):
        errors.append("before and after screenshots are required")
    if not re.search(r"变更类别：\s*[ABCD]", text):
        errors.append("change category must be A, B, C or D")
    if re.search(r"结果：\s*完成", text) and re.search(r"检查范围：\s*(?:无|待验证|未执行)", text):
        errors.append("completed records must include executed checks")
    if errors:
        print("feedback record validation failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("feedback record validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
