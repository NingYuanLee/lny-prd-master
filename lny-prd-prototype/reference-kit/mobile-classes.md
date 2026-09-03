# 触屏单页类名（reference-kit 分片）
> 本文件是 `reference-kit.md` 的分片。索引与全局 token（圆角阴影 / 高保真落地 / 间距 / 滚动容器）见 [../reference-kit.md](../reference-kit.md)。

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

> **L2/L3 与 ② 对齐**：规格 L2 =【下沉首屏】（可选）+【滚动容器】；L3 = 滚动容器内的 `md-module`（普通 / 吸顶）。完整决策表见 `lny-prd-ui/reference/visual-rules.md` **§1.3.4**。

**A. 下沉式首页（Hero 钉底 + sheet 滚过）** — `gold/mobile-grid.html`

```html
<div class="md-mobile-page md-mp md-immersive">
  <!-- L2【下沉首屏】：与 md-mobile-body 同级，勿放进 sheet -->
  <div class="md-hero">
    <div class="md-swiper">…Banner 下沉…</div>
  </div>
  <!-- L2【滚动容器】 -->
  <main class="md-mobile-body">
    <div class="md-mobile-sheet">
      <section class="md-module">…L3 普通模块…</section>
    </div>
  </main>
  <nav class="md-tabbar">…</nav>
</div>
```

**B. 无下沉 / 随滚 Banner** — 页根 **不要** 并列 `md-hero`；Banner 放在 sheet 内第一个 `md-module`：

```html
<div class="md-mobile-page md-mp md-standard">
  <main class="md-mobile-body">
    <div class="md-mobile-sheet">
      <section class="md-module">
        <div class="md-swiper">…Banner 随内容滚…</div>
      </section>
      <section class="md-module">…</section>
    </div>
  </main>
</div>
```

**C. 列表页（L1 固定工具条在 body 外）** — `gold/mobile-list.html`

```html
<div class="md-mobile-page md-mp md-standard">
  <header class="md-appbar md-appbar--mobile md-appbar--center">…</header>
  <div class="md-list-toolbar">…搜索+筛选+页内签…</div>
  <main class="md-mobile-body">
    <div class="md-mobile-sheet">…仅 L3 列表模块…</div>
  </main>
  <nav class="md-tabbar">…</nav>
</div>
```

**D. L3 吸顶模块（规格点名时）** — 模块在 `md-mobile-body` / sheet **内**，滚过锚点后 sticky；顶距须 ≥ L1 固定区高度（若上方还有 overlay 顶栏一并计入）：

```html
<section class="md-module md-module--sticky" style="top: var(--md-sticky-top, 0px)">
  …页内二级 Tab / 章节签…
</section>
```

（`md-module--sticky` 为语义类名；实现为 `position: sticky` + 正确 `top`。当前金样以 L1 固定工具条为主，吸顶模块按规格补页。）

**下沉式完整示例（宫格首页）**

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
          <article class="md-card md-card--tile">…</article>
        </div>
      </section>
    </div>
  </main>
  <nav class="md-tabbar">…</nav>
</div>
```

有 TabBar 时 **不用**返回型顶栏（`md-appbar--mobile` 带返回钮）；可用 **`md-appbar--center`** 居中标题，或 **不写 `md-appbar`** 改由 `md-hero` / `md-list-toolbar` / 金刚区等自定义顶区。**沉浸式（L0）≠ 必下沉**：仅规格写 L2【下沉首屏】时用 **`md-immersive` + 页级 `md-hero`**；Hero **绝对定位钉底层、不随滚**；`md-mobile-body` 内 **必须** `md-mobile-sheet`，白底滚过盖住 Banner；顶距由 `::before` 占位露图并可点穿轮播。CSS 选择器：`.md-mobile-page.md-immersive:has(> .md-hero)`。**随滚 Banner** 禁止页级 `md-hero`，见上文 **B**。详情 **`md-appbar--overlay`** 叠在 16:9 主图上，滚正文后 **`is-solid`** 变纯色顶栏（`proto-page.js` 自动绑定）。**L3 模块**：每个分区包 `md-module`；`--md-module-gap`（16px）统一间距；分区头在模块内。**L1 固定**（`md-list-toolbar` 等）在 `md-mobile-body` **外**，与 **L3 吸顶**（body 内 sticky）勿混。**列表卡点名一种**（见下节）。详情主图 `md-swiper--wide`（16:9）；介绍配图 `md-media--16x9`。触屏正文 `--md-safe-*`；标准顶栏左右 4px；overlay/cover 避让胶囊。`md-search` 仅左图标+输入。半屏 `md-drawer--left/bottom/right`。`<meta viewport>` 须 `viewport-fit=cover`。**禁止**手写 `md-status-bar`（`proto-page.js` 注入）。页根 **`md-immersive`** 或 **`md-standard`**。

### 触屏列表区

同一模块只选一种（分区可各自点名）。规格有字段才写对应节点，禁止为好看编造业务字段。单行/多行选择直接执行共享 `PT-MOBILE-LIST`；该规则命中“字段少但值长”的多行分支时加 `md-card--long`，标题/摘要字号略大。**触屏列表卡高度随内容**，禁止给卡片或 `__body` 设 `min-height`（左图/图标位仍固定尺寸）。

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

**③·订单横卡** `md-card--order`：电商订单列表专用（金样 `mobile-order-list.html` / 夹具 PAGE-MP-014）。可选 `md-order-card__promo` 推广条；`__head` 店头（店名+`chevron-right`+徽标+状态）；`__body` 多行商品价量；`__foot` 实付款；`__actions` 浅底操作条（「更多」靠左，其余 `md-btn--soft` 靠右）。顶栏 **返回+搜索** + **下划线页签+筛选**（`md-list-toolbar` 在 body 外）。

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

**④ 横卡单行**（列表区内容行）`md-set-row`：定高、不换行；左图标→标题；右说明/计数/小标签。最多 3 个**短**字段；**任一字段值很长（单行放不下）改走横卡多行 + `md-card--long`**。**每行独立纸面，上下有缝**（放进 `md-stack`，**不要**包进 `md-set-group`）。列表区与功能区的差别：**列表非分组**，条目可无限（即便分页加载，叠在一起也看不出页边界）；**功能成组**，每组入口有限。视觉上：通栏挤在一组纸面里、行间只有分割线；列表单行各自独立有缝。列表卡（封面/双列/横卡多行/单行/订单）统一用 **轻阴影** `--md-shadow-surface`；**高度随内容**，禁止 `min-height`。**功能区**（通栏 / 一行两个 / 金刚）与 **页内签**：**不要**圆角阴影卡片壳（平铺即可）。**不要**用 `md-set-pair` 冒充列表。

**⑤ 父子章节列表** `md-chapter-list`（`PT-LOCATOR` 触屏专形；金样 `gold/mobile-chapter-list.html`；夹具 `PAGE-MP-015`）：每组 `__group` 含 `__head`（**toggle 展开/收起** + 父章 `__parent`）与 `__body`（子章 `__child`）。父章加粗，子章缩进+圆点。**不是**维护树、**不是**横卡、**不是** MP-013 split。可整页目录或模块内列表。

**与 `md-tree` 何时用**：见 [`../lny-prd-master/reference-page-types.md`](../../lny-prd-master/reference-page-types.md) **「树 vs 章节列表选型」**。一句话：**章/节/大纲导航** → `md-chapter-list`；**分类/组织/权限层级数据**（点节点换右区或维护）→ `md-tree`；**左分组右横卡滚联动** → `md-locator`。

```html
<div class="md-chapter-list__group is-open">
  <div class="md-chapter-list__head">
    <button type="button" class="md-chapter-list__toggle md-icon-btn" aria-expanded="true" aria-label="收起子章节">
      <span class="md-icon" data-icon="chevron-right"></span>
    </button>
    <a class="md-chapter-list__parent" href="#ch1">第一章 概述</a>
  </div>
  <div class="md-chapter-list__body">
    <a class="md-chapter-list__child" href="#ch1-1">1.1 背景</a>
  </div>
</div>
```

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

形态选型执行共享 **`PT-MOBILE-FUNC`**（详表见 `lny-prd-ui/reference/visual-rules.md` **§1.3.6**）。摘要：

| 形态 | 要点 |
|------|------|
| 宫格 `md-king` | ≥5 个或极短标签一行扫视；4/5 列与个数对齐 |
| 双卡 `md-king--pair` | 标题+说明；或**无列表**时填实视口 |
| 宫格+双卡 | 多层级入口（金样 MP-001） |
| 通栏 / 一行两个 | 2～4 轻入口、服务页气质；信息少→`md-set-pair`，菜单式→通栏 |

**禁止**：因首页默认宫格；因 4 个入口机械 4 列；**砍掉列表后**仍留稀疏宫格——改双卡或宫格+双卡。

金刚宫格 `md-king`（4/5 列）/ 金刚双卡 `md-king--pair` / **服务条 `md-svc-strip`**（2/3/4 等分一整块、项间**不贯通**短竖线、图标文字上下居中）/ 通栏 `md-set-row` / 一行两个 `md-set-pair`。**金刚不限首页**。通栏与一行两个的 **分组标题可有可无**。通栏包在 `md-set-group` 里连成一片；组内用 **淡色内缩分割线**（`--md-divider-soft`，左右仍留距）。**触屏功能区跟正文同左右安全距**（通栏/一行两个/金刚不要负边距贴手机框）。**设置项与功能入口同壳**：设置项在当前行直接操作（开关等）；功能入口只跳转或开半屏/弹窗（常带右箭头）。**功能区**与 **页内签**：**不要**圆角、轻阴影卡片壳。**我的 / 设置** 页根加 **`md-set-page`**（浅灰 `#f7f7f7` 同详情），组与组靠外边距/gap 漏底。列表单行是内容、独立有缝、一般不带箭头；数据流可无限。金样：宫格+双卡+列表见 `gold/mobile-grid.html`，通栏/一行两个见 `gold/mobile-menu.html`，设置见 `gold/mobile-settings.html`。

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

触屏顶栏六种（规格点名一种；**有 TabBar 时不用返回型顶栏**，可用 L2 居中标题或 L1 自定义顶区；**左上悬浮胶囊与页内顶栏互斥**）：

| # | 形态 | 用法 | 金样 |
|---|------|------|------|
| L1 | 底 TabBar + **无**标题栏 + 自定义顶区 | `md-hero` / `md-list-toolbar`（搜索+筛选+页签）/ 金刚区等；正文自定 | `gold/mobile-grid.html`；列表工具条见 `mobile-list.html` |
| L2 | 底 TabBar + 标题栏（**无返回** + **标题居中**） | `md-appbar md-appbar--mobile md-appbar--center`；其下可再接 `md-list-toolbar` 等 | `gold/mobile-list.html` |
| L3 | **透明叠图**顶栏 + 沉浸式正文 | `md-immersive` + `md-appbar--overlay` + `md-hero`/`md-swiper--wide`；半透明返回 + **标题靠左**；滚正文后 **`is-solid`** 变纯色 | `gold/mobile-detail.html` |
| L4 | **无**标题栏 + **左上悬浮胶囊** + 沉浸式正文 | 页根 `md-pod--tl`（与 L2/L5 互斥）；`md-hero` + `md-mobile-sheet` | `gold/mobile-pod.html` |
| L5 | **标准**标题栏 | `md-standard` + `md-appbar md-appbar--mobile`；纯色底 + **返回** + **标题靠左** | `gold/mobile-form.html`、`gold/mobile-menu.html` |
| L6 | **双层高**封面顶栏 | `md-immersive` + `md-appbar--cover` + `md-appbar__cover`；高度约 **2×** 标准栏；**标题与返回靠下缘靠左**（返回可选） | `gold/mobile-settings.html` |

```html
<!-- L2 居中标题（TabBar 页常用） -->
<header class="md-appbar md-appbar--mobile md-appbar--center">
  <h1 class="md-appbar__title">在售商品</h1>
</header>
<!-- 列表工具条：搜索与筛选图标同一行；筛选改条件后 md-search-row__filter 高亮 -->
<form class="md-search-row">
  <label class="md-search">…</label>
  <button type="button" class="md-icon-btn md-search-row__filter" data-filter-drawer="filterSheet" aria-label="筛选">…</button>
</form>

<!-- L3 透明叠图（滚正文后 is-solid） -->
<header class="md-appbar md-appbar--mobile md-appbar--overlay">
  <a class="md-icon-btn" href="#" aria-label="返回"><span class="md-icon" data-icon="chevron-left"></span></a>
  <h1 class="md-appbar__title">商品详情</h1>
</header>

<!-- L5 标准 -->
<header class="md-appbar md-appbar--mobile">
  <a class="md-icon-btn" href="#" aria-label="返回"><span class="md-icon" data-icon="back"></span></a>
  <h1 class="md-appbar__title">编辑资料</h1>
</header>
```

```html
<header class="md-appbar md-appbar--mobile md-appbar--cover">
  <div class="md-appbar__cover md-media-ph md-media-ph--2" aria-hidden="true"></div>
  <a class="md-icon-btn" href="#" aria-label="返回"><span class="md-icon" data-icon="back"></span></a>
  <h1 class="md-appbar__title">设置</h1>
</header>
```

禁止：有 TabBar 又写 L5 返回顶栏；L4 左上胶囊与 L2/L5/L6 页内顶栏同页并存；L3 不写 `md-immersive` 或漏绑滚动变实底；把 L6 封面顶栏拉成 16:9 Hero。

金刚区选型见 **`PT-MOBILE-FUNC`**（§1.3.6）：≥5 或极短标签→4/5 列宫格；标题+说明或无列表填实→`md-king--pair` 双卡（小图标与文案均靠左；**外层 `padding:0`**，块间距靠父级 `md-module`/`md-mobile-sheet` 的 `gap`，内距只在 `md-king__item`）：

```html
<nav class="md-king md-king--pair">
  <button type="button" class="md-king__item">
    <span class="md-king__icon"><span class="md-icon" data-icon="goods" aria-hidden="true"></span></span>
    <span class="md-king__name">时令鲜果</span>
    <span class="md-king__desc">当季直达</span>
  </button>
</nav>
```

**服务条 `md-svc-strip`**（我的/服务页、**桌面常用功能**）：**一整块白底**，一排 **2 / 3 / 4 / 5 / 6** 个入口等分；项间 **不贯通** 的细竖线；每项 **上区图标或统计数值 + 下区文字**，上下居中。上区二选一：`__icon`（图标，可挂 **`__badge` 数字角标**）或 **`__value`**（统计数值，可挂可点 **`__help` 问号** 看说明弹窗，`data-svc-help-title` / `data-svc-help`）；金额等较长可用 `__value--sm`。桌面 **`md-set-page`** 下可直接放 `<nav class="md-svc-strip md-svc-strip--desk md-svc-strip--cols-4">`（与 `md-set-group` 并列，浅灰底漏间距）；触屏包在 `md-module` 内。桌面修饰符 **`--desk`** 略增高、去掉按压缩放。

```html
<nav class="md-svc-strip md-svc-strip--cols-4" aria-label="常用服务">
  <a class="md-svc-strip__item" href="#">
    <span class="md-svc-strip__icon">
      <span class="md-icon" data-icon="goods" aria-hidden="true"></span>
      <span class="md-svc-strip__badge">2</span>
    </span>
    <span class="md-svc-strip__label">待付款</span>
  </a>
  <a class="md-svc-strip__item" href="#">
    <span class="md-svc-strip__value">
      1,280
      <button type="button" class="md-svc-strip__help" aria-label="积分说明"
        data-svc-help-title="积分说明" data-svc-help="100 积分抵 1 元。">?</button>
    </span>
    <span class="md-svc-strip__label">积分</span>
  </a>
  <!-- 2～4 项；修饰符 --cols-2 / --cols-3 / --cols-4 -->
</nav>
```

禁止：把服务条写成 `md-king` 多列宫格；项间拉满高度的竖线；入口左对齐（须整体居中）；每项单独圆角阴影底；统计数值与图标同项叠放；角标可点（须 `pointer-events: none`）；问号说明用 Toast 代替弹窗。

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

自定义状态（例如业务明确需要的 `pending`）不得只增加一个状态按钮；必须在页面提供对应视觉块并标记：`<div class="is-hidden" data-state-for="COMP-001" data-state="pending">…</div>`。脚本会在切态时只显示匹配状态。无视觉差异的状态（如把 `edit`、`disabled` 当作泛化枚举）不得加入状态演示。

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

抽屉：`ProtoPage.openDrawer(id)` / `closeDrawer(id)`，遮罩 id 为 `{id}Backdrop`。**触屏抽屉内** `md-field` / 底栏 `md-drawer__actions` 按钮自动用表单页密度（约 40px 输入、34px 按钮；抽屉常在页根外，勿依赖页内 `md-field--sm` 才变矮）。**底半屏** `md-drawer--bottom`：高度随内容、最大 **70vh**，超出时 `__body` 滚动；关闭钮 `md-drawer__close` 在面板右上角（`openDrawer` / 页初始化会自动补，轮盘 `md-wheel` 除外）。**底半屏放选项时每项独占一行**（`md-drawer__opt` / `md-choice-group` / `md-set-picks` / 下拉 `md-select-sheet__opt`），不要用表单标签换行。

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
