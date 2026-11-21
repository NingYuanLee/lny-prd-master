---
name: lny-prd-master
description: >-
  LNY-PRD 的轻量入口与立项。Use for `/lny-prd-master`, 空目录立项、已有 PRD 项目的状态路由，
  or when the user explicitly asks to continue or choose the next PRD step. Direct step requests such as
  `/lny-prd-ui`, `/lny-prd-api`, `/lny-prd-feature`, `/lny-prd-page`, `/lny-prd-prototype`,
  `/lny-prd-check`, `/lny-prd-review`, `/lny-prd-sp`, and `/lny-prd-iter` should load their own skill directly.
  默认按请求执行，但原型目标会自动推进到原型完成。Q-P 不自动执行，原型完成后必须提示用户是否运行 Q-P。只有用户明确要求完整链、自动检查或自动推进时才读取 `reference-full-chain.md`。
---

## 入口协议

本技能只负责三件事：确认 PRD 根目录、识别用户意图、加载一个对应子技能。不要在这里展开子步骤的全部写作规范。

先检查 PRD 根目录：

1. 无非隐藏文件时走立项。
2. 有 `main_spec.md` 时读取状态并路由。
3. 有其他文件但没有 `main_spec.md` 时提示用户移入 PRD 根或开始立项，不擅自生成根规范。

默认模式是“按请求执行”。用户只要求一个页面、接口、功能、检查或评审时，只加载对应技能并在该步骤收尾。用户说“继续”时，从最早未完成步骤恢复，但仍不自动扩大到完整链。

用户明确说“完整做完”“直接出可评审原型”“自动推进”“自动检查”或“一次做完规格三件套”时，先读取 [`reference-full-chain.md`](reference-full-chain.md)，再按其中的依赖链执行。原型目标即使未说完整链，也自动补齐必要规格并进入⑥；页面设计决策按 [`reference-design-decision.md`](reference-design-decision.md) 自动完成，只有关键目标、品牌事实、资产或范围冲突时才询问使用者。⑥完成后先提示是否执行 Q-P，除非用户已经明确要求检查。

## 路由表

| 用户意图 | 读取 |
|---|---|
| 新项目、空目录、立项 | 本文“立项” |
| UI、页面清单、组件体验 | `lny-prd-ui/SKILL.md` |
| API、接口语义 | `lny-prd-api/SKILL.md` |
| Feature、业务规则、验收标准 | `lny-prd-feature/SKILL.md` |
| 单页 PRD、页面数据流 | `lny-prd-page/SKILL.md` |
| 原型、演示、页面实现 | `lny-prd-prototype/SKILL.md` |
| 规格检查、原型检查、完整检查 | `lny-prd-check/SKILL.md` |
| 需求或范围评审 | `lny-prd-review/SKILL.md` |
| 估点、SP | `lny-prd-sp/SKILL.md` |
| 新版本、新迭代 | `lny-prd-iter/SKILL.md` |

进入子技能前读取 [`reference-common.md`](reference-common.md)。只有涉及对应场景时再读取 `reference-routing.md`、`reference-artifact-paths.md`、`framework-exclusions.md` 或 `reference-agent-orchestration.md`。

## 立项

立项时读取 [`reference-init.md`](reference-init.md) 和 [`framework-exclusions.md`](framework-exclusions.md)。输入可以是一次性 YAML，也可以是自然语言补充。最少需要项目名称、产品定位、需求故事、产品目标和终端范围。

确认摘要必须逐条展示将排除的能力类别。用户确认后创建：

- `main_spec.md`
- `ui_manifest.md`、`api_spec.md`、`feature_spec.md`
- `api/`、`ui/`、`feature/`
- `versions/v1.0.0/iteration_notes.md`

立项只初始化 `v1.0.0`。不要创建 `delivery_scope.md`，它只由⑧在用户确认评审结论后创建。立项完成后，如果用户没有明确“只做立项”，按当前请求路由到下一步骤，不自动开启完整链。

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

结束时用四项短报：已完成、未完成、门禁状态、下一停点。原型完成后的下一停点默认是“等待用户决定是否执行 Q-P”。产物按 [`reference-common.md`](reference-common.md) 的精简规范写。完整公共规则见 [`reference-common.md`](reference-common.md)。完整自动链见 [`reference-full-chain.md`](reference-full-chain.md)。

### 1.2 Subagent 与并行编排

总控负责判断①的只读资料归纳是否值得并行，并确定本轮由②③④中的谁工作。存在独立分片时读取 `reference-agent-orchestration.md`；无 subagent/Task 时按同一依赖图顺序执行。

⑥ 只保留壳层与文件结构约束。原型页仍由 `lny-prd-prototype/SKILL.md` 负责视觉与交互验收。

