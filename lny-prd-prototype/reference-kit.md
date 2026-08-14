# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角 4px、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。

**原型默认高保真**：与 `ui/PAGE`「视觉细节」估点档位无关。⑥ 必须按本节「高保真落地」出图，禁止线框式两张灰卡、禁止「示例商品 A」。

`pages_prd` ASCII **只定分区上下顺序**，不是视觉稿。写页前必须 Read [`gold/README.md`](gold/README.md) 与对应金样，复制骨架再换文案。禁止把 `┌─┐` 画成带边框空盒子。

## 高保真落地（必守）

写每一页 HTML 时按此表。未达则不得交付。

| 项 | 要求 |
|----|------|
| 金样 | 按页类型 Read `gold/`：`mobile-grid` / `mobile-list` / `mobile-detail` / `mobile-form` / `mobile-settings` / `mobile-wizard` / `mobile-timeline` / `mobile-buttons` / `mobile-tree` / `desktop-list` / `desktop-form` / `desktop-dashboard` / `desktop-split` / `desktop-settings` / `desktop-wizard` / `desktop-timeline`。复制骨架含 script。密度不得低于金样。禁止用 `desktop-list` 硬套工作台；禁止用 `mobile-list` 硬套触屏树 |
| 估点档 | 忽略「视觉细节=粗糙」；⑥ 不降档；须满足 `reference-mobile-design.md` 审美必做 |
| 舒适默认 | §2.3 漏写也要落地：隐藏 `md-skel-host`、插画 `md-empty`、失败可重试、按下态、浮层过渡、D1-1 `md-d1--list`+`md-col-*`。禁止发明新跳转/字段/弹窗；**有字段时必须按层级排版** |
| 夹具数据 | 用符合业务域的中文名称与真实量级价格（如 `有机草莓 250g` / `¥19.90`）。**禁止** `示例商品 A/B`、`测试数据`、`xxx`、`Item 1` |
| 条数 | 列表/卡片/表格默认态 **≥4 条**（规格写明空态、或 API 写死更少条数时从其规定；首页有「每页条数」则按其值） |
| 字段 | API/COMP 已列的展示字段都要出现（名称、图、价、库存状态等）；**不**发明规格没有的字段（如无「销量」就不要写已售） |
| 图片 | `md-card__media md-media-ph md-media-ph--{1-6}` 轮换；禁止无编号的纯灰 `md-media-ph`、禁止随机色块。点图由 `proto-page.js` 注入 `.md-lightbox` 放大阅览（同页一组、翻页不循环；封面/头像/空态/图表除外） |
| 移动端 | 状态栏由 `proto-page.js` 固定顶注入；页根须标 `md-immersive` 或 `md-standard`；`md-section-head`；列表卡三形态择一：`md-card--cover` / `md-card--tile`（`md-grid-2`）/ `md-card--row` 或 `--plain`；触屏 `md-search` 仅左图标+输入；`viewport-fit=cover`；左右下及四角走 `--md-safe-*` |
| 桌面端 | 必须有 `md-breadcrumb`（内容区顶部，**不要** `md-page-head` 大标题）；表格首列可用 `md-row-goods` + `md-thumb md-media-ph--n`。D1-1 列表：页内签在筛选上方且整区切换；`md-d1--list` 让分页与表横条贴底，并走 **紧凑密度**；勾选列 `md-col-check` 左冻、操作列 `md-col-actions` 右冻定宽；中间列按语义加 `md-col-name` / `md-col-price` / `md-col-status` / `md-col-date`（名称吃剩余，金额/状态/日期窄，禁止均分或被 `min-width` 拉长）；操作过多用 `md-actions` + `data-menu`「更多」下拉；`md-d1__stats` 靠左、`md-d1__pager` 靠右。规格出现的弹窗/签/下拉/日期/按钮组必须用本节 AD 控件，禁止裸 `alert` / 无样式 `<select>` |
| 间距 | 触屏滚动区模块间距走 `--md-module-gap`（`md-module`）；卡片/栅格内距走套件；禁止内联 `margin` 当排版 |

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`proto-map.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。镜像 `versions/{v}/prototypes/{终端}/` 时 **须连同 `assets/`**（含 extras 与 `icons/`）。禁止改 kit 源文件来迁就某一页。

## 引用（硬性）

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | `assets/mui-kit.css` + `assets/md-icons.js` + `assets/icons-extra.js` + `assets/proto-page.js` |
| `index.html` 汇总壳 | 上表 + `assets/proto-shell.css` + `assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |
| `map.html` | `assets/mui-kit.css` + `assets/proto-shell.css` + `assets/proto-map.js`；只填 `ProtoMap.boot({ project, terminal, pages, links })`，禁止手写拖拽/缩放/导出 |

禁止：页内 `<style>` 改 `--md-primary` / 另写一套按钮色；内联 `style` 仅允许布局占位（宽高/显示），不得当主题。

## `index.html`（数据驱动壳）

只填 `PROTO_SHELL`，**不要**手写侧栏/顶栏/状态演示/规格说明 DOM。右下角 SKILL 标注由 `proto-shell.js` 注入，不要写进本页 HTML。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>MP 原型</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
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
<div class="md-d1 md-d1--list">
  <div class="md-breadcrumb">
    <span>商品</span>
    <span>/</span>
    <span class="is-current">商品列表</span>
  </div>
  <nav class="md-tabs md-tabs--page">
    <button type="button" class="md-tab is-active" data-panel="panelAll">全部</button>
    <button type="button" class="md-tab" data-panel="panelOn">有货</button>
  </nav>
  <div class="md-tab-panels md-d1__workspace">
    <div id="panelAll" class="md-tab-panel is-active">
      <div class="md-d1__search">
        <label class="md-field md-field--sm">
          <span class="md-field__label">商品名称</span>
          <input class="md-field__input" type="text" placeholder="请输入商品名称">
        </label>
        <div class="md-filter__actions md-btn-group">
          <button type="button" class="md-btn md-btn--contained">查询</button>
          <button type="button" class="md-btn md-btn--outlined">重置</button>
        </div>
      </div>
      <div class="md-d1__toolbar">
        <div class="md-btn-group">
          <button type="button" class="md-btn md-btn--contained">新增</button>
        </div>
      </div>
      <div class="md-d1__list">
        <div class="md-table-wrap">
          <table class="md-table">
            <thead>
              <tr>
                <th class="md-col-check"><label class="md-check"><input type="checkbox"></label></th>
                <th class="md-col-name">商品名称</th>
                <th class="md-col-price">售价</th>
                <th class="md-col-actions">操作</th>
              </tr>
            </thead>
            <tbody>…</tbody>
          </table>
        </div>
        <div class="md-d1__footer">
          <span class="md-d1__stats md-caption">共 6 条</span>
          <div class="md-d1__pager">
            <nav class="md-pagination">…</nav>
          </div>
        </div>
      </div>
    </div>
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
<div class="md-mobile-page md-mp md-immersive">
  <div class="md-hero">
    <div class="md-swiper">…Banner 下沉…</div>
  </div>
  <main class="md-mobile-body">
    <div class="md-mobile-sheet">
      <section class="md-module">
        <nav class="md-king">…5 列金刚区…</nav>
      </section>
      <section class="md-module">
        <nav class="md-king md-king--pair">…一排两张大卡…</nav>
      </section>
      <section class="md-module">
        <div class="md-section-head">
          <h1 class="md-section-head__title">推荐</h1>
          <a class="md-btn md-btn--link" href="…">查看全部</a>
        </div>
        <div class="md-grid-2">
          <article class="md-card md-card--tile" data-comp="COMP-001" data-state="default">
            <div class="md-card__media md-media-ph md-media-ph--1"></div>
            <div class="md-card__body">
              <h2 class="md-card__title">标题最多两行</h2>
              <p class="md-price">¥19.90</p>
              <p class="md-card__time">今天上架</p>
            </div>
          </article>
        </div>
      </section>
    </div>
  </main>
  <nav class="md-tabbar">…</nav>
</div>
```

有 TabBar 时 **不要**再写 `md-appbar`。**沉浸式下沉**：`md-immersive` + `md-hero` 时，Hero **绝对定位钉在页顶底层、不随滚**；`md-mobile-body` 内必须包一层 **`md-mobile-sheet`（白底、宽 100%、无外边距、可有内边距）**，滚动时白底从上层盖住 Banner；顶距由 `::before` 占位露图并可点穿轮播。详情 `md-appbar--overlay` 仍叠最上层。**触屏滚动区按模块切分**：每个 L3 分区包 `md-module`；`md-mobile-body` / `md-mobile-sheet` 用 `--md-module-gap`（16px）统一模块间距；分区头放在模块内，禁止用内联 margin 拉开模块。**列表卡三形态择一**（见下节）。详情/内容页主图用 `md-swiper md-swiper--wide`（**16:9**），介绍配图用 `md-media--16x9`。评论附图用 `md-comment__photos` / `md-card__photos`（**1:1**、圆角、横向排布超出换行）。触屏正文左右下走 `--md-safe-*`；标准顶栏同样走安全距，MP 另避让胶囊。触屏 `md-search` 仅左图标+输入（无「搜索」文案、无右侧搜索按钮）。左/底/右半屏：`md-drawer--left/bottom/right`。移动页 `<meta viewport>` 须带 `viewport-fit=cover`。**禁止**在页内手写 `md-status-bar`：由 `proto-page.js` 注入固定顶演示层。页根必须标 **`md-immersive`**（状态栏背景透明）或 **`md-standard`**（状态栏背景不透明）。可点文案与 Tab 走套件安全距（左右下及四角）。

### 触屏列表卡片三形态

同一列表（或同一模块）只选一种。规格有字段才写对应节点，**禁止**为好看编造业务字段。

**① 封面叠字** `md-card--cover`：一行一列大图，单行标题悬图片底部。默认高度随 **16:9**；`--ratio-2x1` / `--ratio-1x1` 换比例；`--h-sm/md/lg` 固定高度。

```html
<a class="md-card md-card--cover" href="…">
  <div class="md-card__media md-media-ph md-media-ph--1">
    <span class="md-card__tag md-chip md-chip--success">有货</span>
    <h2 class="md-card__title">单行标题截断</h2>
  </div>
</a>
<!-- 固定高度：md-card--cover md-card--h-md -->
```

**② 双列瓷砖** `md-card--tile` + `md-grid-2`：上图 **1:1**，标题最多两行，可选 `__chips` 小标签/图标、`md-price`、`__time` 小字。

```html
<article class="md-card md-card--tile">
  <div class="md-card__media md-media-ph md-media-ph--1">
    <span class="md-card__tag md-chip md-chip--primary">新品</span>
  </div>
  <div class="md-card__body">
    <h2 class="md-card__title">标题最多两行</h2>
    <div class="md-card__chips"><span class="md-chip md-chip--outlined">小标签</span></div>
    <p class="md-price">¥19.90</p>
    <p class="md-card__time"><span class="md-icon" data-icon="schedule"></span>今天上架</p>
  </div>
</article>
```

**③ 横卡 / 纯文** `md-card--row` 或 `--plain`：左图右文、左图标/头像右文、或无图纯文（评论可带 `__photos` 小图一排）。

```html
<a class="md-card md-card--row" href="…">
  <div class="md-card__media md-media-ph md-media-ph--1">
    <span class="md-card__tag md-chip md-chip--success">有货</span>
  </div>
  <!-- 无封面：<span class="md-card__leading"><span class="md-icon" data-icon="goods"></span></span> -->
  <!-- 头像：<span class="md-card__leading md-card__leading--avatar md-media-ph md-media-ph--n"></span> -->
  <div class="md-card__body">
    <div class="md-card__main">
      <h2 class="md-card__title">标题最多两行截断</h2>
      <p class="md-card__subtitle">副标题一行</p>
      <p class="md-card__text">摘要最多两行</p>
    </div>
    <div class="md-card__foot">
      <div class="md-card__meta">
        <span class="md-card__meta-item"><span class="md-icon" data-icon="schedule"></span>昨天</span>
      </div>
      <p class="md-price">¥19.90</p>
    </div>
  </div>
</a>
```

```html
<article class="md-card md-card--plain">
  <div class="md-card__body">
    <div class="md-card__main">
      <h2 class="md-card__title">用户名</h2>
      <p class="md-card__text">评论文案</p>
    </div>
    <div class="md-card__photos">
      <div class="md-card__photo md-media-ph md-media-ph--1"></div>
    </div>
    <div class="md-card__foot">
      <div class="md-card__meta">
        <span class="md-card__meta-item">2026-08-10</span>
      </div>
    </div>
  </div>
</article>
```

| 节点 | 规则 |
|------|------|
| `__title` | ①单行悬底；②③最多两行截断 |
| `__subtitle` | ③次级一行 |
| `__text` | ③摘要；横卡默认两行截断 |
| `__chips` | ②正文小标签/小图标，不是封面角标 |
| `__time` | ②底部小字时间/浏览 |
| `__meta` / `__meta-item` | ③时间、浏览、点赞等小字；可带 14px 图标或 `__thumb` |
| `__foot` | ③底栏：左 meta、右价格 |
| `__leading` | ③左侧小图标；`--avatar` 为圆头像 |
| `__tag` | 状态标签贴**封面**左上或右上（`--tr`） |
| `__photos` / `__photo` | ③纯文/评论小图，1:1，一排最多五张 |

触屏顶栏四种（规格点名一种，禁止混用、禁止把封面顶栏拉成 16:9）：

| 形态 | 用法 | 金样 |
|------|------|------|
| 16:9 大背景 + slogan | `md-immersive` + `md-hero` + `md-swiper`；有 TabBar 则无页内顶栏 | `gold/mobile-grid.html` |
| 16:9 大背景 + 左上返回和标题 | `md-immersive` + `md-appbar--overlay` + `md-swiper--wide` | `gold/mobile-detail.html` |
| 标准高度标题栏 + 靠左返回和标题 | `md-standard` + `md-appbar md-appbar--mobile` | `gold/mobile-form.html` |
| 两倍标准高度封面 + 标题 | `md-immersive` + `md-appbar--cover` + `__cover` 背景图；高度约 `2 ×` 标准标题栏 | `gold/mobile-settings.html` |

```html
<header class="md-appbar md-appbar--mobile md-appbar--cover">
  <div class="md-appbar__cover md-media-ph md-media-ph--2" aria-hidden="true"></div>
  <a class="md-icon-btn" href="#" aria-label="返回"><span class="md-icon" data-icon="back"></span></a>
  <h1 class="md-appbar__title">设置</h1>
</header>
```

金刚区默认 4/5 列（图标文字上下居中）。一排两张大卡用 `md-king--pair`，小图标与文案均靠左：

```html
<nav class="md-king md-king--pair">
  <button type="button" class="md-king__item">
    <span class="md-king__icon"><span class="md-icon" data-icon="goods" aria-hidden="true"></span></span>
    <span class="md-king__name">时令鲜果</span>
    <span class="md-king__desc">当季直达</span>
  </button>
</nav>
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

**页内分页签**（放在搜索栏上方；`data-panel` 对应的面板里装筛选+功能+列表+分页整区）

```html
<nav class="md-tabs md-tabs--page">
  <button type="button" class="md-tab is-active" data-panel="p1">全部</button>
  <button type="button" class="md-tab" data-panel="p2">已下架</button>
</nav>
<div class="md-tab-panels md-d1__workspace">
  <div id="p1" class="md-tab-panel is-active">…筛选/功能/列表/分页…</div>
  <div id="p2" class="md-tab-panel">…</div>
</div>
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

桌面用原生 `md-select` 或 `md-select-btn` + `md-menu`。**触屏**同样写 `md-field--select` + `md-select`：选项 **≤6** 中间弹窗，**≥7** 底半屏，列表均可上下滚动。禁止系统原生选择器。可用 `data-sheet="center|bottom"` 强制形态，`data-native="1"` 退回原生。

**日期 / 时间**

```html
<label class="md-field md-field--sm md-field--date">
  <span class="md-field__label">上架日期</span>
  <input class="md-field__input" type="text" placeholder="年-月-日" autocomplete="off">
</label>
<label class="md-field md-field--sm md-field--daterange">
  <span class="md-field__label">上架日期</span>
  <input class="md-field__input" type="text" placeholder="开始日期 ~ 结束日期" autocomplete="off" readonly>
</label>
<label class="md-field md-field--sm md-field--time">
  <span class="md-field__label">时间</span>
  <input class="md-field__input" type="time">
</label>
```

单日用 `md-field--date`（聚焦弹出月历）。日期段用 `md-field--daterange`：先点开始日、再点结束日，输入框显示 `YYYY-MM-DD ~ YYYY-MM-DD`，起止写在 `data-start` / `data-end`。时间用 `md-field--time` + `type="time"`。禁止再写 `datetime-local` 裸控件。

**只读输入**（灰底、淡字；日期段触发器的 `readonly` 不要套本类）

```html
<label class="md-field md-field--readonly">
  <span class="md-field__label">只读</span>
  <input class="md-field__input" type="text" value="不可编辑" readonly>
</label>
```

触屏单日与省市区（只有年-月-日 / 省-市-区三级滚轮，**禁止**加开始/结束日期签）：

```html
<label class="md-field">
  <span class="md-field__label">期望到货日期</span>
  <button type="button" class="md-field__input md-picker-trigger" data-wheel="date">请选择日期</button>
</label>
<label class="md-field">
  <span class="md-field__label">收货地区</span>
  <button type="button" class="md-field__input md-picker-trigger" data-wheel="region">请选择省市区</button>
</label>
```

触屏日期段（列表筛选等才用，带开始/结束两个签）：

```html
<label class="md-field">
  <span class="md-field__label">上架日期</span>
  <button type="button" class="md-field__input md-picker-trigger" data-wheel="daterange">请选择日期段</button>
</label>
```

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

触屏页：`.md-choice-group` 自动变成标签（选中右上对号角标），且每个输入组独立成行。列表行内的 `md-radio` / `md-check`（或 `.md-choice-group--list`）仍用左侧圆圈/方块。桌面不变。

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
ProtoPage.setProgress("#wizBar", 40);          // 无极进度条，右侧显示 40%
ProtoPage.setAdvance("#wizProg", 40, "1 / 3");   // 分段进步条，自定义右侧文案
```

触屏页 `ProtoPage.snackbar` 为居中 Toast（半透明黑底圆角、白图标+白字）。桌面仍为底部条。

```html
<button type="button" class="md-btn md-btn--text md-tooltip" data-tip="刷新列表">刷新</button>
```

触屏按钮对照金样 `gold/mobile-buttons.html`：小 `--sm` / 中默认 / 大 `--lg`；形态含线框 `--outlined`、色块 `--contained`、文字 `--text`、**纯文字链接 `--link`（无线框无背景，用于查看更多/了解全部）**、置灰 `disabled`、角标内嵌 `md-badge`。

```html
<button type="button" class="md-btn md-btn--outlined md-btn--sm">线框</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">色块</button>
<button type="button" class="md-btn md-btn--outlined md-btn--sm" disabled>线框置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm" disabled>色块置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">角标<span class="md-badge">8</span></button>
```

```html
<div class="md-advance" data-segments="3" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="33">
  <div class="md-advance__head">
    <span class="md-advance__label">完成进度</span>
    <span class="md-advance__value">1 / 3</span>
  </div>
  <div class="md-advance__track">
    <div class="md-advance__seg"><div class="md-advance__bar"></div></div>
    <div class="md-advance__seg"><div class="md-advance__bar"></div></div>
    <div class="md-advance__seg"><div class="md-advance__bar"></div></div>
  </div>
</div>
```

**进步条** `md-advance`：分段分布，步骤/向导用。`data-segments` 默认 4（2–12）。`ProtoPage.setAdvance` 按百分比填已完成段、当前段余量、其余留空。缺 `__seg` 时脚本按 `data-segments` 补齐。触屏可用 `md-advance--lg`。

```html
<div class="md-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="40">
  <div class="md-progress__head">
    <span class="md-progress__label">上传进度</span>
    <span class="md-progress__value">40%</span>
  </div>
  <div class="md-progress__track">
    <div class="md-progress__bar" style="width:40%"></div>
  </div>
</div>
```

**进度条** `md-progress`：无极连续轨道，上传/完整度用。`ProtoPage.setProgress` 把单根 `__bar` 拉到对应宽度。不确定进度用 `md-progress--indeterminate`（或旧类 `md-linear`）。触屏可用 `md-progress--lg`。

```html
<ol class="md-timeline">
  <li class="md-timeline__item is-done">
    <div class="md-timeline__rail" aria-hidden="true">
      <span class="md-timeline__node"></span>
      <span class="md-timeline__line"></span>
    </div>
    <article class="md-timeline__body md-card md-card--row">
      <div class="md-card__media md-media-ph md-media-ph--1"></div>
      <div class="md-card__body">
        <div class="md-card__main">
          <h2 class="md-card__title">已提交</h2>
          <p class="md-card__text">右侧图文说明。</p>
        </div>
      </div>
    </article>
  </li>
</ol>
```

**时间轴** `md-timeline`：左侧竖状 `__rail`（节点 `__node` + 连线 `__line`），右侧 `__body` 用 `md-card--row` 图文。`is-done` 已完成、`is-active` 当前。点节点由 `proto-page.js` 切高亮。金样 `gold/mobile-timeline.html` / `gold/desktop-timeline.html`。

## 无类名组合（禁止裸 HTML）

套件没有「一模一样」的控件时，**必须**用下表组合，禁止自造 class、禁止无 `md-*` 的 `<button>` / `<input>` / `<table>`、禁止用随机色块当图。

| 规格里出现 | 必须用 | 禁止 |
|------------|--------|------|
| 筛选 / 搜索栏 | `md-filter` 或 `md-d1__search` | 无 class 的 `<form>` |
| 侧滑 / 抽屉 | `md-drawer md-drawer--left/right/bottom` + `md-backdrop` | 自造 `position:fixed` 面板；`display` 瞬切 |
| 轮播 Banner | `md-swiper` + `__track` + `__slide` + `__dots` | 自造横向滚动无指示点 |
| 金刚区 | `md-king` + `md-king__item`（4/5 列：图标+文字上下居中同底）；或 `md-king--pair`（一排两张大卡，小图标与 `__name`/`__desc` 均靠左） | 图标单独色块、文字露在底外；无热区的纯文字宫格；双卡内容居中 |
| 方形图标按钮 | `md-btn--stack` 或金刚项同款：图标上、文字下、共一块底 | 图标独立成钮、文字在旁或底外 |
| 贴底主操作 | `md-action-bar` 或 `md-tabbar` | 主按钮写在滚动内容末尾 |
| 上传 | `md-upload`；单图 `md-upload--single`；多图 `md-upload-grid`；文件 `md-upload--file` | 裸 `<input type="file">` |
| 触屏滑动条 | `md-slider`（`--steps` 五步 / `--fluid` 无极） | 无刻度无当前值的裸 range |
| 触屏日期/省市区 | `data-wheel="date|region"` 底半屏三级联动，无开始/结束签 | 原生 `type=date`；三个独立下拉；给省市区加日期段签 |
| 触屏日期段 | `data-wheel="daterange"` 底半屏，开始/结束两个签 | 两个独立日期框硬凑；原生 `type=date` |
| 空态 | `md-empty md-empty--illus` | 一行灰字 / 空白 |
| 加载 | `md-skeleton` / `data-state="loading"` + `md-skel-host` | 纯文字「加载中」 |
| 封面 / 图片位 | `md-card__media md-media-ph md-media-ph--1`～`--6` 轮换；点图 `.md-lightbox` 同页一组翻页不循环 | `style="background:#xxx"` 色块；无编号灰块 |
| D1-2 表单 | `md-d1` + `md-d1__form` + `md-field--sm` | 无纸面的裸 label 堆叠；弹窗内 56px 大输入框 |
| 步骤条 | `md-stepper` + `md-step`；已完成 `is-done`；当前 `is-active` | 纯数字列表 |
| 进步条 | `md-advance` + `__head` + `__track` + `__seg` + `__bar`；`data-segments`；触屏可 `--lg` | 用无极 `md-progress` 冒充分步 |
| 进度条 | `md-progress` + `__head` + `__track` + `__bar`；不确定 `--indeterminate`；触屏可 `--lg` | 裸 `<progress>` / 自造色条 / 用分段 `md-advance` 冒充上传 |
| 时间轴 | `md-timeline` + `__item` `__rail` `__node` `__line` `__body`；右图文 `md-card--row`；`is-done` / `is-active` | 用列表硬套竖轨；左图右线反过来 |
| 树 | `md-tree` + `__item` `__toggle` `__label`；分支 `li.is-open`；当前 `is-active` | 无类名嵌套 `ul`；触屏用列表硬套分类树 |
| 图表 | `md-chart-ph` 占位条 | 手写 canvas / 自造柱 |
| 页内分页签 | `md-tabs md-tabs--page` + `md-tab` + `md-tab-panel` | 自造下划线 `div` / 裸 `<a>` 签 |
| 按钮组 / 工具栏按钮 | `md-btn-group` / `md-d1__toolbar` | 无 class 的一排 `<button>` |
| 下拉 | `md-field--select` + `md-select`，或 `md-select-btn` + `md-menu` | 未包 `md-field` 的裸 `<select>`；触屏用系统原生选择器 |
| 日期 / 时间 | `md-field--date` / `md-field--daterange` / `md-field--time` + `type="date|time|datetime-local"` | 自造日历、两个裸日期框冒充日期段 |
| 开关 | `md-switch-row` + `md-switch` | 自造滑块 / 裸 checkbox 当开关 |
| 单选 | 桌面/列表：`md-choice-group` + `md-radio`；触屏表单：同上（自动标签角标） | 未包 `md-radio` 的裸 `<input type="radio">` |
| 多选 | 桌面/列表：`md-choice-group` + `md-check`；触屏表单：同上（自动标签角标）；列表行勿包成标签 | 未包 `md-check` 的裸 `<input type="checkbox">` |
| 弹窗 / 确认 | `md-dialog` + `md-backdrop`；确认用 `ProtoPage.confirm` | `alert()` / `confirm()` |
| Toast / 提示 | `ProtoPage.snackbar` / `md-alert` / `md-tooltip` | 页内红字当提示 |

D5 弹窗用 `md-dialog` + `md-backdrop`，打开后有遮罩淡入和面板缩放；禁止 `alert('原型：…')`。

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / `--text` / **`--link`（纯文字无线框无背景，查看更多/了解全部）**；`--sm` `--lg`；置灰 `disabled`；角标内嵌 `md-badge` |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input`；只读加 `md-field--readonly` + `readonly`（灰底淡字）。日期段 `readonly` 触发器不要加 `--readonly` |
| 卡片 | `md-card` **`--cover`（大图叠字）`--tile`（双列 1:1）`--row`（左图右文）`--plain`（纯文/评论）** `md-card__media` `md-card__leading` `--avatar` `md-card__body` `md-card__main` `md-card__title` `md-card__subtitle` `md-card__text` `md-card__chips` `md-card__time` `md-card__foot` `md-card__meta` `md-card__photos` `md-card__photo` `md-card__tag` `--tl/--tr` `md-price` |
| 详情 16:9 图 | `md-swiper--wide`；介绍配图 `md-media--16x9`；评论 `md-comment` `__user` `__time` `__text` `__photos` `__photo`（一排最多五张） |
| 分区 / 模块 | `md-module`（L3，模块间距 `--md-module-gap`）`md-section-head` `md-section-head__title` |
| 系统栏 | `md-status-bar`（`proto-page.js` 固定顶注入；页内禁止手写；时间/信号贴顶、电量信号贴右，不为胶囊留空） |
| 触屏顶栏 | ① `md-hero` 16:9+slogan ② `--overlay` 叠 16:9 ③ 标准 `md-appbar--mobile` ④ `--cover` 两倍高度封面 |
| 桌面面包屑 | `md-breadcrumb`（D1 内容区顶部，禁止再写 `md-page-head`） |
| 操作列 | `md-col-actions` 定宽；过多操作用 `md-actions` + `data-menu`「更多」+ `md-menu md-menu--fixed`（打开时抬高当前行，菜单留在单元格内，避免被后续表行挡住，也避免点菜单打不开弹窗） |
| 语义列宽 | `md-col-check` 勾选；`md-col-name` 名称吃剩余；`md-col-price` 金额窄右齐；`md-col-status` 状态/短枚举；`md-col-date` 日期；`md-col-id` 短码；`md-col-num` 数量。禁止所有列均分 |
| D1-1 紧凑 | 根节点 `md-d1 md-d1--list`（矮行、小内外距）；**不要**套到 D1-2 表单页 |
| 工作台 | `md-stat-grid` `md-stat-card`；趋势 `md-chart-ph` |
| 分栏 | `md-d1--split` / 触屏 `md-tree-page`；`md-split` `__side` `__main`；树 `md-tree` `__item` `__toggle` `__label` `is-open` `is-active` |
| 设置分组 | `md-set-group` `__title` `md-set-row`；一行一项开关 |
| 汇总分页 | `md-d1__footer`：`md-d1__stats` 靠左，`md-d1__pager` 靠右 |
| 纸面/表格 | `md-paper` `md-table` `md-table-wrap` `md-col-check` `md-col-name` `md-col-price` `md-col-status` `md-col-date` `md-col-actions` `md-pagination` `md-page-btn` |
| 筛选栏 | `md-filter` / `md-d1__search`；动作区 `md-filter__actions` |
| 抽屉 | `md-drawer` `--left/--right/--bottom`；`ProtoPage.openDrawer` |
| 轮播 / 金刚区 | `md-swiper` `md-king`（5 列图标文字上下同底）`md-king--pair`（双卡靠左小图标）`__name` `__desc`；沉浸式 `md-immersive` + `md-hero`；标准 `md-standard`；方形图标钮 `md-btn--stack` |
| 主操作条 | `md-action-bar`（无 TabBar 的提交/购买） |
| 上传 | `md-upload` `md-upload--single` `md-upload-grid` `md-upload--file` |
| 滑动条 | `md-slider` `--steps` `--fluid` |
| 底半屏三级 | `data-wheel="date"` / `data-wheel="region"` / `data-wheel="daterange"` |
| 空态 | `md-empty md-empty--illus` + `__art` `__title` `__text` |
| 骨架 | `md-skeleton` `--text/--title/--media/--row`；`md-skel-host` |
| 步骤/树/图 | `md-stepper` `md-step` `md-tree` `md-chart-ph` `md-stat-grid` `md-stat-card` |
| 时间轴 | `md-timeline` `__item` `__rail` `__node` `__line` `__body`；右图文 `md-card--row`；`is-done` / `is-active` |
| 进步条 | `md-advance` `__label` `__value` `__track` `__seg` `__bar`；`data-segments`；`--lg`；`ProtoPage.setAdvance` |
| 进度条 | `md-progress` `__label` `__value` `__track` `__bar`；`--lg`；`--indeterminate`；`ProtoPage.setProgress` |
| Chip/Alert | `md-chip` `md-badge` `md-alert md-alert--error/--info/--success/--warning` |
| 状态组 | `md-toggle md-toggle--vert`（状态演示已内置） |
| 按钮组 | `md-btn-group` `md-btn-group--split` `md-d1__toolbar` |
| 下拉 | `md-field--select` `md-select` `md-select-btn` `md-menu` `md-menu__item`；触屏 ≤6 中间弹窗 / ≥7 底半屏 `md-select-sheet` |
| 日期时间 | `md-field--date` `md-field--daterange` `md-field--time` `md-cal` |
| 开关/单选/多选 | `md-switch` `md-switch-row` `md-radio` `md-check` `md-choice-group`；触屏表单标签角标，列表 `--list` 或行内圆/方 |
| 页内签 | `md-tabs md-tabs--page` `md-tab` `md-tab-panel` `md-tab-panels` `md-d1__workspace` |
| 弹窗/确认 | `md-dialog` `md-dialog--sm/--lg`；`ProtoPage.openDialog` / `confirm` |
| 提示 | 触屏：居中 `md-snackbar--toast`（半透明黑底、白图标白字）；桌面：底部 `md-snackbar`；`md-tooltip` `data-tip` |
