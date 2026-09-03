# 跨宿主 Agent 编排契约

本文件只规定任务如何拆分、委派、回收和降级，不改变十步流程、事实所有权或正式产物路径。主 Agent 在任何并行委派前必须完整 Read 本文件；子 Agent 只需读取自己的任务包与对应子技能。

## 1. 正确性原则

1. **并行是优化，不是前置条件**：有 subagent/Task 能力时 fan-out/fan-in；没有、被关闭、额度不足或并发槽不足时按同一依赖图顺序执行。两条路径必须生成相同正式产物并经过相同门禁。
2. **先锁边界再分片**：主 Agent 先确定工作版本、对象 ID、依赖、正式输出路径和共享文件，再启动子任务。产品事实未定时不得用多个 Agent 分别猜答案。
3. **一个正式文件一个写者**：同一轮内，每个可写路径只归一个 Agent。子 Agent 不写索引、壳层、流水、汇总报告或其他共享入口。
4. **主 Agent 单写并收口**：根四规范索引/注册表、`iteration_notes.md`、三类变更台账、`pages_prd/_shell/`、端级与总原型入口、`delivery_scope.md`、`sp_report.md` 和最终门禁/评审结论只由主 Agent 写。
5. **依赖优先于并发**：只有前置依赖全部完成的任务才能进入同一波次；波次内互不依赖，波次间等待全部有效结果后再继续。
6. **不为并行制造副本**：禁止把正式文件复制到 `versions/{v}/`、临时镜像目录或备用文件再合并。需要中间结论时优先让子 Agent 在返回消息中给结构化结果；确需临时文件时放系统临时目录并在交付前清理。

## 2. 宿主适配

主 Agent 先检查本轮实际暴露的工具和并发限制，只使用已存在的能力；禁止凭宿主名称猜工具。

| 宿主 | 已确认的优先调用方式 | fan-in / 降级 |
|------|----------------------|---------------|
| Codex（实际暴露 collaboration tools） | 对每个独立任务调用 `spawn_agent({task_name, message})`；完整逻辑 `task_id` 放在 `message`，`task_name` 另行规范化为小写字母/数字/下划线（如 `page_page_mp_003`），并保存返回的 agent id/canonical name。按本轮可用并发槽分波，不硬编码槽数。 | `wait_agent` 只代表收到一次 mailbox 更新，必须循环等待，并用 `list_agents` 确认本波所有目标均为终态后再 fan-in；需纠偏时用 `send_message`，已结束后续作业才用 `followup_task`。不可用时顺序执行。不得用用户可见新 task/thread 代替当前任务的 subagent。 |
| ChatGPT 其他表面 | 用自然语言明确要求“每个分片一个 subagent、并行执行、等待全部完成后汇总”；若实际工具 schema 已暴露，则按该 schema 调用。 | 不假定一定存在 `spawn_agent`/`wait_agent` 这些工具名；没有可确认的 subagent 原语时顺序执行。 |
| Cursor | 若本轮提供 `Task`，在同一条 Agent 消息中发起多个独立 Task 调用；已有自定义子代理时可用 `/name` 显式指定，未配置时使用可用通用 Task/自动委派。 | 前台任务直接收结果；后台任务保存返回的 agent ID，等待或恢复后再汇总。无 `Task` 时顺序执行。默认共享 checkout，必须遵守独占输出；不得假设已启用隔离 worktree。 |
| TraeWork CN | 先读本轮 `Task` 的实际 schema。若列出通用写任务类型，按 `Task(description="简短可见摘要", subagent_type="general_purpose_task", query="完整任务包", response_language="zh")` 调用；`response_language` 仅在 schema 提供时传入。每个分片调用一次并在同一轮并行发起；若只提供自动委派，则用任务描述明确要求启动 SubAgent。 | 等待全部 Task 返回后汇总。未暴露 Task、参数/类型不匹配或 SubAgent 被关闭时顺序执行。TraeCode 的 `.trae/agents/` 配置能力不得被当作 TraeWork 必备能力。 |
| 其他宿主 | 使用其明确暴露的并行任务原语，并套用本文件任务契约。 | 无可确认原语则顺序执行，不猜工具名或参数。 |

维护依据（2026-09-03 核验）：Codex Subagents 文档 `https://developers.openai.com/codex/multi-agent/`；Cursor Subagents 文档 `https://cursor.com/docs/context/subagents`；TRAE Subagent 文档 `https://docs.trae.cn/ide_subagents` 仅作为 TraeCode 概念旁证。TraeWork 的上述 `Task` 参数来自当前安装运行时内置工作流；公开文档、内置示例与当前工具不一致时，一律以本轮实际 schema 为准并降级。

## 3. 是否值得并行

同时满足才启动多个 Agent：

- 至少 2 个边界清晰、互不依赖的任务；
- 每个任务有独占输出，或完全只读并只返回结论；
- 启动与汇总成本低于顺序处理成本；
- 主 Agent 能在进入下一步前验证每个分片。

简单改字、单文件小修、同一文件多段编辑、尚未确定 ID/范围、强顺序数据依赖不并行。并发数取“宿主可用槽位”和“当前就绪任务数”的较小值，优先 2～4 个高价值分片；任务更多时分波，禁止为追求数量一次启动大量低价值 Agent。

## 4. 委派任务包

每个子任务提示必须自足，至少包含：

| 字段 | 必填内容 |
|------|----------|
| `task_id` | 任务包内稳定且唯一，如 `page-PAGE-MP-003`、`sp-fe`；它不是宿主调用名，Codex `task_name` 需另行规范化 |
| `step` | 十步编号与技能名；要求先 Read 对应 `SKILL.md` |
| `depends_on` | 已完成的前置任务 ID；无则写 `[]` |
| `read_inputs` | 允许读取的正式文件/章节，含工作版本 |
| `write_paths` | 独占正式输出路径；只读任务写 `[]` |
| `forbidden_paths` | 共享文件及所有非本任务路径；至少覆盖本步主写文件 |
| `acceptance` | 必须执行的自检、引用闭环与完成证据 |
| `return` | `status`、`changed_files`、`checks`、`open_questions`；不得只回复“完成” |

子 Agent 必须先完成只读前检，再写正式路径。遇到产品事实缺失、输入冲突或需要写禁止路径时，返回 `blocked` 与证据，不扩展职责；`blocked` 默认必须满足 `changed_files: []`。若写入后才发现失败，必须返回 `failed` 并列出实际变更，主 Agent 核对该独占路径、修复或重做并重新验收；验收前不得把半成品当作已完成产物。

## 5. 十步并行图

| 步骤 | 可并行分片 | 主 Agent 独占 / fan-in |
|------|------------|------------------------|
| ① 立项 | 大量输入资料的只读归纳、Story/术语候选核对 | 用户确认、ID/范围锁定、全部脚手架与根规范单写 |
| ② UI | 已锁定 PAGE/COMP ID 后，每个 `ui/PAGE-*.md` 或 `ui/COMP-*.md` 独占文件 | `ui_manifest.md` 的 §3 注册/索引、§4 组件索引、§5 收敛、台账状态和流水 |
| ③ API | 已锁定 API/EXT ID 后，每个 `api/API-*.md` 或 `api/EXT-*.md` 独占文件 | `api_spec.md` 索引/公共约定、跨接口冲突消解、台账状态和流水 |
| ④ Feature | Module 边界与 Feature ID 锁定后，每个 `feature/FEATURE-*.md` 独占文件 | Module 定义、`feature_spec.md` 索引/依赖、跨 Feature AC 去重、台账状态和流水 |
| ⑤ 单页 PRD | 每个 `pages_prd/{终端}/PAGE-*.md` 独占文件 | ⑤输入自检、桌面 `_shell`、跨页导航一致性、台账 `待⑤→已完成` |
| ⑥ 原型 | kit、共享资产和页面输入就绪后，每个业务 `PAGE-*.html` 独占文件 | kit/共享 assets、终端 `index.html`/`map.html`、`prototypes/index.html`、跨页连线与整体验收 |
| ⑦ 检查 | 路径/语义/原型/浏览器等只读检查维度；脚本互不写业务文件时可并行运行 | 去重、严重级排序、唯一 `NEXT_STEP_ROUTE`、Q-S/Q-P/full 总结论 |
| ⑧ 评审 | 用户价值、范围、验收、风险、证据层等只读评审维度 | 唯一产品判断与结论包；确认后单写 `delivery_scope.md`、Feature 状态和批准快照 |
| ⑨ SP | `sp-fe` 与 `sp-be` 并行；范围很大时可在两侧内部按 Feature 分波只返回明细 | 复用消重、校准、FE/BE 汇总、单写 `sp_report.md`，再单写刷新总入口 |
| ⑩ 迭代 | 大量自然语言变更可按页面/API/Feature三类只读解析与冲突检查 | 版本号、目录创建、三类台账、`eval_signals.md`、四规范变更记录与委派清单 |

②③④之间默认仍按事实依赖执行：②先锁 PAGE/COMP；随后③与④只有在输入已充分且互不等待时才可并行。任何一方引用尚未锁定对象时顺序执行。⑤必须等待本轮②③④相关分片全部收口；⑥等待⑤与Q-S；⑧等待Q-S与Q-P；⑨等待⑧最终通过且范围已确认；⑩等待⑧终态，结论有交付范围时还须等待⑨有效完成。

## 6. 回收与失败

1. 每波结束，主 Agent 收集所有 `status/changed_files/checks/open_questions`，并核对写路径没有交叉或越界。
2. 回收以“可独立验收对象/依赖组”为原子单位。某个 PAGE/API/Feature 等对象的明细、引用和自检已闭环时，主 Agent 可立即收口该对象对应的共享索引、台账与流水；失败对象保持原状态。只有跨对象不可分割的依赖组才等待整组通过后收口。
3. 一个分片失败不自动重做已通过且已收口的对象。能用现有事实修复则只重派失败任务；缺产品事实才停下询问。成功但尚未收口的独占产物必须在本轮结束前由主 Agent 接纳并收口，或明确标为未完成并在下一轮优先核对，禁止静默遗留孤立正式文件。
4. `blocked` 分片不得遗留正式文件变更；`failed` 若已写入，主 Agent 只处理其声明的独占路径，恢复到可验收状态或完成后再收口。子 Agent 声称完成但文件缺失、自检缺失或引用未闭环，也按失败处理。
5. 一个波次的所有就绪对象均完成“验收并收口”或明确失败处置后，才进入依赖它们的下一波；主 Agent 最后运行该步完整门禁。
6. 宿主中途失去并行能力时，主 Agent 从未完成任务开始顺序接管，不重写已验收并收口的独占产物。
