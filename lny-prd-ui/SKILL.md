---
name: lny-prd-ui
description: >-
  维护 ui_manifest 索引与 ui/PAGE-*.md、ui/COMP-*.md 明细；仅更新 main_spec §5 统计。
  Use when the user mentions /lny-prd-ui, @lny-prd-ui, UI 清单, 页面架构, PAGE-*, COMP-*.
disable-model-invocation: true
---

## 与总控的关系

本步为 **② `/lny-prd-ui`**。产物：`ui_manifest.md` + `ui/`。禁止改 `main_spec` 第4章、禁止写 API/原型。下一跳通常 **③ api** 与 **④ feature**（规格三件套批）。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑧ 追加；过程流水见 master §1.1。

# 用户界面设计 `/lny-prd-ui`

## Additional resources

- 模板与 L/D 层级、控件形态：[`reference.md`](reference.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`
- 旧项目迁移：`scripts/migrate-prd-structure.mjs`
- 桌面壳 PRD 由 **⑤** 落盘：`lny-prd-page/reference.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 及本项目追加排除。不为框架通用已排除项建 `ui/PAGE-*`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 PAGE。**新立项只走目录化**（`ui_manifest` 只留索引 + `ui/` 明细）；旧「manifest 内嵌全文」只读兼容，禁止双轨扩写。

## 职责与禁止

- **负责**：`ui_manifest.md` 与 `ui/PAGE-*.md`、`ui/COMP-*.md` 单一事实源一致；`main_spec.md` **只写 §5 统计**。
- **禁止**：改第4章终端表；写 `api_spec` 字段；改 `prototypes/`；写预览壳机制（状态演示/postMessage/`map.html`）；在根规范「变更记录」表新增行；落盘 `pages_prd/_shell`（属 ⑤）。仅当 PM 已说出点位或 AD 字典条目才写埋点；**禁止自拟埋点方案**。

COMP **编号必填** `COMP-{三位序号}`，与 `ui_manifest` §4「组件编号」列、`ui/COMP-*.md` 文件名一致。

## 局部自定义 UI 组件（判定）

满足其一即可建 COMP：多页复用，或多态展示。禁止按面积拆碎；同一状态机且视觉相邻 → 一个 COMP。单页 ≥3 个独立状态机/数据域 → 必须拆页。PAGE 纯组合，状态写在 COMP。详情与模板见 [`reference.md`](reference.md)。

## 写产物纪律

1. 开笔前 Read `main_spec` 第4章（只读）、§5、`ui_manifest` 与相关 `ui/` 明细。
2. 一次对话一条主线；先清单后落盘；整块写。
3. 收尾：更新 §5 统计；`versions/{版本号}/iteration_notes.md` 文末追加业务变更流水（非则跳过）。

## 前置条件

已有 `main_spec.md`。⑧ 委派进入时 Read `ui_changes.md` 中 `待②` 条目。

## 输入

```yaml
版本号: v1.0.0
操作模式: add 或 modify
页面信息:
  - 页面编号: PAGE-MP-001
    页面名称: 首页
```

未指定版本号时按 master §1.1 取 `versions/` 最大版本。

## 执行步骤

1. 校验 `main_spec` 第4章终端；目标终端不在表中则停，交 ①。
2. 缺 `ui_manifest.md` / `ui/` 时按 [`reference.md`](reference.md) 创建索引骨架（立项兜底）。
3. 处理 MP 分包与 TabBar（`§3.1`）；更新 `§3.2` 页面索引与 `ui/PAGE-*.md`。
4. 涉及 COMP：更新 §4（含组件编号）与 `ui/COMP-*.md`（设计前提 + 状态矩阵必填）。
5. 更新 `main_spec` §5 统计；文末追加 `iteration_notes`（若有业务变更）。
6. 输出已改文件与页面编号。
