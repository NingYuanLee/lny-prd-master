---
name: lny-prd-sp
description: >-
  按指定版本汇总 FE/BE 故事点，覆盖写入 versions/{v}/sp_report.md。只读规格与台账，不改正文。
  Use when the user mentions /lny-prd-sp, @lny-prd-sp, 故事点, 估点, SP, sp_report.
disable-model-invocation: true
---

## 与总控的关系

本步为 **⑨ `/lny-prd-sp`**。只写 `versions/{v}/sp_report.md`。落盘后 **同一轮** 按总控 **§3.3** 交 ⑥「只刷总入口」（Read `lny-prd-prototype/SKILL.md` 该节 + `reference-scope.md`），禁止本步手改 HTML，禁止停下来只说「交总控」。建议在 ⑦ 产品链可估之后。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑧ 追加。

# 版本故事点 `/lny-prd-sp`

## Additional resources

- 权重表与报告模板：[`reference-weights.md`](reference-weights.md)
- 原理说明书：仓库 `README.md` 第八章

## 职责与禁止

- **负责**：按版本计算 FE_SP / BE_SP；同版本重跑直接覆盖报告；落盘后同轮交 ⑥ 只刷总入口。
- **禁止**：改规格/台账/`eval_signals`/DDL/人天；手改 `prototypes/`（含 `index.html`）；产品链不可估时仍写报告但停算（数值用 `—`），**仍须**刷总入口。

## 计分范围

- 无有效台账行 → 全量 active 规格。
- 有台账 → 仅本版变更对象，乘变更形态 × 存量数据影响。

## 门禁

1. 产品链不可估 → 结论「不可估」，不输出数值合计。
2. FE 信号不全 → `FE_SP` 为 `—`。
3. BE 信号不全 → `BE_SP` 为 `—`。
4. 任一侧为 `—` 则合计为 `—`。

## 前置条件

存在 `versions/{版本号}/`。未指定则取 `versions/` 最大版本并写进报告抬头。

## 执行步骤

1. 解析版本；判定全量或本版变更。
2. 读 `ui/PAGE`、`pages_prd` §5/§7、`api/`、`feature/`、`eval_signals.md`（若有）。
3. 产品链门禁。不可估则数值用 `—`，不编造合计；**不要结束**。
4. 可估则 Read [`reference-weights.md`](reference-weights.md) 计算（明细按小计降序；报告末可选附录「压缩候选」，不进合计、不换算人天、不宣布 MVP）；不可估则跳过本步。
5. 覆盖写入 `sp_report.md`（UTF-8）。对话回报 FE_SP / BE_SP / 合计三行。默认不写 `iteration_notes`。
6. **只刷总入口**：Read `lny-prd-prototype/SKILL.md`「只刷总入口」与 [`../lny-prd-prototype/reference-scope.md`](../lny-prd-prototype/reference-scope.md)。有任一 `prototypes/{终端}/` 则覆盖刷新 `prototypes/index.html` 及 `versions/{v}/prototypes/index.html`；无则跳过并说明。禁止重画各端页面。
