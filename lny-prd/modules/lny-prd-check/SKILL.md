
## 与总控的关系

本技能保留 **⑦ `$lny-prd`** 编号，但不是⑥之后的一次性串行步骤，而是横向门禁：⑤后按影响范围执行 **⑦/Q-S**，⑥作者自检后按影响范围执行 **⑦/Q-P**。两者通过后完成自动验证；只有当前目标需要正式评审或出现产品决策冲突时才进入⑧。显式调用未指定模式时执行 `full`。只读输出报告与定向委派，不改任何文件。

## 模式

| 模式 | 时机 | 检查范围 | 通过后 |
|------|------|----------|--------|
| `Q-S` | ⑤完成后 | `reference-checks.md` 第一部分文档性 + 第三部分估点信号；根 `pages_prd/` 纳入闭环 | 自动进入⑥；明确“只要规格”则停止 |
| `Q-P` | ⑥作者自检后 | 第二部分功能性与原型符合规格；须有本轮有效Q-S，否则先补跑Q-S | 完成自动验证；需要正式评审时进入⑧ |
| `full` | 显式检查未限定对象 | 先Q-S，再在有业务原型时Q-P | 给出是否具备⑧评审条件 |

门禁失败时不询问“是否修复”：可由责任技能依据现有事实自动修复的，同轮定向返修并重跑该门禁；缺产品事实、外部输入或用户取舍时才停止询问。Q-P发现规格问题必须回②③④⑤与Q-S，不能只改HTML掩盖。

# 检查 `$lny-prd`

## Additional resources

- 检查表全文：[`reference-checks.md`](reference-checks.md)
- 跨步骤页型不变量：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 路径扫描器：`scripts/verify-artifact-paths.py`
- 跨文档语义扫描器：`scripts/validate-prd-project.py`
- 事实一致性扫描器：`scripts/audit-fact-consistency.py`
- 决策兑现扫描器：`scripts/audit-decision-walkthrough.py`
- 原型浏览器冒烟：`../modules/lny-prd-prototype/scripts/verify-prototype-browser.mjs`
- 框架排除：`modules/lny-prd-master/framework-exclusions.md`
- 统一检查报告：`modules/lny-prd-master/reference-check-report.md`

## 职责与禁止

- **负责**：按模式检查文档性、功能性、估点信号与评审就绪度；判定产品链可估、FE/BE/迭代信号是否齐，并输出门禁结果、责任步骤与“是否具备⑧条件”（**不计 SP**）。
- **不评审主观审美**：不替产品决定品牌偏好或视觉方向；Q-P 会检查视觉方向是否落地、素材是否可实现、真实渲染是否通过客观门槛，并读取 `score-visual-quality.mjs` 的结果。
- **禁止**：改规格/台账/原型/流水；本步计算或写入标准工时点（属 ⑨）。
- **不做产品评审**：不判断需求是否值得做、范围是否合理或是否应该批准；这些属于 ⑧ `$lny-prd`。

开笔前 Read `modules/lny-prd-master/framework-exclusions.md`。规格重复展开框架能力 → 🔴 阻塞。

## 工作版本

用户显式 `vX.Y.Z` 且目录存在则用之，否则 `versions/` 最大 semver。报告抬头写明版本。

## 并行分片

需要并行时完整 Read [`../lny-prd-master/reference-agent-orchestration.md`](../lny-prd-master/reference-agent-orchestration.md)。路径、跨文档语义、单页规格、原型静态与浏览器冒烟等互不写业务文件的检查可作为只读子任务并行；每个子 Agent 只返回带文件/位置/严重级/责任步骤的发现。主 Agent 必须等待全部检查完成，统一去重、排序并给出唯一门禁结论与 `NEXT_STEP_ROUTE`。任何子 Agent 都不得修改被检查产物；无 subagent/Task 时顺序执行完整检查表。

## 执行步骤

1. 解析工作版本；目录须已存在。
2. 选择模式。`Q-S`/`full`：Read产物路径契约与共享页型不变量，运行两个Python扫描器，再按 [`reference-checks.md`](reference-checks.md) 第一、第三部分检查根 `pages_prd/` 工作源。扫描器的 `NEXT_STEP_ROUTE:` 作为自动返修建议。
3. `Q-P`/`full`：确认有本轮有效Q-S；按检查表第二部分对照根工作源与原型。宿主可解析 `playwright` 与 `pngjs` 时运行浏览器脚本、保留真实渲染截图并运行 `score-visual-quality.mjs`。exit 1逐页列问题，exit 2只披露环境缺失并继续静态检查。不得在业务项目安装npm依赖。
4. 输出模式、门禁结果、通篇连续问题序号与责任步骤。Q-S失败回②③④⑤；Q-P纯实现失败回⑥；Q-P发现规格根因回②③④⑤并重新走Q-S→⑥→Q-P。
5. Q-S与Q-P均通过且存在产品取舍对象时，输出“具备⑧评审条件”。只有当前目标需要正式评审时才进入⑧。已有⑧批准范围且产品链可估时才建议⑨。

须关注项用 🔴/🟠/🟢。齐/可估/无缺口不占序号。

## 按检查类型读取规则

Q-S 读取 `reference-q-s.md`，Q-P 读取 `reference-q-p.md`，full 读取 `reference-full.md` 并依次执行 Q-S 与 Q-P。常规单项检查不读取完整 `reference-checks.md`，只有复杂失败复核时才读取对应章节。

## 产物长度

正式产物遵守 `../lny-prd-master/reference-common.md` 的产物精简规范。只写本步骤新增的事实和决策，重复内容用编号或路径引用。
