# 原型壳层（§A–D）

仅在生成/更新原型时 Read。壳层资源（`kit/`）与总入口写法见本文件。**禁止**另写侧栏/顶栏/状态演示/规格说明 DOM 或 `fitPhoneFrame`——套件 `proto-shell.js` 已实现。壳层和总入口的样式与交互由本文件固定。业务 `PAGE-*.html` 只嵌入壳层，不继承壳层皮肤，页面视觉由业务规格和页面设计决定。

## 目录

- 单页、`index.html`、`assets/` 均在 `prototypes/{终端}/`（`MP` / `H5` / `APP` / `PC` / `AD`）。框架通用页（如 AD 登录）不生成 `PAGE-*.html`。
- 根 `prototypes/` 是唯一原型树；禁止写 `versions/{版本号}/prototypes/`、`node_modules` / npm / `prototypes-mui-app/`。
- 生成前 `copy-kit.py`；各端 `index.html` 只填 `PROTO_SHELL`。总入口见 [`reference-scope.md`](reference-scope.md)。
- 各端 `index.html` 右下角 SKILL 小字由 `proto-shell.js` 注入（GitHub / Gitee 技能包地址）。禁止手写、禁止删。总入口标注见 [`reference-scope.md`](reference-scope.md)。

## 复制与引用（壳层）

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/modules/lny-prd-prototype/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。禁止改 kit 源文件来迁就某一页，也禁止将套件副本写到 `versions/{v}/prototypes/`。禁止生成 `serve.json`。本地预览：在 `prototypes/` 目录执行 `python -m http.server`。

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | 按页面实际使用引用本地资源。业务页可以只使用项目自有 CSS；移动页需要状态栏或页面行为时引用 `./assets/proto-page.js`，使用套件控件时再引用 `./assets/mui-kit.css`，使用套件图标时再引用图标脚本 |
| `index.html` 汇总壳 | 上表 + `./assets/proto-shell.css` + `./assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |

业务页可以使用项目自有 CSS、组件库和 `assets/` 下真实素材。页面不需要套件样式时无需引入 `mui-kit.css`。壳层源文件保持不改，业务页的视觉实现可以独立组织。

### `index.html`（数据驱动壳）

只填 `PROTO_SHELL`，**不要**手写侧栏/顶栏/状态演示/规格说明 DOM。右下角 SKILL 标注由 `proto-shell.js` 注入，不要写进本页 HTML。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>MP 原型</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <link rel="stylesheet" href="./assets/mui-kit.css">
  <link rel="stylesheet" href="./assets/proto-shell.css">
</head>
<body>
  <div id="proto-root"></div>
  <script>
    window.PROTO_SHELL = {
      terminal: "MP",
      mode: "mobile",
      title: "小程序原型",
      pages: [
        {
          id: "PAGE-MP-001",
          name: "首页",
          module: "首页",
          file: "./PAGE-MP-001.html",
          stateDemo: true,
          comps: [],
          spec: {
            layout: "依据 ui/PAGE-MP-001.md …",
            comps: "COMP-001 · 商品卡片 · 状态见页内/豁免",
            apis: "API-MP-001 · 查询推荐\n进页请求；失败 Toast。",
            features: "FEATURE-001 · … · 本页关联点",
            actions: "点击 · 卡片无出页（当前演示）"
          }
        }
      ]
    };
  </script>
  <script src="./assets/md-icons.js"></script>
  <script src="./assets/icons-extra.js"></script>
  <script src="./assets/proto-shell.js"></script>
</body>
</html>
```

| 字段 | 规则 |
|------|------|
| `mode` | MP/H5/APP → `mobile`（手机框 + `fitPhoneFrame`）；PC/AD → `desktop`（iframe 铺满，无手机框） |
| `stateDemo` | 默认显示状态演示；仅当页内 TabBar/Tabs/SegmentedControl 明确承担同一 COMP 切态时才写 `false` |
| `tabBarExempt` | 已废弃兼容字段，不控制状态演示；禁止用它隐藏有 COMP 的页面 |
| `comps[].states` | 与 `ui/COMP-*.md` 状态矩阵 **逐字、按行顺序一致**；每个状态必须有页面视觉实现 |
| `spec` 五项 | 顺序固定；接口首行 `API-* · 描述`，交互另起一行 |

## 硬规则（套件已实现，禁止改布局）

- 左菜单通顶；按模块分组，分组标题可点收缩，当前页所在组保持展开。菜单项显示页面名称，下方小字 PAGE 编码。AppBar 只在主内容区上方、让出侧栏宽度。
- 页单收起、状态演示收起按钮在顶栏；收起后宽度 0、不留窄条。
- 状态演示在 iframe **左侧**并排（固定 200px），禁止放 iframe 上方或顶栏内。
- 移动端预览：375×812 为**屏内**尺寸，`scale ≤ 1`，外围无滚动条；iframe 内滚动保留。设备框 10px 边框在屏外（`box-sizing: content-box`），避免壳页全局 `border-box` 把右边/底边切掉约 20px。
- 规格说明面板固定 375px。桌面 iframe 无手机框，可不套缩放。
- 不区分观看模式，无 `?audience=`。顶栏始终提供：规格说明、状态演示。

```text
┌──────────┬────────────────────────────────────────────┐
│          │ AppBar [☰页单] [◧状态演示] … [规格说明]          │
│ 左菜单   ├──────────┬─────────────────────────────────┤
│ （通顶） │ 状态演示  │ iframe（移动端 §D 缩放）         │
│          │ 200px    │                                 │
└──────────┴──────────┴─────────────────────────────────┘
```

### A. 桌面（PC / AD）

一套壳：`mode: "desktop"`。侧栏两级（模块 → 页面），模块组可收缩；不得用覆盖式侧栏做主导航。单页只承载界面，规格进右侧规格说明。页面类名可用套件类名，也可用项目自有样式；壳层 DOM 一律由 `proto-shell.js` 渲染。

### B. 移动（MP / H5 / APP）

每端：`index.html`（`mode: "mobile"`）+ 单页。本版本未生成的页可不进菜单。

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
