# 模块契约索引

本文件是统一入口内部模块的导航索引。模块自身的 `SKILL.md` 负责执行细节，模板和检查表负责具体格式。本表只维护模块之间不会重复的公共契约。

## 读取顺序

1. 读取 `modules/lny-prd-master/SKILL.md`，确认项目根目录、当前版本和用户要求。
2. 读取本文件，确定当前步骤的输入、正式产物和下一跳。
3. 读取 `reference-common.md`。
4. 读取当前模块的 `SKILL.md`。
5. 只加载当前模块明确引用的模板、参考资料和脚本。

完整自动链只有用户明确要求完整完成、自动推进或自动检查时才读取 `reference-full-chain.md`。

## 步骤契约

| 步骤 | 模块 | 输入重点 | 正式产物 | 写入边界 | 默认下一跳 |
|---|---|---|---|---|---|
| ① | `lny-prd-master` | 项目目录、碎片输入、用户意图、当前状态 | 根规范、项目骨架、工作台记录 | 立项文件、总控状态、`product_workspace.md`、`evidence_log.md`、`learning_log.md` | 按影响范围自动路由 |
| Discovery | `lny-prd-discovery` | 用户反馈、访谈、竞品、数据和当前假设 | 证据与假设记录 | `evidence_log.md`、按确认结果回流正式规格 | 按影响范围回到规格或验证 |
| ② | `lny-prd-ui` | 根规范、Feature、API、既有 UI 事实 | `ui_manifest.md`、`ui/` | UI 结构、交互、视觉方向 | ③ / ④ |
| ③ | `lny-prd-api` | 根规范、页面需求、Feature | `api_spec.md`、`api/` | API 与 EXT 需求语义 | ④ |
| ④ | `lny-prd-feature` | Story、根规范、页面和 API 输入 | `feature_spec.md`、`feature/` | Module、Feature、AC | ⑤ |
| ⑤ | `lny-prd-page` | UI、API、Feature 三件套 | `pages_prd/`、`_shell/` | 单页 PRD 与页面线框 | ⑦/Q-S |
| ⑥ | `lny-prd-prototype` | 根 `pages_prd/`、UI 明细、COMP | `prototypes/` | 当前原型与入口壳 | ⑦/Q-P |
| ⑦ | `lny-prd-check` | 当前版本和根工作源 | 只读检查报告 | 不改业务产物 | 责任步骤返修 |
| ⑧ | `lny-prd-review` | 检查证据、版本范围、产品目标 | 评审结论、批准范围 | 仅确认后写评审事实 | ⑨ 或返修 |
| ⑨ | `lny-prd-sp` | 已确认交付范围 | `sp_report.md` | 估点报告与原型总入口版本清单 | ⑩ 或结束 |
| ⑩ | `lny-prd-iter` | 上版终态、SP、未清台账 | 新版本壳与变更台账 | 版本目录和变更记录 | ② |
| Learning | `lny-prd-learning` | 发布反馈、指标、实验结果和复盘 | 发布学习记录 | `learning_log.md`、证据同步和回流委派 | 按影响范围进入返修或迭代 |

## 不变量

- 根工作源是当前事实。`versions/` 只保存版本证据和迭代记录，不作为当前步骤的写入目标。
- 同一身份事实在索引、明细和单页 PRD 中出现时，索引或上游明细是正本，其他位置必须与正本逐项一致。Q-S 运行 `audit-fact-consistency.py` 捕获漏改。
- 每个正式文件只有一个负责步骤。其他步骤只能读取、引用或报告缺口。
- Q-S 和 Q-P 是只读门禁。失败时回到负责产物的步骤修复。
- 评审结论未经用户确认不得写成批准事实。
- 原型只读取根 `pages_prd/`，不得把原型复制到版本目录。
- 新版本只能由 ⑩ 创建。普通修改留在当前版本工作源。

