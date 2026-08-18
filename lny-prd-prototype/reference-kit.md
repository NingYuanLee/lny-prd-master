# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角 4px、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。

**原型默认高保真**：与 `ui/PAGE`「视觉细节」估点档位无关。⑥ 必须按本节「高保真落地」出图，禁止线框式两张灰卡、禁止「示例商品 A」。

`pages_prd` ASCII **只定分区上下顺序**，不是视觉稿。写页前必须 Read [`gold/README.md`](gold/README.md) 与对应金样，**对标视觉下限**再换文案。禁止把 `┌─┐` 画成带边框空盒子，也禁止把金样演示功能（凡图即灯箱、全套表单样例）搬进规格没写的业务页。点图预览只默认给详情页与横卡多行。

## 高保真落地（必守）

写每一页 HTML 时按此表。未达则不得交付。

| 项 | 要求 |
|----|------|
| 金样 | 按页类型 Read `gold/`（表见该文）。**对标视觉下限**（密度/类名不得低于金样），不要整页照搬演示功能。禁止用 `desktop-lists` 硬套工作台；禁止用 `mobile-list` 硬套触屏树 |
| 估点档 | 忽略「视觉细节=粗糙」；⑥ 不降档；须满足 `reference-mobile-design.md` 审美必做 |
| 舒适默认 | §2.3 漏写也要落地：隐藏 `md-skel-host`、插画 `md-empty`、失败可重试、按下态、浮层过渡、D1-1 `md-d1--list`+`md-col-*`。禁止发明新跳转/字段/弹窗；**有字段时必须按层级排版** |
| 演示数据 | 用符合业务域的中文名称与真实量级价格（如 `有机草莓 250g` / `¥19.90`）。**禁止** `示例商品 A/B`、`测试数据`、`xxx`、`Item 1` |
| 条数 | 直接执行共享 `PT-DENSITY`，只对明确列表/宫格/时间轴/D1-1 生效；详情附属区和摘要短表不套门槛 |
| 字段 | API/COMP 已列的展示字段都要出现（名称、图、价、库存状态等）；**不**发明规格没有的字段（如无「销量」就不要写已售） |
| 图片 | `md-card__media` **只能**出现在 `--cover` / `--tile` / `--row` 卡内。横卡必须是 `md-card md-card--row`，左图套件**宽高双锁定**（触屏 96×96，竖图只加高不改宽；桌面 112 同理），**禁止**漏写 `--row` 或给左图写 `height:auto`/`width:100%`（会被拉高再撑宽挤掉正文）。页顶大背景用 `md-hero`/`md-appbar--cover`；详情主图 `md-swiper--wide`；介绍配图 `md-media--16x9`。占位图 `md-media-ph--{1-6}` 轮换；禁止无编号纯灰、禁止随机色块。点图预览默认给：详情页图（页根 `data-lightbox`；**轮播 / 图文 / 评论各一组**）、横卡多行卡内图（每卡一组）、**单图/多图/视频上传缩略**。封面叠字 / 双列 / Banner / 文件上传默认不可预览（`data-preview=on/off` 例外）；可用 `data-lightbox-group` 自定义组容器 |
| 按钮 | 可点操作用套件类：`md-btn` + `--contained` / `--outlined` / `--soft` / `--text` / `--link`，或 `md-icon-btn` / `md-tab` / `md-menu__item` / `md-page-btn` / `md-tree__item`。禁止裸 `<button>`、禁止 `<input type="submit">` 露出浏览器灰钮/立体边 |
| 移动端 | 状态栏由 `proto-page.js` 固定顶注入；页根须标 `md-immersive` 或 `md-standard`；`md-section-head`；**列表区** `md-card--cover` / `--tile` / `--row`（多行，可无左图+小图）/ `md-set-row`（单行）；**功能区** `md-king` / `--pair` / `md-set-row` 通栏 / `md-set-pair`；触屏 `md-search` 仅左图标+输入；`viewport-fit=cover`；正文左右下走 `--md-safe-*`；标准顶栏左右 4px |
| 桌面端 | 必须有 `md-breadcrumb`（内容区顶部，不要 `md-page-head` 大标题）；表格首列可用 `md-row-goods` + `md-thumb md-media-ph--n`。D1-1 的冻结、操作阈值、语义列宽、紧凑密度和底部对齐直接执行共享 `PT-DESKTOP-LIST`：根用 `md-d1--list`，列用对应 `md-col-*`，更多菜单用 `md-actions` + `data-menu`，汇总/分页用 `md-d1__stats` / `md-d1__pager`。触屏弹窗/半屏内边距收紧；底半屏高度随内容、最大 70vh、超出正文滚动、关闭钮在面板右上角（`md-drawer__close`）。规格出现的弹窗/签/下拉/日期/按钮组必须用本节 AD 控件，禁止裸 `alert` / 无样式 `<select>` |
| 间距 | 触屏滚动区模块间距走 `--md-module-gap`（`md-module`）；卡片/栅格内距走套件；禁止内联 `margin` 当排版 |

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`proto-map.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。镜像 `versions/{v}/prototypes/{终端}/` 时 **须连同 `assets/`**（含 extras 与 `icons/`）。禁止改 kit 源文件来迁就某一页。禁止生成 `serve.json`。本地预览：在 `prototypes/` 目录执行 `python -m http.server`。

## 引用（硬性）

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | `./assets/mui-kit.css` + `./assets/md-icons.js` + `./assets/icons-extra.js` + `./assets/proto-page.js` |
| `index.html` 汇总壳 | 上表 + `./assets/proto-shell.css` + `./assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |
| `map.html` | `./assets/mui-kit.css` + `./assets/proto-shell.css` + `./assets/proto-map.js`；只填 `ProtoMap.boot({ project, terminal, pages, links })`，禁止手写拖拽/缩放/导出 |

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
          tabBarExempt: true,
          comps: [],
          spec: {
            layout: "依据 ui/PAGE-MP-001.md …",
            comps: "COMP-001 · 商品卡片 · 状态见页内/豁免",
            apis: "API-MP-001 · 查询推荐\n进页请求；失败 Toast。",
            features: "FEATURE-001 · … · 本页关联点",
            actions: "点击 · 卡片无出页（当前演示）"
          },
          brief: "首页展示推荐商品，可从底栏进入商品列表。"
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
          <div class="md-d1__stats"><span>共</span><strong class="md-d1__stats-num">6</strong><span>条</span></div>
          <div class="md-d1__pager">
            <span class="md-d1__pager-meta">第 <strong>1</strong> / 1 页</span>
            <nav class="md-pagination" aria-label="分页">…</nav>
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

操作列（**按操作个数选形态；常规动作默认图标钮，禁止无脑照抄「更多」**）：

```html
<!-- PT-DESKTOP-LIST：当前操作数无需“更多” -->
<td class="md-col-actions"><div class="md-actions">
  <button type="button" class="md-icon-btn" data-act="view" title="查看" aria-label="查看"><span class="md-icon" data-icon="view" aria-hidden="true"></span></button>
  <button type="button" class="md-icon-btn" data-act="edit" title="编辑" aria-label="编辑"><span class="md-icon" data-icon="edit" aria-hidden="true"></span></button>
</div></td>

<!-- ≥3：直出 1～2 个图标 + 更多图标；非常规文案进菜单 -->
<td class="md-col-actions"><div class="md-actions">
  <button type="button" class="md-icon-btn" data-act="view" title="查看" aria-label="查看"><span class="md-icon" data-icon="view" aria-hidden="true"></span></button>
  <div class="md-select-wrap">
    <button type="button" class="md-icon-btn" data-menu="actMenu1" title="更多" aria-label="更多"><span class="md-icon" data-icon="more" aria-hidden="true"></span></button>
    <ul id="actMenu1" class="md-menu md-menu--right md-menu--fixed">…</ul>
  </div>
</div></td>
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
          <a class="md-btn md-btn--link" href="./…">查看全部</a>
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

有 TabBar 时 **不要**再写 `md-appbar`。**沉浸式下沉**：`md-immersive` + `md-hero` 时，Hero **绝对定位钉在页顶底层、不随滚**；`md-mobile-body` 内必须包一层 **`md-mobile-sheet`（白底、宽 100%、无外边距、可有内边距）**，滚动时白底从上层盖住 Banner；顶距由 `::before` 占位露图并可点穿轮播。详情 `md-appbar--overlay` 仍叠最上层。**触屏滚动区按模块切分**：每个 L3 分区包 `md-module`；`md-mobile-body` / `md-mobile-sheet` 用 `--md-module-gap`（16px）统一模块间距；分区头放在模块内，禁止用内联 margin 拉开模块。**列表卡点名一种**（见下节）。详情/内容页主图用 `md-swiper md-swiper--wide`（**16:9**），介绍配图用 `md-media--16x9`。评论附图用 `md-comment__photos`（约 **40px**、**1:1**、圆角、横向排布超出换行，不要按正文宽五等分）。触屏正文左右下走 `--md-safe-*`；标准顶栏左右 4px（不预留 96 胶囊空）；overlay/cover 仍避让胶囊。触屏 `md-search` 仅左图标+输入（无「搜索」文案、无右侧搜索按钮）。左/底/右半屏：`md-drawer--left/bottom/right`。移动页 `<meta viewport>` 须带 `viewport-fit=cover`。**禁止**在页内手写 `md-status-bar`：由 `proto-page.js` 注入固定顶演示层。页根必须标 **`md-immersive`**（状态栏背景透明）或 **`md-standard`**（状态栏背景不透明）。正文可点文案与 Tab 走左右下安全距；标准顶栏左右贴边。

### 触屏列表区

同一模块只选一种（分区可各自点名）。规格有字段才写对应节点，禁止为好看编造业务字段。单行/多行选择直接执行共享 `PT-MOBILE-LIST`；该规则命中“字段少但值长”的多行分支时加 `md-card--long`，标题/摘要字号略大且高度随内容，不定 `min-height`。

**① 封面叠字** `md-card--cover`：一行一列大图，单行标题悬图片底部。图 **可横可竖**，或 **定宽、高度随图**（`--ratio-auto`，须内嵌 `<img>`）。套件默认 **16:9**；点名 `--ratio-16x9` / `--ratio-2x1` / `--ratio-4x3` / `--ratio-3x4` / `--ratio-2x3` / `--ratio-1x1`；`--h-sm/md/lg` 固定高度。

```html
<a class="md-card md-card--cover" href="./…">
  <div class="md-card__media md-media-ph md-media-ph--1">
    <span class="md-card__tag md-chip md-chip--success">有货</span>
    <h2 class="md-card__title">单行标题截断</h2>
  </div>
</a>
<!-- 横/竖：md-card--cover md-card--ratio-3x4 ；随图：md-card--ratio-auto ；定高：md-card--h-md -->
```

**② 双列瓷砖** `md-card--tile` + `md-grid-2`：上图 **可横可竖**，或 **定宽、高度随图**（`--ratio-auto`，须内嵌 `<img>`）。套件默认 1:1；点名 `--ratio-*`。标题最多两行，可选 `__chips` 小标签/图标、`md-price`、`__time` 小字。

```html
<article class="md-card md-card--tile">
  <!-- 横/竖/随图：再加 md-card--ratio-16x9 / --ratio-3x4 / --ratio-auto -->
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

**③ 横卡多行** `md-card--row`：内容与操作布局执行共享 `PT-MOBILE-LIST`。左可为封面 / 图标 / 头像 / 无；图片只允许 1:1 或竖图，宽高双锁定（默认 96×96），禁止 `width:100%` / `height:auto`。右轨用 `__rail`，多操作底栏用 `__actions--bar`，溢出菜单用 `data-menu` + `md-menu--fixed`；有按钮时根用 `<article>`。可选 `__photos` 最多五张 1:1 小图；共享规则命中“字段少但值长”分支时再加 `md-card--long`。

```html
<article class="md-card md-card--row">
  <a class="md-card__media md-media-ph md-media-ph--1" href="./…"></a>
  <!-- 竖图：卡片再加 md-card--ratio-3x4 ；不要用 16:9 / 2:1 -->
  <!-- 字段少但值长：再加 md-card--long -->
  <!-- 无封面：<span class="md-card__leading">…</span> -->
  <div class="md-card__body">
    <div class="md-card__main">
      <h2 class="md-card__title"><a href="./…">标题最多两行截断</a></h2>
      <p class="md-card__subtitle">副标题一行</p>
      <p class="md-card__text">摘要最多两行</p>
      <div class="md-card__chips"><span class="md-chip md-chip--outlined">标签</span></div>
    </div>
    <div class="md-card__photos">
      <div class="md-card__photo md-media-ph md-media-ph--1"></div>
    </div>
    <div class="md-card__meta">
      <span class="md-card__meta-item"><span class="md-icon" data-icon="schedule"></span>昨天</span>
    </div>
  </div>
  <div class="md-card__rail">
    <div class="md-card__aside">
      <p class="md-price">¥19.90</p>
      <p class="md-card__dist">1.2km</p>
    </div>
    <!-- 仅一个按钮：放在轨内即右下角 -->
    <div class="md-card__actions">
      <button type="button" class="md-btn md-btn--soft md-btn--sm">加购</button>
    </div>
  </div>
  <!-- 多个按钮：底栏靠右（不要与轨内按钮并用）
  <div class="md-card__actions md-card__actions--bar">
    <div class="md-select-wrap">
      <button type="button" class="md-btn md-btn--text md-btn--sm" data-menu="rowMore1">更多</button>
      <ul id="rowMore1" class="md-menu md-menu--right md-menu--fixed">…</ul>
    </div>
    <button type="button" class="md-btn md-btn--text md-btn--sm">收藏</button>
    <button type="button" class="md-btn md-btn--soft md-btn--sm">加购</button>
  </div>
  -->
</article>
```

**④ 横卡单行**（列表区内容行）`md-set-row`：定高、不换行；左图标→标题；右说明/计数/小标签。最多 3 个**短**字段；**任一字段值很长（单行放不下）改走横卡多行 + `md-card--long`**。**每行独立纸面，上下有缝**（放进 `md-stack`，**不要**包进 `md-set-group`）。列表区与功能区的差别：**列表非分组**，条目可无限（即便分页加载，叠在一起也看不出页边界）；**功能成组**，每组入口有限。视觉上：通栏挤在一组纸面里、行间只有分割线；列表单行各自独立有缝。列表卡（封面/双列/横卡多行/单行）统一用 **轻阴影** `--md-shadow-surface`。**功能区**（通栏 / 一行两个 / 金刚）与 **页内签**：**不要**圆角阴影卡片壳（平铺即可）。**不要**用 `md-set-pair` 冒充列表。

```html
<div class="md-stack">
  <a class="md-set-row" href="./…">
    <span class="md-set-row__lead">
      <span class="md-icon" data-icon="goods" aria-hidden="true"></span>
      <span class="md-set-row__label">有机草莓 250g</span>
    </span>
    <span class="md-set-row__trail">
      <span class="md-set-row__hint">¥19.90</span>
    </span>
  </a>
  <!-- 下一行同结构，行间有缝 -->
</div>
```

### 触屏功能区

金刚宫格 `md-king`（4/5 列）/ 金刚双卡 `md-king--pair` / 通栏 `md-set-row` / 一行两个 `md-set-pair`。**金刚不限首页**。**金刚双卡 vs 一行两个**：信息多（要标题+说明）用双卡；信息少（图标+短标题）用一行两个。通栏与一行两个的 **分组标题可有可无**。通栏包在 `md-set-group` 里连成一片；组内用 **淡色内缩分割线**（`--md-divider-soft`，左右仍留距）。**触屏功能区跟正文同左右安全距**（通栏/一行两个/金刚不要负边距贴手机框）。**设置项与功能入口同壳**：设置项在当前行直接操作（开关等）；功能入口只跳转或开半屏/弹窗（常带右箭头）。**功能区**与 **页内签**：**不要**圆角、轻阴影卡片壳。**我的 / 设置** 页根加 **`md-set-page`**（浅灰 `#f7f7f7` 同详情），组与组靠外边距/gap 漏底。列表单行是内容、独立有缝、一般不带箭头；数据流可无限。金样：金刚见 `gold/mobile-grid.html`，入口见 `gold/mobile-menu.html`，设置见 `gold/mobile-settings.html`。

| 节点 | 规则 |
|------|------|
| `__title` | ①单行悬底；②③最多两行截断 |
| `__subtitle` | ③次级一行 |
| `__text` | ③摘要；横卡默认两行截断 |
| `__chips` | ②③正文小标签/小图标，靠左；不是封面角标 |
| `__time` | ②底部小字时间/浏览 |
| `__meta` / `__meta-item` | ③时间、浏览、点赞等小字；可带 14px 图标或 `__thumb` |
| `__foot` | ③可选；只放左栏次要信息，不要再把价格塞进 `__foot` |
| `__rail` / `__aside` | ③右侧留白轨；价格 / 距离靠右上，留边框安全距 |
| `__dist` | ③右上距离/位置小字，跟价格同一轨 |
| `__actions` | ③单按钮放轨内（右下角）；多按钮用 `--bar` 底栏靠右从右到左；过多收「更多」`data-menu` |
| `__leading` | ③左侧小图标（固定 40）；`--avatar` 为圆头像（同固定 40）。占位可同节点挂 `md-media-ph`（金样写法），勿再给同节点写铺满宽高 |
| `__tag` | 状态标签贴**封面**左上或右上（`--tr`） |
| `__photos` / `__photo` | ③横卡多行文本区小缩略图（约 40px、1:1），一排最多五张；不要按正文宽五等分。评论附图走 `md-comment__photos`，同样约 40px |

触屏顶栏四种（规格点名一种，禁止混用、禁止把封面顶栏拉成 16:9）：

| 形态 | 用法 | 金样 |
|------|------|------|
| 16:9 大背景 + slogan | `md-immersive` + `md-hero` + `md-swiper`；有 TabBar 则无页内顶栏 | `gold/mobile-grid.html` |
| 16:9 大背景 + 左上返回和标题 | `md-immersive` + `md-appbar--overlay` + `md-swiper--wide` | `gold/mobile-detail.html` |
| 标准高度标题栏 + 靠左返回和标题 | `md-standard` + `md-appbar md-appbar--mobile` | `gold/mobile-form.html`（另加 `md-form-page`） |
| 两倍标准高度封面 + 标题 | `md-immersive` + `md-appbar--cover` + `__cover` 背景图；高度约 `2 ×` 标准标题栏 | `gold/mobile-settings.html` |

```html
<header class="md-appbar md-appbar--mobile md-appbar--cover">
  <div class="md-appbar__cover md-media-ph md-media-ph--2" aria-hidden="true"></div>
  <a class="md-icon-btn" href="#" aria-label="返回"><span class="md-icon" data-icon="back"></span></a>
  <h1 class="md-appbar__title">设置</h1>
</header>
```

金刚区默认 4/5 列（图标文字上下居中），**可出现在任意需要入口区的页面，不限首页**。信息多、要标题+说明时用 `md-king--pair` 双卡（小图标与文案均靠左）：

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

抽屉：`ProtoPage.openDrawer(id)` / `closeDrawer(id)`，遮罩 id 为 `{id}Backdrop`。**底半屏** `md-drawer--bottom`：高度随内容、最大 **70vh**，超出时 `__body` 滚动；关闭钮 `md-drawer__close` 在面板右上角（`openDrawer` / 页初始化会自动补，轮盘 `md-wheel` 除外）。**底半屏放选项时每项独占一行**（`md-drawer__opt` / `md-choice-group` / `md-set-picks` / 下拉 `md-select-sheet__opt`），不要用表单标签换行。

```html
<aside id="catSheet" class="md-drawer md-drawer--bottom">
  <button type="button" class="md-drawer__close" aria-label="关闭" onclick="ProtoPage.closeDrawer('catSheet')">
    <span class="md-icon" data-icon="close" aria-hidden="true"></span>
  </button>
  <h2 class="md-drawer__title">分类</h2>
  <div class="md-drawer__body">
    <div class="md-choice-group">
      <label class="md-radio"><input type="radio" name="cat" checked> 水果</label>
      <label class="md-radio"><input type="radio" name="cat"> 坚果</label>
    </div>
    <!-- 或纯选项行：<button type="button" class="md-drawer__opt">水果</button> -->
  </div>
  <div class="md-drawer__actions">
    <a class="md-btn md-btn--contained" href="./…">去列表</a>
  </div>
</aside>
```

## AD 常用控件（规格里有则必须用）

弹窗、确认、Toast、页内签、按钮组、下拉、日期/时间 **禁止**再用浏览器原生丑控件或 `alert()`。可点按钮 **禁止**裸 `<button>` / `<input type="submit">`（系统灰钮、立体边）；必须 `md-btn` + 形态类，对照金样 `gold/mobile-buttons.html`。

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

**触屏页内签**（贴在搜索/筛选下方，不进滚动区；未选中浅底色字、选中色块白字。禁止桌面 `md-tabs--page` 下划线）

```html
<nav class="md-tabs">
  <button type="button" class="md-tab is-active" data-panel="listAll">全部</button>
  <button type="button" class="md-tab" data-panel="listIn">有货</button>
  <button type="button" class="md-tab" data-panel="listOut">售罄</button>
</nav>
<div class="md-tab-panels">
  <div id="listAll" class="md-tab-panel is-active">…</div>
  <div id="listIn" class="md-tab-panel">…</div>
  <div id="listOut" class="md-tab-panel">…</div>
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

**只读 / 禁用输入**（**视觉一致**：灰底 `#eee`、标签缺口同色灰底、淡字；语义上 `readonly` 仍可复制文本，`disabled` 不参与提交。日期段触发器的 `readonly` 不要套 `md-field--readonly`）

```html
<label class="md-field md-field--readonly">
  <span class="md-field__label">只读</span>
  <input class="md-field__input" type="text" value="不可编辑" readonly>
</label>
<label class="md-field">
  <span class="md-field__label">禁用</span>
  <input class="md-field__input" type="text" value="不可修改" disabled>
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

触屏按钮对照金样 `gold/mobile-buttons.html`：小 `--sm` / 中默认 / 大 `--lg`；形态含线框 `--outlined`、色块 `--contained`、**浅底 `--soft`（无边框、浅色底+有色字）**、文字 `--text`、**纯文字链接 `--link`（无线框无背景，用于查看更多/了解全部；字色须区别紧邻正文，默认主色）**、置灰 `disabled`、角标内嵌 `md-badge`。

```html
<button type="button" class="md-btn md-btn--outlined md-btn--sm">线框</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">色块</button>
<button type="button" class="md-btn md-btn--soft md-btn--sm">浅底</button>
<button type="button" class="md-btn md-btn--outlined md-btn--sm" disabled>线框置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm" disabled>色块置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">角标<span class="md-badge">8</span></button>
```

功能区通栏 / 一行两个对照金样 `gold/mobile-menu.html` / `gold/desktop-menu.html`。分组标题可无。短说明可省略，通栏箭头保留。**右侧说明位也可换成方形配图**：`md-set-row--thumb` + `__thumb`（1:1，约 52px），行高随之加高；有图时不再叠文字 `__hint`。字段多改列表区横卡多行。

```html
<a class="md-set-row" href="./PAGE-MP-002.html">
  <span class="md-set-row__lead">
    <span class="md-icon" data-icon="goods" aria-hidden="true"></span>
    <span class="md-set-row__label">我的订单</span>
  </span>
  <span class="md-set-row__trail">
    <span class="md-set-row__hint">查看全部</span>
    <span class="md-icon" data-icon="chevron-right" aria-hidden="true"></span>
  </span>
</a>

<!-- 右侧方形配图（行更高） -->
<a class="md-set-row md-set-row--thumb" href="#">
  <span class="md-set-row__lead">
    <span class="md-icon" data-icon="star" aria-hidden="true"></span>
    <span class="md-set-row__label">会员专享</span>
  </span>
  <span class="md-set-row__trail">
    <span class="md-set-row__thumb md-media-ph md-media-ph--2" aria-hidden="true"></span>
    <span class="md-icon" data-icon="chevron-right" aria-hidden="true"></span>
  </span>
</a>
```

一行两个用 `md-set-pair` 包两格（信息少：图标+短标题；信息多改用 `md-king--pair` 金刚双卡）：

```html
<div class="md-set-pair">
  <a class="md-set-row" href="#">…左格…</a>
  <a class="md-set-row" href="#">…右格…</a>
</div>
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
      <div class="md-card__body">
        <div class="md-card__main">
          <h2 class="md-card__title">已提交</h2>
          <p class="md-card__text">横卡文本说明；需要时在正文下加多张小图。</p>
        </div>
        <div class="md-card__photos">
          <div class="md-card__photo md-media-ph md-media-ph--1"></div>
          <div class="md-card__photo md-media-ph md-media-ph--2"></div>
        </div>
      </div>
    </article>
  </li>
</ol>
```

**时间轴** `md-timeline`：`__item` + `__rail`（`__node` + `__line`）+ `__body`。`is-done` 已完成、`is-active` 当前。点节点切高亮；若带 `data-target` / `data-section` 则滚动对应锚点。

- **触屏 / 桌面**：右侧 `__body` 用 `md-card--row` **横卡文本**（**禁止左图**）；正文内可选 `md-card__photos` + `md-card__photo` 多张小图。金样 `gold/mobile-timeline.html` / `gold/desktop-timeline.html`。桌面不要左右分栏，章节大纲才走 `desktop-locator.html`。

## 无类名组合（禁止裸 HTML）

套件没有「一模一样」的控件时，**必须**用下表组合，禁止自造 class、禁止无 `md-*` 的 `<button>` / `<input>` / `<table>`、禁止用随机色块当图。

| 规格里出现 | 必须用 | 禁止 |
|------------|--------|------|
| 筛选 / 搜索栏 | `md-filter` 或 `md-d1__search` | 无 class 的 `<form>`；筛选区 label / 输入字号更小（套件已收紧） |
| 侧滑 / 抽屉 | `md-drawer md-drawer--left/right/bottom` + `md-backdrop`；底半屏高度随内容、最大 70vh、`__close` 右上角；选项用 `__opt` / `md-choice-group` 且每项一行 | 自造 `position:fixed` 面板；`display` 瞬切；底半屏定死全高或关闭钮只放底栏；底半屏选项标签换行挤一行 |
| 轮播 Banner | `md-swiper` + `__track` + `__slide` + `__dots` | 自造横向滚动无指示点 |
| 金刚区 | `md-king` + `md-king__item`（4/5 列：图标+文字上下居中同底）；或 `md-king--pair`（一排两张大卡，小图标与 `__name`/`__desc` 均靠左）。**不限首页**；信息多用双卡 | 图标单独色块、文字露在底外；无热区的纯文字宫格；双卡内容居中；把双卡和一行两个按是否首页选型 |
| 方形图标按钮 | `md-btn--stack` 或金刚项同款：图标上、文字下、共一块底 | 图标独立成钮、文字在旁或底外 |
| 贴底主操作 | `md-action-bar` 或 `md-tabbar`；**一行仅一钮时占满整行** | 主按钮写在滚动内容末尾；单钮却缩成短条靠左 |
| 上传 | `md-upload`；单图 `md-upload--single`；多图 `md-upload-grid`；文件 `md-upload--file`。**单图/多图/视频缩略默认可点预览**（多图一组）；文件上传不进灯箱；`data-preview=off` 可关 | 裸 `<input type="file">`；上传缩略不可点放大 |
| 触屏滑动条 | `md-slider`（`--steps` 五档位 / `--fluid` 无极） | 无刻度无当前值的裸 range |
| 触屏日期/省市区 | `data-wheel="date|region"` 底半屏三级联动，无开始/结束签 | 原生 `type=date`；三个独立下拉；给省市区加日期段签 |
| 触屏日期段 | `data-wheel="daterange"` 底半屏，开始/结束两个签 | 两个独立日期框硬凑；原生 `type=date` |
| 空态 | `md-empty md-empty--illus` | 一行灰字 / 空白 |
| 加载 | `md-skeleton` / `data-state="loading"` + `md-skel-host` | 纯文字「加载中」 |
| 封面 / 图片位 | 必须挂在点名形态内：`md-card--cover` / `--tile` / `--row` 的 `md-card__media md-media-ph--1`～`--6`；横卡根节点必须带 `md-card--row`（左图**宽高双锁**）；详情主图 `md-swiper--wide`；介绍配图 `md-media--16x9`；页顶大背景 `md-hero` / `md-appbar--cover` | **裸** `md-card__media` 或横卡漏写 `--row` / 左图 `height:auto`（会被拉高再撑宽挤掉正文）；`style="background:#xxx"` 色块；无编号灰块；给封面叠字 / 双列 / Banner / 文件上传加预览 |
| D1-2 表单 | `md-d1` + `md-d1__form` + `md-field--sm`；通栏不限宽（`--md-field-min` 只约束字段）；行距靠 grid `row-gap`；整页 `--cols-1/2/3/4`；块内 `md-form-block--cols-*` | 无纸面的裸 label 堆叠；弹窗内双列并排；字段包进无 gap 的裸 div 导致上下贴死；**用表单栅格冒充页面左右分栏** |
| 页面分栏 | `md-layout--full/2col/fix-left/fix-right/3col/pin`；定宽栏 `--md-layout-aside` | 用 `md-d1__form` 当页面布局 |
| 进步条 / 进度条 / 页签 | 同属状态导览：`md-tabs` / `md-stepper` / `md-advance` / `md-progress` | 用无极冒充分段；把签与进步条写成互不相关两套 |
| 定位导航 | `md-locator` `--cats` / `--outline`；左栏 `md-split--outline` 可收缩为点线轨；右悬浮 `md-locator-float` 收起同样变点线轨；滚正文时当前章 `is-active` 联动 | 用 `md-tree` 冒充分类钮；用分类冒充可展开树；把时间轴做成大纲分栏 |
| 树 | 不分页 `md-tree` + `__item` `__toggle` `__label`；总控 `md-tree-bar`；节点 `__ops`（增子/重命名/删除）；拖放 `上/中/下`；表内 `md-table--nest`。只读 `data-tree-edit="off"`；末级禁增 `data-leaf` / `data-leaf-add="off"` | 无类名嵌套 `ul`；用分类定位冒充树；触屏用列表硬套分类树 |
| 步骤条 | `md-stepper` + `md-step`；已完成 `is-done`；当前 `is-active`。桌面数字步骤可点跳步（`proto-page.js` 自动绑）；自管步进写 `data-wizard="off"` | 纯数字列表；桌面数字步骤不可点 |
| 进步条 | `md-advance` + `__head` + `__track` + `__seg` + `__bar`；`data-segments`；触屏可 `--lg` | 用无极 `md-progress` 冒充分步 |
| 进度条 | `md-progress` + `__head` + `__track` + `__bar`；不确定 `--indeterminate`；触屏可 `--lg` | 裸 `<progress>` / 自造色条 / 用分段 `md-advance` 冒充上传 |
| 时间轴 | `md-timeline` + `__item` `__rail` `__node` `__line` `__body`；右 **横卡文本** `md-card--row`（无左图，正文可 `__photos`）；`is-done` / `is-active` | 用列表硬套竖轨；时间轴右卡加左图；桌面做成左右分栏导航 |
| 图表 | `md-chart-ph` 占位条 | 手写 canvas / 自造柱 |
| 页内分页签 | 桌面：`md-tabs md-tabs--page` 下划线（**平铺，无圆角阴影卡片壳**）；触屏：`md-tabs`（自动按钮组，浅底/选中色块） | 触屏用桌面下划线签；自造下划线 `div` / 裸 `<a>` 签；页内签套卡片壳 |
| 主/线/浅底/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / **`--soft`（无边框浅底色字）** / `--text` / `--link`；**通栏整行** `--block`（或 `md-btn-row` 竖叠）；图标钮 `md-icon-btn`。触屏贴底 `md-action-bar` / 半屏 `md-drawer__actions` **仅一钮时自动占满** | 裸 `<button>`、`<input type="submit">`、Bootstrap/`btn`、浏览器灰钮；一行一主钮却缩成短条 |
| 悬浮胶囊 / 桌面悬浮按钮 | 形态与阈值执行共享 `PT-FLOAT`；触屏用 `md-pod` 方位类，桌面用 `md-pod--desk`，折叠用 `md-pod--fold` + `__toggle` | 写进滚动层；违反共享方位；用 `md-fab` 冒充；功能钮缩放回弹 |
| 按钮组 / 工具栏按钮 | `md-btn-group` / `md-d1__toolbar`（功能栏**平铺，无圆角阴影**；保留内边距；区块间距靠父级 gap） | 无 class 的一排 `<button>`；功能栏套卡片壳 |
| 下拉 | 少选项：`md-field--select` + `md-select`；多选/搜索/树：`md-field--combo` + `md-combo`（`data-mode="multi"` / `data-search="1"` / `data-tree="leaf|1"`）；菜单：`md-select-btn` + `md-menu` | 未包 `md-field` 的裸 `<select>`；触屏用系统原生选择器；自造 autocomplete 面板 |
| 日期 / 时间 | `md-field--date` / `md-field--daterange` / `md-field--time` + `type="date|time|datetime-local"` | 自造日历、两个裸日期框冒充日期段 |
| 开关 | `md-switch-row` + `md-switch` | 自造滑块 / 裸 checkbox 当开关 |
| 功能区通栏 / 一行两个 | 通栏包 `md-set-group`；一行两个 `md-set-pair`（信息少）。右说明可为文字 `__hint` 或方形 `__thumb`（`--thumb`，整行加高）。信息多改 `md-king--pair`。**平铺，无圆角阴影卡片壳** | 一排 `md-btn`；右图用列表横卡冒充；功能入口右图进灯箱；信息多却硬用一行两个；功能区套列表卡圆角阴影 |
| 单选 | 桌面/列表：`md-choice-group` + `md-radio`；触屏表单：同上（自动标签角标） | 未包 `md-radio` 的裸 `<input type="radio">` |
| 多选 | 桌面/列表：`md-choice-group` + `md-check`；触屏表单：同上（自动标签角标）；列表行勿包成标签 | 未包 `md-check` 的裸 `<input type="checkbox">` |
| 弹窗 / 确认 | `md-dialog` + `md-backdrop`；确认用 `ProtoPage.confirm` | `alert()` / `confirm()` |
| Toast / 提示 | `ProtoPage.snackbar` / `md-alert` / `md-tooltip` | 页内红字当提示 |

D5 弹窗用 `md-dialog` + `md-backdrop`，打开后有遮罩淡入和面板缩放；禁止 `alert('原型：…')`。**触屏**弹窗内边距收紧；底半屏 `md-drawer--bottom` 高度随内容、最大 70vh、超出 `__body` 滚动，关闭用面板右上角 `md-drawer__close`（`openDrawer` 会自动补）。**表单弹窗** `md-dialog__form`：**一行只放一个输入项**（单列），不要双列并排字段。整页 D1-2 `md-d1__form` 仍可双列。

### 详情页：标题区 + 图文混排

对照金样 `gold/mobile-detail.html` / `gold/desktop-detail.html`（图文签）。页根加 **`md-detail-page`**。字段详情见同页字段签。

| 层级 | 写法 | 规则 |
|------|------|------|
| 页底 | `md-detail-page` | **整页浅灰**（`#f7f7f7`）；滚动盖住 Hero 的 sheet 也用同色 |
| 内容壳 | `md-detail-content`（触屏可叠在 `md-mobile-sheet`） | **透底**；用 `gap`（`--md-detail-block-gap`）拉开区块，**漏出浅灰** |
| 模块 | `md-module` | 标题/图文等为 **白底通栏区块**（有内边距、无圆角/阴影）；模块间靠间隙露灰 |
| 标题区 | `md-detail-head` | 商品名（一级）/ 价+状态同行 / 短摘要；落在白底模块内 |
| 图文混排 | `md-article` | **四级标题** `__h1`～`__h4`；短段默认**不**首行缩进；大段多行正文用 `__body` 才缩进；多项目用 `__list`（`--ordered` 有序）；配图 `__figures--1/2`；图注 `__caption` 居中；表格 `__table-wrap` |
| 评论 | `md-comment-list` > `md-comment` | 评论模块 **透底**；条目仍 **列表卡**（轻阴影 `--md-shadow-surface`、间距露灰） |
| 点图预览 | 页根 `data-lightbox` | **分区成组**：轮播（`.md-swiper`）一组、图文（`.md-article`）一组、评论（`.md-comment-list`）一组；翻上一张/下一张不跨区。可选 `data-lightbox-group` 自定容器 |
| 页内导航 | 右下 `md-pod--detail-nav`（脚本默认注入） | **目录** + **返回顶部**；点目录底半屏列出本页 `data-section`（金样：基本信息 / 店铺信息 / 商品介绍 / 商品评论），点选滚动定位。`data-detail-nav="off"` 关闭；`"toc"` / `"top"` 只留其一 |

```html
<div class="md-mobile-page md-immersive md-detail-page" data-lightbox>
  <!-- 主图 md-hero … -->
  <main class="md-mobile-body">
    <div class="md-mobile-sheet md-detail-content">
      <section class="md-module">
        <div class="md-detail-head">
          <h1 class="md-detail-head__title">有机草莓 250g</h1>
          <div class="md-detail-head__bar">
            <p class="md-price">¥19.90</p>
            <span class="md-chip md-chip--success">有货</span>
          </div>
          <p class="md-detail-head__lead">短摘要</p>
        </div>
      </section>
      <section class="md-module">
        <div class="md-article">
          <h2 class="md-article__h2">商品说明</h2>
          <h3 class="md-article__h3">产地与口感</h3>
          <p class="md-article__body">大段多行正文才首行缩进……</p>
          <p>短说明不缩进。</p>
          <ul class="md-article__list">
            <li>多项目罗列用项目符号</li>
            <li>有序可用 md-article__list--ordered</li>
          </ul>
          <div class="md-article__figures md-article__figures--1">
            <div class="md-article__figure">
              <div class="md-media--16x9 md-media-ph md-media-ph--2"></div>
              <p class="md-article__caption">图注居中</p>
            </div>
          </div>
          <div class="md-article__figures md-article__figures--2">
            <div class="md-article__figure">…</div>
            <div class="md-article__figure">…</div>
          </div>
          <div class="md-article__table-wrap">
            <table class="md-article__table">
              <thead><tr><th>项目</th><th>规格</th><th>说明</th></tr></thead>
              <tbody><tr><td>净含量</td><td>250g</td><td>约一盒</td></tr></tbody>
              <caption>列多时可左右滑动</caption>
            </table>
          </div>
        </div>
      </section>
    </div>
  </main>
</div>
```

禁止：内容区/模块再套 `md-card` 式圆角阴影；说明配图用列表 1:1/竖图；短句硬套首行缩进；大段正文漏写 `__body`；多项目硬塞成一段不缩进正文；图注左对齐当正文；详情规格表用 D1-1 冻结列表壳。

### 字段详情：名称 + 值（可分组）

对照金样 `gold/mobile-fields.html` / `gold/desktop-detail.html` 字段签。页根仍用 **`md-detail-page`**（浅灰底 + 白底分组区块）。适用于订单/工单/档案等 **只读多字段** 核对页。**一条对象**；多条记录的分组字段列表走 `desktop-lists` 的 `md-group-list`，不要互套。

| 层级 | 写法 | 规则 |
|------|------|------|
| 页壳 | 同详情页：`md-detail-page` + `md-detail-content` + `md-module` | 触屏用 **标准顶栏**（返回+标题），一般 **不要** 沉浸式 16:9；桌面面包屑 |
| 概览（可选） | `md-detail-head` | 主标题 / 状态 Chip / 短说明；有次要操作放 `__actions` |
| 分组 | 每组一个 `md-module` + `md-section-head` + `data-section` | 字段多才分组；组名进目录 |
| 字段表 | `dl.md-desc` > `__row` > `__label` + `__value` | **左名右值**；空值显示「—」；状态可用 Chip |
| 长文案 | `__row--stack` | 名在上、值在下（地址、备注等） |
| 桌面多列 | `md-desc--cols-2` / `--cols-3` | 仅桌面；触屏强制单列。跨列长行加 `__row--span` |

```html
<section class="md-module" data-section="基本信息">
  <div class="md-section-head">
    <h2 class="md-section-head__title">基本信息</h2>
  </div>
  <dl class="md-desc"><!-- 桌面可加 md-desc--cols-2 -->
    <div class="md-desc__row">
      <dt class="md-desc__label">订单编号</dt>
      <dd class="md-desc__value">OD-20240815-8821</dd>
    </div>
    <div class="md-desc__row md-desc__row--stack md-desc__row--span">
      <dt class="md-desc__label">收货地址</dt>
      <dd class="md-desc__value">……</dd>
    </div>
  </dl>
</section>
```

禁止：把字段详情做成可编辑 `md-field` 表单；用 D1-1 表格壳硬套字段表；无分组却堆成一篇图文；桌面沉浸式叠层；用 `md-group-list` 冒充单对象字段详情。

### 资料卡片 `md-profile`

**适用场景**：店铺资料、个人资料、公司资料，以及品牌/机构等同类主体卡；**不限详情页**（列表、主页、关于页等凡要展示主体摘要都可用）。同一套结构，按场景换左图与文案即可（个人用 `--avatar` 圆头像；店铺/公司用默认圆角方图作门头或 Logo）。

分上中下三层，**中、下可选**。**最精简**：只留上层，且上层仅有左图 + 中间 `__title` + `__subtitle`（无 `__meta` / `__tags` / `__side`，也无中层统计、下层按钮）。

| 层 | 类名 | 规则 |
|----|------|------|
| 根 | `md-profile` | **默认平铺**：无圆角、无轻阴影（各场景一致，不限详情）。**页顶使用**加 `--top`（或沉浸式无 Hero/顶栏时自动）：`padding-top` = 状态栏高 + 顶部安全区 |
| 上（必选） | `__head` | 左 `__media` + 中 `__main`；右 `__side` **可选** |
| 左图 | `__media` | **精简必留**。个人头像加 `--avatar`（圆）；店铺门头 / 公司 Logo 用默认圆角方图；尺寸 `--sm` / 默认 / `--lg`。**不进灯箱** |
| 中文 | `__main` | 靠左：`__title`（**精简必留**）→ `__subtitle`（**精简必留作说明**）→ 可选 `__meta` → 可选 `__tags` |
| 右钮 | `__side` | **可选**；有则靠上一个按钮（关注/收藏/详情/查看/编辑等），常用 `md-btn--outlined md-btn--sm` |
| 中（可选） | `__stats` > `__stat` | 一排 **2～5** 项；`__stat-value` + `__stat-label`；项间 **不通顶** 细竖线 |
| 下（可选） | `__foot` | **1～3** 个浅纯色底按钮（默认 `md-btn--soft`；强调可加 `md-btn--primary`） |

```html
<!-- 最精简：仅上层 · 左图 + 标题 + 说明；页顶再加 md-profile--top -->
<article class="md-profile md-profile--top">
  <div class="md-profile__head">
    <div class="md-profile__media md-profile__media--avatar md-media-ph md-media-ph--1"></div>
    <div class="md-profile__main">
      <h2 class="md-profile__title">阿宁</h2>
      <p class="md-profile__subtitle">果园主理人 · 冷链直达</p>
    </div>
  </div>
</article>

<!-- 完整示例（中层/下层/右钮/标签均可按需删） -->
<article class="md-profile">
  <div class="md-profile__head">
    <div class="md-profile__media md-media-ph md-media-ph--3"></div>
    <div class="md-profile__main">
      <h2 class="md-profile__title">鲜果直达旗舰店</h2>
      <p class="md-profile__subtitle">冷链鲜果 · 次日达</p>
      <p class="md-profile__meta">
        <span class="md-profile__rating">★★★★☆ 4.8</span>
        <span>1.2万粉丝</span>
      </p>
      <div class="md-profile__tags">
        <span class="md-chip md-chip--outlined">五年老店</span>
        <span class="md-chip md-chip--primary">SVIP</span>
      </div>
    </div>
    <div class="md-profile__side">
      <button type="button" class="md-btn md-btn--outlined md-btn--sm">关注</button>
    </div>
  </div>
  <div class="md-profile__stats">
    <div class="md-profile__stat">
      <p class="md-profile__stat-value">128</p>
      <p class="md-profile__stat-label">在售</p>
    </div>
    <div class="md-profile__stat">
      <p class="md-profile__stat-value">4.9</p>
      <p class="md-profile__stat-label">评分</p>
    </div>
  </div>
  <div class="md-profile__foot">
    <button type="button" class="md-btn md-btn--soft md-btn--sm">进店逛逛</button>
    <button type="button" class="md-btn md-btn--soft md-btn--sm">联系客服</button>
  </div>
</article>
```

禁止：中层竖线拉满整行高度；下层用描边主按钮冒充浅底；左图裸 `md-card__media`；把资料卡当成列表横卡 `--row`；精简形态再拆成裸头像+正文另排；**页顶资料卡顶到状态栏**（须 `--top` 或依赖自动避让）；给资料卡加列表式圆角轻阴影（默认必须平铺）。

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/浅底/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / **`--soft`（无边框浅底色字）** / `--text` / **`--link`（纯文字无线框无背景，查看更多/了解全部）**；`--sm` `--lg`；置灰 `disabled`；角标内嵌 `md-badge`。**`--text`/`--link` 字色须区别紧邻正文**（默认主色，禁止跟正文同色） |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input`；只读加 `md-field--readonly` + `readonly`，或 `disabled`（**灰底淡字**）。日期段 `readonly` 触发器不要加 `--readonly` |
| 卡片 | `md-card` **`--cover` / `--tile`（可横可竖或 `--ratio-auto` 定宽随图）`--row`（左图仅 1:1 或竖图 `--ratio-3x4/2x3`；字段少因值长再加 `--long`）**；列表单行 `md-set-row`。`md-card__media` `md-card__leading` `--avatar` `md-card__body` `md-card__main` `md-card__title` `md-card__subtitle` `md-card__text` `md-card__chips` `md-card__rail` `md-card__aside` `md-card__dist` `md-card__actions` `--bar` `md-card__time` `md-card__foot` `md-card__meta` `md-card__photos` `md-card__photo` `md-card__tag` `--tl/--tr` `md-price` |
| 资料卡片 | `md-profile`（店铺/个人/公司；**默认平铺**无圆角/轻阴影）；**最精简**=仅 `__head`（`__media` + `__title` + `__subtitle`）；完整再加 `__side` / `__meta` / `__tags` / `__stats` / `__foot`；**页顶**加 `--top` |
| 详情页 | 页根 `md-detail-page`（整页浅灰）；内容壳透底；标题/图文 **白底区块**、间隙露灰；`md-detail-head`；`md-article` 四级标题；短段不缩进、大段 `__body` 缩进、多项目 `__list`；`__figures--1/2`+居中 `__caption`+表格可横滑；**评论列表卡**；可嵌平铺 **资料卡片**；右下 **目录+返回顶部** |
| 字段详情 | 同 `md-detail-page` 壳；分组 `md-module`+`md-section-head`；`md-desc` 左名右值（`--stack` 上下、桌面 `--cols-2/3`、跨列 `--span`）；金样 `mobile-fields` / `desktop-detail` 字段签 |
| 分区 / 模块 | `md-module`（L3，模块间距 `--md-module-gap`）`md-section-head` `md-section-head__title` |
| 系统栏 | `md-status-bar`（`proto-page.js` 固定顶注入；页内禁止手写；时间/信号靠顶略放大，左右各收一个图标身位，不为胶囊留空） |
| 触屏顶栏 | ① `md-hero` 16:9+slogan ② `--overlay` 叠 16:9 ③ 标准 `md-appbar--mobile` ④ `--cover` 两倍高度封面 |
| 桌面面包屑 | `md-breadcrumb`（D1 内容区顶部，禁止再写 `md-page-head`） |
| 操作列 | 阈值与收纳执行 `PT-DESKTOP-LIST`。`md-col-actions` 宽按直出按钮形态与数量钉整列（表头与单元格同宽；套件实测 `.md-actions`）；常规动作 `md-icon-btn` + `title`/`aria-label`；删除加 `md-icon--danger`；「更多」用 `data-menu` + `md-menu md-menu--fixed` |
| 语义列宽 | `md-col-check` 勾选；`md-col-name` 名称硬锁定宽；`md-col-desc` / `md-col-note` 说明吃剩余；`md-col-date` / 最后数据列规则同前；`md-col-price` / `md-col-status` / `md-col-id` / `md-col-num`。**多字段单元格**用 `md-cell-stack`（`__primary` / `__secondary`）。长值省略不得溢出叠邻列；悬停看全文、点击复制 |
| D1-1 紧凑 | 根节点 `md-d1 md-d1--list`；**不要**套到 D1-2 表单页 |
| 列表六型 | 选型 `desktop-lists`（**金样只对标列表区**）：分页标准 `md-d1--list`；分页树表 `md-table--nest`；分组字段 `md-group-list`；只读树 `data-tree-edit="off"`；**分页无图/有图卡片** `md-d1__list` + `md-card-grid` + 底栏 `md-d1__footer`（同一行等高；无图卡右上角或表列 `md-col-switch` 可放开关；卡右下角 `md-card__foot` 可放按钮）。筛区/功能栏按规格另加 |
| 工作台 | `md-stat-grid` `md-stat-card`；趋势 `md-chart-ph` |
| 页面分栏 | `md-layout` `--full` / `--2col` / `--fix-left` / `--fix-right` / `--3col` / `--pin` + `__pane` / `__pane--span`。定宽栏 `--md-layout-aside`。**禁止**用 `md-d1__form` 冒充 |
| 分栏 / 树 | `md-d1--split`；`md-split` `__side` `__main`；树 `md-tree` `__row` `__ops` `md-tree-bar`；拖到节点上/中/下；只读 `data-tree-edit="off"`；定位导航 `md-locator` `--cats` / `--outline`（`data-target`，滚正文高亮联动）；左大纲 `md-split--outline` + `data-outline-toggle`（收起变点线轨）；右悬浮 `md-locator-float`（收起同样点线轨） |
| 表内嵌套树 | `md-table--nest` + `md-row--child` + `md-nest-toggle`（空按钮，CSS 画 +/−）；`data-row-id` / `data-parent`；子行 `.md-nest-name` 缩进 |
| 分组字段列表 | `md-group-list` `__group` `__head` `__item` + `md-desc`；无分页；**多条记录**；组标题加粗坐白底卡；记录间浅线左右内缩、不贴边；字段行不再分割。单对象字段详情用 `md-module`+`md-desc`，见 `desktop-detail` 字段签 |
| D1-2 表单栅格 | `md-d1__form`（默认双列，通栏 `width:100%`，`row-gap` 保留）；整页 `--cols-1/2/3/4`；块内 `md-form-block--cols-*`；字段 `--md-field-min`。弹窗 `md-dialog__form` 单列 |
| 下拉组合框 | `md-combo` + `md-combo__trigger` / `__panel` / `__value`（hidden）；`data-search="1"` 模糊搜；`data-mode="multi"` 多选；`data-tree="leaf"` 叶节点单选；`data-tree="1"` 树多选。`ProtoPage.bindCombos` 自动绑 |
| 设置分组 | `md-set-group` `__title` `md-set-row`（**设置项**：当页当行直接操作；左 `md-icon` 可有可无 + `__label`；右开关/值/本行菜单）；开关 `md-switch`（热区铺满，可点）；无极 `md-set-block` + `md-slider--fluid`；横向多选 `md-set-picks` / `md-set-pick`（`__face` 可为 `__label` 文字 / 图标 / `__media` 图片；`__mark` 含 `__off`+`__on`，未选也显示空圈）；下拉 `md-set-row` + `data-menu` |
| 列表单行 | 仅在共享 `PT-MOBILE-LIST` 判定为单行时使用 `md-stack` > `md-set-row`；结构用 `__lead`（图标+`__label`）+ `__trail`（说明/计数/小标签，一般无箭头） |
| 功能区通栏 / 一行两个 | **功能入口**：通栏 `md-set-group`；一行两个 `md-set-pair`；右可为 `__hint` 或 **方形 `__thumb`**（`--thumb`，行更高）；常带箭头；**无圆角阴影卡片壳**；触屏**跟正文同左右安全距**，分割线内缩 |
| 汇总分页 | `md-d1__footer`：`md-d1__stats`（`md-d1__stats-num` 高亮条数）靠左；`md-d1__pager`（浅底条 + 每页 + 页码 + `md-pagination` 胶囊）靠右 |
| 列表开关列 | `md-col-switch` + `md-switch md-switch--compact`（标准列表某一列内直接操作） |
| 卡片列表操作 | `md-card--tile` 的 `md-card__head`（标题+右上角开关）/ `md-card__foot`（价格左、右下角 `md-card__actions` 按钮） |
| 纸面/表格 | `md-paper` `md-table` `md-table-wrap` `md-col-check` `md-col-name` `md-col-desc` `md-col-note` `md-col-price` `md-col-status` `md-col-date` `md-col-actions` `md-pagination` `md-page-btn` |
| 筛选栏 | `md-filter` / `md-d1__search`；动作区 `md-filter__actions` |
| 抽屉 | `md-drawer` `--left/--right/--bottom`；底 `__close`；底选项 `__opt` 或 `md-choice-group` 每项一行；`ProtoPage.openDrawer` |
| 轮播 / 金刚区 | `md-swiper` `md-king`（5 列图标文字上下同底、**无阴影**）`md-king--pair`（双卡靠左小图标+标题说明、**无阴影**；**信息多时用**；**不限首页**）`__name` `__desc`；沉浸式 `md-immersive` + `md-hero`；标准 `md-standard`；方形图标钮 `md-btn--stack` |
| 主操作条 | `md-action-bar`（无 TabBar 的提交/购买） |
| 触屏表单页壳 | `md-form-page`：浅灰 `#f7f7f7`；分区用白底 `md-module`（有内边距，组间露灰）；与详情/设置同色底 |
| 悬浮胶囊 | 位置、数量阈值与反馈执行共享 `PT-FLOAT`。触屏实现用页根 `md-pod` + 方位类并通过 `--md-pod-clearance` 避让底栏；桌面实现用 `md-pod md-pod--desk` + `fixed`，折叠态用 `md-pod--fold` + `__toggle`；文档内嵌加 `--static`；禁止 `md-fab` |
| 上传 | `md-upload` `md-upload--single` `md-upload-grid` `md-upload--file`（图/视频缩略默认可预览） |
| 滑动条 | `md-slider` `--steps` `--fluid` |
| 底半屏三级 | `data-wheel="date"` / `data-wheel="region"` / `data-wheel="daterange"` |
| 空态 | `md-empty md-empty--illus` + `__art` `__title` `__text` |
| 骨架 | `md-skeleton` `--text/--title/--media/--row`；`md-skel-host` |
| 步骤/树/图 | `md-stepper` `md-step` `md-tree` `md-chart-ph` `md-stat-grid` `md-stat-card` |
| 时间轴 | `md-timeline` `__item` `__rail` `__node` `__line` `__body`；右 **横卡文本** `md-card--row`（无左图，正文可 `__photos`）；`is-done` / `is-active` |
| 进步条 | `md-advance` `__label` `__value` `__track` `__seg` `__bar`；`data-segments`；`--lg`；`ProtoPage.setAdvance` |
| 进度条 | `md-progress` `__label` `__value` `__track` `__bar`；`--lg`；`--indeterminate`；`ProtoPage.setProgress` |
| Chip/Alert | `md-chip` `md-badge` `md-alert md-alert--error/--info/--success/--warning` |
| 状态组 | `md-toggle md-toggle--vert`（状态演示已内置） |
| 按钮组 | `md-btn-group` `md-btn-group--split` `md-d1__toolbar`（AD 功能栏平铺、无圆角阴影） |
| 下拉 | `md-field--select` `md-select` `md-select-btn` `md-menu` `md-menu__item`；触屏 ≤6 中间弹窗 / ≥7 底半屏 `md-select-sheet` |
| 日期时间 | `md-field--date` `md-field--daterange` `md-field--time` `md-cal` |
| 开关/单选/多选 | `md-switch` `md-switch-row` `md-radio` `md-check` `md-choice-group`；触屏表单标签角标，列表 `--list` 或行内圆/方 |
| 页内签 | `md-tabs md-tabs--page` `md-tab` `md-tab-panel` `md-tab-panels` `md-d1__workspace`；**平铺无卡片壳** |
| 弹窗/确认 | `md-dialog` `md-dialog--sm/--lg`；触屏紧内边距；**表单 `md-dialog__form` 单列一行一项**；底半屏 `md-drawer--bottom` + `__close`；`ProtoPage.openDialog` / `confirm` |
| 提示 | 触屏：居中 `md-snackbar--toast`（半透明黑底、白图标白字）；桌面：底部 `md-snackbar`；`md-tooltip` `data-tip` |

```html
<!-- 放在 .md-mobile-page 下，与 md-tabbar / md-action-bar 同级；不要放进 md-mobile-body -->
<nav class="md-pod md-pod--tl" aria-label="返回与分享">
  <button type="button" class="md-pod__item" aria-label="返回"><span class="md-icon" data-icon="chevron-left"></span></button>
  <button type="button" class="md-pod__item" aria-label="分享"><span class="md-icon" data-icon="share"></span></button>
</nav>
<nav class="md-pod md-pod--br" aria-label="收藏">
  <button type="button" class="md-pod__item" aria-label="收藏"><span class="md-icon" data-icon="favorite"></span></button>
</nav>
<!-- 桌面：放在 .md-d1 下；方位和折叠阈值见 PT-FLOAT -->
<nav class="md-pod md-pod--desk" aria-label="快捷操作">
  <button type="button" class="md-pod__item" aria-label="添加"><span class="md-icon" data-icon="add"></span></button>
  <button type="button" class="md-pod__item" aria-label="刷新"><span class="md-icon" data-icon="refresh"></span></button>
</nav>
<!-- PT-FLOAT 命中折叠态时写 md-pod--fold，最后一颗是 __toggle -->
<nav class="md-pod md-pod--desk md-pod--fold" aria-label="快捷操作">
  <button type="button" class="md-pod__item" aria-label="添加"><span class="md-icon" data-icon="add"></span></button>
  <button type="button" class="md-pod__item" aria-label="刷新"><span class="md-icon" data-icon="refresh"></span></button>
  <button type="button" class="md-pod__item" aria-label="筛选"><span class="md-icon" data-icon="filter"></span></button>
  <button type="button" class="md-pod__item" aria-label="分享"><span class="md-icon" data-icon="share"></span></button>
  <button type="button" class="md-pod__item md-pod__toggle" aria-label="展开快捷操作"><span class="md-icon" data-icon="add"></span></button>
</nav>
```
