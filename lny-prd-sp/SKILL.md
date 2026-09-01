---
name: lny-prd-sp
description: >-
  按指定版本汇总 FE/BE 标准工时点（1 SP = 1 个有效工程小时），覆盖写入
  versions/{v}/sp_report.md。只读规格与台账，不改正文。Use when the user mentions
  /lny-prd-sp, @lny-prd-sp, 故事点, 估点, 工时点, SP, sp_report.
---

## 与总控的关系

本步为 **⑨ `/lny-prd-sp`**，位于 ⑧ 评审确认之后、⑩ 新迭代之前。只按 `delivery_scope.md` 已确认的交付范围写 `versions/{v}/sp_report.md`，禁止退回全量 active 规格猜范围。落盘后 **同一轮** 按总控 **§3.3** 交 ⑥「只刷总入口」（Read `lny-prd-prototype/SKILL.md` 该节 + `reference-scope.md`），禁止本步手改 HTML，禁止停下来只说「交总控」。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑩ 追加。

# 版本标准工时点 `/lny-prd-sp`

## Additional resources

- 权重表与报告模板：[`reference-weights.md`](reference-weights.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)

## 职责与禁止

- **负责**：按版本计算 FE_SP / BE_SP；同版本重跑直接覆盖报告；落盘后同轮交 ⑥ 只刷总入口。
- **禁止**：改规格/台账/`eval_signals`/DDL/人员排期；手改 `prototypes/`（含 `index.html`）；产品链不可估时仍写报告但停算（数值用 `—`），**仍须**刷总入口。

本技能的 `SP` 是**标准工时点**：`1 SP = 1 个有效工程小时`。它表示熟悉项目的工程师在规格完整、现有工程与公共组件可用时，用于实现、开发自测、常规联调和常规评审修正的净投入。等待外部排期、需求/设计返工、环境事故和不可预见故障不计入。FE_SP + BE_SP 是总人时，不是可直接换算的日历工期、人数承诺或发布日期。

默认使用 `hour-v1` 经验基准。没有真实工时样本时，FE/BE 校准系数均为 `1.0（暂定）`，禁止声称已完成团队校准；用户明确给出系数，或至少 3 个已完成版本的 FE/BE 实际小时后，才按权重说明计算并使用团队系数。

可选输入：`FE校准系数`、`BE校准系数`，以及有明确证据的对象级复用关系。系数须为正数；不得仅凭页面相似、终端相近或“通常会共用代码”自行折减。

```yaml
版本号: v1.2.0
FE校准系数: 0.85        # 可选；无可靠样本则省略
BE校准系数: 0.90        # 可选；无可靠样本则省略
复用关系:                # 可选；仅列有证据的对象
  PAGE-H5-003: 同代码跨端适配自 PAGE-MP-003
```

## 计分范围

- 先读取目标版本 `delivery_scope.md`。只纳入其中已确认的 `本期开发` Feature 及其 PAGE/API/EXT 证据；不得把全部 active Feature 当默认范围。
- 有台账时，在已确认 Feature 范围内按本版变更对象计分，并应用变更形态 × 存量数据影响。
- 无有效台账行时，按已确认的 `本期开发` Feature 全量计分。
- `本期下线` 只计算台账中明确登记的下线实现影响，不把 deprecated Feature 正文当新增实现量。
- `评审结论=不进入本期` 时无交付范围，明确回复“本版本无需估点”，不创建空 `sp_report.md`。

## 门禁

1. 产品链不可估 → 结论「不可估」，不输出数值合计。
2. FE 信号不全 → `FE_SP` 为 `—`。
3. BE 信号不全 → `BE_SP` 为 `—`。
4. 任一侧为 `—` 则合计为 `—`。

## 前置条件

存在 `versions/{版本号}/`，且 ⑧ 已创建 `delivery_scope.md`。范围须为产品确认后的终态：新格式 `评审结论=通过`、`评审状态=approved`、确认/阻塞数为 0、无 `open` 决策；旧格式缺 `评审结论` 时，范围及所有 Feature 行均 `approved`、计数为 0、无 `open` 决策可兼容视为通过。未指定版本则取 `versions/` 最大版本并写进报告抬头。

## 执行步骤

1. 解析版本；先读 `delivery_scope.md` 并锁定已确认 Feature 范围，再判定全量或本版变更。范围缺失、未确认或仍有 open 决策时停止估点并建议回 ⑧，不写报告。
2. 读范围内 Feature 对应的 `ui/PAGE`、`pages_prd` §5/§7、`api/`、`feature/`、`eval_signals.md`（若有）。
3. 产品链门禁。不可估则数值用 `—`，不编造合计；**不要结束**。
4. 可估则 Read [`reference-weights.md`](reference-weights.md) 计算（先算对象基准点，再应用单一实现系数，最后分别应用 FE/BE 校准系数；明细按小计降序；报告末可选附录「压缩候选」，不进合计、不换算工期、不宣布 MVP）；不可估则跳过本步。
5. 覆盖写入 `sp_report.md`（UTF-8）。默认不写 `iteration_notes`。对话必须按下列五行回报，禁止只报三个数字：

```text
FE_SP：{n / —}
BE_SP：{n / —}
合计：{n / —}
校准系数：FE {1.0（暂定） / n（来源）}；BE {1.0（暂定） / n（来源）}
口径：合计是标准工程人时，不是日历工期、人数或发布日。
```

无用户给出的系数、且不满 3 个已完成版本的实际小时样本时，必须写 `1.0（暂定）`，禁止写「已校准」。

6. **只刷总入口**：Read `lny-prd-prototype/SKILL.md`「只刷总入口」与 [`../lny-prd-prototype/reference-scope.md`](../lny-prd-prototype/reference-scope.md)。有任一 `prototypes/{终端}/` 则覆盖刷新 `prototypes/index.html`；无则跳过并说明。禁止重画各端页面或写 `versions/{v}/prototypes/`。
