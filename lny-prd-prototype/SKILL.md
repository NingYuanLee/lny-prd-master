---
name: PRD Prototype (李宁远产品工作流)
description: 李宁远产品工作流 - 生成可交互原型。桌面端基于 Material UI（React）构建并产出静态文件至按端分目录的 prototypes/；移动端为静态 HTML，含 index.html 汇总预览与 map.html 关系画布（默认同步）；versions 下仅镜像静态产物。
---

## 与总控的关系

全流程见 **`lny-prd-master/SKILL.md`**。本步为 **⑥ `/lny-prd-prototype`**（方案 A：建议在 **⑤ 单页 PRD** 之后；**不硬阻塞**）。完成后可经总控进入 **⑦ `/lny-prd-check`**。

# 生成原型图 `/lny-prd-prototype`

## 总控入口（无需用户自选子指令）

若由 **总控**（**`@lny-prd-master` / `/lny-prd-master`** 等，见 `lny-prd-master`）进入：仅在 **架构与接口规格已满足总控判定** 时进入本步；**完整 Read 本文后再执行**。

## 本步职责与禁止越权

- **开笔前**：Read **`lny-prd-master/SKILL.md` →「框架内置能力（不纳入 PRD）」** 及本项目追加排除项。**不生成**已排除项对应 `PAGE-*.html`。**可选（不阻塞）**：若存在 `versions/{版本号}/pages_prd/` 对应 `PAGE-*`，**可 Read** 加厚交互/跳转描述；**主事实源仍为** `ui/PAGE-*.md`、`api/`、`feature/`。
- **负责**：根据 **`main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md`** 生成或更新 **`prototypes/{终端}/`** 与 **`versions/{版本号}/prototypes/{终端}/`**（仅静态文件镜像）；维护根目录 **`prototypes-mui-app/`** 中的 **React + Material UI** 桌面构建工程并在变更后 **自动 build** 到 `prototypes/` 对应桌面子目录；含各端 `index.html`、移动类 **`map.html` 关系画布**、桌面/移动 **通顶左栏 + 让位顶栏** 导航壳、**iframe 左侧 §C 状态面板**、**右侧规格抽屉** 等（见下文 **壳层布局总则** 与 **§A / §B / §C / §E**）。
- **禁止**：在规格中缺失页面/接口/交互说明时，**仅用 HTML 编造**为「事实来源」；缺项须提示用户先走 **`lny-prd-ui`** / **`lny-prd-api`** / **`lny-prd-feature`** / **`lny-prd-page`** 补全规格后再生成；在 **`main_spec.md`、`api_spec.md`、`ui_manifest.md`、`feature_spec.md`** 等规范 **「变更记录」** 表中 **新增行**（**仅** `/lny-prd-iter` 可追加新版本记录，见 `lny-prd-master` **§1.1**）；**修改** 根目录 **`main_spec.md`、`api_spec.md`、`ui_manifest.md`、`feature_spec.md`** 任一正文，或写入 **`versions/{版本号}/iteration_notes.md`** 及其它 **非原型** 路径（本步 **只** 维护 **`prototypes/`**、**`versions/.../prototypes/`**、**`prototypes-mui-app/`**）；若对话要求改规格或写迭代流水，**拒绝落盘**并引导用户走 **`/lny-prd-ui`**、**`/lny-prd-api`**、**`/lny-prd-feature`**、**`/lny-prd-page`** 或总控对应步。**禁止**交付有已知 BUG 的原型（见 §G BUG 预防规则）；**禁止**在正常页面视图中保留演示专用按钮（必须归位 §C 面板，见 §C.5）。

## 规格先行（必须先文档、后原型）

1. **输入源（须 Read）**：与本次生成相关的 `main_spec.md`、`ui_manifest.md`、`api_spec.md`（§4 索引）、`api/API-*.md`、`feature_spec.md`；**可选** `versions/{版本号}/pages_prd/` 对应页。
2. **若规格文档与目标页不一致或缺块**：**停止**生成/覆盖原型；说明缺哪一类内容，并指向总控下的 **②（`lny-prd-ui`）**、**③（`lny-prd-api`）**、**④（`lny-prd-feature`）** 或 **⑤（`lny-prd-page`）**；**禁止**以原型为主反向改写规格作为主要手段。
3. **写盘顺序**：确认规格内容已覆盖本批页面后，再写入 **`prototypes/{终端}/`** 并完成 **`versions/{版本号}/prototypes/{终端}/`** 静态镜像；桌面端须 **先 build 再复制**；大改交互时优先改文档再同步原型。

## 写产物纪律（防碎片化）

1. **开笔前**：Read 三份规格相关章节 + 既有 `prototypes/{终端}/` 与 **`prototypes-mui-app/`** 目录结构，明确将生成/覆盖的文件列表。
2. **一次对话一条主线**：例如「仅本版本变更页面」或「仅补 `prototypes/MP/index.html` 菜单」。
3. **先清单后落盘**：列出将新增/更新的 **原型路径**（含各端 HTML、构建产物与 `assets/`），再写入。
4. **与编号一致**：原型中的 `API-{终端}-{序号}`、`PAGE-*` 与 `api_spec` / `main_spec` 一致。
5. **中文 UTF-8**：含 CJK 的原型文件须遵守上文 **§F**（写盘方式 + 写后 `verify-prototype-utf8.py`）；**禁止**用 StrReplace 改中文块。

## 规范参考
- 根规格与索引模板：**`lny-prd-master/SKILL.md`**（main_spec）；**`lny-prd-api` / `lny-prd-ui` / `lny-prd-feature` SKILL**（api_spec / ui_manifest / feature_spec 及明细目录）
- 页面与组件索引：`ui_manifest.md`（页面清单与组件索引）+ `ui/PAGE-*.md` / `ui/COMP-*.md`
- 功能模块信息：`ui_manifest.md` 页面清单与 `ui/PAGE-*.md` 中的模块描述
- Feature 规则与清单：`feature_spec.md` 索引 + `feature/FEATURE-*.md`（用于壳侧说明区中的 Feature 关联清单）
- 页面跳转关系：`ui_manifest.md` / `ui/PAGE-*.md` 中各页面的跳转目标
- 接口与页面关联：`api_spec.md` 与 `ui_manifest.md`/`ui/` 中与页面绑定的 **API 编号**（生成桌面端与移动端 **导航壳右侧抽屉** 中「接口交互说明」时以此为准）
- 布局与组件说明：**`ui/PAGE-*.md`**（导航壳右侧抽屉「页面布局说明」）、**`ui/COMP-*.md`**（「局部自定义UI组件说明」）；局部组件判定与状态矩阵见 **`lny-prd-ui/SKILL.md` →「局部自定义UI组件：判定、边界与状态职责」**
- 原型存放（按端）：`prototypes/{终端编码}/PAGE-{终端}-{序号}.html`（终端编码与页面编号中 `{终端}` 一致：`MP` / `H5` / `APP` / `PC` / `AD`）
- 版本原型（仅静态、同结构镜像）：`versions/{版本号}/prototypes/{终端编码}/PAGE-{终端}-{序号}.html`
- 桌面端 React 源码与构建：`prototypes-mui-app/`（**不**同步入 `versions/`）

## 原型生成专项规则（非 PRD 正文约束）

以下规则仅约束 **HTML / 构建后静态原型** 的产出形态，不改变 `main_spec.md` / 单页 PRD 的正文写法；执行 `/lny-prd-prototype` 时必须遵守。

### 目录、MCP 与构建（桌面 Material UI）

1. **按端子目录（`prototypes/`）**  
   - 单页、汇总 index、桌面端构建产物均位于 **`prototypes/{终端编码}/`**，`{终端编码}` 为 **`PAGE-{终端}-{序号}`** 中的 `{终端}`：`MP` / `H5` / `APP` / `PC` / `AD`。  
   - 示例：`prototypes/MP/PAGE-MP-001.html`、`prototypes/MP/index.html`、`prototypes/MP/map.html`、`prototypes/AD/PAGE-AD-002.html`（**框架通用** 内置页如 AD 登录 **不生成** `PAGE-*.html`，见 master **排除口径**）。

2. **`versions/{版本号}/prototypes/` 仅静态镜像**  
   - 将 `prototypes/{终端}/` 下本版本所需文件 **按相同相对路径** 复制到 **`versions/{版本号}/prototypes/{终端}/`**。  
   - **禁止**在该目录下存放 **`node_modules`、未构建的 `src/`、`package.json`、锁文件、Vite/Webpack 配置** 等；这些 **仅** 允许存在于项目根的 **`prototypes-mui-app/`**。

3. **`prototypes-mui-app/`（React + Material UI）**  
   - 与 `prototypes/` 并列，位于 **PRD 项目根目录**：存放桌面端 **React + [Material UI](https://mui.com/material-ui/)**（如 `@mui/material`、`@mui/icons-material`）源码与构建脚本。  
   - **知识来源**：若已配置 **mui-mcp**（或等价、面向 MUI/Material UI 文档与组件的 MCP），**优先**通过 MCP 查询组件与布局用法；**若无**，则阅读 **[MUI 官网](https://mui.com/)**（Material UI 文档与示例）后再编码。  
   - **自动 build**：在 `prototypes-mui-app/` 内执行依赖安装与 **`npm run build`**（或项目统一脚本如 `pnpm build`）；**`build` 输出目录**须指向 **`prototypes/PC/`、`prototypes/AD/`**（或与多页入口一致的路径），使桌面单页与壳层以 **静态 HTML + JS + CSS + 资源** 形式落在 `prototypes/{终端}/`。每次变更桌面原型源码后 **须构建成功** 再向用户宣告完成。  
   - **`prototypes-mui-app/` 自身不复制到 `versions/`**。

### 壳层布局总则（桌面 §A / 移动 §B 共用）

汇总预览页 / 桌面导航壳须遵守下列 **骨架**，避免顶栏与预览区争抢垂直空间导致 **组件状态演示** 溢出不可见：

1. **左侧菜单通顶**
   - **页面清单 / 模块导航侧栏** 自视口 **顶边** 起向下延伸（**通顶**），**不**被顶部栏压在上方。
   - **顶部栏（`AppBar`）** 仅占据 **主内容区** 上方一条带：**起始水平位置 = 当前侧栏右缘**；侧栏展开时顶栏 **让出** 侧栏宽度，**禁止**顶栏横跨整屏盖住侧栏。

2. **侧栏收起/展开在顶栏**
   - 侧栏 **收起 / 展开** 按钮（如 `Menu` / `ChevronLeft` 图标）须放在 **顶部栏内**（建议靠左，紧邻主内容区左缘）。
   - **收起后**：左侧菜单 **完全消失**（宽度 **0** 或等效 unmount，**不留** 窄条占位）；顶部栏与主内容区左缘对齐至视口左缘（或壳层设计约定的最左内边距），预览区获得最大水平空间。
   - **展开后**：侧栏恢复通顶宽度；顶栏与主内容区整体 **右移** 让位。
   - **收起/展开后须调用 `fitPhoneFrame()`**（移动端 §D），使 iframe 设备框等比重算。

2b. **§C 组件状态演示收起/展开在顶栏（与页单收起并列）**
   - 当前预览页 **须展示 §C 状态面板** 时（非 TabBar 豁免页），顶栏在页单收起按钮旁增加 **§C 收起/展开** 按钮（如 `◧` / `Tune` 图标）；**TabBar 豁免页或本页无 COMP 状态条时隐藏该按钮**。
   - **收起后**：§C 面板宽度 **0**、完全不可见（**不留**窄条）；预览区获得更大水平空间；**须**在 transition 结束后调用 **`fitPhoneFrame()`**。
   - **展开后**：§C 面板恢复默认宽度 **200px**（固定）；同样 **须** 调用 **`fitPhoneFrame()`**。
   - 切换预览页导致 §C 显隐变化时，同步更新顶栏按钮可见性并重算缩放。

3. **组件状态演示在 iframe 左侧（禁止放顶）**
   - **禁止**将 **§C**「组件状态演示」放在 iframe **上方** 或顶栏内（易在窄屏/多 COMP 时 **垂直溢出** 导致看不见）。
   - 主内容区（顶栏下方）横向顺序固定为：**【组件状态面板】（可选，§C）→ iframe 预览**；状态面板与 iframe **同一行、并排**，iframe 占剩余宽度；状态面板 **固定宽度 200px**、内容过长时 **面板内纵向滚动**。

4. **移动端 iframe 预览区等比缩放（禁止外围滚动条）**
   - 移动端汇总页（§B）中，**iframe 外围预览区**（深色背景 `.preview-area`）须 **始终完整显示** 设备框，**禁止**出现预览区外围纵向/横向滚动条（`overflow: auto` 导致壳层滚动）。
   - 设备框逻辑尺寸固定（默认 **375×812**，与小程序设计稿一致）；空间不足时 **等比缩小**（`scale ≤ 1`，**禁止**放大超过 1:1）。
   - 实现须含 **缩放占位容器**（如 `.phone-scale-host`）+ **`transform: scale(var(--phone-scale))`** + **`fitPhoneFrame()`** 重算；**页单**收起/展开、**§C 面板**收起/展开、§C 面板因切页显隐、窗口 `resize`、侧栏拖曳结束时须重算。细则见 **§D**。
   - **iframe 内**页面滚动（如 `.page-body { overflow-y: auto }`）**保留**，与壳层缩放无关。

```text
展开侧栏时（示意）：
┌──────────┬────────────────────────────────────────────┐
│          │ AppBar [☰页单] [◧§C] … [规格说明]           │
│ 左菜单   ├──────────┬─────────────────────────────────┤
│ （通顶） │ §C 状态  │ iframe 预览（§D 等比缩放）       │
│          │ 面板     │                                  │
└──────────┴──────────┴─────────────────────────────────┘

收起侧栏时：左列宽度为 0；AppBar 与「§C + iframe」自左缘起占满（右 Drawer 触发仍在 AppBar）。
收起 §C 时：§C 列宽度为 0；顶栏 ◧ 按钮仍可见（当前页有 §C 时）；须 fitPhoneFrame 重算。
```

### A. 桌面端（PC 网页、管理后台等）

1. **侧栏菜单默认两级**
   - **一级**：功能 **模块**（与架构表中的模块划分一致，可有分组标题样式）。
   - **二级**：具体 **页面**（一条菜单对应一个 `PAGE-*` 原型入口）。
   - 左侧导航为 **通顶侧栏**（Material UI：**`Drawer` `variant="persistent"`** 或 **`Box` + `List`** 等固定左列），遵循上文 **「壳层布局总则」**：侧栏 **通顶**、顶栏 **让位**、**收起按钮在 AppBar**、收起后侧栏 **完全消失**。**不得**用 **临时覆盖式 Drawer** 或 **Modal** 承载模块/页面主导航。
   - 同一桌面端站点一套壳层即可；点击二级项在主内容区加载对应页面原型（**iframe** 或与 **§C 状态面板** 并排的预览区，项目内约定一致）；主内容区须为 **§C 状态面板（左）+ iframe（右）** 横向布局（TabBar 豁免页可隐藏状态面板，见 **§C**）。

2. **说明类内容放在导航壳，不从右侧抽屉重复进单页**
   - **禁止**在单个桌面端页面原型内再嵌一整块「本页接口清单 / 全量规格说明」作为主内容或固定侧栏（避免与壳层重复、碎片化）；**页面 HTML 仅承载界面骨架与演示交互**。
   - **仅**规格说明使用 **右侧 Drawer**；左侧仍为 **A.1** 所述通顶侧栏，二者勿混用。
   - 在 **外层导航壳**（**通顶左栏** + **仅覆盖主内容区的 `AppBar`** + **主内容区「§C 状态面板 + iframe」**）提供 **从右侧弹出的 `Drawer` `anchor="right"` `variant="temporary"`（或 `persistent`）** 承载规格说明，**抽屉宽度固定 375px**（与移动端设计稿逻辑宽一致），随 **当前选中的预览页** 切换内容；抽屉内固定为 **五项**（顺序与标题建议保持一致，便于研发对照文档）：
     1. **页面布局说明**：依据 **`ui/PAGE-*.md`** 撰写（与 `PAGE-*` 一致，勿编造文档未载明的结构）。
     2. **局部自定义UI组件说明**：依据 **`ui/COMP-*.md`**（及 **§4** 组件名称）撰写（组件名称与清单 **逐字一致**；职责、**UI 状态矩阵**、在本页中的用途写清；注明 **状态切换入口**：页内 TabBar/Tabs **或** 壳层 **iframe 左侧** 状态面板，见 **§C**）。
     3. **接口交互说明**：依据 **`api_spec.md` §4** 与 **`api/API-*.md`** 及本页绑定的 **`API-{终端}-{序号}`** 逐条说明触发时机、业务要点、成功 / 失败 / 兜底表现。
     4. **Feature 关联清单**：依据 **`feature_spec.md`** 与 `feature/FEATURE-*.md` 中本页关联的 `FEATURE-*`，逐条写明 Feature 编号、名称与本页作用点；无关联写 **无**。
     5. **E. 操作交互说明**（抽屉内第 5 项，**非**流程步骤 ⑤ 单页 PRD）：以 **监听事件类型** 为主线分项说明（如 点击 / 滑动 / 拖拽 / 滚动 / 下拉刷新 / 输入失焦 / 页面进入 / **壳层 · 组件状态切换** 等），写清可见反馈与纯本地状态流转；不涉及后端数据变更的交互归此组。
   - 抽屉可由壳层工具栏按钮（如「规格说明」）打开/关闭；**当前页** 以侧栏选中态为准，**无需**在抽屉内再单独做与选中态重复的「当前页面」标题块。

3. **UI 技术栈：Material UI（React），静态产出**
   - 桌面端壳层与 **`PAGE-PC-*`、`PAGE-AD-*`** 单页界面骨架须在 **`prototypes-mui-app/`** 中以 **React + [Material UI](https://mui.com/material-ui/)** 实现（`@mui/material`、`@mui/icons-material` 等）；**禁止**再以 Ant Design 作为桌面默认栈。
   - 交付物为 **`npm run build`** 后的 **静态文件**（见上文 **「目录、MCP 与构建」**），落在 **`prototypes/PC/`、`prototypes/AD/`**；若需与 PRD 历史兼容、临时保留某页纯手写 HTML，须在注释中标明 **「待迁入 `prototypes-mui-app`」** 并尽快收口到 MUI 工程。

#### 桌面端抽屉内每条记录书写格式（壳层内嵌 `DATA`、注释区或等价载体须遵守）

- **页面布局说明 / 局部自定义UI组件说明**：与 **`ui/PAGE-*.md` / `ui/COMP-*.md`** 条目对应；长描述可采用 **标题 + 换行段落**，避免挤作单行。
- **接口交互说明**：**首行（同一行）** **接口编码** + **描述**（可用 **「 · 」** 连接；编码须为完整 **`API-{终端}-{序号}`**，名称与 `api_spec.md` **§4** 描述列或 `api/API-*.md` **接口用途**一致）；**交互描述独占换行**，置于第二行及以下，写触发时机、关键业务字段依赖、成功/失败表现。
- **Feature 关联清单**：每条记录使用 **`FEATURE-* · 名称 · 本页关联点`**；来源路径可在下一行补充（如 `feature/FEATURE-001.md`）；无关联写 **无**。
- **操作交互说明**：**不写事件序号**（不加 `①②`/`1.` 等前缀）。每条同一行内 **事件类型 · 交互描述**（可用 **「 · 」** 或空格隔开）；**事件类型** 为用语统一的监听/生命周期归类；**交互描述** 写界面反馈、动效、校验与状态流转。

### B. 移动端（微信小程序、H5、APP 等终端）

除各 **`PAGE-*` 单页原型** 外，**每个移动端终端**（或产品在本版本中定义的每条终端线，如仅 MP）须额外生成 **一个汇总预览页**：

| 区域 | 内容 |
|------|------|
| **左侧** | **可折叠页面清单侧栏**（**非** 覆盖式 Drawer）：遵循 **「壳层布局总则」**——**通顶**、**收起/展开按钮在顶栏**、收起后 **完全消失**（不留窄条）；默认展开。宜支持 **拖曳分隔条** 调节宽度（合理 min/max）。选中项切换 **当前预览** 对应的原型 HTML。 |
| **顶栏（主内容区）** | **页单收起**（☰）与 **§C 收起**（当前页有状态演示时显示，TabBar 豁免页隐藏）；二者收起后均须 **`fitPhoneFrame()`** 重算 iframe 缩放。 |
| **中间** | 顶栏下方横向：**【§C 组件状态面板】（iframe 左侧，可选，可顶栏收起）** + **`iframe` 预览**（占剩余宽度）。`iframe` 的 `src` 指向同端 `PAGE-*.html` 或 `versions/...` 镜像。**禁止**把 §C 放在 iframe **上方**。预览区须 **等比缩放完整显示设备框、无外围滚动条**（见 **§D**）。 |
| **右侧** | **抽屉（Drawer）**：宽度 **375px**（固定）；与桌面端导航壳 **同一套五项说明**（见上文 **A.2**），内容结构一致：**① 页面布局说明**（**`ui/PAGE-*.md`**，旧版 manifest 大段正文已废弃）**② 局部自定义UI组件说明**（**`ui/COMP-*.md`**）**③ 接口交互说明**（`api_spec.md` §4 + `api/API-*.md`）**④ Feature 关联清单**（`feature_spec.md` / `feature/FEATURE-*.md`）**E. 操作交互说明**（抽屉内第 5 项；以 **监听事件类型** 为主线，**非**流程步骤 **⑤ 单页 PRD**）。由 **顶栏** 按钮打开/关闭；**当前页** 以左侧页单侧栏 **选中态** 为准，抽屉内 **不**再重复「当前页面」标题或与 **③** 重复的「仅列接口编号」摘要区。 |

**关系画布（移动端默认必做，细则见 §E）**

除 **`index.html` 汇总预览** 外，每个移动终端须同步生成 **`prototypes/{终端}/map.html`**：**全页缩略 iframe 节点 + SVG 跳转连线 + 画布平移缩放**；与单页、`index.html` **同源**；`index.html` ↔ `map.html` 顶栏互链。执行本步生成或更新移动类单页 / `index.html` 时 **须同步创建或更新 `map.html`**，完成后再 **镜像** 至 `versions/{版本号}/prototypes/{终端}/map.html`。

- **汇总页书写格式**：右侧抽屉内五项的 **分行/换行规则** 与桌面端 **「桌面端抽屉内每条记录书写格式」** 相同；**E. 操作交互说明** 等同于原「用户视觉交互」写法（事件类型 · 交互描述，不写事件序号）。
- **文件命名与路径**：`prototypes/{终端}/index.html`（例：`prototypes/MP/index.html`）；在 **`versions/{版本号}/prototypes/{终端}/`** 下 **同名复制**（仅静态）。
- 若某版本仅含部分页面，汇总页菜单仅列出本版本已生成的页面即可。

### C. 壳层局部自定义UI组件状态切换（iframe 左侧）

在 **导航壳 / 汇总预览页**（桌面壳层、移动 `prototypes/{终端}/index.html`）中，于 **iframe 左侧**（与 iframe **同一行、主内容区内**）增加 **局部自定义UI组件状态切换演示面板**，便于评审 COMP 多态；**不**替代 `ui/COMP-*.md` 规格正文。**布局**须符合 **「壳层布局总则」** 第 3 条（**禁止**放在 iframe 上方或顶栏内）。

1. **读入与对象**
   - 读当前预览页对应的 **`ui/PAGE-*.md`、`ui/COMP-*.md`** 中的 **COMP 列表** 与 **UI 状态矩阵**。
   - 控制对象为需演示多态的 **局部自定义UI组件**（非页面级路由、非壳层规格 Drawer）。

2. **TabBar 豁免（页内已有切换控件）**
   - 若 iframe 内页面 **已含 TabBar、BottomNavigation、Tabs、SegmentedControl 等页内主导航/分段控件**，且该控件 **即** 用于切换某 COMP（或整页主内容区）的展示状态：
     - **禁止**在 iframe 左侧 **重复** 增加同义状态面板。
     - 壳层 **隐藏** §C 面板，或在面板内 **仅**标注「状态切换见页内 {控件名}」；评审时 **直接操作页内 TabBar** 即可。
   - 判定依据：`ui/PAGE-*` 或 `ui/COMP-*` 是否声明 **「状态切换由页内 TabBar（或同类）承担」**（见 COMP 模板 **§3 状态切换入口**）。

3. **无 TabBar 时：iframe 左侧强制增加控制**
   - 若当前页 **无** TabBar 或同类页内状态切换控件，壳层须在 **iframe 左侧** 增加 **「组件状态演示」** 面板（**非** iframe 上方）：
     - **位置**：主内容区顶栏下方，横向 **【§C 面板】| iframe**；面板 **不**放入 iframe 内。
     - **粒度**：每个 COMP 一组；组名 = COMP 名称（与 `ui/COMP-*` / `§5` **逐字一致**）。
     - **控件形态**：纵向排列的下拉、按钮组或 MUI `ToggleButtonGroup`（**竖向**或分组 stack）；选项 = 该 COMP **状态矩阵** 中的状态名。
     - **尺寸与滚动**：面板 **固定宽度 200px**；COMP 多或选项多时在 **面板内纵向滚动**，**不**撑高整行导致 iframe 被顶出视口。
     - **顶栏收起**：面板须支持 **`.collapsed` 宽度 0**（与页单侧栏收起规则一致）；顶栏 **§C 收起按钮** 控制；收起/展开后 **`fitPhoneFrame()`**（§D）。
     - **联动**：切换时通过 **`postMessage`** 或壳层约定的 **`URL hash/query`** 驱动 iframe 内对应 COMP 切态（iframe 内页须监听并渲染）。
     - **数据来源**：壳层内嵌 `DATA` / 注释区自 `ui/COMP-*.md` 状态矩阵生成，**禁止**编造未在规格中登记的状态。

4. **桌面端与移动端**
   - **移动端汇总页（§B）**：**左页单（通顶）** · **顶栏（让位页单）** · 中间 **§C 面板 + iframe** · 右 Drawer（顶栏触发）；iframe 预览区 **§D 等比缩放**。
   - **桌面端壳层（§A）**：**左模块导航（通顶）** · **顶栏（让位侧栏，含侧栏收起与规格说明）** · 主内容 **§C 面板 + iframe** · 右规格 Drawer。

5. **状态演示归属判断原则（必守）**
   - 以下状态 **必须** 放在壳层「组件状态演示」区（§C 面板），**禁止**在正常页面视图中出现演示按钮：
     - 由 **后端返回数据不同** 产生的不同 UI 状态（如：空数据 / 加载中 / 加载失败 / 数据完整 / 数据部分 / 网络异常 等）
     - 由 **系统/环境条件** 触发的状态（如：权限不足、未授权、设备不支持、版本过低 等）
   - 以下状态 **可以** 不在壳层 §C 面板，而通过 **页内用户操作** 自然触发：
     - 用户 **点击/滑动/输入** 等主动操作产生的状态变化（如：展开/收起、选中/未选中、输入验证通过/失败、切换Tab 等）
     - 由 **页内 TabBar / Tabs / SegmentedControl** 等页内控件触发的状态切换（见上述 TabBar 豁免规则）
   - **自检**：逐页检查 `<body>` 内是否有 `<button class="demo-*">` / `onclick="setDemo*"` 等 **演示专用** 控件——若有且操作为「模拟后端数据变化」→ **必须** 移至 §C 面板。

### D. 移动端 iframe 预览区等比缩放（§B 汇总页必做）

移动端 `prototypes/{终端}/index.html` 汇总页中，**设备框 + iframe** 须按可用空间 **等比缩小**，保证 **整框可见** 且 **预览区外围无滚动条**。

1. **HTML 结构（三层）**

```html
<div class="preview-area">
  <div class="phone-scale-host">
    <div class="phone-frame">
      <iframe id="previewFrame" src="PAGE-*.html" title="页面原型预览"></iframe>
    </div>
  </div>
</div>
```

2. **CSS 要点**

| 选择器 | 规则 |
|--------|------|
| `.preview-area` | `overflow: hidden`（**禁止** `overflow: auto`）；`min-width: 0; min-height: 0`；居中 flex；`padding: 24px`（参与缩放计算） |
| `.state-panel` | 展开态 **固定 `width: 200px`**；`.collapsed` 时 `width: 0` |
| `.phone-scale-host` | `width: calc(375px * var(--phone-scale, 1))`；`height: calc(812px * var(--phone-scale, 1))`；`overflow: hidden`；`flex-shrink: 0` |
| `.phone-frame` | 固定 `375×812`；`transform: scale(var(--phone-scale, 1))`；`transform-origin: top left`；圆角/阴影按需 |
| `.drawer`（规格说明） | **固定 `width: 375px`**；关闭 `right: -375px`；打开 `right: 0` |

- **为何需要 `.phone-scale-host`**：仅对 `.phone-frame` 做 `transform: scale` **不改变布局占位**，配合 `overflow: hidden` 仍会裁切；host 同步缩小占位尺寸，才能消除外围滚动条。
- 若产品约定非 iPhone X 尺寸，可改基准宽高，但 **host 与 frame 须同一组数值**，`fitPhoneFrame` 中 `pad` 与 `.preview-area` padding 一致。

3. **`fitPhoneFrame()` 脚本（必接）**

```javascript
function fitPhoneFrame() {
  var area = document.querySelector('.preview-area');
  var host = document.querySelector('.phone-scale-host');
  if (!area || !host) return;
  var pad = 48; // .preview-area padding 24px × 2
  var scaleX = (area.clientWidth - pad) / 375;
  var scaleY = (area.clientHeight - pad) / 812;
  var scale = Math.min(1, scaleX, scaleY);
  if (!isFinite(scale) || scale <= 0) scale = 1;
  host.style.setProperty('--phone-scale', String(scale));
}
```

4. **重算时机（均须调用 `fitPhoneFrame`）**

- 页面初次加载
- `window` `resize`
- 切换预览页（`loadPage` 或等价）
- §C 状态面板因切页 **显隐**（`renderStatePanel` 或等价）
- **§C 状态面板顶栏收起/展开**（transition 结束后，如 `setTimeout(..., 220)`）
- 左侧页单 **顶栏收起/展开**（侧栏 width transition 结束后，如 `setTimeout(..., 220)`）
- 侧栏拖曳 `mouseup`

5. **§C 顶栏收起（与 §D 缩放联动，必做）**

- 顶栏增加 `#statePanelToggle`（或等价），**仅**当 `.state-panel.show` 时可见；TabBar 豁免页 **隐藏**。
- `.state-panel.collapsed`：`width: 0`、`opacity: 0`、`pointer-events: none`、去右边框；加 width transition 与页单侧栏一致。
- `.state-panel` 展开态 **固定 `width: 200px`**（**禁止** 200～280px 浮动区间）。
- `toggleStatePanel()` 切换 `statePanelOpen`，收起/展开后 **`setTimeout(fitPhoneFrame, 220)`**。
- 切到无 §C 的页面时重置 `statePanelOpen = true` 并隐藏顶栏按钮。

7. **规格说明 Drawer 宽度（壳层必做）**

- 右侧规格抽屉（`.drawer` / MUI `Drawer`）**固定宽度 375px**，与 iframe 内设备逻辑宽一致。
- 关闭态 `right: -375px`（或等效完全离屏）；打开态 `right: 0`。
- 桌面端 MUI 壳层：`PaperProps={{ sx: { width: 375 } }}` 或等价。

8. **禁止与例外**

- **禁止**预览区外围滚动条作为默认交互（不得仅用 `overflow: auto` + 固定 812px 框）。
- **禁止**壳层缩放导致 iframe 内逻辑视口错乱：缩放仅作用于 **壳层 DOM**，iframe 内仍按 375 逻辑宽渲染；页面内滚动仍由单页 `PAGE-*.html` 自身 CSS 控制。
- **桌面端（§A）** 若 iframe 预览非固定手机框，可不套用本节；**MP / H5 / APP 汇总页** 默认套用。

### E. 移动端关系画布（`map.html`，默认必做）

**移动端（MP / H5 / APP）执行本步或单独绘制原型时，须同步维护关系画布**，不得只生成单页与 `index.html` 而遗漏 `map.html`。桌面端（PC / AD）**不强制**；若用户明确要求全端关系图，可复用同一模式。

#### E.1 三件套与同步方向

| 产物 | 路径 | 职责 |
|------|------|------|
| 单页原型 | `prototypes/{终端}/PAGE-{终端}-{序号}.html` | 可点击跳转的页面 HTML |
| 汇总预览 | `prototypes/{终端}/index.html` | 左页单 + §C + iframe + 规格 Drawer（§B） |
| **关系画布** | `prototypes/{终端}/map.html` | 全页面缩略预览 + 连线 + 平移缩放 |

页面清单、跳转关系须与 `ui_manifest.md` / `ui/PAGE-*.md` / 单页内 `href` / `location.href` 一致。**同步方向**：规格 → 单页 → `index.html` + `map.html`；**禁止**以 `map.html` 为唯一事实来源反向改规格。

#### E.2 工作流

```
Task Progress:
- [ ] 1. 从 ui_manifest §3 + ui/PAGE-*.md 列出本终端全部 PAGE-*
- [ ] 2. 从单页 href/location.href + PRD「操作交互说明」提取 LINKS
- [ ] 3. 创建或更新 prototypes/{终端}/map.html（PAGES + LINKS + 布局）
- [ ] 4. index.html 顶栏「关系画布」→ map.html；map.html 顶栏「单页预览」→ index.html
- [ ] 5. 单页跳转变更时同步更新 map.html LINKS 与 index.html PAGE_DATA.actions
- [ ] 6. 镜像至 versions/{版本号}/prototypes/{终端}/map.html
```

#### E.3 构建 `PAGES` 数组

每条页面一条记录：

```javascript
{ id: 'PAGE-MP-001', name: '首页', module: '主包 · home', file: 'PAGE-MP-001.html', x: 480, y: 320 }
```

| 字段 | 来源 |
|------|------|
| `id` | `PAGE-{终端}-{序号}`，与规格逐字一致 |
| `name` | `ui_manifest` 页面名称 |
| `module` | 主包/分包 + 模块名（如 `分包 · order`） |
| `file` | 同目录单页文件名 |
| `x`, `y` | 初始画布坐标（见 E.5） |

`index.html` 侧栏页单与 `PAGES` **须同源**（同一终端、同一页面集合）。

#### E.4 构建 `LINKS` 数组

从以下来源 **合并去重**，禁止编造规格未载明的跳转：

1. 单页内 `href="PAGE-*.html"`、`location.href='PAGE-*.html'`
2. `ui/PAGE-*.md` 功能清单与操作说明中的跳转目标
3. `index.html` 内 `PAGE_DATA[pageId].actions` 中「跳转 PAGE-*」描述
4. TabBar：`switchTab` 或页内 `<a class="tab-item">` 双向链接 → `type: 'tab'`
5. 弹窗嵌入另一页主体（如修改预定嵌入预定页）→ `type: 'embed'`

```javascript
{ from: 'PAGE-MP-001', to: 'PAGE-MP-003', type: 'forward', label: '搜索入口' }
```

| type | 含义 | 线型 |
|------|------|------|
| `forward` | 正向跳转 | 绿色实线 + 箭头 |
| `back` | 返回 | 灰色虚线 + 箭头 |
| `tab` | TabBar / 底部主导航 | 蓝色虚线 + 箭头 |
| `embed` | 弹窗/Sheet 嵌入另一页 | 紫色点线，无箭头 |

`label` 取交互触发点简称；TabBar 可省略 label。

辅助检索（PRD 项目根目录）：

```bash
rg "href=\"PAGE-|location\.href\s*=\s*['\"]PAGE-" prototypes/MP/
```

#### E.5 初始布局

按 **业务簇** 排布，避免连线交叉过多：

```text
[城市/搜索簇]          [购票主链路 →]
     ↑                      005 → 010 → 006 → 007
[001]←tab→[002]→[008]───────────────────────────┘
  ↓ 卡片
[005]
```

建议坐标间距：水平 ≥ 240px，垂直 ≥ 280px；节点宽固定 **200px**（iframe 375×812 缩至 **0.5333**）。大改布局时可保留用户拖过的 `x/y`；新增节点用默认坐标。

#### E.6 `map.html` 结构与必备能力

单文件 HTML，无外部依赖。

**DOM 骨架**：

```html
<div id="map-shell">
  <div class="toolbar">…缩放 / 全屏 / 导出 / 图例 / index 互链…</div>
  <div id="viewport">
    <div id="world">
      <svg id="connections"></svg>
      <!-- JS 动态插入 .page-node -->
    </div>
  </div>
  <div class="hint">…</div>
</div>
<div class="toast" id="toast"></div>
```

**节点结构**：

```html
<div class="page-node" data-id="PAGE-MP-001" style="left:480px;top:320px">
  <div class="node-header"><!-- 可拖拽 -->
    <div class="node-id">PAGE-MP-001</div>
    <div class="node-name">首页</div>
    <div class="node-module">主包 · home</div>
  </div>
  <div class="phone-wrap">
    <iframe src="PAGE-MP-001.html" loading="lazy"></iframe>
    <div class="phone-overlay"></div><!-- 点击 window.open 单页 -->
  </div>
</div>
```

| 能力 | 交互 |
|------|------|
| 画布平移 | 空白处拖拽 |
| 缩放 | 滚轮（以光标为中心）；工具栏 +/− / 1:1 / 适应；`scale` 限制 `[0.15, 2.5]` |
| 全屏 | 工具栏 **全屏** / **退出全屏**；快捷键 **F** 切换；**Esc** 退出（浏览器默认） |
| 节点拖拽 | 拖标题栏；按 `1/scale` 换算位移；拖拽后重绘连线 |
| 页面预览 | iframe `pointer-events: none`；点击 overlay 新标签打开单页 |
| 连线 | SVG 二次贝塞尔；边到边 `getEdgePoint`；同对节点平行错开；拖拽节点时实时更新 |

**尺寸常量**：设备逻辑 **375×812**；节点预览宽 **200px**；`NODE_W = 200`。

**连线样式**：

```javascript
var STYLE = {
  forward: { stroke: '#3fb950', dash: '', width: 2 },
  back:    { stroke: '#8b949e', dash: '6 4', width: 1.5 },
  tab:     { stroke: '#58a6ff', dash: '8 4', width: 2 },
  embed:   { stroke: '#d2a8ff', dash: '2 4', width: 1.5 }
};
```

**须保留的核心函数**：`applyTransform`、`getNodeBox`、`getEdgePoint`、`drawConnections`、`createNodes`、`fitAll`、`zoomAt`、`getContentBounds`、`exportCanvasImage`、`toggleFullscreen`、`updateFullscreenButton`。

**布局壳**：`#map-shell` 使用 `flex` 纵向布局（工具栏 + `#viewport` flex:1）；**禁止**工具栏与 viewport 双 `position: fixed` 导致全屏高度异常。

**互链**：`index.html` 顶栏 `<a href="map.html">关系画布</a>`；`map.html` 顶栏 `<a href="index.html">单页预览</a>`。

**性能**：iframe 使用 `loading="lazy"`；页面数 > 15 时可改为缩略占位 + 双击加载 iframe（按需扩展，默认全量 iframe）。

#### E.6b 布局位置持久化（`map.html` 必做）

两层机制：**localStorage** 自动保存（debounce 300ms，键名 `{项目}-{终端}-map-layout-v1`，含 `pages[{id,x,y}]` + `viewport{scale,panX,panY}`） + 工具栏 **「导出坐标」** 复制 PAGES 数组到剪贴板供团队更新源码。

工具栏须含：`全屏`、`导出坐标`、`导出图片`、`重置布局`（清除 localStorage 恢复默认）、保存状态提示。禁止仅内存持有坐标不做 localStorage；禁止以 localStorage 反向改规格。

#### E.6c 导出画布图片（`map.html` 必做）

将当前布局下全部节点 + 连线导出为 PNG。

| 项 | 规则 |
|----|------|
| 文件名 | `{终端编码}-map-{YYYY-MM-DD}.png` |
| 范围 | 全 PAGES 包围盒 + 48px 边距 |
| 技术 | `html2canvas@1.4.1` `scale: 2`（懒加载 CDN）；iframe 替换为占位块（展现编号+名称） |
| 交互 | 生成中禁用按钮 + Toast；完成后自动下载 |

实现：离屏容器 `#export-snapshot`（`position:fixed; left:-99999px`），克隆 `#connections` SVG + 各 `.page-node`，节点坐标保持世界坐标，`translate(offsetX, offsetY)` 对齐裁切框。`drawConnections()` 后导出确保连线一致；同对节点多连线须已平行错开。禁止要求手动截图或导出空白图。

#### E.6d 全屏（`map.html` 必做）

将 `#map-shell`（工具栏 + 画布 + hint）进入浏览器原生全屏：`requestFullscreen`/`webkitRequestFullscreen`。按钮文案：非全屏「全屏」/ 全屏中「退出全屏」；快捷键 **F** 切换（输入框不触发）、**Esc** 退出；`fullscreenchange` 时更新文案并重绘连线；不支持时 Toast 提示。

实现：`#map-shell` 占满 `100%`；`#viewport` 为 `flex:1; min-height:0`；Toast 置 shell 外。

#### E.7 同步纪律与验收

1. 增删页面：同步更新单页、`index.html` 侧栏、`map.html` PAGES/LINKS、版本镜像
2. 改跳转：先走 `/lny-prd-ui` → 改单页 → 改 `map.html` LINKS + `index.html` PAGE_DATA.actions
3. 验收：`map.html` 可本地打开；`ui_manifest §3` 页面无遗漏；单页跳转在 LINKS 有对应 `forward`/`back`/`tab`；TabBar 双向 `tab`；全屏/F/Esc/布局持久化/导出图片/index↔map 互链均可用；已镜像至 `versions/`

参考实现：`prototypes/MP/map.html`。

### F. 中文 UTF-8 写盘纪律（必做，防乱码）

> 乱码是写盘方式问题，非业务逻辑问题。事后修复脚本仅作紧急抢救；常规生成须事前规避 + 写后 30 秒验收。

#### F.1 根因与正确写盘

| 现象 | 根因 | 正确做法 | 禁止 |
|------|------|---------|------|
| 页面出现 `?`/半拉中文 | StrReplace 破坏 UTF-8 多字节中文 | 整文件 `write_text(encoding='utf-8')`；仅改 ASCII 可用 StrReplace | StrReplace 含 CJK / >3 行区块 |
| `UnicodeDecodeError: invalid continuation byte` | 文件已是无效 UTF-8 | 从同端已验收页复制壳层再改；禁止从已乱码文件续改 | `read_text(errors='replace')` 后写回 |
| PowerShell `python -c` 失败 | Windows GBK 与 UTF-8 混用 | 补丁写在 `.py` 源码内（`# -*- coding: utf-8 -*-`） | `python -c "…中文…"` / Shell heredoc |
| 原型镜像不一致 | 对主路径和镜像分次 StrReplace | 同一脚本同时写 `prototypes/` + `versions/.../prototypes/`，或 `shutil.copy2` | 对两路径分别 StrReplace |

#### F.2 写后验收（必做，≈30 秒）

```bash
python scripts/verify-prototype-utf8.py prototypes/MP/PAGE-MP-010.html versions/v1.0.0/prototypes/MP/PAGE-MP-010.html
```
- **exit 0** → 可继续；**exit 1** → 不得交付，用 F.1 整文件重写，禁止先汇报再跑 repair
- 校验项：合法 UTF-8；HTML 含 charset/lang；无 `??`/乱码占位
- **禁止**未跑验收就汇报「原型已更新」；禁止 `repair-*`/`fix-*` 纳入常规步骤

#### F.3 推荐脚本骨架

```python
# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "prototypes/MP/PAGE-MP-XXX.html",
    ROOT / "versions/v1.0.0/prototypes/MP/PAGE-MP-XXX.html",
]

def main():
    text = TARGETS[0].read_text(encoding="utf-8")
    text = text.replace("旧文案", "新文案")
    for p in TARGETS:
        p.write_text(text, encoding="utf-8", newline="\n")

if __name__ == "__main__":
    main()
```

### G. 原型 BUG 预防规则（必守）

> **原则**：交付原型前须消除已知 BUG；严禁将明显有缺陷的原型作为「已完成」交付。

#### G.1 代码变更引用检查（必做）

对原型 HTML/JS 做 **任何涉及删除或重命名** 的操作（函数、变量、CSS 类、id、DOM 元素）时，**必须先** 全文件搜索引用并修复，再宣告完成：

| 变更类型 | 须搜索的模式 | 工具/命令 |
|---------|-------------|----------|
| 删除函数 `foo()` | `foo(`、`foo (` | `rg "foo\(" prototypes/` |
| 删除变量 `bar` | `bar`（注意排除 `foobar` 等超集） | `rg "\bbar\b" prototypes/` |
| 删除 CSS 类 `.cls` | `cls`、`class="cls"` | `rg "cls" prototypes/` |
| 删除 id `#x` | `x`、`getElementById('x')` | `rg "getElementById\('x'\)" prototypes/` |
| 删除 DOM 元素 | 元素 id、class、关联的事件绑定 | `rg "addEventListener"` 等 |
| 拆分/合并 `<script src>` 标签 | `<script src="...">` 之后是否有 `</script>` | 打开 HTML，检查 Networks 面板各 js 是否 200 加载；检查 Console 无 ReferenceError |
| 新增函数/注入代码模板 | 函数体内引用的全局变量名（如 `ApiClient`、`ProtoStore`） | 搜索 `var {变量名}`、`global\.{变量名}`、`window\.{变量名}` 确认变量真实存在；对比同文件已有代码确认命名一致；**特别关注** `ProtoApiClient` vs `ApiClient` 的拼写差异 |
| 壳层汇总页菜单项超出视口 | `.sidebar` 的 `overflow` 值 | 检查 `index.html` 中 `.sidebar` 有 `overflow-y: auto`（折叠态仍 `overflow: hidden`）；视图高度 600px 时仍可滚动到底部菜单项 |

**警告**：`<script src="...">` 非自闭合标签，改写极易丢失 `</script>` 导致 `ReferenceError`——改写后须打开页检查 Console。新增代码引用全局变量须搜索确认 `assets/` 下存在对应定义；禁止凭记忆写变量名（如 `ProtoApiClient`）。删除/重命名后须实际打开文件验证无控制台报错。

#### G.2 状态演示按钮归位检查（必做）

> 详细规则见上文 **§C.5「状态演示归属判断原则」**。

每生成或修改一个 `PAGE-*.html` 原型后，逐文件检查：

1. 搜索演示标记：`demo-`/`setDemo`/`showDemo`/`mock-`/`test-`/`fake-` + `alert('原型`/`alert("原型` + `v{版本号}` 开头 id
2. 判定归属：模拟后端/系统状态 → 移至 §C 面板并删页内按钮；用户交互操作 → 保留
3. §C 面板须用统一 MUI 控件（`ToggleButtonGroup`/`Select`/`ButtonGroup`），禁止与原页面风格不一致的自定义样式

#### G.3 自检清单（生成/修改原型后必须逐页过）

| 序号 | 检查项 | 通过标准 |
|------|--------|---------|
| G3.1 | JS 控制台报错 | 打开原型 HTML，F12 Console 无红色报错 |
| G3.2 | 页面渲染完整 | 所有节点可见，无 `display:none` 导致的意外隐藏 |
| G3.3 | 演示按钮归位 | 页内无 `demo-*` / `setDemo*` 等演示专用按钮（若有且为后端模拟 → 移至 §C） |
| G3.4 | §C 状态选项一致 | §C 面板选项与 `ui/COMP-*.md` 状态矩阵 **逐字一致** |
| G3.5 | 链接/表单可操作 | 跳转 `href`、`location.href`、`postMessage` 监听均有效 |
| G3.6 | UTF-8 无乱码 | `verify-prototype-utf8.py` 返回 exit 0 |
| G3.7 | 版本专属演示标记清理 | 页内无上一版本的演示横幅 ID（如 `v107DemoTip`、`v107MpHint`、`v108DemoTip` 等），无版本号出现在 HTML `id` 中作演示标记 |
| G3.8 | alert 桩位已升级为真实交互 | 页内无 `alert('原型：…')` / `alert("原型：…")` 等未实现功能的桩位；交互均已落地为真实弹窗/跳转/Toast（接口模拟演示除外，须标注 `// 接口桩位-待接入`） |
| G3.9 | 单一功能无重复事件监听 | 同一操作（如教程步骤按钮点击）无全局 `click` + 局部 `onclick` **两套** 监听器同时存在；旧桩位事件监听器已移除 |
| G3.10 | `<script>` 标签闭合 | 所有 `<script src="...">`（外部脚本）均有对应 `</script>`；打开 HTML 后 F12 Network 确认 js 文件均 200 加载；Console 无 `ReferenceError: xxx is not defined` |
| G3.11 | 全局变量引用存在 | 页内所有 `XXX.invoke()`、`XXX.method()` 等全局调用的变量名在 `assets/` 下有对应的 `global.XXX =` 或 `var XXX =` 定义；`rg "ProtoApiClient" prototypes/` 须返回 0（该变量名不存在） |
| G3.12 | 壳层侧栏可滚动 | `index.html` 的 `.sidebar` 设置了 `overflow-y: auto`（非 `overflow: hidden`）；`.sidebar-header` 有 `flex-shrink: 0`；所有 `.sidebar-group` 菜单项均可由滚动到达 |

#### G.4 跨版本补丁卫生检查（迭代切换必做）

> 补丁直接改 `prototypes/` 根目录后镜像到 `versions/`，旧版本标记会随模板污染后续版本。

**版本切换前清理**（`/lny-prd-iter` 或 `/lny-prd-prototype` 前）：

| 搜索 | 标准 | 命令 |
|------|------|------|
| 上版演示 id | root `prototypes/` 无 `v{旧版}` 开头 id | `rg "id=\"v[0-9]+\.[0-9]+\.[0-9]+" prototypes/` |
| alert 桩位 | root `prototypes/` 无 `alert('原型：` | `rg "alert\([\"']原型" prototypes/` |
| 版专属 CSS 注释 | 无对应功能则移除 | `rg "/\* v[0-9]\.[0-9]\.[0-9]" prototypes/` |

**补丁纪律**：每个 `patch_*.py` 须配套卸载逻辑（`unpatch_*.py` 或 `--revert`）；禁止单独补丁 root 不写卸载；以干净 root 为基准生成新版。

**生成后自检**：root 无前版演示 id/alert 桩位；版本目录无跨版污染；补丁脚本有卸载入口。

## 前置条件
- 必须已执行 `/lny-prd-master` 初始化项目
- 必须已执行 **`/lny-prd-ui`** 完成用户界面设计（含页面与组件索引）
- `ui_manifest.md` 或 `ui/PAGE-*.md` 中必须包含目标页面定义
- 项目根目录须存在 **`ui_manifest.md`** 与 **`api_spec.md`**，且与本次生成页面相关章节已可读（与上文 **规格先行** 一致）

## 输入变量
```yaml
版本号: v1.0.0
页面编号列表: (可选，不指定则生成本版本所有变更页面)
```

触发时一次给齐 **版本号**、**页面编号列表**（可选）；须已有 `versions/{版本号}/`；范围不明则对话补全。

## 执行步骤

1. **参数与环境**：`版本号` 必填；须存在 `versions/{版本号}/`；缺则提示。
2. **读入上下文**：`main_spec.md`（第4章终端说明）、`api_spec.md`、`ui_manifest.md`、`feature_spec.md`（及 `ui/`、`feature/` 明细若存在）；`versions/{版本号}/iteration_notes.md` 作本版变更摘要。
3. **工程与目录**：按需初始化或增量修改 **`prototypes-mui-app/`**；确保 `prototypes/{终端}/`、`versions/{版本号}/prototypes/{终端}/` 父目录存在（`{终端}` 取本批页面实际集合，∈ `MP`/`H5`/`APP`/`PC`/`AD`）。
4. **桌面类**（`PAGE-PC-*`、`PAGE-AD-*`）：在 **`prototypes-mui-app/`** 内开发 React + MUI → **build** → 静态产物入 **`prototypes/PC/`、`prototypes/AD/`**（优先 mui-mcp / [MUI 文档](https://mui.com/material-ui/)）。
5. **页面范围**：按 `页面编号列表` 或本版本全部目标页；逐页更新 **`prototypes/{终端}/PAGE-*.html`**（及构建 chunk）；**移动类**可为静态 HTML，模块带 `data-module-id="{页面编号}-{区域缩写}"`。桌面/移动结构细则见上文 **§A / §B**。
6. **壳与汇总**：桌面 **布局母版**（通顶左栏 + 让位顶栏 + **§C 左 panel + iframe**）+ 右侧五项 **Drawer**；每移动终端线 **`index.html`**（§B + §D）+ **`map.html` 关系画布**（§E，与单页跳转同步）；**镜像**至 **`versions/{版本号}/prototypes/{终端}/`**（仅静态，无 `node_modules`/源码）。
7. **交互（力所能及）**：跳转、表单反馈、列表加载、弹窗/抽屉、Tab、移动端下拉刷新、可交互元素 `title` 等；**局部自定义UI组件多态演示**：壳层 **§C 左侧面板** + iframe **`postMessage`/hash 联动**（TabBar 豁免页隐藏 §C 面板）；**遵守 §C.5** 判断哪些状态归入 §C。
8. **UTF-8 验收（§F.3）**：对本次新增/更新的每个 `prototypes/**` 与对应 `versions/.../prototypes/**` 镜像执行 `python scripts/verify-prototype-utf8.py …`；**失败则重写，不得交付**。
9. **BUG 自检（§G.3）**：逐页过自检清单——JS 控制台无报错、演示按钮归位 §C、§C 状态选项与 COMP 一致、链接/表单可操作；**有 BUG 修复后再宣告完成**。
10. **输出**：构建命令与结果摘要；`prototypes/` 与 `versions/.../prototypes/` 变更路径列表（不含 `node_modules`）；附 **UTF-8 验收通过 + BUG 自检通过** 说明。

## 输出示例
```
已生成 / 已构建原型：

【MUI 工程】prototypes-mui-app/ → npm run build → 静态产物

prototypes/
├── MP/
│   ├── index.html
│   ├── map.html              # 关系画布（移动端默认）
│   └── PAGE-MP-001.html
├── AD/
│   ├── index.html              # 或由 Vite 生成的壳层入口 + assets/
│   └── ...
└── PC/
    └── ...

versions/v1.0.0/prototypes/    # 仅静态镜像，与上表同结构
├── MP/
│   ├── index.html
│   ├── map.html
│   └── PAGE-MP-001.html
└── AD/
    └── ...
```
