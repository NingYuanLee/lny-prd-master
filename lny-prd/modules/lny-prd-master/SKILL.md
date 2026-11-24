
## 入口协议

本技能只负责四件事：确认 PRD 根目录、归一化碎片输入、识别用户意图、按影响范围编排必要步骤。不要在这里展开子步骤的全部写作规范。

公共模块契约见 [`reference-module-contracts.md`](reference-module-contracts.md)。本文件负责总控决策，模块执行细节只在对应模块目录维护。

原型反馈或局部修改先读取 [`reference-change-routing.md`](reference-change-routing.md)，按 A～D 分类后走最小必要写入和检查范围。

规格和原型完成后按 [`reference-decision-walkthrough.md`](reference-decision-walkthrough.md) 自动对照前置产品决策走查。

执行强度按 [`reference-flexible-execution.md`](reference-flexible-execution.md) 调整。小范围可逆修改走快速路径，不因为缺少正式记录或完整门禁停止。

先检查 PRD 根目录：

1. 无非隐藏文件时走立项。
2. 有 `main_spec.md` 时读取状态并路由。
3. 有其他文件但没有 `main_spec.md` 时提示用户移入 PRD 根或开始立项，不擅自生成根规范。

默认模式是“智能按需推进”。用户只要求一个页面、接口、功能、检查或评审时，先计算最小必要依赖路径，再自动完成该目标需要的上下游步骤。用户说“继续”时，从最早未完成且与当前目标相关的步骤恢复。不要因缺少普通字段停止，按 `reference-smart-autopilot.md` 补齐并记录假设。

用户明确说“完整做完”“直接出可评审原型”“自动推进”“自动检查”或“一次做完规格三件套”时，先读取 [`reference-full-chain.md`](reference-full-chain.md)，再按其中的依赖链执行。一般产品目标也可以自动补齐必要规格并进入下游步骤，是否继续由用户目标、当前状态和影响范围决定。原型目标即使未说完整链，也自动补齐必要规格并进入⑥；页面设计决策按 [`reference-design-decision.md`](reference-design-decision.md) 自动完成，只有关键目标、品牌事实、资产或范围冲突时才询问使用者。⑥完成后自动执行作者自检和 Q-P，准备进入正式产品评审时才停下。

## 路由表

| 用户意图 | 读取 |
|---|---|
| 新项目、空目录、立项 | 本文“立项” |
| UI、页面清单、组件体验 | `modules/lny-prd-ui/SKILL.md` |
| API、接口语义 | `modules/lny-prd-api/SKILL.md` |
| Feature、业务规则、验收标准 | `modules/lny-prd-feature/SKILL.md` |
| 单页 PRD、页面数据流 | `modules/lny-prd-page/SKILL.md` |
| 原型、演示、页面实现 | `modules/lny-prd-prototype/SKILL.md` |
| 规格检查、原型检查、完整检查 | `modules/lny-prd-check/SKILL.md` |
| 需求或范围评审 | `modules/lny-prd-review/SKILL.md` |
| 估点、SP | `modules/lny-prd-sp/SKILL.md` |
| 新版本、新迭代 | `modules/lny-prd-iter/SKILL.md` |

进入子技能前读取 [`reference-common.md`](reference-common.md)。只有涉及对应场景时再读取 `reference-routing.md`、`reference-artifact-paths.md`、`framework-exclusions.md` 或 `reference-agent-orchestration.md`。

## 立项

立项时读取 [`reference-init.md`](reference-init.md) 和 [`framework-exclusions.md`](framework-exclusions.md)。输入可以是碎片化自然语言、一次性 YAML、文件、截图、链接或自然语言补充。模型从现有材料中提取项目名称、定位、用户问题、产品目标和终端范围，缺少普通信息时使用高可信推断或可逆默认继续，只有冲突、关键事实缺失或范围变化时询问。

确认摘要必须逐条展示将排除的能力类别。用户确认后创建：

- `main_spec.md`
- `ui_manifest.md`、`api_spec.md`、`feature_spec.md`
- `api/`、`ui/`、`feature/`
- `versions/v1.0.0/iteration_notes.md`

立项只初始化 `v1.0.0`。不要创建 `delivery_scope.md`，它只由⑧在用户确认评审结论后创建。立项完成后，如果用户没有明确“只做立项”，按智能自动推进协议路由到当前目标所需的下一步骤，不无条件扩展到无关能力。

## 子技能边界速查

| 步骤 | 正式产物 | 主要禁止 |
|---|---|---|
| ② | `ui_manifest.md`、`ui/` | 不改终端说明、API字段或原型 |
| ③ | `api_spec.md`、`api/` | 不写 UI 线框、路由或 JSON 契约 |
| ④ | `feature_spec.md`、`feature/` | 不写接口字段或 UI 线框 |
| ⑤ | `pages_prd/`、`_shell` | 不替代②③④、不写版本快照 |
| ⑥ | `prototypes/` | 不用 HTML 代替规格、不写版本原型副本 |
| ⑦ | 只读 Q-S/Q-P/full 报告 | 不改 PRD 正文 |
| ⑧ | 评审结论和批准快照 | 未确认不得落盘 |
| ⑨ | `sp_report.md`，必要时只刷总入口 | 不改范围、规格或业务页 |
| ⑩ | 新版本目录、台账、迭代信号 | 不写规格正文或生成 `pages_prd` |

## 收尾

结束时用四项短报：已完成、自动采用的关键假设、未完成或待确认、下一动作。原型完成后自动执行作者自检和 Q-P，准备进入正式产品评审时才停下。产物按 [`reference-common.md`](reference-common.md) 的精简规范写。完整公共规则见 [`reference-common.md`](reference-common.md)。完整自动链见 [`reference-full-chain.md`](reference-full-chain.md)。

### 1.2 Subagent 与并行编排

总控负责判断①的只读资料归纳是否值得并行，并确定本轮由②③④中的谁工作。存在独立分片时读取 `reference-agent-orchestration.md`；无 subagent/Task 时按同一依赖图顺序执行。

⑥ 只保留壳层与文件结构约束。原型页仍由 `modules/lny-prd-prototype/SKILL.md` 负责视觉与交互验收。

