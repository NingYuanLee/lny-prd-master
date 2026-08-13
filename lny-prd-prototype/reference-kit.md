# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角 4px、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。

**原型默认高保真**：与 `ui/PAGE`「视觉细节」估点档位无关。⑥ 必须按本节「高保真落地」出图，禁止线框式两张灰卡、禁止「示例商品 A」。

## 高保真落地（必守）

写每一页 HTML 时按此表。未达则不得交付。

| 项 | 要求 |
|----|------|
| 夹具数据 | 用符合业务域的中文名称与真实量级价格（如 `有机草莓 250g` / `¥19.90`）。**禁止** `示例商品 A/B`、`测试数据`、`xxx`、`Item 1` |
| 条数 | 列表/卡片/表格默认态 **≥4 条**（规格写明空态、或 API 写死更少条数时从其规定；首页有「每页条数」则按其值） |
| 字段 | API/COMP 已列的展示字段都要出现（名称、图、价、库存状态等）；**不**发明规格没有的字段（如无「销量」就不要写已售） |
| 图片 | `md-card__media md-media-ph md-media-ph--{1-6}` 轮换；禁止无编号的纯灰 `md-media-ph`、禁止随机色块 |
| 移动端 | 必须有 `md-status-bar`（L0 系统栏）；`md-section-head` 写分区标题；列表优先 `md-card md-card--row` |
| 桌面端 | 必须有 `md-page-head`；表格首列可用 `md-row-goods` + `md-thumb md-media-ph--n`。规格出现的弹窗/签/下拉/日期/按钮组必须用本节 AD 控件，禁止裸 `alert` / 无样式 `<select>` |
| 间距 | 只用套件：分区头 / 栅格 / `md-d1`，禁止用内联 `margin` 当排版 |

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。镜像 `versions/{v}/prototypes/{终端}/` 时 **须连同 `assets/`**（含 extras 与 `icons/`）。禁止改 kit 源文件来迁就某一页。

## 引用（硬性）

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | `assets/mui-kit.css` + `assets/md-icons.js` + `assets/icons-extra.js` + `assets/proto-page.js` |
| `index.html` 汇总壳 | 上表 + `assets/proto-shell.css` + `assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |
| `map.html` | 建议 `assets/mui-kit.css` 做工具栏；画布逻辑仍按 `reference-shell.md` §E |

禁止：页内 `<style>` 改 `--md-primary` / 另写一套按钮色；内联 `style` 仅允许布局占位（宽高/显示），不得当主题。

## `index.html`（数据驱动壳）

只填 `PROTO_SHELL`，**不要**手写侧栏/顶栏/状态演示/规格说明 DOM。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>MP 原型</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="assets/mui-kit.css">
  <link rel="stylesheet" href="assets/proto-shell.css">
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
          file: "PAGE-MP-001.html",
          tabBarExempt: true,
          comps: [],
          spec: {
            layout: "依据 ui/PAGE-MP-001.md …",
            comps: "COMP-001 · 商品卡片 · 状态见页内/豁免",
            apis: "API-MP-001 · 查询推荐\n进页请求；失败 Toast。",
            features: "FEATURE-001 · … · 本页关联点",
            actions: "点击 · 卡片无出页（夹具）"
          },
          brief: "首页展示推荐商品，可从底栏进入商品列表。"
        }
      ]
    };
  </script>
  <script src="assets/md-icons.js"></script>
  <script src="assets/icons-extra.js"></script>
  <script src="assets/proto-shell.js"></script>
</body>
</html>
```

| 字段 | 规则 |
|------|------|
| `mode` | MP/H5/APP → `mobile`（手机框 + `fitPhoneFrame`）；PC/AD → `desktop`（iframe 铺满，无手机框） |
| `tabBarExempt` | 页内已有 TabBar/Tabs 承担 COMP 切态时 `true`，壳层隐藏状态演示 |
| `brief` | 当前页范围说明（人话，无 API 编号） |
| `comps[].states` | 与 `ui/COMP-*.md` 状态矩阵 **逐字一致** |
| `spec` 五项 | 顺序固定；接口首行 `API-* · 描述`，交互另起一行 |

## 单页类名（只许用这些，禁止自造皮肤类）

**桌面 D1-1**

```html
<div class="md-d1">
  <div class="md-page-head">
    <h1 class="md-h3">商品列表</h1>
    <span class="md-caption">共 6 条</span>
  </div>
  <nav class="md-tabs md-tabs--page">
    <button type="button" class="md-tab is-active" data-panel="panelAll">全部</button>
    <button type="button" class="md-tab" data-panel="panelOn">在售</button>
  </nav>
  <div class="md-d1__search">
    <label class="md-field md-field--sm">
      <span class="md-field__label">商品名称</span>
      <input class="md-field__input" type="text" placeholder="请输入商品名称">
    </label>
    <label class="md-field md-field--sm md-field--select">
      <span class="md-field__label">库存状态</span>
      <select class="md-select">
        <option>全部</option>
        <option>有货</option>
        <option>缺货</option>
      </select>
    </label>
    <label class="md-field md-field--sm md-field--date">
      <span class="md-field__label">上架日期</span>
      <input class="md-field__input" type="text" placeholder="年-月-日" autocomplete="off">
    </label>
    <div class="md-btn-group">
      <button type="button" class="md-btn md-btn--contained">查询</button>
      <button type="button" class="md-btn md-btn--outlined">重置</button>
    </div>
  </div>
  <div class="md-d1__toolbar">
    <div class="md-btn-group">
      <button type="button" class="md-btn md-btn--contained">新增</button>
      <button type="button" class="md-btn md-btn--outlined">导出</button>
    </div>
    <div class="md-select-wrap">
      <button type="button" class="md-select-btn" data-menu="moreMenu">更多操作</button>
      <ul id="moreMenu" class="md-menu">
        <li><button type="button" class="md-menu__item">批量上架</button></li>
        <li><button type="button" class="md-menu__item">批量下架</button></li>
      </ul>
    </div>
  </div>
  <div id="panelAll" class="md-tab-panel is-active">
    <!-- 表格 -->
  </div>
  <div class="md-d1__footer">
    <label class="md-field md-field--sm md-field--select">
      <span class="md-field__label">每页条数</span>
      <select class="md-select"><option>10</option><option selected>20</option></select>
    </label>
    <nav class="md-pagination">…</nav>
  </div>
</div>
<div id="editBackdrop" class="md-backdrop"></div>
<div id="edit" class="md-dialog">
  <h2 class="md-dialog__title">编辑商品</h2>
  <div class="md-dialog__body">…</div>
  <div class="md-dialog__actions">
    <button type="button" class="md-btn md-btn--text" onclick="ProtoPage.closeDialog('edit')">取消</button>
    <button type="button" class="md-btn md-btn--contained">保存</button>
  </div>
</div>
```

上表为 **控件拼装示例**。具体筛选项、签、弹窗、工具栏按钮 **以该页 `pages_prd` / `ui/PAGE` 为准**，规格没有的不要画进业务页。

**移动页**

```html
<div class="md-mobile-page">
  <div class="md-status-bar" aria-hidden="true">
    <span>9:41</span>
    <span class="md-status-bar__signals"></span>
  </div>
  <header class="md-appbar md-appbar--mobile">
    <div class="md-appbar__title">首页</div>
  </header>
  <main class="md-mobile-body">
    <div class="md-section-head">
      <h1 class="md-section-head__title">推荐</h1>
    </div>
    <div class="md-grid-2">
      <article class="md-card" data-comp="COMP-001" data-state="default">
        <div class="md-card__media md-media-ph md-media-ph--1"></div>
        <div class="md-card__body">
          <h2 class="md-card__title">有机草莓 250g</h2>
          <p class="md-price">¥19.90</p>
        </div>
      </article>
    </div>
  </main>
  <nav class="md-tabbar">…</nav>
</div>
```

**COMP 切态**（iframe 内）

```html
<article class="md-card" data-comp="COMP-001" data-state="default">
  <div class="md-card__media md-media-ph md-media-ph--1"></div>
  …
</article>
<div class="md-skel-host is-hidden" data-skel-for="COMP-001">
  <div class="md-skeleton md-skeleton--media"></div>
  <div class="md-skeleton md-skeleton--title"></div>
  <div class="md-skeleton md-skeleton--text"></div>
</div>
<div class="md-empty md-empty--illus is-hidden" data-empty-for="COMP-001"
     data-empty-text="暂无数据" data-error-text="加载失败">
  <div class="md-empty__art" aria-hidden="true"></div>
  <p class="md-empty__title">暂无内容</p>
  <p class="md-empty__text">暂无数据</p>
</div>
```

壳层 `postMessage({ type:'comp-state', compId, state })` 由 `proto-page.js` 写到 `data-state`。`loading` 显示骨架（卡片内渐变 + `.md-skel-host`）；`empty`/`error` 隐藏卡片并显示 `.md-empty`。空态文案写在 `.md-empty__text`，禁止让脚本把插画 DOM 整段清掉。

**筛选栏 / 抽屉 / 上传**

```html
<div class="md-filter">
  <label class="md-field md-field--sm">…</label>
  <div class="md-filter__actions">
    <button type="button" class="md-btn md-btn--contained">查询</button>
  </div>
</div>

<div id="filterBackdrop" class="md-backdrop"></div>
<aside id="filterDrawer" class="md-drawer md-drawer--right">
  <h2 class="md-drawer__title">筛选</h2>
  <div class="md-drawer__body">…</div>
  <div class="md-drawer__actions">
    <button type="button" class="md-btn md-btn--text" onclick="ProtoPage.closeDrawer('filterDrawer')">取消</button>
  </div>
</aside>

<label class="md-upload">
  <input type="file">
  <span>点击或拖拽上传</span>
  <p class="md-upload__hint">支持图片 / 文件</p>
</label>
```

抽屉：`ProtoPage.openDrawer(id)` / `closeDrawer(id)`，遮罩 id 为 `{id}Backdrop`。

## AD 常用控件（规格里有则必须用）

弹窗、确认、Toast、页内签、按钮组、下拉、日期/时间 **禁止**再用浏览器原生丑控件或 `alert()`。

**页内分页签**

```html
<nav class="md-tabs md-tabs--page">
  <button type="button" class="md-tab is-active" data-panel="p1">全部</button>
  <button type="button" class="md-tab" data-panel="p2">已下架</button>
</nav>
<div id="p1" class="md-tab-panel is-active">…</div>
<div id="p2" class="md-tab-panel">…</div>
```

**按钮组 / 分裂按钮**

```html
<div class="md-btn-group">
  <button type="button" class="md-btn md-btn--contained">查询</button>
  <button type="button" class="md-btn md-btn--outlined">重置</button>
</div>
<div class="md-btn-group md-btn-group--split">
  <button type="button" class="md-btn md-btn--contained">保存</button>
  <button type="button" class="md-btn md-btn--contained" data-menu="saveMenu">▾</button>
</div>
```

**下拉（原生 select 或菜单）**

```html
<label class="md-field md-field--sm md-field--select">
  <span class="md-field__label">状态</span>
  <select class="md-select">
    <option>全部</option>
    <option>启用</option>
  </select>
</label>
<div class="md-select-wrap">
  <button type="button" class="md-select-btn" data-menu="opMenu">更多操作</button>
  <ul id="opMenu" class="md-menu">
    <li><button type="button" class="md-menu__item">导出</button></li>
    <li class="md-menu__sep"></li>
    <li><button type="button" class="md-menu__item">删除</button></li>
  </ul>
</div>
```

**日期 / 时间**

```html
<label class="md-field md-field--sm md-field--date">
  <span class="md-field__label">开始日期</span>
  <input class="md-field__input" type="text" placeholder="年-月-日" autocomplete="off">
</label>
<label class="md-field md-field--sm md-field--time">
  <span class="md-field__label">时间</span>
  <input class="md-field__input" type="time">
</label>
<label class="md-field md-field--sm md-field--date">
  <span class="md-field__label">截止日期</span>
  <input class="md-field__input" type="text" placeholder="年-月-日" autocomplete="off">
</label>
```

日期框用 `md-field--date` + 文本输入（聚焦弹出套件月历）。时间用 `md-field--time` + `type="time"`。禁止再写 `datetime-local` 裸控件。

**开关 / 单选 / 多选**

```html
<label class="md-switch-row">
  <span class="md-switch">
    <input type="checkbox">
    <span class="md-switch__track"></span>
    <span class="md-switch__thumb"></span>
  </span>
  <span>上架</span>
</label>
<div class="md-choice-group">
  <span class="md-choice-group__label">配送方式</span>
  <label class="md-radio"><input type="radio" name="ship" checked> 包邮</label>
  <label class="md-radio"><input type="radio" name="ship"> 到店自提</label>
</div>
<div class="md-choice-group">
  <span class="md-choice-group__label">适用渠道</span>
  <label class="md-check"><input type="checkbox" checked> 小程序</label>
  <label class="md-check"><input type="checkbox"> 后台展示</label>
</div>
```

表单弹窗、整页表单、筛选栏规格出现开关/单选/多选时必须用上表，禁止裸 `input` 或自造 toggle。

**弹窗 / 确认 / Toast / 气泡**

```html
<button type="button" class="md-btn md-btn--contained" onclick="ProtoPage.openDialog('edit')">打开</button>
<div id="editBackdrop" class="md-backdrop"></div>
<div id="edit" class="md-dialog">
  <h2 class="md-dialog__title">标题</h2>
  <div class="md-dialog__body">
    <div class="md-dialog__form">
      <label class="md-field md-field--sm">
        <span class="md-field__label">名称</span>
        <input class="md-field__input" type="text">
      </label>
      <label class="md-field md-field--sm">
        <span class="md-field__label">售价</span>
        <input class="md-field__input" type="text">
      </label>
    </div>
  </div>
  <div class="md-dialog__actions">
    <button type="button" class="md-btn md-btn--text" onclick="ProtoPage.closeDialog('edit')">取消</button>
    <button type="button" class="md-btn md-btn--contained">确定</button>
  </div>
</div>
```

```js
ProtoPage.snackbar("已保存");
ProtoPage.snackbar("失败", { severity: "error" });
ProtoPage.confirm({ title: "删除确认", body: "删除后不可恢复", onOk: function () {} });
```

```html
<button type="button" class="md-btn md-btn--text md-tooltip" data-tip="刷新列表">刷新</button>
```

## 无类名组合（禁止裸 HTML）

套件没有「一模一样」的控件时，**必须**用下表组合，禁止自造 class、禁止无 `md-*` 的 `<button>` / `<input>` / `<table>`、禁止用随机色块当图。

| 规格里出现 | 必须用 | 禁止 |
|------------|--------|------|
| 筛选 / 搜索栏 | `md-filter` 或 `md-d1__search` | 无 class 的 `<form>` |
| 侧滑 / 抽屉 | `md-drawer` + `md-backdrop` | 自造 `position:fixed` 面板 |
| 上传 | `md-upload` | 裸 `<input type="file">` |
| 空态 | `md-empty md-empty--illus` | 一行灰字 / 空白 |
| 加载 | `md-skeleton` / `data-state="loading"` + `md-skel-host` | 纯文字「加载中」 |
| 封面 / 图片位 | `md-card__media md-media-ph md-media-ph--1`～`--6` 轮换 | `style="background:#xxx"` 色块；无编号灰块 |
| D1-2 表单 | `md-d1` + `md-d1__form` + `md-field--sm` | 无纸面的裸 label 堆叠；弹窗内 56px 大输入框 |
| 步骤条 | `md-stepper` + `md-step` | 纯数字列表 |
| 树 | `md-tree` | 无类名嵌套 `ul` |
| 图表 | `md-chart-ph` 占位条 | 手写 canvas / 自造柱 |
| 页内分页签 | `md-tabs md-tabs--page` + `md-tab` + `md-tab-panel` | 自造下划线 `div` / 裸 `<a>` 签 |
| 按钮组 / 工具栏按钮 | `md-btn-group` / `md-d1__toolbar` | 无 class 的一排 `<button>` |
| 下拉 | `md-field--select` + `md-select`，或 `md-select-btn` + `md-menu` | 未包 `md-field` 的裸 `<select>` |
| 日期 / 时间 | `md-field--date` / `md-field--time` + `type="date|time|datetime-local"` | 自造日历、纯文本日期 |
| 开关 | `md-switch-row` + `md-switch` | 自造滑块 / 裸 checkbox 当开关 |
| 单选 | `md-choice-group` + `md-radio` | 未包 `md-radio` 的裸 `<input type="radio">` |
| 多选 | `md-choice-group` + `md-check` | 未包 `md-check` 的裸 `<input type="checkbox">` |
| 弹窗 / 确认 | `md-dialog` + `md-backdrop`；确认用 `ProtoPage.confirm` | `alert()` / `confirm()` |
| Toast / 提示 | `ProtoPage.snackbar` / `md-alert` / `md-tooltip` | 页内红字当提示 |

D5 弹窗用 `md-dialog` + `md-backdrop`，打开后有遮罩淡入和面板缩放；禁止 `alert('原型：…')`。

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/字按钮 | `md-btn md-btn--contained` / `--outlined` / `--text`；`--sm` `--lg` |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input` |
| 卡片 | `md-card` `md-card--row` `md-card__media` `md-media-ph md-media-ph--n` `md-card__body` `md-card__title` `md-price` |
| 分区头 | `md-section-head` `md-section-head__title` |
| 系统栏 | `md-status-bar`（移动端必有） |
| 桌面页头 | `md-page-head`；表内缩略图 `md-row-goods` `md-thumb` |
| 纸面/表格 | `md-paper` `md-table` `md-pagination` `md-page-btn` |
| 筛选栏 | `md-filter` / `md-d1__search`；动作区 `md-filter__actions` |
| 抽屉 | `md-drawer` `md-drawer--left/right`；`ProtoPage.openDrawer` |
| 上传 | `md-upload` |
| 空态 | `md-empty md-empty--illus` + `__art` `__title` `__text` |
| 骨架 | `md-skeleton` `--text/--title/--media/--row`；`md-skel-host` |
| 步骤/树/图 | `md-stepper` `md-tree` `md-chart-ph` |
| Chip/Alert | `md-chip` `md-alert md-alert--error/--info/--success/--warning` |
| 状态组 | `md-toggle md-toggle--vert`（状态演示已内置） |
| 按钮组 | `md-btn-group` `md-btn-group--split` `md-d1__toolbar` |
| 下拉 | `md-field--select` `md-select` `md-select-btn` `md-menu` `md-menu__item` |
| 日期时间 | `md-field--date` `md-field--time` `md-cal` |
| 开关/单选/多选 | `md-switch` `md-switch-row` `md-radio` `md-check` `md-choice-group` |
| 页内签 | `md-tabs md-tabs--page` `md-tab` `md-tab-panel` |
| 弹窗/确认 | `md-dialog` `md-dialog--sm/--lg`；`ProtoPage.openDialog` / `confirm` |
| 提示 | `md-snackbar` `--success/--error`；`md-tooltip` `data-tip` |
