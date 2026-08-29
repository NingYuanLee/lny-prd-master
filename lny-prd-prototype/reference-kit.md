# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角/阴影见下节 token、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。

## 圆角与阴影 token（套件 / 金样 / 夹具统一）

**禁止**在业务页 HTML 内联 `border-radius` / `box-shadow` 硬编码 px；一律用 `mui-kit.css` 变量。

| 圆角 token | 值 | 典型用途 |
|------------|-----|----------|
| `--md-radius-xs` | 2px | 勾选框、进度条轨道、细条 |
| `--md-radius-sm` / `--md-radius` | 4px | **默认**：卡片、按钮、字段、模块 |
| `--md-radius-md` | 8px | 缩略图、媒体、角标折角（`--md-radius-tag-br/bl`） |
| `--md-radius-lg` | 12px | 标签容器、资料头像圆角矩形 |
| `--md-radius-xl` | 16px | 半屏抽屉顶角（`--md-radius-sheet-top`） |
| `--md-radius-2xl` | 20px | 搜索条等大圆角输入 |
| `--md-radius-pill` | 999px | 胶囊、角标 |
| `--md-radius-circle` | 50% | 头像、圆点 |
| `--md-radius-dialog` | 8px（=`--md-radius-md`） | **弹窗主体**（`md-dialog`、触屏 ≤6 项中间选项弹窗）统一圆角 |

| 阴影 token | 用途 |
|------------|------|
| `--md-shadow-dialog` | **弹窗主体**统一 elevation（=`--md-shadow-24`）；`md-dialog` / 中间选项弹窗同阴影 |
| `--md-shadow-surface` | **列表卡**统一轻阴影（封面/横卡/双列等） |
| `--md-shadow-1` … `--md-shadow-24` | MUI elevation（按钮 hover、浮层等） |
| `--md-shadow-right` / `--md-shadow-left` | 冻结列、侧栏等**方向性**阴影 |
| `--md-shadow-edge-top` / `--md-shadow-edge-bottom` | 顶/底 1px 分隔阴影 |
| `--md-shadow-focus*` | 焦点环（按钮、时间轴节点等） |
| `--md-shadow-tab-active` | 页内签选中轻阴影 |
| `--proto-shadow-phone` | 汇总壳手机框（`proto-shell.css`） |

功能区（通栏 / 一行两个 / 页内签 / 金刚）与资料卡默认：**无圆角、无卡片阴影**（平铺）。列表卡与评论条目：**`--md-shadow-surface` + `--md-radius-sm`**。

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
| 移动端 | 状态栏由 `proto-page.js` 固定顶注入；页根须标 `md-immersive` 或 `md-standard`；**列表/详情等多模块页**在须区分分区时用 `md-section-head`（产品文案如「精选」「评论」）；**金刚/通栏/服务条等功能区默认无 `md-section-head`**（见 `gold/mobile-grid.html` / `mobile-menu.html`；§1.3.5）。**列表区** `md-card--cover` / `--tile` / `--row`（多行，可无左图+小图）/ `md-set-row`（单行）；**功能区** `md-king` / `--pair` / `md-set-row` 通栏 / `md-set-pair`；触屏 `md-search` 仅左图标+输入；`viewport-fit=cover`；正文左右下走 `--md-safe-*`；标准顶栏左右 4px |
| 桌面端 | 必须有 `md-breadcrumb`（内容区顶部，不要 `md-page-head` 大标题）；表格首列可用 `md-row-goods` + `md-thumb md-media-ph--n`。D1-1 的冻结、操作阈值、语义列宽、紧凑密度和底部对齐直接执行共享 `PT-DESKTOP-LIST`：根用 `md-d1--list`，列用对应 `md-col-*`，更多菜单用 `md-actions` + `data-menu`，汇总/分页用 `md-d1__stats` / `md-d1__pager`。触屏弹窗/半屏内边距收紧；底半屏高度随内容、最大 70vh、超出正文滚动、关闭钮在面板右上角（`md-drawer__close`）。规格出现的弹窗/签/下拉/日期/按钮组必须用本节 AD 控件，禁止裸 `alert` / 无样式 `<select>` |
| 间距 | 触屏走 **§触屏间距三层联动** + **§滚动容器底与边**：滚动区基础 padding/背景只在 L2 承担一次；父级 `gap` 定兄弟节奏；块 seam 边不重复叠 padding/margin；块内 content padding 写在 `__item`/`__body` |

## 触屏间距三层联动（间距预算）

写触屏页时，**父级 gap、兄弟 margin、自身 padding** 只选一层承担「块与块之间」的缝，避免叠成 24～28px 的大空白。

| 层 | 负责什么 | 典型 token / 类 | 规则 |
|----|----------|-----------------|------|
| **L1 父级弹性 gap** | 兄弟块之间的默认节奏 | `md-mobile-sheet` / `md-mobile-body` → `--md-module-gap`（**12px**）；`md-module` → `--md-space`（8px）；`md-list-toolbar` → `--md-space` | **不轻易为单个块改父 gap**（会影响其它无内边距 sibling） |
| **L2 兄弟外边距** | 非 flex、或需负补偿时偶用 | `margin-top` / `margin-bottom` | 父已有 `gap` 时 **禁止** sibling 再叠上下 margin |
| **L3 块 padding** | 块内触控区、文字缩进 | `md-king__item`、`md-set-row` 行内距等 | **seam 边**（顶/底朝向相邻兄弟）**不**重复 L1；只给 **content** 留 padding |

**间距预算**（兄弟 A、B 之间的视觉缝）：

```text
缝 ≈ parent.gap + A.padding-bottom + B.padding-top + A.margin-bottom + B.margin-top
```

目标：≈ **一个节奏单位**（8 或 16px），不要叠成双倍。

**决策顺序**

1. 找最近的 **flex 列父级**及其 `gap`。
2. 标记每个直接子块：seam 方向有无上下 padding/margin。
3. **混合 sibling**（有的有 padding、有的无）→ **保留父 gap**，去掉有 padding 块在 seam 方向的上下 padding（**不要**动父 gap）。
4. **全部 sibling 都要块级外距且要露底**（如 `md-set-page` 浅灰分组）→ 可减父 gap，改靠组外边距/gap 漏底。
5. 仅需 **块内** 呼吸 → padding 写在 `__item` / `__body`，外层 `nav`/`section` seam 边为 0。

**正反例**

| 场景 | 做法 |
|------|------|
| ✅ 首页专题入口 | `md-mobile-sheet { gap:12px }` + `md-module` + `md-king--pair { padding:0 }` + `md-king__item { padding:14px 16px }` |
| ❌ 叠缝 | sheet `gap:16px` **且** `md-king--pair { padding:4px 0 12px }` → 缝 20～28px |
| ✅ 列表工具条 | 搜索行/tab  seam 边无 padding → 父 `md-list-toolbar { gap:8px }` |
| ✅ 模块内标题+列表 | `md-module { gap:8px }`；`md-section-head` 无额外上下 margin |

金样：`gold/mobile-grid.html`（专题 `md-king--pair`）、`gold/mobile-list.html`（`md-list-toolbar`）。

## 滚动容器底与边（L2 统一）

**原则**：全页滚动区 **只在一层** 写基础内边距 + 基础背景色；`md-module` 只管块内 content padding，**不要**每个模块各自叠页级 safe 或整页白/灰底。

| 场景 | 承担层 | 背景 | 内边距（套件默认） | 模块 |
|------|--------|------|-------------------|------|
| **body（纯滚动壳）** | `md-mobile-body` | **透明** | **0** | 只负责 overflow，不承担 safe |
| **sheet（默认）** | `md-mobile-sheet` | **浅灰** `#f7f7f7` | 上 **12**；**左右 safe 12**；下 12 + 底安全区；`gap` **12** | 白底块在 `md-module` / 卡片内 |
| **sheet 贴边** | `md-mobile-sheet--flush-x` | 浅灰 | **左右 0**（上下仍统一） | 详情/表单/设置/树等白块通栏 |
| **下沉滚过** | 同上 sheet | 浅灰 | 同上 | Hero 在 body 外同级 |

```text
body：    md-mobile-body          透明 + padding 0（纯滚动）
sheet：   md-mobile-sheet         浅灰 #f7f7f7 + 统一上下/左右内边距（默认左右有 safe）
贴边：    md-mobile-sheet--flush-x  左右 padding 0（详情/表单/设置/树）
模块：    md-module / 卡片        白底内容；块内 safe 写在 module（贴边 sheet 时）
```

**禁止**：body 与 sheet 同时叠 safe；贴边页忘记 `--flush-x` 又在 module 外留 safe。

### 何时有 sheet、何时没有

| 位置 | sheet？ | DOM 位置 |
|------|---------|----------|
| **L2 滚动主内容** | **必须有** | `md-mobile-body` 的 **唯一** 直接子节点 → `md-mobile-sheet` → L3 |
| **L1 固定**（顶栏/搜索筛选/TabBar/贴底条） | **没有** | 页根下与 `md-mobile-body` **并列** |
| **L2 下沉 Hero** | **没有** | 页根下与 `md-mobile-body` **并列**的 `md-hero` |
| **L5 浮层** | **没有** | 页根级 drawer/dialog/toast |

**一种页只有一个 sheet**；禁止 body 里嵌套多层 sheet，禁止 sheet 里再套 Hero。

**sheet 修饰**（都有 sheet，只变左右 safe）：

| 类名 | 左右 safe | 用于 |
|------|-----------|------|
| `md-mobile-sheet` | 默认 **有** | 列表、按钮、时间轴、下沉首页 |
| `md-mobile-sheet--flush-x` | **无** | 详情/字段详情/树（或页根 `md-detail-page` 等自动 lr0） |
| `+ md-detail-content` | **无** | 详情语义壳，等价 flush-x |

**无 sheet 的旧 HTML** 不再推荐；`body` 已无默认 padding/灰底，缺 sheet 会丢滚动区样式。

**② 页型选型**（列表型 vs 浅灰壳、何时改页型、详情评论 hybrid）：见 [`lny-prd-ui/reference.md`](../lny-prd-ui/reference.md) §1.3.4「滚动区页型选型」；② 写 L2 时引用，⑥ 按选型落 sheet 修饰类。

**触屏金样 DOM 纪律**：14 个 `mobile-*.html` **全部** `body` > `sheet`；⑥ 新页照抄。改 `kit/` 后须对业务根 `prototypes/{终端}/` 执行 `copy-kit.py`（或 **`sync-mp-sheet-fixtures.py`** 一键同步 MP+AD 夹具注释与 kit）。对照 **`verify-fixture-gold-parity.py`** 确认 14×MP + 14×AD 夹具与金样文件齐套。

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`proto-map.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。禁止改 kit 源文件来迁就某一页，也禁止将套件副本写到 `versions/{v}/prototypes/`。禁止生成 `serve.json`。本地预览：在 `prototypes/` 目录执行 `python -m http.server`。

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

> **L2/L3 与 ② 对齐**：规格 L2 =【下沉首屏】（可选）+【滚动容器】；L3 = 滚动容器内的 `md-module`（普通 / 吸顶）。完整决策表见 `lny-prd-ui/reference.md` **§1.3.4**。

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

**与 `md-tree` 何时用**：见 [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md) **「树 vs 章节列表选型」**。一句话：**章/节/大纲导航** → `md-chapter-list`；**分类/组织/权限层级数据**（点节点换右区或维护）→ `md-tree`；**左分组右横卡滚联动** → `md-locator`。

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

形态选型执行共享 **`PT-MOBILE-FUNC`**（详表见 `lny-prd-ui/reference.md` **§1.3.6**）。摘要：

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

**只读 / 禁用输入**（**视觉一致**，金样只保留一项：`md-field--readonly` + `readonly` 或 `disabled` 均可；灰底 `#eee`、标签缺口同色灰底、淡字。日期段触发器的 `readonly` 不要套 `md-field--readonly`）

```html
<label class="md-field md-field--readonly">
  <span class="md-field__label">只读/禁用</span>
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

触屏按钮对照金样 `gold/mobile-buttons.html`：小 `--sm` / 中默认 / 大 `--lg`；形态含线框 `--outlined`、色块 `--contained`、**浅底 `--soft`（无边框、浅色底+有色字）**、文字 `--text`、**纯文字链接 `--link`（无线框无背景，用于查看更多/了解全部；字色须区别紧邻正文，默认主色）**、置灰 `disabled`、角标内嵌 `md-badge`。

```html
<button type="button" class="md-btn md-btn--outlined md-btn--sm">线框</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">色块</button>
<button type="button" class="md-btn md-btn--soft md-btn--sm">浅底</button>
<button type="button" class="md-btn md-btn--outlined md-btn--sm" disabled>线框置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm" disabled>色块置灰</button>
<button type="button" class="md-btn md-btn--contained md-btn--sm">角标<span class="md-badge">8</span></button>
```

功能区通栏 / 一行两个对照金样 `gold/mobile-menu.html` / `gold/desktop-menu.html`。桌面宽屏用 **`md-set-grid--cols-2/3/4`** 包多列 `md-set-row`；触屏仍通栏 / `md-set-pair`。分组标题可无。短说明可省略，通栏箭头保留。**右侧说明位也可换成方形配图**：`md-set-row--thumb` + `__thumb`（1:1，约 52px），行高随之加高；有图时不再叠文字 `__hint`。字段多改列表区横卡多行。

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

**进步条** `md-advance`：分段分布；作**向导导航**时与数字步骤**二选一**（触屏三选一含无极进度），**只展示**完成段，**不可点击**切换步，靠上一步/下一步。`data-segments` 默认 4（2–12）。`ProtoPage.setAdvance` 按百分比填已完成段、当前段余量、其余留空。缺 `__seg` 时脚本按 `data-segments` 补齐。触屏可用 `md-advance--lg`。

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

**时间轴** `md-timeline`：`__item` + `__rail`（`__node` + `__line`）+ `__body`。`is-done` 已完成、`is-active` 当前（外圈高亮）、`is-origin` 起点（空心圆）、`is-path` 途经小圆点。**物流/进度只读页**（触屏与桌面）统一 `md-timeline--static`：**仅展示已发生节点**（禁止占位未发生节点、禁止灰色「待完成」竖轨）；倒序（最新在上、起点在下）；竖线全程主色；当前实心+外圈，途经小圆点，起点底部空心。**可交互章节导航**（点选滚锚点、滚正文高亮）走 `desktop-locator.html` / `mobile-locator.html`，**禁止**在时间轴页演示可点切换进度以免与物流轴混淆。

- **触屏 / 桌面**：右侧 `__body` 用 `md-card--row` **横卡文本**（**禁止左图**）；正文内可选 `md-card__photos` + `md-card__photo` 多张小图。金样 `gold/mobile-timeline.html` / `gold/desktop-timeline.html`。桌面不要左右分栏，章节大纲才走 `desktop-locator.html`。

## 无类名组合（禁止裸 HTML）

套件没有「一模一样」的控件时，**必须**用下表组合，禁止自造 class、禁止无 `md-*` 的 `<button>` / `<input>` / `<table>`、禁止用随机色块当图。

| 规格里出现 | 必须用 | 禁止 |
|------------|--------|------|
| 筛选 / 搜索栏 | `md-filter` 或 `md-d1__search` | 无 class 的 `<form>`；筛选区 label / 输入字号更小（套件已收紧） |
| 侧滑 / 抽屉 | `md-drawer md-drawer--left/right/bottom` + `md-backdrop`；底半屏高度随内容、最大 70vh、`__close` 右上角；选项用 `__opt` / `md-choice-group` 且每项一行 | 自造 `position:fixed` 面板；`display` 瞬切；底半屏定死全高或关闭钮只放底栏；底半屏选项标签换行挤一行 |
| 轮播 Banner | `md-swiper` + `__track` + `__slide` + `__dots` | 自造横向滚动无指示点 |
| 金刚区 | `md-king`（4/5 列：图标+文字上下居中同底）；或 `md-king--pair`（一排两张大卡，小图标与 `__name`/`__desc` 均靠左）。按 **`PT-MOBILE-FUNC`** 选型；**不限首页** | 图标单独色块、文字露在底外；无热区的纯文字宫格；双卡内容居中；4 个入口机械 4 列；把双卡和一行两个按是否首页选型；砍掉列表后仍留稀疏宫格 |
| 服务条 | `md-svc-strip` + `__item` + `__icon`/`__value` + `__label`；图标可挂 **`__badge`**；数值可挂 **`__help`**（`data-svc-help*` 弹窗说明）；修饰符 `--cols-2/3/4/5/6`；桌面 **`--desk`** | 冒充 `md-king`；贯通竖线；项独立圆角灰底；同项既图标又数值；角标可点 |
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
| 步骤向导 | 数字 `md-stepper` **或** 分段 `md-advance` **或** 无极 `md-progress`（三选一，禁止同页叠加）；**仅 stepper 可点跳步** | 同页叠 stepper + advance；advance/progress 可点切换 |
| 定位导航 | `md-locator` `--cats` / `--outline`；`md-locator__item--l2` 子章缩进；触屏整页 **`md-chapter-list`**（`__parent`/`__child`/`__group`）；左栏 `md-split--outline` 可收缩为点线轨；右悬浮 `md-locator-float` 收起同样变点线轨；滚正文时当前章 `is-active` 联动 | 用 `md-tree` 冒充分类钮；用分类冒充可展开树；章节列表画成横卡或树 |
| 树 | 不分页 `md-tree` + `__item` `__toggle` `__label`；总控 `md-tree-bar`（左 **根节点**、右 **展开/收起切换** `data-tree-act="toggle-all"`，`unfold`/`fold` 随态）；节点 `__ops`（增子/重命名/删除）；拖放 `上/中/下`；表内 `md-table--nest`。只读 `data-tree-edit="off"`；末级禁增 `data-leaf` / `data-leaf-add="off"` | 无类名嵌套 `ul`；用分类定位冒充树；触屏用列表硬套分类树 |
| 步骤条 | `md-stepper` + `md-step`；已完成 `is-done`；当前 `is-active`。**唯一可点跳步**的向导导航（`proto-page.js` 自动绑）；自管步进写 `data-wizard="off"`。**不与 `md-advance` 同页** | 纯数字列表；与分段进步条同屏叠加 |
| 进步条 | `md-advance` + `__head` + `__track` + `__seg` + `__bar`；`data-segments`；触屏可 `--lg`；向导时 **只展示**（`data-wizard-host`）。**不与 `md-stepper` 同页** | 用无极 `md-progress` 冒充分步；段可点跳步 |
| 进度条 | `md-progress` + `__head` + `__track` + `__bar`；不确定 `--indeterminate`；触屏可 `--lg`；向导时 **只展示** | 裸 `<progress>` / 自造色条 / 用分段 `md-advance` 冒充上传 / 进度条可点跳步 |
| 时间轴 | `md-timeline` + `__item` `__rail` `__node` `__line` `__body`；右 **横卡文本** `md-card--row`（无左图，正文可 `__photos`）；`is-done` / `is-active` | 用列表硬套竖轨；时间轴右卡加左图；桌面做成左右分栏导航 |
| 图表 | `md-chart-ph` 占位条 | 手写 canvas / 自造柱 |
| 页内分页签 | 桌面：`md-tabs md-tabs--page` 下划线（**平铺，无圆角阴影卡片壳**）；触屏：`md-tabs`（自动按钮组，浅底/选中色块） | 触屏用桌面下划线签；自造下划线 `div` / 裸 `<a>` 签；页内签套卡片壳 |
| 主/线/浅底/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / **`--soft`（无边框浅底色字）** / `--text` / `--link`；**通栏整行** `--block`（或 `md-btn-row` 竖叠）；图标钮 `md-icon-btn`。触屏贴底 `md-action-bar` / 半屏 `md-drawer__actions` **仅一钮时自动占满** | 裸 `<button>`、`<input type="submit">`、Bootstrap/`btn`、浏览器灰钮；一行一主钮却缩成短条 |
| 悬浮胶囊 / 桌面悬浮按钮 | 形态与阈值执行共享 `PT-FLOAT`；触屏用 `md-pod` 方位类，桌面用 `md-pod--desk`，折叠用 `md-pod--fold` + `__toggle` | 写进滚动层；违反共享方位；用 `md-fab` 冒充；功能钮缩放回弹 |
| 按钮组 / 工具栏按钮 | `md-btn-group` / `md-d1__toolbar`（功能栏**平铺，无圆角阴影**；保留内边距；块间间距优先靠各块 `padding`，不够再父级 `gap`） | 无 class 的一排 `<button>`；功能栏套卡片壳 |
| 下拉 | 少选项：`md-field--select` + `md-select`；多选/搜索/树：`md-field--combo` + `md-combo`（`data-mode="multi"` / `data-search="1"` / `data-tree="leaf|1"`）；菜单：`md-select-btn` + `md-menu` | 未包 `md-field` 的裸 `<select>`；触屏用系统原生选择器；自造 autocomplete 面板 |
| 日期 / 时间 | `md-field--date` / `md-field--daterange` / `md-field--time` + `type="date|time|datetime-local"` | 自造日历、两个裸日期框冒充日期段 |
| 开关 | `md-switch-row` + `md-switch` | 自造滑块 / 裸 checkbox 当开关 |
| 功能区通栏 / 一行两个 | 通栏包 `md-set-group`；触屏单列通栏 / `md-set-pair` 一行两个。桌面 **`md-d1.md-set-page` + `md-set-grid--cols-2/3/4`** 多列入口（仍 `md-set-row`）。右说明可为文字 `__hint` 或方形 `__thumb`（`--thumb`，行更高）。信息多改 `md-king--pair`。**平铺，无圆角阴影卡片壳** | 一排 `md-btn`；右图用列表横卡冒充；功能入口右图进灯箱；信息多却硬用一行两个；功能区套列表卡圆角阴影 |
| 单选 | 桌面/列表：`md-choice-group` + `md-radio`；触屏表单：同上（自动标签角标） | 未包 `md-radio` 的裸 `<input type="radio">` |
| 多选 | 桌面/列表：`md-choice-group` + `md-check`；触屏表单：同上（自动标签角标）；列表行勿包成标签 | 未包 `md-check` 的裸 `<input type="checkbox">` |
| 弹窗 / 确认 | `md-dialog` + `md-backdrop`；确认用 `ProtoPage.confirm` | `alert()` / `confirm()` |
| Toast / 提示 | `ProtoPage.snackbar` / `md-alert` / `md-tooltip` | 页内红字当提示 |

D5 弹窗用 `md-dialog` + **`md-backdrop`（半透明黑、全屏、`z-index` 低于面板）**，打开后遮罩淡入并 **拦截穿透点击**（`pointer-events` 随 `is-open` 开启）；**面板主体**白底、**统一圆角 `--md-radius-dialog` + 统一阴影 `--md-shadow-dialog`**（禁止直角无阴影或页内自写 `box-shadow`）；面板缩放在遮罩之上。

**写 HTML 时的固定顺序（⑥ 必遵守）**：每个弹窗/抽屉 id 须 **先写遮罩、再写面板**——`<div id="editBackdrop" class="md-backdrop"></div>` → `<div id="edit" class="md-dialog">…</div>`；抽屉同理 `{drawerId}Backdrop` + `md-drawer`。打开 **必须** `ProtoPage.openDialog('edit')` / `openDrawer('filterSheet')`；缺遮罩时脚本会运行时补，但 **coverage 与技能验收仍要求 HTML 显式配对**。点遮罩关闭由脚本绑定。

触屏下拉 **≤6 项中间弹窗**（`md-select-sheet--center`）与 `md-dialog` **同一圆角/阴影 token**。禁止无遮罩弹窗、`alert('原型：…')`。**触屏**弹窗内边距收紧；底半屏 `md-drawer--bottom` 高度随内容、最大 70vh、超出 `__body` 滚动，关闭用面板右上角 `md-drawer__close`（`openDrawer` 会自动补）。**表单弹窗** `md-dialog__form`：**一行只放一个输入项**（单列），不要双列并排字段。整页 D1-2 `md-d1__form` 仍可双列。

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
| 页内导航 | 触屏：右下 `md-pod--detail-nav`（目录半屏 + 回顶）。**桌面详情**：`md-d1--detail-split` + `md-split--outline-right`，右栏 `md-locator--outline` 常驻目录，点选滚锚点、滚正文 `is-active` 联动；`data-detail-nav="off"` 或右栏目录时脚本不注入悬浮钮 | 桌面用右下悬浮目录；用悬浮大纲冒充详情分栏 |

```html
<div class="md-mobile-page md-immersive md-detail-page" data-lightbox>
  <!-- 主图 md-hero … -->
  <main class="md-mobile-body">
    <div class="md-mobile-sheet md-mobile-sheet--flush-x md-detail-content">
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

### 字段列表（MP-012 / AD-012）

对照金样 `gold/mobile-fields.html` / `gold/desktop-fields.html`（六型合览见 `desktop-lists.html` 第三签）/ 夹具 `PAGE-AD-012`。**产品定性：列表族 · 无分页 · 多条记录按组**（字段列表页；按组扫读字段名+值，不是图文详情，不是横卡列表）。触屏用 **默认 sheet（safe-x）** + **`md-group-list`**（白底组卡浮浅灰，与横卡列表同滚动壳）。桌面用 **`md-d1 md-d1--list`** + 同结构 `md-group-list`。`desktop-detail` 字段签仅作 **单组 `md-desc` 排版参考**，不是 MP-012 页型。

| 层级 | 写法 | 规则 |
|------|------|------|
| 页壳 | 触屏：`md-standard` + `body` > `md-mobile-sheet`（默认 safe）；桌面：`md-d1 md-d1--list` + 面包屑 | **不要** `md-detail-page` / flush sheet；**不要** 搜索筛选工具栏 |
| 列表 | `div.md-group-list` > `__group` > `__head` + 多条 `__item` | 组标题加粗；组间露灰；记录间浅线左右内缩 |
| 字段表 | 每条 `__item` 内 `dl.md-desc` > `__row` > `__label` + `__value` | **左名右值**；空值「—」；状态可用 Chip |
| 长文案 | `__row--stack` / `__row--span` | 名在上、值在下；桌面组内可加 `md-desc--cols-2` |

```html
<main class="md-mobile-body">
  <div class="md-mobile-sheet">
    <div class="md-group-list" data-section="字段列表">
      <section class="md-group-list__group">
        <div class="md-group-list__head">水果</div>
        <article class="md-group-list__item">
          <dl class="md-desc">
            <div class="md-desc__row">
              <dt class="md-desc__label">商品名称</dt>
              <dd class="md-desc__value">有机草莓 250g</dd>
            </div>
          </dl>
        </article>
      </section>
    </div>
  </div>
</main>
```

禁止：把分组字段做成可编辑 `md-field` 表单；用 D1-1 标准表壳硬套；无分组堆成一篇图文；触屏 flush 浅灰壳或 `md-detail-page`；用单对象 `md-module` 冒充 MP-012。

### 单组字段排版（详情页内模块，非 MP-012）

详情页 **模块内** 只读字段表（单组、可双列）见 `gold/desktop-detail.html` 字段签：`md-module` + `md-section-head` + `dl.md-desc`。适用于图文详情里的「基本信息」等分组，**不是**不分页分组字段列表页。

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

**我的页个人信息 `md-profile--me`**：与详情店铺资料卡同根组件，只保留上层 `__head`；左 **`__media--avatar` 圆角矩形**（可 `--lg`，**非正圆**）点击后 **底半屏** 选「微信头像授权 / 从相册选择」；右三行：`__name` 昵称（大号黑字，点击 **底半屏** 选「微信昵称授权 / 手动输入保存」）→ `__uid`（小字灰 + 线框复制）→ `__extra`（按需留空或加文案/按钮）；右上可选 `__edit` 浅底小钮跳资料设置。不要套 `__stats` / `__foot` / 店铺标签 unless 规格要求。

```html
<article class="md-profile md-profile--me">
  <a class="md-btn md-btn--soft md-btn--sm md-profile__edit" href="./PAGE-MP-006.html">编辑</a>
  <div class="md-profile__head">
    <button type="button" class="md-profile__media md-profile__media--avatar md-profile__media--lg md-media-ph md-media-ph--1" aria-label="更换头像" data-profile-avatar></button>
    <label class="md-upload is-hidden" aria-hidden="true">
      <input type="file" accept="image/*" data-profile-avatar-file tabindex="-1">
    </label>
    <div class="md-profile__main">
      <button type="button" class="md-profile__title md-profile__name">阿宁</button>
      <p class="md-profile__uid">
        <span class="md-profile__uid-text">ID：8829103</span>
        <button type="button" class="md-btn md-btn--outlined md-btn--sm md-profile__copy" data-copy="8829103">复制</button>
      </p>
      <div class="md-profile__extra"></div>
    </div>
  </div>
</article>
```

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/浅底/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / **`--soft`（无边框浅底色字）** / `--text` / **`--link`（纯文字无线框无背景，查看更多/了解全部）**；`--sm` `--lg`；置灰 `disabled`；角标内嵌 `md-badge`。**`--text`/`--link` 字色须区别紧邻正文**（默认主色，禁止跟正文同色） |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input`；不可编辑一项即可：`md-field--readonly` + `readonly` 或 `disabled`（**视觉相同、灰底淡字**）。日期段 `readonly` 触发器不要加 `--readonly` |
| 卡片 | `md-card` **`--cover` / `--tile`（可横可竖或 `--ratio-auto` 定宽随图）`--row`（左图仅 1:1 或竖图 `--ratio-3x4/2x3`；字段少因值长再加 `--long`）**；列表单行 `md-set-row`。`md-card__media` `md-card__leading` `--avatar` `md-card__body` `md-card__main` `md-card__title` `md-card__subtitle` `md-card__text` `md-card__chips` `md-card__rail` `md-card__aside` `md-card__dist` `md-card__actions` `--bar` `md-card__time` `md-card__foot` `md-card__meta` `md-card__photos` `md-card__photo` `md-card__tag` `--tl/--tr` `md-price` |
| 资料卡片 | `md-profile`（店铺/个人/公司；**默认平铺**无圆角/轻阴影）；**最精简**=仅 `__head`（`__media` + `__title` + `__subtitle`）；完整再加 `__side` / `__meta` / `__tags` / `__stats` / `__foot`；**页顶**加 `--top` |
| 详情页 | 页根 `md-detail-page`（整页浅灰）；内容壳透底；标题/图文 **白底区块**、间隙露灰；`md-detail-head`；`md-article` 四级标题；短段不缩进、大段 `__body` 缩进、多项目 `__list`；`__figures--1/2`+居中 `__caption`+表格可横滑；**评论列表卡**；可嵌平铺 **资料卡片**；触屏右下 **目录+回顶**；桌面 **`md-split--outline-right` 右定宽目录** |
| 字段详情 | 同 `md-detail-page` 壳；分组 `md-module`+`md-section-head`；`md-desc` 左名右值（`--stack` 上下、桌面 `--cols-2/3`、跨列 `--span`）；金样 `mobile-fields` / `desktop-detail` 字段签 |
| 分区 / 模块 | `md-module`（L3，模块间距 `--md-module-gap`）；**列表/表单/详情等须区分的内容分区**才加 `md-section-head` + `md-section-head__title`（产品文案）；**金刚/通栏/服务条等功能区默认不加**（§1.3.5 / 金样 `mobile-grid` 金刚 module） |
| 系统栏 | `md-status-bar`（`proto-page.js` 固定顶注入；页内禁止手写；时间/信号靠顶略放大，左右各收一个图标身位，不为胶囊留空） |
| 触屏顶栏 | L1 无栏+自定义顶区 · L2 `--center` 居中无返回 · L3 `--overlay` 透明滚变实 · L4 无栏+`md-pod--tl` · L5 标准返回+左标题 · L6 `--cover` 双层封面 |
| 桌面面包屑 | `md-breadcrumb`（D1 内容区顶部，禁止再写 `md-page-head`） |
| 操作列 | 阈值与收纳执行 `PT-DESKTOP-LIST`。`md-col-actions` **按直出按钮形态+数量钉 px 列宽**（colgroup + `--md-col-actions-w`；表头 th 与 td 同宽；`ProtoPage.syncActionColWidths` 按图标 28px / 文字钮测字宽取各行 max，**不随浏览器 resize 变化**；tbody 变更才重算）；常规动作 `md-icon-btn` + `title`/`aria-label`；删除加 `md-icon--danger`；「更多」用 `data-menu` + `md-menu md-menu--fixed`（`md-select-wrap` 不计子节点档位） |
| 语义列宽 | `md-col-check` 勾选；`md-col-name` 名称硬锁定宽；`md-col-desc` / `md-col-note` 说明吃剩余；`md-col-date` / 最后数据列规则同前；`md-col-price` / `md-col-status` / `md-col-id` / `md-col-num`。**多字段单元格**用 `md-cell-stack`（`__primary` / `__secondary`）。长值省略不得溢出叠邻列；悬停看全文、点击复制 |
| D1-1 紧凑 | 根节点 `md-d1 md-d1--list`；**不要**套到 D1-2 表单页 |
| 列表六型 | 选型 `desktop-lists`（**金样只对标列表区**）：分页标准 `md-d1--list`；分页树表 `md-table--nest`；分组字段 `md-group-list`；只读树 `data-tree-edit="off"`；**分页无图/有图卡片** `md-d1__list` + `md-card-grid` + 底栏 `md-d1__footer`（同一行等高；无图卡右上角或表列 `md-col-switch` 可放开关；卡右下角 `md-card__foot` 可放按钮）。筛区/功能栏按规格另加 |
| 工作台 | `md-stat-grid` `md-stat-card`；趋势 `md-chart-ph` |
| 页面分栏 | `md-layout` `--full` / `--2col` / `--fix-left` / `--fix-right` / `--3col` / `--pin` + `__pane` / `__pane--span`。定宽栏 `--md-layout-aside`。**禁止**用 `md-d1__form` 冒充 |
| 分栏 / 树 | `md-d1--split`；`md-split` `__side` `__main`；树 `md-tree` `__row` `__ops` `md-tree-bar`（左根节点、右展开/收起切换）；右区维护表单 `md-split__form`；拖到节点上/中/下；只读 `data-tree-edit="off"`；定位导航 `md-locator` `--cats` / `--outline`（`data-target`，滚正文高亮联动）；左大纲 `md-split--outline` + `data-outline-toggle`（收起变点线轨）；桌面详情右栏 `md-split--outline-right`；章节页右悬浮 `md-locator-float`（收起同样点线轨） |
| 表内嵌套树 | `md-table--nest` + `md-row--child` + `md-nest-toggle`（空按钮，CSS 画 +/−）；`data-row-id` / `data-parent`；子行 `.md-nest-name` 缩进 |
| 分组字段列表 / 字段列表 | `md-group-list` `__group` `__head` `__item` + `md-desc`；无分页；**多条记录**；组标题加粗坐白底卡；记录间浅线左右内缩、不贴边；字段行不再分割。MP-012 / AD-012 页型；触屏 sheet safe。单组排版见 `desktop-detail` 字段签 |
| D1-2 表单栅格 | `md-d1__form`（默认双列，通栏 `width:100%`，`row-gap` 保留）；整页 `--cols-1/2/3/4`；块内 `md-form-block--cols-*`；字段 `--md-field-min`。弹窗 `md-dialog__form` 单列 |
| 下拉组合框 | `md-combo` + `md-combo__trigger` / `__panel` / `__value`（hidden）；`data-search="1"` 模糊搜；`data-mode="multi"` 多选；`data-tree="leaf"` 叶节点单选；`data-tree="1"` 树多选。`ProtoPage.bindCombos` 自动绑 |
| 设置分组 | `md-set-group` `__title` `md-set-row`（**设置项**：当页当行直接操作；左 `md-icon` 可有可无 + `__label`；右开关/值/本行菜单）；开关 `md-switch`（热区铺满，可点）；无极 `md-set-block` + `md-slider--fluid`；横向多选 `md-set-picks` / `md-set-pick`（`__face` 可为 `__label` 文字 / 图标 / `__media` 图片；图片竖版大图用 **`md-set-picks--media-9x16` + `__media--9x16`**；`__mark` 含 `__off`+`__on`，未选也显示空圈）；下拉 `md-set-row` + `data-menu` |
| 列表单行 | 仅在共享 `PT-MOBILE-LIST` 判定为单行时使用 `md-stack` > `md-set-row`；结构用 `__lead`（图标+`__label`）+ `__trail`（说明/计数/小标签，一般无箭头） |
| 功能区通栏 / 一行两个 | **功能入口**：触屏通栏 `md-set-group` / 一行两个 `md-set-pair`；**桌面** `md-set-grid--cols-2/3/4` 多列 `md-set-row`；右可为 `__hint` 或 **方形 `__thumb`**；常带箭头；**无圆角阴影卡片壳**；触屏**跟正文同左右安全距**，分割线内缩 |
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
| 步骤/树/图/章节 | `md-stepper` `md-step` `md-tree` `md-chapter-list` `md-chart-ph` `md-stat-grid` `md-stat-card` |
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
| 弹窗/确认 | `md-dialog` `md-dialog--sm/--lg`；**统一 `--md-radius-dialog` / `--md-shadow-dialog`**；触屏紧内边距；**表单 `md-dialog__form` 单列一行一项**；底半屏 `md-drawer--bottom` + `__close`；`ProtoPage.openDialog` / `confirm` |
| 提示 | 触屏：居中 `md-snackbar--toast`（半透明黑底、白图标白字）；桌面：底部 `md-snackbar`；`md-tooltip` `data-tip` |

```html
<!-- 放在 .md-mobile-page 下，与 md-tabbar / md-action-bar 同级；不要放进 md-mobile-body -->
<nav class="md-pod md-pod--tl" aria-label="返回、首页与分享">
  <button type="button" class="md-pod__item" aria-label="返回"><span class="md-icon" data-icon="chevron-left"></span></button>
  <button type="button" class="md-pod__item" aria-label="首页"><span class="md-icon" data-icon="home"></span></button>
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
