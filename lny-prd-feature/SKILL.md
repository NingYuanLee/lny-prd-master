---
name: lny-prd-feature
description: >-
  维护 feature_spec 索引与 feature/FEATURE-*.md 明细，并与 PAGE/API/EXT 保持引用闭环。
  Use when the user mentions /lny-prd-feature, @lny-prd-feature, 功能规格, FEATURE-*.
disable-model-invocation: true
---

## 与总控的关系

本步为 **④ `/lny-prd-feature`**。产物：`feature_spec.md` + `feature/`。禁止写接口字段表与 UI 线框。下一跳通常 **⑤ page**。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑧ 追加；过程流水见 master §1.1。

# 功能规格 `/lny-prd-feature`

## Additional resources

- 索引、明细、双图规范：[`reference.md`](reference.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md`。不为框架通用已排除项建 Feature；业务流程 Feature 仍须编写且只写差异。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 Feature 或把其写进范围内。

## 职责与禁止

- **负责**：Feature 索引与明细（目标/规则/AC/双图）；FEATURE ↔ PAGE/API/EXT 闭环；`main_spec` §7 统计。
- **禁止**：在 `api_spec` 写字段；在 `ui_manifest` 写线框；写入预览壳机制；根规范「变更记录」表新增行。②③④⑤⑥ **禁止**展开「明确不做」。仅当 PM 已说出点位才写埋点；**禁止自拟埋点方案**。

编号：新增只用 `FEATURE-{三位序号}`。历史 `FEATURE-MP-001` **只读兼容**，新项目禁止再用。

## 写产物纪律

开笔前 Read 索引 + `feature/` + 根规格校验引用。先清单后落盘。命中双图必画条件则补图（节点用 PAGE/API/EXT 编号）。`iteration_notes` 文末追加业务变更。

## 前置条件

已有 `main_spec.md`、`api_spec.md`、`ui_manifest.md`。⑧ 委派进入时 Read `feature_changes.md` 中 `待④`。

## 输入

```yaml
版本号: v1.1.0
操作模式: add 或 modify
功能信息:
  - 功能编号: FEATURE-001
    功能名称: 商品筛选与排序
    关联页面: [PAGE-MP-002]
    关联接口: [API-MP-003]
```

## 执行步骤

1. 缺 `feature_spec.md` / `feature/` 时按 [`reference.md`](reference.md) 创建骨架。
2. add：分配编号、写明细、更新 §3；modify：同步明细与索引。
3. 补双图或免画理由；更新 `main_spec` §7。
4. 确认索引有文件、文件有索引、关联 ID 有定义。
