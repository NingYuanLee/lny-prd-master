---
name: lny-prd-check
description: >-
  横向只读质量门禁：Q-S 检查单页 PRD 完成后的规格闭环，Q-P 检查原型实现，full 依次执行两者；通过后判断是否具备⑧评审条件。不判断需求是否值得做，不修改仓库文件。
  Use when the user mentions /lny-prd-check, @lny-prd-check, PRD 检查, 文档验收, 估点就绪度, or 交付门禁.
---

## 与总控的关系

本技能保留 **⑦ `/lny-prd-check`** 编号，但不是⑥之后的一次性串行步骤，而是横向门禁：⑤后自动执行 **⑦/Q-S**，⑥作者自检后自动执行 **⑦/Q-P**。两者均通过后才询问是否进入⑧；用户已明确要求评审时可同轮直接进入⑧。显式调用未指定模式时执行 `full`。只读输出报告与定向委派，不改任何文件。

## 模式

| 模式 | 时机 | 检查范围 | 通过后 |
|------|------|----------|--------|
| `Q-S` | ⑤完成后 | `reference-checks.md` 第一部分文档性 + 第三部分估点信号；根 `pages_prd/` 纳入闭环 | 自动进入⑥；明确“只要规格”则停止 |
| `Q-P` | ⑥作者自检后 | 第二部分功能性与原型符合规格；须有本轮有效Q-S，否则先补跑Q-S | 询问是否进入⑧；用户已明确要求评审则直接进入 |
| `full` | 显式检查未限定对象 | 先Q-S，再在有业务原型时Q-P | 给出是否具备⑧评审条件 |

门禁失败时不询问“是否修复”：可由责任技能依据现有事实自动修复的，同轮定向返修并重跑该门禁；缺产品事实、外部输入或用户取舍时才停止询问。Q-P发现规格问题必须回②③④⑤与Q-S，不能只改HTML掩盖。

# 检查 `/lny-prd-check`

## Additional resources

- 检查表全文：[`reference-checks.md`](reference-checks.md)
- 跨步骤页型不变量：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 路径扫描器：`scripts/verify-artifact-paths.py`
- 跨文档语义扫描器：`scripts/validate-prd-project.py`
- 原型浏览器冒烟：`../lny-prd-prototype/scripts/verify-prototype-browser.mjs`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 职责与禁止

- **负责**：按模式检查文档性、功能性、估点信号与评审就绪度；判定产品链可估、FE/BE/迭代信号是否齐，并输出门禁结果、责任步骤与“是否具备⑧条件”（**不计 SP**）。
- **禁止**：改规格/台账/原型/流水；本步计算或写入标准工时点（属 ⑨）。
- **不做产品评审**：不判断需求是否值得做、范围是否合理或是否应该批准；这些属于 ⑧ `/lny-prd-review`。

开笔前 Read `lny-prd-master/framework-exclusions.md`。规格重复展开框架能力 → 🔴 阻塞。

## 工作版本

用户显式 `vX.Y.Z` 且目录存在则用之，否则 `versions/` 最大 semver。报告抬头写明版本。

## 执行步骤

1. 解析工作版本；目录须已存在。
2. 选择模式。`Q-S`/`full`：Read产物路径契约与共享页型不变量，运行两个Python扫描器，再按 [`reference-checks.md`](reference-checks.md) 第一、第三部分检查根 `pages_prd/` 工作源。扫描器的 `NEXT_STEP_ROUTE:` 作为自动返修建议。
3. `Q-P`/`full`：确认有本轮有效Q-S；按检查表第二部分对照根工作源与原型。宿主可解析 `playwright` 与 `pngjs` 时运行浏览器脚本；exit 1逐页列问题，exit 2只披露环境缺失并继续静态检查。不得在业务项目安装npm依赖。
4. 输出模式、门禁结果、通篇连续问题序号与责任步骤。Q-S失败回②③④⑤；Q-P纯实现失败回⑥；Q-P发现规格根因回②③④⑤并重新走Q-S→⑥→Q-P。
5. Q-S与Q-P均通过且存在产品取舍对象时，输出“具备⑧评审条件”。自动主链在此询问产品是否进入⑧；显式评审请求不重复询问。已有⑧批准范围且产品链可估时才建议⑨。

须关注项用 🔴/🟠/🟢。齐/可估/无缺口不占序号。
