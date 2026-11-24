---
name: lny-prd
description: >-
  LNY PRD Workflow 统一工作流。根据用户意图和 PRD 项目状态按需加载立项、UI、API、Feature、单页 PRD、原型、检查、评审、估点或迭代规则，维护规格与原型的一致性。原型步骤产出可直接演示的高保真单页、真实感模拟数据和有依据的视觉表达。Use for PRD projects, requirements, UI, API, feature specs, page PRDs, prototypes, checks, reviews, estimation, or iteration work.
---

# LNY PRD Workflow 统一入口

本技能是 LNY PRD Workflow 的唯一公开入口。先读取 `modules/lny-prd-master/SKILL.md` 与 [`modules/lny-prd-master/reference-smart-autopilot.md`](modules/lny-prd-master/reference-smart-autopilot.md)，确认项目根目录、用户意图和当前状态，再只加载本轮需要的步骤模块。不要一次读取所有模块。

模块输入、产物、写入边界和下一跳以 `modules/lny-prd-master/reference-module-contracts.md` 为公共索引。模块细节与模板仍以当前模块文件为准。

控制面文件职责见 `modules/lny-prd-master/reference-control-plane.md`，检查输出统一遵守 `modules/lny-prd-master/reference-check-report.md`。

规格和原型完成后按 [`modules/lny-prd-master/reference-decision-walkthrough.md`](modules/lny-prd-master/reference-decision-walkthrough.md) 自动对照最初产品决策走查。只有决策冲突、范围变化或不可逆取舍才请求产品确认。

完整路由图见 [`modules/lny-prd-master/reference-workflow-map.md`](modules/lny-prd-master/reference-workflow-map.md)。

执行弹性和检查强度按 [`modules/lny-prd-master/reference-flexible-execution.md`](modules/lny-prd-master/reference-flexible-execution.md) 判断。规则保护事实和决策，不要求每次输入都走完整链。

对外按五个阶段理解工作流：理解与决策、规格与原型、自动验证、交付准备、发布学习。内部步骤按影响范围自动选取。

“理解与决策”内部包含一个可选的探索讨论分支。明确反馈和证据充分时直接跳过，问题模糊、假设冲突或需要比较方案时进入 Discovery。

## 按需加载

| 用户意图 | 读取模块 |
|---|---|
| 新项目、空目录、立项、继续或选择下一步 | `modules/lny-prd-master/SKILL.md` |
| UI、页面清单、组件、视觉和交互 | `modules/lny-prd-ui/SKILL.md` |
| 用户问题、证据、假设、访谈、实验和机会 | `modules/lny-prd-discovery/SKILL.md` |
| API、接口、字段语义 | `modules/lny-prd-api/SKILL.md` |
| Feature、业务规则、验收标准 | `modules/lny-prd-feature/SKILL.md` |
| 单页 PRD、页面数据流、业务壳 | `modules/lny-prd-page/SKILL.md` |
| 原型、演示、页面实现 | `modules/lny-prd-prototype/SKILL.md` |
| 规格检查、原型检查、完整检查 | `modules/lny-prd-check/SKILL.md` |
| 需求或交付范围评审 | `modules/lny-prd-review/SKILL.md` |
| 估点、标准工时 | `modules/lny-prd-sp/SKILL.md` |
| 新版本、新迭代、变更台账 | `modules/lny-prd-iter/SKILL.md` |
| 发布反馈、指标、实验结果和复盘回流 | `modules/lny-prd-learning/SKILL.md` |

进入任何步骤前先读取 `modules/lny-prd-master/reference-common.md`。智能自动推进按 [`modules/lny-prd-master/reference-smart-autopilot.md`](modules/lny-prd-master/reference-smart-autopilot.md) 计算最小必要路径。项目位于代码库或多人协作目录时，按 [`modules/lny-prd-master/reference-repository-sharing.md`](modules/lny-prd-master/reference-repository-sharing.md) 判断共享与本地文件。只有当前规则明确引用时，再读取对应模块的 `reference*.md`、`reference/`、`kit/` 或 `scripts/` 文件。用户明确要求完整做完、自动推进或自动检查时，再读取 `modules/lny-prd-master/reference-full-chain.md` 补充完整链规则。

## 上下文边界

- 本轮只加载当前步骤、必要的公共规则和直接依赖。
- 输入可以是碎片化自然语言、文件、截图、链接或局部修改意见。普通缺字段由模型按上下文补全并记录假设，不要求用户先填写完整 YAML。
- 用户当前明确意图、已批准事实、项目现有事实、高可信推断和可逆默认按优先级参与决策。冲突、范围变化、关键事实缺失或批准动作才暂停询问。
- `product_workspace.md`、`evidence_log.md` 和 `learning_log.md` 作为可选工作台记录，由总控按需维护，不替代正式规格正本。
- 完成当前步骤后，根据台账和用户请求决定下一步，不预加载后续模块。
- `COMP-*` 作为 UI 模块中的跨页公共组件复用，页面原型实现必须读取被引用的组件明细。
- `ui/visual/`、`COMP-*` 和可选的 `project-theme.css` 提供视觉参考与组件复用，详见 `modules/lny-prd-ui/reference/visual-consistency.md`。
- 原型步骤默认按演示级高保真协议生成可直接打开的业务页面，包含真实感模拟数据、完整默认态和可操作反馈。具体规则按需加载 `modules/lny-prd-prototype/reference-demo-fidelity.md`。
- 原型壳层和总入口使用技能内置的固定样式与交互，业务单页保持独立的视觉设计空间。
- 所有模块文档位于本技能目录内，`modules/` 下的 `SKILL.md` 是内部步骤说明，不是独立技能入口。

## 兼容调用

旧的 `/lny-prd-master`、`/lny-prd-ui` 等名称统一改用 `$lny-prd`，并在请求中说明目标步骤，例如“用 UI 步骤设计页面”或“继续生成原型”。

