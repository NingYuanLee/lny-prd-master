# 领域模块、Feature 产物模板与双图规范

立项与本步维护均 Read 本节落盘。新功能只用 `FEATURE-{三位序号}`；历史 `FEATURE-MP-001` 只读兼容、禁止新项目再用。

> 本文件中代码块内是项目产物模板，代码块外是 Agent 写作说明。生成项目文档时不得把代码块外说明或 `SKILL.md` 的治理规则复制进去。

## feature_spec.md 模板

> **单一事实源**：`feature_spec.md` 的领域模块定义与 Feature 索引骨架 **只在本节维护**；立项 **`/lny-prd-master`** 与本步 **`/lny-prd-feature`** 均 **Read 本节** 落盘或更新。不新增独立 Module 技能或 `module/` 目录。

```markdown
# 功能规格说明书 - {项目名称}

> 本文件记录领域边界、公共语义与 Feature 导航；单功能规则、流程和验收见 `feature/FEATURE-*.md`。

## 文档信息

| 属性 | 内容 |
|------|------|
| 文档版本 | v1.0.0 |
| 创建日期 | {创建日期} |
| 最后更新 | {更新日期} |
| 维护人 | 产品经理 |
| 状态 | 草稿 |

### 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|----------|------|
| v1.0.0 | {创建日期} | 初始版本 | 产品经理 |

## 1. 文档范围与关系

本文件维护公共语义、领域模块定义与 Feature 导航；单功能事实见 `feature/FEATURE-*.md`。

### 1.1 与根规格的分工

| 文档 | 职责 |
|------|------|
| `main_spec.md` | 项目概述、需求故事、终端说明（第4章）、各域入口（§5 UI / §6 API / §7 Feature） |
| `ui_manifest.md` + `ui/` | 页面/组件布局与 UI 状态（**不写**业务流程正文） |
| `api_spec.md` + `api/` | 接口需求（**不写**跨页流程编排） |
| **`feature_spec.md` + `feature/`** | **领域模块边界 + 业务能力级**规则、流程、验收、关联 `STORY-*` / `PAGE-*` / `API-*` / `EXT-*` |

### 1.2 引用与闭环

- Feature 索引与 `feature/FEATURE-*.md` 明细一一对应；索引只提供编号、名称和路径。
- Story 本身定义在 `main_spec.md`；Story 与 Feature 的关系记录在 Feature 明细的「关联 STORY」。
- Module 边界记录在本文件；Feature 明细通过「模块编号」归属唯一 Module。
- 页面与接口关系记录在 Feature 明细的 `PAGE-*`、`API-*`、`EXT-*` 引用中。

## 2. 公共语义

- **Feature 编号**：`FEATURE-{三位序号}`；历史项目可能保留带终端码的旧编号。
- **规格状态**：`draft` / `active` / `deprecated`。
- **评审状态**：`pending` / `reviewing` / `approved` / `blocked`。
- **优先级**：`P0` / `P1` / `P2`。
- **来源与归属**：每个 Feature 关联至少一个 `STORY-*`，并归属唯一 `MODULE-*`。
- **关联对象**：页面使用 `PAGE-*`，内部接口使用 `API-*`，第三方接口使用 `EXT-*`；确无关联时记为「无」。

## 3. 领域模块定义

> Module 表示稳定的领域边界；跨模块协作以各 Module 声明的对外能力、依赖和交互为准。

### 3.1 MODULE-001 {模块名称}

| 属性 | 内容 |
|------|------|
| 模块编号 | MODULE-001 |
| 模块名称 | {稳定的领域名称} |
| 领域职责 | {本领域负责解决什么问题} |
| 核心业务对象 | {对象、概念或状态；无则说明} |
| 范围内 | {本模块负责的能力边界} |
| 范围外 | {明确不由本模块负责的事项} |
| 对外提供能力 | {供其他模块使用的业务能力；无则写无} |
| 依赖模块 | {MODULE-* / 无} |
| 跨模块交互 | {业务语义、触发条件和结果；无则写无} |

## 4. Feature 索引表

| 功能编号 | 功能名称 | 明细路径 |
|----------|----------|----------|
| {FEATURE-001} | {功能名称} | feature/FEATURE-001.md |

## 5. 跨功能约定（如有）

无
```

## 立项落盘与 `feature/` 目录初始化

**`/lny-prd-master` 立项时**：创建空目录 **`feature/`**，按上文 **「feature_spec.md 模板」** 生成根目录 **`feature_spec.md`**。若初始 Story 尚未拆解，可暂留 Module 模板与空 Feature 索引；④ 必须补齐 Module 后才能创建 Feature。

**`/lny-prd-feature` 续跑时**：

1. 若 **`feature_spec.md` 不存在**：按 **「feature_spec.md 模板」** 在根目录创建；同步创建 **`feature/`**（若不存在）。
2. 若 **`feature/` 不存在**：创建空目录；旧版单体 `feature_spec.md` 大段功能正文须 **迁移** 至 `feature/FEATURE-*.md` 后改维护索引模式。
3. 新增 **`FEATURE-*`**：先按 `SKILL.md` 领域粒度门禁定义/确认 **§3 Module** → 更新 **§4** 索引行 → 按 **「明细必填字段」** 创建 **`feature/FEATURE-{三位序号}.md`**。
4. **禁止**在 `feature/` 存放接口字段表、UI 布局正文、原型 HTML；**禁止**写入预览壳专用机制（状态演示、postMessage 等）。

## 双图规范（时序图 + 流程图）

| 维度 | 时序图 `sequenceDiagram` | 流程图 `flowchart TD` |
|------|--------------------------|----------------------|
| 表达 | 参与方消息顺序、调用时序、重试/补偿链路 | 业务主路径、分支判断、状态迁移、终止条件 |
| **必画** | 跨角色协同（用户/前端/后端/第三方）、异步回调、失败补偿、重试 | 分支 >= 3 条、状态迁移复杂、含审批/回滚 |
| **免画** | 单步配置类、无分支无状态迁移的简单功能；免画须写明理由 |

图示仅表达业务逻辑，不替代 api_spec 字段定义与 ui_manifest 布局。图中可定位到页面/接口的节点优先使用 PAGE-*/API-*/EXT-* 标识（可附中文名），避免泛称。

**编号落图（必须）**：
- **时序图** participant 优先写 PAGE-* / API-* / EXT-* + 服务角色；消息名优先写 API-* / EXT-*（可补中文语义）
- **流程图** 关键节点命名优先带 PAGE-*/API-*/EXT-*；判断/异常节点涉及接口调用时体现对应编号
- 仅在无法映射编号时（纯本地状态切换、系统内部步骤）才允许泛化节点名

## 明细必填字段（`feature/FEATURE-*.md`）

**填写约束（本步只填格）**：

| 字段 | 取值 / 规则 |
|------|-------------|
| 模块编号 | 唯一 `MODULE-*`；须在 `feature_spec.md` §3 定义；明细不复制模块名称 |
| 评审状态 | `pending` / `reviewing` / `approved` / `blocked`；只表达产品评审，不复制研发状态 |
| 关联 STORY | 至少一条有效 `STORY-*`；可多条，多条时区分 **主** / **次**；禁止 **框架承接** 或 **无** |
| 分支数 | 正整数；主路径计 **1**；每条独立业务分支 +1（与流程图分支对齐） |
| AC 表 | active Feature 至少一条；AC ID 在本 Feature 内唯一，验收描述与验证方式非空且可验证；涉及页面行为时填关联 `PAGE-*`，有数据依赖则填关联 `API-*`/`EXT-*`；业务规则用 `BR-*` 编号可被 AC 引用；`验证方式`只写所需产品证据，不写终端或交付角色。旧表缺「关联页面」可读，新建/修改 AC 必填页面或显式「无」；关联页面须在单页 PRD §6 以 AC ID 反向登记 |

`验证方式`与任务分工正交：推荐使用 `UI 检查`、`UI + API 联调`、`API 校验`、`数据校验`、`异常流测试`、`幂等测试`、`第三方联调`、`端到端测试`等证据类型。禁止填写 `MP + API 联调`、`FE + API 联调`、`BE 验证`、`AD 测试`等含终端码或交付角色的文案；PAGE/API/EXT 归属由稳定编号表达，SP `FE/BE` 不得回写本列。

每个功能明细至少包含以下结构：

```markdown
# FEATURE-001 {功能名称}

## 1. 基本信息
| 属性 | 内容 |
|------|------|
| 功能编号 | FEATURE-001 |
| 功能名称 | |
| 模块编号 | MODULE-001 |
| 优先级 | P0 / P1 / P2 |
| 状态 | draft / active / deprecated |
| 评审状态 | pending / reviewing / approved / blocked |
| 关联 STORY | {STORY-001（主）; STORY-002（次）} |
| 分支数 | {≥1} |

## 2. 功能目标与范围
- 目标：
- 范围内：
- 范围外：

## 3. 核心规则
| 规则编号 | 规则说明 |
|----------|----------|
| BR-1 | |
| BR-2 | |

## 4. 交互与状态（概要）
- 正常流：
- 异常流：
- 边界条件：

## 5. 验收标准
| AC 编号 | 验收描述（可验证） | 关联规则 | 关联页面 | 关联接口 | 验证方式 |
|---------|-------------------|----------|----------|----------|----------|
| AC-1 | | BR-1 | PAGE-… / 无 | API-… / 无 | UI + API / 数据校验 / 其它 |
| AC-2 | | — | PAGE-… / 无 | EXT-… / 无 | 第三方联调 / 其它 |

## 6. 关联对象
- 关联页面：PAGE-...
- 关联接口：API-...
- 关联第三方接口：EXT-...
- 引用文档：ui/PAGE-....md, api/API-....md, api/EXT-....md

## 7. 时序图（按触发条件必填）

~~~mermaid
sequenceDiagram
    participant User as 用户
    participant UI_MP_002 as PAGE-MP-002 商品列表页
    participant API_MP_003 as API-MP-003 查询商品列表
    User->>UI_MP_002: 在 PAGE-MP-002 提交筛选条件
    UI_MP_002->>API_MP_003: 调用 API-MP-003 查询列表
    API_MP_003-->>UI_MP_002: 返回列表结果 / 错误码
    UI_MP_002-->>User: 刷新列表或提示失败重试
    Note over UI_MP_002,API_MP_003: 异常流示例：API-MP-003 失败后展示重试入口
~~~

## 8. 流程图（按触发条件必填）

~~~mermaid
flowchart TD
    startNode[开始] --> submitAction[PAGE-MP-002 提交筛选]
    submitAction --> ruleCheck{PAGE-MP-002 参数校验通过?}
    ruleCheck -->|是| executeAction[调用 API-MP-003 查询列表]
    ruleCheck -->|否| rejectAction[PAGE-MP-002 提示参数不合法]
    executeAction --> apiResult{API-MP-003 返回成功?}
    apiResult -->|是| showData[PAGE-MP-002 渲染列表]
    apiResult -->|否| showError[PAGE-MP-002 展示失败并允许重试]
    showData --> finished[结束]
    showError --> finished
    rejectAction --> finished
~~~

## 9. 变更备注（可选）
- ...
```
