#!/usr/bin/env python3
"""Classify prototype feedback and suggest the smallest affected workflow."""
from __future__ import annotations

import argparse
import json
import re


RULES = {
    "D": ("产品事实", ("业务规则", "字段", "接口", "权限", "Feature", "AC", "验收", "流程", "范围", "页面归属", "数据", "状态机")),
    "C": ("页面结构", ("新增页面", "删除页面", "增加区块", "删除区块", "新增入口", "筛选入口", "操作入口", "分区顺序", "跳转", "路由", "终端", "布局结构", "页面组成")),
    "B": ("交互表现", ("点击", "按下", "弹窗", "抽屉", "加载", "空态", "失败", "禁用", "展开", "收起", "过渡", "反馈", "交互")),
    "A": ("视觉微调", ("间距", "留白", "颜色", "色彩", "边框", "圆角", "阴影", "字号", "字体", "图片", "裁切", "对齐", "文案", "标题", "视觉", "样式", "风格")),
}


def classify(feedback: str) -> tuple[str, list[str]]:
    matches = {
        category: [keyword for keyword in keywords if keyword.lower() in feedback.lower()]
        for category, (_, keywords) in RULES.items()
    }
    for category in ("D", "C", "B", "A"):
        if matches[category]:
            return category, matches[category]
    return "C", ["未命中明确关键词，按结构变化保守处理"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feedback")
    parser.add_argument("--page-id")
    args = parser.parse_args()
    category, matched = classify(args.feedback)
    label = RULES[category][0]
    page = args.page_id or "受影响 PAGE"
    routes = {
        "A": {
            "write": [f"prototypes/{{终端}}/{page}.html", f"prototypes/.design-decisions/{page}.md"],
            "checks": ["真实渲染", "视觉自评", "UTF-8", "目标页浏览器检查"],
        },
        "B": {
            "write": [f"prototypes/{{终端}}/{page}.html", f"ui/{page}.md 或 ui/COMP-*.md", f"pages_prd/{{终端}}/{page}.md（若交互契约变化）"],
            "checks": ["受影响页 Q-P", "状态契约变化时执行定向 Q-S", "事实一致性审计"],
        },
        "C": {
            "write": ["ui/", "pages_prd/", "prototypes/"],
            "checks": ["受影响对象 Q-S", "事实一致性审计", "受影响页 Q-P"],
        },
        "D": {
            "write": ["先改事实正本", "同步索引和下游明细", "更新受影响原型"],
            "checks": ["语义检查", "事实一致性审计", "受影响页 Q-P", "涉及范围时执行评审"],
        },
    }
    print(json.dumps({"category": category, "label": label, "matched": matched, "feedback": args.feedback, **routes[category]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
