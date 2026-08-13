# 原型壳层与关系图（§A–E）

仅在生成/更新原型时 Read。皮肤、类名、`PROTO_SHELL` 字段见 [`reference-kit.md`](reference-kit.md)。**禁止**另写侧栏/顶栏/状态演示/规格说明 DOM 或 `fitPhoneFrame`——套件 `proto-shell.js` 已实现。

## 目录

- 单页、`index.html`、`assets/` 均在 `prototypes/{终端}/`（`MP` / `H5` / `APP` / `PC` / `AD`）。框架通用页（如 AD 登录）不生成 `PAGE-*.html`。
- 镜像到 `versions/{版本号}/prototypes/{终端}/`（含 `assets/`）。禁止 `node_modules` / npm / `prototypes-mui-app/`。
- 生成前 `copy-kit.py`；`index.html` 只填 `PROTO_SHELL`。根 `scope.html` 见 [`reference-scope.md`](reference-scope.md)。

## 硬规则（套件已实现，禁止改布局）

- 左菜单通顶；AppBar 只在主内容区上方、让出侧栏宽度。
- 页单收起、状态演示收起按钮在顶栏；收起后宽度 0、不留窄条。
- 状态演示在 iframe **左侧**并排（固定 200px），禁止放 iframe 上方或顶栏内。
- 移动端预览：375×812 设备框，`scale ≤ 1`，外围无滚动条；iframe 内滚动保留。
- 规格说明面板固定 375px。桌面 iframe 无手机框，可不套缩放。
- 不区分观看模式，无 `?audience=`。顶栏始终提供：规格说明、状态演示、关系图（移动端）、范围说明（当前页短说明）。

```text
┌──────────┬────────────────────────────────────────────┐
│          │ AppBar [☰页单] [◧状态演示] … [范围说明] [规格说明] │
│ 左菜单   ├──────────┬─────────────────────────────────┤
│ （通顶） │ 状态演示  │ iframe（移动端 §D 缩放）         │
│          │ 200px    │                                 │
└──────────┴──────────┴─────────────────────────────────┘
```

### A. 桌面（PC / AD）

一套壳：`mode: "desktop"`。侧栏两级（模块 → 页面），不得用覆盖式侧栏做主导航。单页只承载界面，规格进右侧规格说明。D1-1 用 `.md-d1` / `.md-table`，D5 用 `.md-dialog`。

### B. 移动（MP / H5 / APP）

每端：`index.html`（`mode: "mobile"`）+ 单页 + **`map.html`（关系图，默认必做）**。`index.html` ↔ `map.html` 顶栏互链。本版本未生成的页可不进菜单。

### 规格说明五项（`PROTO_SHELL.pages[].spec`）

顺序固定。当前页以侧栏选中为准，规格说明内不重复「当前页面」标题。

1. **页面布局说明** ← `ui/PAGE-*.md`
2. **局部自定义UI组件说明** ← `ui/COMP-*.md`（名称逐字一致；注明状态切换入口）
3. **接口交互说明**：首行 `API-{终端}-{序号} · 描述`；交互独占第二行起
4. **Feature 关联清单**：`FEATURE-* · 名称 · 本页关联点`；无则 **无**
5. **操作交互说明**（非流程 ⑤）：`事件类型 · 交互描述`，不写序号

### 范围说明（当前页，`PROTO_SHELL.pages[].brief`）

人话两三句：这页干什么、主路径能做什么。从 `ui/PAGE-*.md` / `pages_prd` 抽取。禁止编造、禁止贴 API 编号。切页后跟着变。**不**链根 `scope.html`。

### C. 状态演示

数据来自 `ui/COMP-*.md` 状态矩阵，禁止编造。选项与矩阵逐字一致。`tabBarExempt: true` 时隐藏状态演示（页内 TabBar/Tabs 已承担切态）。

- **须进状态演示**（禁止页内演示按钮）：后端数据态（空/加载/失败）、系统/环境态（权限、未授权）。
- **可留页内**：用户点击/滑动/输入、页内 TabBar 切态。
- 自检：`demo-*` / `setDemo*` 且模拟后端 → 移入状态演示。切态用 `postMessage`（`proto-page.js` 已监听）。

### D. 移动端缩放

由 `proto-shell.js` 的 `fitPhoneFrame` 在加载、resize、切页、页单/状态演示收起后重算。禁止另写缩放脚本或给 `.preview-area` 设 `overflow: auto`。

---

### E. 移动端关系图（`map.html`，默认必做）

移动端须同步维护关系图，不得只生成单页与 `index.html`。桌面端不强制。

#### E.1 三件套与同步方向

| 产物 | 路径 | 职责 |
|------|------|------|
| 单页原型 | `prototypes/{终端}/PAGE-{终端}-{序号}.html` | 可点击跳转的页面 HTML |
| 汇总预览 | `prototypes/{终端}/index.html` | `PROTO_SHELL` 壳（§B） |
| **关系图** | `prototypes/{终端}/map.html` | 缩略预览 + 连线 + 平移缩放 |

页面清单、跳转须与 `ui_manifest` / `ui/PAGE-*` / 单页 `href` 一致。同步：规格 → 单页 → `index.html` + `map.html`。禁止以 `map.html` 反向改规格。

#### E.2 工作流

```
- [ ] 1. 从 ui_manifest §3 + ui/PAGE-*.md 列出本终端 PAGE-*
- [ ] 2. 从单页 href/location.href + 操作说明提取 LINKS
- [ ] 3. 创建或更新 map.html（PAGES + LINKS + 布局）
- [ ] 4. index ↔ map 顶栏互链
- [ ] 5. 跳转变更时同步 LINKS 与 spec.actions
- [ ] 6. 镜像至 versions/{版本号}/prototypes/{终端}/map.html
```

#### E.3 `PAGES`

```javascript
{ id: 'PAGE-MP-001', name: '首页', module: '主包 · home', file: 'PAGE-MP-001.html', x: 480, y: 320 }
```

`id`/`name`/`module`/`file` 与规格逐字一致；`x,y` 见 E.5。须与 `index.html` 页单同源。

#### E.4 `LINKS`

合并去重，禁止编造：单页 `href`/`location.href`；`ui/PAGE-*` 跳转；`spec.actions`；TabBar 双向 → `tab`；弹窗嵌入 → `embed`。

```javascript
{ from: 'PAGE-MP-001', to: 'PAGE-MP-003', type: 'forward', label: '搜索入口' }
```

| type | 含义 | 线型 |
|------|------|------|
| `forward` | 正向跳转 | 绿色实线 + 箭头 |
| `back` | 返回 | 灰色虚线 + 箭头 |
| `tab` | TabBar | 蓝色虚线 + 箭头 |
| `embed` | 弹窗/Sheet 嵌入 | 紫色点线，无箭头 |

`label` 为触发点简称；TabBar 可省略。检索：`rg "href=\"PAGE-|location\\.href" prototypes/MP/`。

#### E.5 初始布局

按业务簇排布。间距水平 ≥ 240px、垂直 ≥ 280px；节点宽 **200px**（375×812 缩至 0.5333）。可保留用户拖过的 `x/y`。

#### E.6 结构与能力

单文件 HTML。`#map-shell` flex 纵向（工具栏 + `#viewport` flex:1）；禁止工具栏与 viewport 双 `position: fixed`。

须具备：空白拖拽平移；滚轮缩放（光标中心，`scale` ∈ `[0.15, 2.5]`）；拖标题栏移节点并重绘连线；iframe `pointer-events: none`，点击 overlay 新标签打开单页；SVG 二次贝塞尔、边到边、平行错开。

核心函数：`applyTransform`、`getNodeBox`、`getEdgePoint`、`drawConnections`、`createNodes`、`fitAll`、`zoomAt`、`getContentBounds`、`exportCanvasImage`、`toggleFullscreen`、`updateFullscreenButton`。

```javascript
var STYLE = {
  forward: { stroke: '#3fb950', dash: '', width: 2 },
  back:    { stroke: '#8b949e', dash: '6 4', width: 1.5 },
  tab:     { stroke: '#58a6ff', dash: '8 4', width: 2 },
  embed:   { stroke: '#d2a8ff', dash: '2 4', width: 1.5 }
};
```

iframe `loading="lazy"`；>15 页可改为占位 + 双击加载。参考 `examples/mini-shop/prototypes/MP/map.html`。

#### E.6b 布局持久化

localStorage（debounce 300ms，键 `{项目}-{终端}-map-layout-v1`，含 `pages[{id,x,y}]` + `viewport`）+ 工具栏「导出坐标」。须有：全屏、导出坐标、导出图片、重置布局。禁止只放内存；禁止用 localStorage 改规格。

#### E.6c 导出 PNG

文件名 `{终端编码}-map-{YYYY-MM-DD}.png`；全 PAGES 包围盒 + 48px；`html2canvas@1.4.1` `scale: 2`（懒加载 CDN）；iframe 换成编号+名称占位；生成中 Toast。离屏 `#export-snapshot` 克隆 SVG 与节点。禁止要求手动截图。

#### E.6d 全屏

`#map-shell` 走 `requestFullscreen`；按钮「全屏」/「退出全屏」；**F** 切换（输入框不触发）、**Esc** 退出；不支持则 Toast。

#### E.7 同步与验收

增删页：同步单页、index 侧栏、PAGES/LINKS、镜像。改跳转：先 ② → 单页 → LINKS + `spec.actions`。验收：可本地打开；manifest 页无遗漏；跳转有对应线型；TabBar 双向 `tab`；全屏/持久化/导出/互链可用；已镜像。
