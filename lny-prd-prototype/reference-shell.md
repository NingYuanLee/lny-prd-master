# 原型壳层与关系图（§A–E）

仅在生成/更新原型时 Read。皮肤、类名、`PROTO_SHELL` 字段见 [`reference-kit.md`](reference-kit.md)（全局 token）与 `reference-kit/shell.md` 分片。**禁止**另写侧栏/顶栏/状态演示/规格说明 DOM 或 `fitPhoneFrame`——套件 `proto-shell.js` 已实现。

## 目录

- 单页、`index.html`、`assets/` 均在 `prototypes/{终端}/`（`MP` / `H5` / `APP` / `PC` / `AD`）。框架通用页（如 AD 登录）不生成 `PAGE-*.html`。
- 根 `prototypes/` 是唯一原型树；禁止写 `versions/{版本号}/prototypes/`、`node_modules` / npm / `prototypes-mui-app/`。
- 生成前 `copy-kit.py`；各端 `index.html` 只填 `PROTO_SHELL`。总入口见 [`reference-scope.md`](reference-scope.md)。
- 各端 `index.html` 右下角 SKILL 小字由 `proto-shell.js` 注入（GitHub / Gitee 技能包地址）。禁止手写、禁止删。总入口标注见 [`reference-scope.md`](reference-scope.md)。

## 硬规则（套件已实现，禁止改布局）

- 左菜单通顶；按模块分组，分组标题可点收缩，当前页所在组保持展开。菜单项显示页面名称，下方小字 PAGE 编码。AppBar 只在主内容区上方、让出侧栏宽度。
- 页单收起、状态演示收起按钮在顶栏；收起后宽度 0、不留窄条。
- 状态演示在 iframe **左侧**并排（固定 200px），禁止放 iframe 上方或顶栏内。
- 移动端预览：375×812 为**屏内**尺寸，`scale ≤ 1`，外围无滚动条；iframe 内滚动保留。设备框 10px 边框在屏外（`box-sizing: content-box`），避免壳页全局 `border-box` 把右边/底边切掉约 20px。
- 规格说明面板固定 375px。桌面 iframe 无手机框，可不套缩放。
- 不区分观看模式，无 `?audience=`。顶栏始终提供：规格说明、状态演示、关系图（移动端）。

```text
┌──────────┬────────────────────────────────────────────┐
│          │ AppBar [☰页单] [◧状态演示] … [规格说明]          │
│ 左菜单   ├──────────┬─────────────────────────────────┤
│ （通顶） │ 状态演示  │ iframe（移动端 §D 缩放）         │
│          │ 200px    │                                 │
└──────────┴──────────┴─────────────────────────────────┘
```

### A. 桌面（PC / AD）

一套壳：`mode: "desktop"`。侧栏两级（模块 → 页面），模块组可收缩；不得用覆盖式侧栏做主导航。单页只承载界面，规格进右侧规格说明。D1-1 用 `.md-d1` / `.md-table`，D5 用 `.md-dialog`。

### B. 移动（MP / H5 / APP）

每端：`index.html`（`mode: "mobile"`）+ 单页 + **`map.html`（关系图，默认必做）**。`index.html` ↔ `map.html` 顶栏互链。本版本未生成的页可不进菜单。

### 规格说明五项（`PROTO_SHELL.pages[].spec`）

顺序固定。当前页以侧栏选中为准，规格说明内不重复「当前页面」标题。

1. **页面布局说明** ← `ui/PAGE-*.md`
2. **局部自定义UI组件说明** ← `ui/COMP-*.md`（名称逐字一致；注明状态切换入口）
3. **接口交互说明**：首行 `API-{终端}-{序号} · 描述`；交互独占第二行起
4. **Feature 关联清单**：`FEATURE-* · 名称 · 本页关联点`；无则 **无**
5. **操作交互说明**（非流程 ⑤）：`事件类型 · 交互描述`，不写序号

### C. 状态演示

数据来自 `ui/COMP-*.md` 状态矩阵，禁止编造。`comps[].states` 必须与矩阵逐字、按行顺序一致；页面实际 DOM 还必须为每个状态提供视觉实现。默认显示状态演示。只有产品页内 TabBar/Tabs/SegmentedControl 明确承担同一组件状态切换时，才显式写 `stateDemo: false` 隐藏壳层演示。旧字段 `tabBarExempt` 不再控制状态面板，禁止用它代替状态矩阵。

- **须进状态演示**（禁止页内演示按钮）：后端数据态（空/加载/失败）、系统/环境态（权限、未授权）。
- **可留页内**：用户点击/滑动/输入、页内 TabBar 切态。
- 自检：`demo-*` / `setDemo*` 且模拟后端 → 移入状态演示。切态用 `postMessage`（`proto-page.js` 已监听）。
- `loading` 必须配 `data-skel-for`，`empty`/`error` 必须配 `data-empty-for`；其它状态必须配 `<… data-state-for="COMP-xxx" data-state="状态" …>` 视觉块。没有视觉差异的状态不得写入矩阵或壳层。

### D. 移动端缩放

由 `proto-shell.js` 的 `fitPhoneFrame` 在加载、resize、切页、页单/状态演示收起后重算。禁止另写缩放脚本或给 `.preview-area` 设 `overflow: auto`。触屏预览区用 `overflow: visible`，手机阴影画在 `.phone-scale-host` 上（不要画在 `.phone-frame` 上，会被缩放层裁掉）。

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
- [ ] 6. 验收 index / map / 单页的路径和互链均在根 prototypes/{终端}/ 内
```

#### E.3 `PAGES`

```javascript
{ id: 'PAGE-MP-001', name: '首页', module: '主包 · home', file: './PAGE-MP-001.html', x: 480, y: 320 }
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

`label` 为触发点简称，画在连线中点（TabBar 可写 `TabBar`）。检索：`rg "href=\"PAGE-|location\\.href" prototypes/MP/`。

#### E.5 初始布局

按业务簇排布。节点预览区宽高比与真机预览一致（默认 **375×812**，与 `fitPhoneFrame` 同源）；节点宽 **200px**，预览区高 `200 × 812 / 375 ≈ 433px`，禁止把缩略裁成扁条。原点水平间距 ≥ **320px**、垂直 ≥ **680px**（预览总高 + 标题栏 + 空隙）。`x,y` 为默认值；用户拖过的位置由套件写入 localStorage，刷新后仍在，**不要**把缓存坐标写回规格。

#### E.6 结构与能力

单文件 HTML。`#map-shell` flex 纵向（工具栏 + `#viewport` flex:1）；禁止工具栏与 viewport 双 `position: fixed`。

须具备：空白拖拽平移；滚轮缩放（光标中心，`scale` ∈ `[0.15, 2.5]`）；拖标题栏移节点并重绘连线；**预览区按真机比例完整显示**（iframe `375×812` 缩放到节点宽）；iframe `pointer-events: none`，点击 overlay 新标签打开单页；SVG **三次贝塞尔**、边到边**端口错开**（同一侧多条线沿边分布，同对节点再垂直错开），**线中点写 `label`**；底部 **图例为色线样本+名称**（由 `proto-map.js` 注入 `#map-legend`，禁止只写「绿实线=跳转」）。

`map.html` **只填数据**：`ProtoMap.boot({ project, terminal, pages, links })`。拖拽、缓存、缩放、导出、全屏由 `assets/proto-map.js` 实现，禁止在 `map.html` 手写第二套画布逻辑。

核心入口：`ProtoMap.boot`（内部含 `applyTransform`、`getNodeBox`、`drawConnections`、`createNodes`、`fitAll`、`zoomAt`、`exportCanvasImage`、`toggleFullscreen`）。

```javascript
ProtoMap.boot({
  project: "mini-shop",
  terminal: "MP",
  pages: [
    { id: "PAGE-MP-001", name: "首页", module: "首页", file: "./PAGE-MP-001.html", x: 80, y: 80 }
  ],
  links: [
    { from: "PAGE-MP-001", to: "PAGE-MP-002", type: "tab", label: "TabBar" }
  ]
});
```

线型由套件内置：`forward` 绿实线、`back` 灰虚线、`tab` 蓝虚线、`embed` 紫点线。iframe `loading="lazy"`；>15 页可改为占位 + 双击加载。实现以本节 `PROTO_MAP.boot` 结构与 `kit/proto-map.js` 为准。

#### E.6b 布局持久化

localStorage（debounce 300ms，键 `{project}-{终端}-map-layout-v1`，含 `pages[{id,x,y}]` + `viewport`）。拖节点、平移、缩放后自动写入；刷新或下次打开同一浏览器仍在原位，清站点数据才恢复默认。工具栏须有：全屏、导出图片、重置布局（清除该键并回到 `boot` 里的默认 `x,y`）。禁止只放内存；禁止把缓存坐标写回规格或 `map.html`。

#### E.6c 导出 PNG

工具栏「导出图片」调用 `ProtoMap.exportCanvasImage`。文件名 `{终端编码}-map-{YYYY-MM-DD}.png`；全 PAGES 包围盒 + 48px；Canvas 2D `scale: 2` 离屏绘制节点占位（编号+名称+真机比例手机框）、错开连线与线标签。**不**依赖 html2canvas / CDN，`file://` 可用。iframe 真机画面不进 PNG。生成中 Toast。禁止要求用户手动截图。

#### E.6d 全屏

`#map-shell` 走 `requestFullscreen`；按钮「全屏」/「退出全屏」；**F** 切换（输入框不触发）、**Esc** 退出；不支持则 Toast。

#### E.7 同步与验收

增删页：同步单页、index 侧栏与 PAGES/LINKS。改跳转：先 ② → 单页 → LINKS + `spec.actions`。验收：可本地打开；manifest 页无遗漏；跳转有对应线型；TabBar 双向 `tab`；全屏/持久化/导出/互链可用；无 `versions/{v}/prototypes/` 副本。
