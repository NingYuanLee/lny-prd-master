---
name: PRD Feature (李宁远产品工作流)
description: 李宁远产品工作流 - 功能规格拆分与维护。维护根 `feature_spec.md`（索引+规则）及 `feature/FEATURE-*.md`（单功能明细），并与 `main_spec`、`api_spec`、`ui_manifest` 保持引用闭环（含 `API-*` 与 `EXT-*`）。
---

## 与总控的关系

全流程见 **`lny-prd-master/SKILL.md`**。本步为 **④ `/lny-prd-feature`**：产出和维护功能逻辑规格，不替代接口需求定义和 UI 布局写作。完成后总控通常进入 **⑤ `/lny-prd-page`**、**⑥ `/lny-prd-prototype`** 或 **⑦ `/lny-prd-check`**。

# 功能规格 `/lny-prd-feature`

## 目标定位

- **开笔前**：Read **`lny-prd-master/SKILL.md` →「框架内置能力（不纳入 PRD）」**（含 **排除口径** 与「仍须写 PRD 的边界」）及本项目追加排除项。**不为** **框架通用** 已排除项创建 Feature；**业务** 流程 Feature **仍须**按 master 边界编写。

将“功能逻辑”从超大 `api_spec.md` 中拆出，形成：

- 根索引：`feature_spec.md`（目录、全局规则、Feature 索引）
- 明细目录：`feature/FEATURE-*.md`（一功能一文件）

根文档只保留索引与规则；细节落在 `feature/` 单文件，避免上下文过载。

## 目录化兼容模式（索引 + 明细）

优先新结构（`feature/` 存在时维护索引+明细），兼容旧结构（仅 `feature_spec.md` 全量描述时允许先维护根文档并提示迁移），双轨过渡（迁移期间根文档可保留摘要，详细规则逐步下沉）。

## 职责边界

| 负责 | 禁止 |
|------|------|
| 维护 `feature_spec.md` Feature 索引（编号/名称/终端模块/优先级/状态/明细路径） | 在 `api_spec.md` 中写字段级请求/响应定义（属 `lny-prd-api`） |
| 维护 `feature/FEATURE-*.md` 明细（目标/范围/验收/关联页面/关联接口/状态） | 在 `ui_manifest.md` 中写页面线框与视觉布局（属 `lny-prd-ui`） |
| 保证 FEATURE-* ↔ PAGE-*/API-*/EXT-* 引用闭环 | 在 `feature/` 写入原型预览壳机制（§C/postMessage/map.html，属 `/lny-prd-prototype`） |
| | 框架内置能力重复建 FEATURE-*（见 master 排除口径）；业务流程 Feature 仍须编写且只写差异 |
| | 在任一根规范「变更记录」表新增行（仅 `/lny-prd-iter`） |

## 编号与路径规则

- 功能编号（新增）：`FEATURE-{三位序号}`（如 `FEATURE-001`）
- 明细路径（新增）：`feature/FEATURE-{三位序号}.md`
- 历史兼容：已存在的 `FEATURE-MP-001` 等旧编号允许保留，不强制改名；仅新功能使用新编号
- 引用方式：只引用 **ID + 路径**，不跨文档复制长段细节

## 写产物纪律（防碎片化）

1. 开笔前 Read `feature_spec.md` + `feature/` + `main_spec`/`api_spec`/`ui_manifest` 校验引用
2. 一次对话一条主线；先清单后落盘，列出新增/修改的 FEATURE-* 与关联 ID 再写入
3. 整块写：优先按功能编号整段/整表更新；收尾确认 FEATURE↔PAGE/API/EXT 交叉引用一致
4. 更新 `main_spec.md` §7 有效 Feature 数（若维护）；在 `versions/{版本号}/iteration_notes.md` 文末追加总结（见 `lny-prd-master` §1.1；不改变更记录表）

## 规范参考

- **根索引模板**：本文 **「feature_spec.md 模板」**（立项 **`/lny-prd-master`** 与本步维护均 **Read 本节**）
- **单功能明细骨架**：本文 **「明细必填字段（`feature/FEATURE-*.md`）」**
- **双图规范**：本文 **「双图规范（时序图 + 流程图）」**
- **main_spec 模板**：**`lny-prd-master/SKILL.md` →「main_spec.md 模板」**（本步 **只写** §7 统计，**只读** 第4章终端表）
- 功能文档位置：`feature_spec.md` → 索引与全局规则；`feature/FEATURE-*.md` → 单功能明细（时序图、流程图、验收标准）
- 编号规则：与 `main_spec.md` **§2.1** 一致，**`FEATURE-{三位序号}`**（如 `FEATURE-001`）；历史 `FEATURE-MP-001` 等旧编号可保留

## feature_spec.md 模板

> **单一事实源**：`feature_spec.md` 根索引骨架 **只在本节维护**；立项 **`/lny-prd-master`** 与本步 **`/lny-prd-feature`** 均 **Read 本节** 落盘或更新。

```markdown
# 功能规格说明书 - {项目名称}

> 产品功能逻辑索引与明细分工：**`lny-prd-feature/SKILL.md`**。

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

## 1. 阅读说明与清单结构约定

> **导读**：本文件 **仅** 维护 **§2 全局规则** 与 **§3 Feature 索引**；**§1** 为书写约定。**单功能详述**（目标、规则、验收、双图）一律落在 **`feature/FEATURE-*.md`**（与 **§3「明细路径」** 同源，**禁止**在本文件重复正文）。双图何时必画、编号落图规则见 **`lny-prd-feature/SKILL.md` →「双图规范」**。

### 1.1 与根规格的分工

| 文档 | 职责 |
|------|------|
| `main_spec.md` | 项目概述、终端说明（第4章）、各域 **统计索引**（§7 Feature 个数） |
| `ui_manifest.md` + `ui/` | 页面/组件布局与 UI 状态（**不写**业务流程正文） |
| `api_spec.md` + `api/` | 接口需求（**不写**跨页流程编排） |
| **`feature_spec.md` + `feature/`** | **业务能力级**规则、流程、验收、关联 `PAGE-*` / `API-*` / `EXT-*` |

### 1.2 引用与闭环

- 索引 **§3** 与 **`feature/FEATURE-*.md`** 双向一致；增删 Feature 时 **同时** 更新索引行与明细文件。
- **只引用 ID + 路径**，不跨文档复制长段细节。
- **框架内置能力**（master **排除口径**）：**不为**登录、RBAC 配置等 **框架通用** 能力 **单独建** `FEATURE-*`；**业务** 流程 Feature **仍须**编写且 **只写差异**。

## 2. 全局规则

- **编号**：新增功能使用 **`FEATURE-{三位序号}`**（如 `FEATURE-001`）；历史 `FEATURE-MP-001` 等旧编号可保留。
- **状态**：`draft` / `active` / `deprecated`（与索引 **§3** 及明细 **§1 基本信息** 一致）。
- **优先级**：`P0` / `P1` / `P2`。
- **关联**：每个 Feature 须声明 **关联页面**（`PAGE-*`）与 **关联接口**（`API-*` / `EXT-*`）；无关联时写 **无**，禁止留空。
- **双图**：跨角色协同、多分支流程等须按 **`lny-prd-feature/SKILL.md`** 补时序图/流程图，或写明免画理由。

## 3. Feature 索引表

| 功能编号 | 功能名称 | 所属模块 | 优先级 | 状态 | 关联页面 | 关联接口 | 明细路径 |
|----------|----------|----------|--------|------|----------|----------|----------|
| {FEATURE-001} | {功能名称} | {模块} | {P0/P1/P2} | {draft/active/deprecated} | {PAGE-MP-001} | {API-MP-001} | feature/FEATURE-001.md |

| 统计项 | 数值 |
|--------|------|
| 有效 Feature 个数 | {数量} |

> 新增功能时在表中追加一行，并创建对应 **`feature/FEATURE-*.md`**；废弃时改 **状态** 为 `deprecated`，**不** 删除历史明细文件。

## 4. 特殊说明（如有）

> **明细单一事实源**：跨功能总则、审批链口径、Feature 间依赖等写在 **`feature/FEATURE-*.md`** 或本节 **跨功能** 约定；若无则写 **无**。
```

## 立项落盘与 `feature/` 目录初始化

**`/lny-prd-master` 立项时**：创建空目录 **`feature/`**，按上文 **「feature_spec.md 模板」** 生成根目录 **`feature_spec.md`**（空索引表；**§3** 可暂无数据行，统计填 **0**）。

**`/lny-prd-feature` 续跑时**：

1. 若 **`feature_spec.md` 不存在**：按 **「feature_spec.md 模板」** 在根目录创建；同步创建 **`feature/`**（若不存在）。
2. 若 **`feature/` 不存在**：创建空目录；旧版单体 `feature_spec.md` 大段功能正文须 **迁移** 至 `feature/FEATURE-*.md` 后改维护索引模式。
3. 新增 **`FEATURE-*`**：更新 **§3** 索引行 → 按 **「明细必填字段」** 创建 **`feature/FEATURE-{三位序号}.md`** → 更新 **`main_spec.md` §7** 有效 Feature 数（若项目维护该统计）。
4. **禁止**在 `feature/` 存放接口字段表、UI 布局正文、原型 HTML；**禁止**写入预览壳专用机制（§C、postMessage 等）。

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

每个功能明细至少包含以下结构：

```markdown
# FEATURE-XXX-001 {功能名称}

## 1. 基本信息
| 属性 | 内容 |
|------|------|
| 功能编号 | FEATURE-XXX-001 |
| 功能名称 | |
| 所属模块 | |
| 优先级 | P0 / P1 / P2 |
| 状态 | draft / active / deprecated |

## 2. 功能目标与范围
- 目标：
- 范围内：
- 范围外：

## 3. 核心规则
- 规则 1：
- 规则 2：

## 4. 交互与状态（概要）
- 正常流：
- 异常流：
- 边界条件：

## 5. 验收标准
- [ ] AC-1
- [ ] AC-2

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

## 输入变量

```yaml
版本号: v1.1.0
操作模式: add 或 modify
功能信息:
  - 功能编号: FEATURE-001   # modify 必填；add 可不填自动分配（新增按跨端编号生成）
    功能名称: 商品筛选与排序
    所属模块: 商品列表
    优先级: P1
    关联页面: [PAGE-MP-002]
    关联接口: [API-MP-003]
关联第三方接口: [EXT-001]
```

## 前置条件

- 必须已执行 `/lny-prd-master` 初始化项目
- 已有 `main_spec.md`、`api_spec.md`、`ui_manifest.md`
- `versions/{版本号}/` 已存在
- 项目根目录必须包含 `feature_spec.md`（立项应已落盘；缺失时按本文 **「feature_spec.md 模板」** 创建）
- 建议存在 `feature/` 目录（立项应已创建；缺失时按本文 **「立项落盘与 `feature/` 目录初始化」** 创建）
- **⑧ 委派进入**：Read `versions/{版本号}/feature_changes.md`，按台账中 **委派步=④** 且 **状态=待④** 的 **FEATURE-*** 条目逐项执行；完成后在 `iteration_notes.md` **文末追加** 摘要（见 `lny-prd-master` **§1.1**）

## `feature_spec.md` 初始化流程（续跑兜底）

若检测到 `feature_spec.md` 不存在：

1. 按本文 **「feature_spec.md 模板」** 在根目录创建
2. **§3 Feature 索引** 统计项填 **0**（尚无功能时）
3. 创建 **`feature/`** 空目录（若不存在）
4. 继续本步的功能索引与明细补充

## 执行步骤

1. 校验 `版本号` 与 `操作模式`，检查 `main_spec.md`、`api_spec.md`、`ui_manifest.md` 是否存在
2. 检查 `feature_spec.md`（不存在则按模板创建 + 建 `feature/` 目录）
3. 读取 `feature_spec.md` 现有索引与 `feature/` 现状 + 根规格校验 PAGE-*/API-*/EXT-* 引用合法
4. `add`：分配新 FEATURE-* 编号，创建 `feature/FEATURE-*.md`，更新 §3 索引行
5. `modify`：更新目标明细文件并同步 `feature_spec.md` 索引行
6. 命中"双图必画"条件时，补齐时序图与流程图，节点优先使用 PAGE-*/API-*/EXT-*；免画则补充理由
7. 更新 `main_spec.md` §7 有效 Feature 统计（与 §3 一致）
8. 确认"索引有文件、文件有索引、关联 ID 有定义、图示规则已满足"
9. 在 `versions/{版本号}/iteration_notes.md` 文末追加本次变更摘要（不改根变更记录表）

## 输出示例

```text
✅ 功能规格已更新：
- feature_spec.md（新增 FEATURE-004 索引）
- feature/FEATURE-004.md（新增明细）
- feature/FEATURE-004.md（已补充时序图/流程图，或已注明免画理由）
- versions/v1.1.0/iteration_notes.md（追加 feature 变更摘要）
```
