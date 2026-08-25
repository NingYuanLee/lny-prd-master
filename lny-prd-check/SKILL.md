---
name: lny-prd-check
description: >-
  只读检查 PRD：文档一致性、功能性验收、产品就绪度（含估点信号）。不修改仓库文件。
  Use when the user mentions /lny-prd-check, @lny-prd-check, PRD 检查, 文档验收, 产品就绪度.
---

## 与总控的关系

本步为 **⑦ `/lny-prd-check`**。只读报告 + 委派建议，不改任何文件。用户确认后由总控执行子技能。全流程见 `lny-prd-master/SKILL.md`。

# 检查 `/lny-prd-check`

## Additional resources

- 检查表全文：[`reference-checks.md`](reference-checks.md)
- 跨步骤页型不变量：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与唯一镜像范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 路径扫描器：`scripts/verify-artifact-paths.py`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 职责与禁止

- **负责**：三大块全检（文档性 | 功能性 | 产品就绪度）；判定产品链可估与 FE/BE/迭代信号是否齐（**不计 SP**）。
- **禁止**：改规格/台账/原型/流水；本步计算或写入标准工时点（属 ⑨）。

开笔前 Read `lny-prd-master/framework-exclusions.md`。规格重复展开框架能力 → 🔴 阻塞。

## 工作版本

用户显式 `vX.Y.Z` 且目录存在则用之，否则 `versions/` 最大 semver。报告抬头写明版本。

## 执行步骤

1. 解析工作版本；目录须已存在。
2. **文档性**：Read 产物路径契约与共享页型不变量；先运行 `python <skillDir>/scripts/verify-artifact-paths.py <prdRoot>`，再按 [`reference-checks.md`](reference-checks.md) §1.1→1.6。扫描命中逐项列为高优先级，不删除文件。
3. **功能性**：先过「无原型」门禁；有原型则按规格外 / 文案 / 主路径 / 实现符合规格。
4. **产品就绪度**：§3.1 虚引用 + FE 三维 + BE 四维 +（有台账时）迭代信号。
5. 输出报告（通篇连续序号）+ 委派建议（`#序号`）。可估且信号较齐时建议总控跑 `/lny-prd-sp`。

须关注项用 🔴/🟠/🟢。齐/可估/无缺口不占序号。
