# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角/阴影见下节 token、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。


## 用法（索引 + 按需分片）

本文件是索引，保留全局 token 与高保真铁律（每页都须遵守）。类名字典按域分片到 `reference-kit/`：Read 本索引后，只再 Read 本页对应的分片，禁止整包全读。

| 分片 | 内容 | 何时 Read |
|------|------|-----------|
| [`reference-kit/shell.md`](reference-kit/shell.md) | 套件复制、引用硬性规则、`index.html` 数据驱动壳 | 生成/更新壳层或总入口 |
| [`reference-kit/mobile-classes.md`](reference-kit/mobile-classes.md) | 触屏单页类名（移动页 A/B、列表区、功能区） | 写 MP/H5/APP 触屏 `PAGE-*.html` 前 |
| [`reference-kit/desktop-controls.md`](reference-kit/desktop-controls.md) | 桌面 AD 常用控件 | 写 AD/PC 桌面 `PAGE-*.html` 前 |
| [`reference-kit/combos.md`](reference-kit/combos.md) | 无类名组合（详情图文/字段列表/资料卡等） | 套件无对应类名时（禁止裸 HTML） |
| [`reference-kit/components.md`](reference-kit/components.md) | 组件速查 | 查组件形态与行为 |

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

`pages_prd` ASCII **只定分区上下顺序**，不是视觉稿。Markdown 标题、L 层、Module、US、Feature 与否定约束均不自动成为 UI 文案；仅当 §2.3 /「结构与控件」明确声明准确的用户可见标题时才渲染标题。Tab、字段名、设置行已自解释的区域不重复加 `md-section-head`。写页前必须 Read [`gold/README.md`](gold/README.md) 与对应金样，**对标视觉下限**再换文案。禁止把 `┌─┐` 画成带边框空盒子，也禁止把金样演示功能（凡图即灯箱、全套表单样例）搬进规格没写的业务页。点图预览只默认给详情页与横卡多行。

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

纸面内放平铺 `md-set-group` 时给 `md-paper` 加 `md-paper--clip`，让圆角裁住组背景；长分类表头/值列用 `md-col-label`（136–160px）。详情页默认或 `data-detail-nav="on"` 仅在正文实际溢出时注入导航，且至少两个有标题分区才显示目录；短页不注入目录或回顶，`off` / `toc` / `top` 等显式模式仍可用。

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
| **L2 滚动主内容** | **必须有** | 每页恰有一个 `md-mobile-body`；其 **唯一** 直接子节点是一个 `md-mobile-sheet`，L3 只能放入 sheet |
| **L1 固定**（顶栏/搜索筛选/TabBar/贴底条） | **没有** | 页根下与 `md-mobile-body` **并列** |
| **L2 下沉 Hero** | **没有** | 页根下与 `md-mobile-body` **并列**的 `md-hero` |
| **L5 浮层** | **没有** | 页根级 drawer/dialog/toast |

**一种页只有一个 sheet**；禁止 body 直放 L3、禁止 body 里嵌套多层 sheet、禁止 sheet 里再套 Hero。固定 L1 必须在 `md-mobile-body` 外与其并列。

**sheet 修饰**（都有 sheet，只变左右 safe）：

| 类名 | 左右 safe | 用于 |
|------|-----------|------|
| `md-mobile-sheet` | 默认 **有** | 列表、按钮、时间轴、下沉首页 |
| `md-mobile-sheet--flush-x` | **无** | 详情/字段详情/树（或页根 `md-detail-page` 等自动 lr0） |
| `+ md-detail-content` | **无** | 详情语义壳，等价 flush-x |

**无 sheet 的旧 HTML** 不再推荐；`body` 已无默认 padding/灰底，缺 sheet 会丢滚动区样式。

**② 页型选型**（列表型 vs 浅灰壳、何时改页型、详情评论 hybrid）：见 [`lny-prd-ui/reference/visual-rules.md`](../lny-prd-ui/reference/visual-rules.md) §1.3.4「滚动区页型选型」；② 写 L2 时引用，⑥ 按选型落 sheet 修饰类。

**触屏金样 DOM 纪律**：14 个 `mobile-*.html` **全部** `body` > `sheet`；⑥ 新页照抄。改 `kit/` 后须对业务根 `prototypes/{终端}/` 执行 `copy-kit.py`（或 **`sync-mp-sheet-fixtures.py`** 一键同步 MP+AD 夹具注释与 kit）。对照 **`verify-fixture-gold-parity.py`** 确认 14×MP + 14×AD 夹具与金样文件齐套。
