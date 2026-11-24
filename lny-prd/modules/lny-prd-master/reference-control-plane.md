# 总控职责与唯一事实源

本文件只定义内部控制文档的职责，避免入口、路由、流程图和模块契约互相复制。

| 文件 | 唯一职责 | 不负责 |
|---|---|---|
| `reference-smart-autopilot.md` | 输入归一化、探索判断、最小依赖路径和停止条件 | 具体状态表、模块产物细节 |
| `reference-routing.md` | 按项目状态和用户目标选择责任步骤 | 解释完整工作方法、重复自动算法 |
| `reference-module-contracts.md` | 模块输入、产物、写入边界和下一跳 | 用户对话路由和检查报告格式 |
| `reference-workflow-map.md` | PM 视图和流程可视化 | 作为 Agent 的执行规则 |
| `reference-change-routing.md` | 原型反馈 A/B/C/D 影响分类 | 替代产品决策或完整迭代台账 |
| `reference-flexible-execution.md` | 检查强度、记录强度和宿主工具选择 | 定义业务流程或产品范围 |
| `reference-check-report.md` | Q-S、Q-P、自动走查的统一报告格式 | 判断产品价值或批准范围 |

当多个文件出现同一条规则时，以本表对应的唯一职责文件为准，其他文件只保留入口引用和必要摘要。

