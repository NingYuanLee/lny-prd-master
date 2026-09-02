---
name: lny-prd-prototype
description: >-
  按规格生成高保真可交互原型。写每一页前必须 Read gold/ 金样以对标视觉下限（密度/类名），
  禁止按 ASCII 线框降质，也禁止把金样里的演示功能整页搬进业务页。
  全端静态 HTML + MUI 套件；按目标页面范围一次完成并逐页验收。Use when the user mentions
  /lny-prd-prototype, @lny-prd-prototype, 原型, prototypes.
---

## 与总控的关系

本步为 **⑥ `/lny-prd-prototype`**。只写根 `prototypes/`（含总入口 `index.html`、各端目录），只读取根 `pages_prd/` 工作源，禁止读取版本快照作为当前依据，禁止生成 `versions/{v}/prototypes/`。禁止改根规格与 `iteration_notes`。缺规格时 **本步内** Read ②③④⑤ 对应 SKILL 并落盘，再经⑦/Q-S通过后写 HTML；**禁止**空中楼阁 HTML，**禁止**停下来只说“交总控”。⑨交来时只走“只刷总入口”。完成作者自检后自动进入 **⑦/Q-P**；Q-P通过才询问是否进入⑧。全流程见 `lny-prd-master/SKILL.md`。

**页面范围**：用户给出 `页面编号列表` 时，一次生成/重画该列表中的业务 `PAGE-*.html`；未指定时，一次完成 `ui_manifest` 中当前全部 active 缺页（排除项不计入）。数量不设固定上限，但每一页都必须独立读取规格、对照金样并通过验收，禁止以页面较多为由合并或跳过质量门禁。因失败中断时列出未完成 PAGE，下一轮「继续」只补 ⑥（总控 **G-partial**），禁止借机重做 ②③④⑤。

# 生成原型 `/lny-prd-prototype`

## Additional resources

- 套件类名与壳数据：[`reference-kit.md`](reference-kit.md)（索引 + `reference-kit/` 分域分片）
- 移动端设计词典落地（原则→金样/Token）：[`reference-mobile-design.md`](reference-mobile-design.md)
- 内置图标：[`reference-icons.md`](reference-icons.md)
- 壳层 / 关系图 / 缩放：[`reference-shell.md`](reference-shell.md)
- 原型总入口：[`reference-scope.md`](reference-scope.md)
- 视觉金样（写页前必读）：[`gold/README.md`](gold/README.md)
- 桌面端设计词典（② 同源）：[`../lny-prd-ui/reference-desktop-design.md`](../lny-prd-ui/reference-desktop-design.md)
- 三步职责、页型编号与金样映射：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- UTF-8 与 BUG / 逐页对照：[`reference-quality.md`](reference-quality.md)
- 复制套件：`<skillDir>/scripts/copy-kit.py`
- 关系图画布：`kit/proto-map.js`（`map.html` 只 boot 数据）
- 搜图标：`<skillDir>/scripts/search-icons.py`
- UTF-8 校验：`<skillDir>/scripts/verify-prototype-utf8.py`
- 规格对照校验：`<skillDir>/scripts/verify-prototype-coverage.py`
- 浏览器冒烟验收：`<skillDir>/scripts/verify-prototype-browser.mjs`
- 夹具·金样对照：`scripts/verify-fixture-gold-parity.py`；一键同步 kit+夹具注释：`scripts/sync-mp-sheet-fixtures.py`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 三步对照（防错用）

先 Read [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)。本步只维护金样类名、视觉密度和 HTML 行为；下方速查表只保留 ⑥ 的专属落地规则。页型 ↔ 编号 ↔ 金样映射与跨步骤不变量以该正本为唯一事实源；本表与正本冲突时以正本为准（发布门禁自动比对）。

**树 vs 章节列表**：写 HTML 前若页含可展开层级列表，先读 master **「树 vs 章节列表选型」**——分类/组织 → `md-tree`（MP-008）；章节目录 → `md-chapter-list`（MP-015）；左分组右横卡滚联动 → `md-locator`（MP-013）。三者禁止混用。

## 金样速查（写 HTML 前扫一眼）

金样用来**快速对标视觉下限**（密度、比例、类名），不是业务功能清单。写页前 Read [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md) **取金样文件名**，再 Read 该金样全文。按**页类型**对照，不要按 PAGE 序号左右对齐；再按本页规格换文案、跳转和控件，并落地舒适默认与 [`reference-mobile-design.md`](reference-mobile-design.md) **审美必做**。类名细则见 [`reference-kit.md`](reference-kit.md)，本步不依赖仓库示例。

**移动端**

| 页型 | 关键类 / 调用 |
|------|----------------|
| PAGE-MP-001 首页 | L2【下沉首屏】页级 `md-hero`（与 body 同级）+ sheet；L3 `md-module`；`PT-MOBILE-FUNC` 宫格+双卡+列表合览；**规格无列表时改双卡/宫格+双卡**；`md-card--cover` + `md-card--tile`；TabBar |
| PAGE-MP-002 商品列表 | L1 固定 `md-appbar--center` + `md-list-toolbar`（body 外）；L2 只滚列表；`PT-MOBILE-LIST`；TabBar；**单列表默认无 `md-section-head`**，「今日上架」仅演示第二列表分区，只有规格 L4 / §2.3 点名用户可见文案时才复用该结构 |
| PAGE-MP-003 详情 | L3 **`md-appbar--overlay`** 滚变实底；`md-profile`；目录四项；右下目录+回顶 |
| PAGE-MP-012 字段列表 | **列表族·无分页·多条按组**；默认 sheet（safe）+ `md-group-list` 白卡浮灰；标准顶栏；= 桌面 lists 第三签；非图文、非横卡列表、非表单 |
| PAGE-MP-004 表单（套件样例） | **样例才整页铺齐**。`md-form-page` 浅灰底+白底 `md-module` 分组；返回顶栏；全部触屏表单控件；`md-action-bar` 贴底。业务表单按规格裁字段并同样分组。进度条见步骤向导 |
| PAGE-MP-005 步骤向导 | `md-form-page`；**数字 `md-stepper` 或分段 `md-advance--lg` 或无极 `md-progress--lg`（三选一）**；**仅 stepper 可点跳步**；advance/progress **只展示**；当前步表单；`md-action-bar` 贴底，最后一步才提交 |
| PAGE-MP-006 设置 | L6 **`md-appbar--cover`**；`md-set-page`；设置项/多选/图片单选等 |
| PAGE-MP-010 我的/服务 | `md-set-page` 浅灰底；顶区 **`md-profile--me`**（圆角矩形头像/昵称均 **底半屏** 改）；**`md-svc-strip`**（2/3/4 等分；`__icon`+**`__badge`** / **`__value`+`__help`**）；功能入口通栏/`md-set-pair`；右可为文字或 **方形配图 `--thumb`**；组间距漏底 |
| PAGE-MP-007 按钮（套件样例） | 小 `--sm` / 中 / 大 `--lg`；线框、色块、**浅底 `--soft`**、文字、**`--link`**、**通栏 `--block` / `md-btn-row`**、置灰、`md-badge`；贴底仅一钮自动占满。禁止当业务首页。禁止裸 `<button>` |
| PAGE-MP-011 悬浮胶囊（套件样例） | L4 无顶栏 + **`md-pod--tl`**；`PT-FLOAT`；与页内顶栏互斥 |
| PAGE-MP-008 分类树 | `md-tree-page`；`md-split` 左多级树右 **图文介绍**（`md-cat-intro`）；浏览用 `data-tree-edit="off"`；点节点只换右区。桌面维护树见 `md-d1--split` |
| PAGE-MP-013 分类导航 | `md-locator-page`；左一级 `md-locator--outline`（子章 `__item--l2`）；右分组 **横卡列表**；点选滚锚点 + 滚正文高亮联动。**不是**树 |
| PAGE-MP-015 章节目录 | `md-chapter-list` + `__group`/`__head`/`__body`/`__parent`/`__child`；**父章 toggle 可收起子章**。不是树、不是横卡 |
| PAGE-MP-014 订单列表 | L1 **返回+搜索**顶栏 + **下划线页签+筛选**（toolbar 在 body 外）；`md-card--order` 推广条/店头/商品行价量/实付款/浅底操作；查看物流 → PAGE-MP-009 |
| PAGE-MP-009 物流时间轴 | `md-timeline--static` 只读；**仅已发生节点**；倒序；`is-active` 当前高亮、`is-path` 途经、`is-origin` 起点空心；竖轨全程主色；右 **横卡文本**（无左图，正文可 `__photos`） |

**桌面端**

| 页型 | 关键类 / 调用 |
|------|----------------|
| PAGE-AD-001 列表 | 六型合一，**金样只对标列表区**（无搜索栏、无功能栏）。分页标准：`md-d1 md-d1--list`、操作列按按钮形态与数量定宽、`md-cell-stack`、`md-col-switch`。树表：`md-table--nest`、子行缩进、+/−。卡片：`md-d1__list`+`md-card-grid`+底栏分页；卡右上角开关/右下角按钮。筛区/功能栏按规格另加，不要从金样抄成「不要筛」 |
| PAGE-AD-002 商品表单 | `md-breadcrumb`；`md-field--sm`；栅格有行距。**按规格裁字段**；分栏布局勿用本表单；状态导览见 stepper / advance |
| PAGE-AD-009 表单（套件样例） | **样例才整页铺齐**。`--cols-1/2/3/4` + `md-combo` 七种下拉。**不要**加 `md-d1--list`，不要触屏 `data-wheel`，不要当页面左右分栏 |
| PAGE-AD-008 详情 | 整页浅灰；白底区块；`md-profile`；灯箱分区；**右定宽目录** + 滚正文联动（`md-split--outline-right`）。图文签。不要沉浸式、不要右下悬浮目录 |
| PAGE-AD-012 字段列表 | **列表族·无分页·多条按组**；`md-d1--list` + `md-group-list`；桌面 `--cols-2` / `--span`。非图文、非表单、非 D1-1 标准表壳 |
| PAGE-AD-003 向导 | **数字 `md-stepper` 或分段 `md-advance`（二选一，禁止同页叠加）**；**仅 stepper 可点跳步**；advance **只展示**；当前步包在 `md-d1__form` |
| PAGE-AD-004 工作台 | 指标卡 `md-stat-grid`；趋势 `md-chart-ph`；下面短表 |
| PAGE-AD-005 商品分类 | 不分页维护树：`md-d1--split` + `md-tree` + `md-tree-bar`（左根节点、右展开/收起切换）；右区 **分类表单**；增子/重命名/删除；拖到上/中/下。只读树与表内嵌套用列表六型金样。**不是**分类钮 |
| PAGE-AD-013 章节大纲（套件样例） | 两种：左可收缩 / 右悬浮可收起；**收起后点线轨**；点选滚锚点；**滚正文时当前点高亮**；与树分离 |
| PAGE-AD-014 页面分栏（套件样例） | `md-layout--full/2col/fix-left/fix-right/3col/pin`；**禁止** `md-d1__form` 冒充分栏。卡片列表见列表六型 |
| PAGE-AD-006 设置 | `md-d1 md-set-page` 浅灰底；**设置项**：开关可点；桌面 **`md-set-grid`** 多列；`md-set-picks` 文字/图标/图片 + 未选空圈；左图标可有可无；无极 / `data-menu` 改值 |
| PAGE-AD-010 我的/服务 | `md-set-page` 浅灰底；**`md-svc-strip--desk`** 订单待办/经营概览；桌面功能入口 **`md-set-grid--cols-2/3/4`**（触屏仍通栏/`md-set-pair`）；右可为文字或方形配图 `--thumb`。不要 `md-d1--list` |
| PAGE-AD-007 时间轴 | 通栏 `md-timeline--static` 只读物流轴；**仅已发生节点**、倒序；左竖轨右 **横卡文本**。可交互章节导航见 PAGE-AD-013，禁止可点切换进度 |
| PAGE-AD-011 悬浮按钮（套件样例） | 仅规格点名时按共享 `PT-FLOAT` 落到业务页；用 `md-pod md-pod--desk` + `position:fixed`，折叠态用 `md-pod--fold` + `__toggle`，禁止触屏方位类和 `md-fab` |
| 关系图 | `ProtoMap.boot`；预览区 **375×812**；连线端口错开 + 线中 `label`；底部色线图例；拖动写入 localStorage；「导出图片」 |

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 与 `lny-prd-master/reference-artifact-paths.md`。不生成已排除项的 `PAGE-*.html`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**在原型中实现或展示清单中的能力。

**输入优先级**：默认 Read 根 `pages_prd/{终端}/{PAGE-ID}.md` 工作源；无则须 `ui直出`（用户确认或台账标明）。缺规格或有 `待②`/`待③`/`待④`/`待⑤` → **本步内补链**：依次完整 Read `lny-prd-ui` / `lny-prd-api` / `lny-prd-feature` / `lny-prd-page` 的 `SKILL.md` 并落盘缺口，执行Q-S，通过后继续写HTML。禁止自行编造规格；禁止因缺口停止本步、只把球踢回总控。

埋点：仅当规格已写明点位或 AD 字典条目时才在原型展示；**禁止自拟埋点方案**。

**向导 / 引导分步页（`PT-STATE-FLOW`）开笔 checklist**（业务页，非套件样例对照）：

- [ ] `ui/PAGE` **步骤区**已三选一点名 + **共 N 步**（L3 只写一种）
- [ ] **禁止**搬金样 **`md-tabs` + `data-wizard-panel` / `data-panel="*Wiz*"`** 签切换对照结构（见 `mobile-wizard.html` / `PAGE-MP-005` 夹具说明）
- [ ] 同页仅一种 `md-stepper` / `md-advance` / `md-progress--lg`（`verify-prototype-coverage.py` 会拦叠加）

## 一条路径（全端静态 HTML + kit）

所有终端（MP / H5 / APP / PC / AD）均为静态 HTML。观感来自技能包 **`kit/`**。图标：闭集 `md-icons.js`；闭集没有的用 **`scripts/search-icons.py`**（技能自带，不调用 Cursor MCP）。**本地 URL 一律相对路径且带 `./`**：静态资源（如 `./assets/mui-kit.css`）、页面跳转与 `<a href>`（如 `./PAGE-MP-001.html`）、`iframe`/`script`/`link` 的 `src`/`href`、壳层 `PROTO_SHELL.pages[].file`、关系图 `map` 数据里的 `file` 等；禁止绝对路径、站点根路径（`/…`）或省略 `./` 的裸相对名。`#` 锚点与 `https://` 外链除外。

**本地预览**：在 `prototypes/` 目录执行 `python -m http.server`（不要用 `npx serve`，也**禁止**在业务项目生成 `serve.json`）。

1. `python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}`
2. Read [`reference-kit.md`](reference-kit.md) 索引（全局 token + **高保真落地**），再 Read 本页对应分片：触屏 `reference-kit/mobile-classes.md`、桌面 `reference-kit/desktop-controls.md`；生成壳层读 `reference-kit/shell.md`（`index.html` 只填 `PROTO_SHELL`）；无对应类名用 `reference-kit/combos.md`「无类名组合」。单页只用 `md-*` 类；**禁止裸 HTML**、禁止「示例 A/B」低保真数据。
3. 业务图标：Read [`reference-icons.md`](reference-icons.md)。闭集能覆盖则 `data-icon`；否则 `search-icons.py --pick 0 --name … --out …/assets`。无网或接口失败时按该文选择闭集近义项并记录替代，**不中止本轮**。
4. 壳层行为（状态演示 / 规格说明 / 缩放 / 关系图）见 [`reference-shell.md`](reference-shell.md)。目标页完成后按 [`reference-scope.md`](reference-scope.md) 覆盖刷新 `prototypes/index.html`（含页底右下 SKILL 标注）。各端 `index.html` 的同类标注由 `proto-shell.js` 注入，禁止手写。

**状态机硬约束**：`PROTO_SHELL.pages[].comps[].states` 只能从对应 `ui/COMP-*.md` 的 UI 状态矩阵复制，逐字且按行顺序一致；禁止凭空补 `edit` / `disabled` / `pending` 等状态。`loading` / `empty` / `error` 必须分别落地 `data-skel-for` / `data-empty-for` 视觉实现，其它状态必须有 `data-state-for` + `data-state` 视觉块。默认显示壳层状态演示；只有页内产品控件明确承担同一 COMP 切态时才写 `stateDemo: false`，不要再用 `tabBarExempt` 隐藏有组件的页面。覆盖验收会同时检查状态矩阵、壳层枚举和页面视觉实现。

**禁止**：初始化 npm/Vite/React；查询 mui-mcp；调用 `user-search-iconfont-mcp`（改用本技能 `search-icons.py`）；页内自造主题色、手绘图标 path 或第二套组件 CSS。

## 金样怎么用（视觉下限，不是功能清单）

金样只做一件事：**方便快速对标，保证视觉效果下限**（密度、图文比例、套件类名、顶栏/底栏结构）。不是业务功能清单，也不是可以跳过的参考图。

禁止两个极端：

1. **照搬功能**：金样表单铺了全套控件就把样例整页搬进业务页。点图预览默认给详情页图片、横卡多行卡内图、**单图/多图/视频上传缩略**；不要给封面叠字 / 双列 / Banner / 文件上传加灯箱。一页铺齐控件只在本页规格写了才用。
2. **忽略金样**：按 ASCII 画空盒子、比金样更瘦、不 Read 对应金样。未 Read 金样 = 本页未完成。

该对标的：分区疏密、卡片形态与图文比例（叠字/瓷砖可横可竖或定宽随图；横卡左图 1:1 或竖图；详情非列表图 16:9）、Chip / 面包屑 / 横卡、`md-*` 类名、本页规格需要的控件行为（轮盘 / 下拉 / 签）。
不该搬的：金样商品名与跳转、套件样例才有的演示交互。

真实项目没有样例店可看时，模型会按 ASCII 线框画出空盒子。用 `gold/` 钉死视觉下限，用 [`reference-mobile-design.md`](reference-mobile-design.md) 钉死审美必做，再用舒适默认抬高：

1. 写页前：Read [`gold/README.md`](gold/README.md) → Read **本页类型**金样全文 → **按视觉骨架落地**（类名与密度不得低于金样）。禁止凭记忆、禁止按 ASCII 从零画。
2. 只替换业务文案、条数、跳转、本页规格里的分区。规格需要的套件行为要保留（轮盘 `data-wheel`、`data-menu` 更多、页内签 `data-panel`）。规格没有的金样演示交互不要搬；换业务时禁止把本页需要的 JS 删成静态壳。
3. ASCII = 分区顺序；金样 = 视觉密度。功能以本页规格为准。`ui/PAGE`「视觉细节」只给 ⑨ 估点，⑥ 视觉不降档。触屏 §1.3.3；桌面 D1-1 §1.4.3。**需求描述 ≠ 可见标题**（`lny-prd-ui` **§1.3.5**）：写 HTML 前对照金样 DOM——**金刚区/通栏/服务条不加 `md-section-head`**（`gold/mobile-grid.html` 金刚 module、`gold/mobile-menu.html`）。禁止把 US/Feature/规格分区词（「刷题入口」「功能入口区」）当 `md-section-head__title`；列表/详情等多模块页仅在须区分分区时加**产品文案**标题（如「精选」「评论」）。
4. **舒适默认（§2.3 漏写也要落地）**：按 `lny-prd-ui` **§1.7.0**。骨架、空态插图、失败可重试、一个主按钮、按下态、浮层过渡、D1-1 语义列宽+`md-d1--list`、评论时间行+附图约 40px、一排最多五张。禁止发明新跳转/新字段/新弹窗。**有字段时必须按层级排版**。**浮层遮罩必做**：凡写 `md-dialog` / `md-drawer`，HTML **必须先写** `<div id="{id}Backdrop" class="md-backdrop">` 再写面板；打开 **必须** `ProtoPage.openDialog` / `openDrawer`（脚本会补遮罩，但 HTML 仍须配对以便 coverage 与预览一致）。禁止无遮罩弹窗、`display` 瞬切、`alert()`。**触屏间距**：按 [`reference-kit.md`](reference-kit.md) **§触屏间距三层联动**——父 gap 定兄弟节奏、seam 边不叠 padding、内距写在 `__item`；混合 sibling 时保留父 gap、改子块 padding。写完后目视检查 seam，禁止零间距也禁止双倍间距。用户未给设计规范 ≠ 可以画线框。点图预览只默认给详情页与横卡多行，不是凡图都预览。
5. 重画不得删 Chip / 面包屑 / 横卡 / `data-icon` / `md-dialog`。未 Read 金样 = 本页未完成。
6. 不是速查表里已有的页型：按金样表选最接近的金样（dashboard / layout / lists / split / locator / settings / menu / wizard / state-flow / timeline / detail），禁止拿 `desktop-lists` 硬套工作台，禁止拿 `md-d1__form` 冒充页面分栏，禁止拿一排按钮硬套功能区。

## 职责与禁止

- **负责**：按目标范围生成/更新根 `prototypes/` 下的 **高保真** 当前原型；逐页对照 `pages_prd`；UTF-8 与 coverage 验收；BUG 自检。
- **禁止**：用 HTML 编造规格；改根规范或流水；交付已知 BUG；页内保留演示专用按钮（须归位状态演示）；因目标页较多而跳过逐页规格读取、金样对照或验收；未 Read 该页 `pages_prd` 或未 Read `gold/` 就写 HTML；按 ASCII 线框降质；把金样演示功能（如凡图即灯箱、全套表单样例）搬进规格没写的业务页；给封面叠字 / 双列 / Banner / 文件上传加预览；裸 `<button>` / `<input type="submit">` 露出浏览器原生皮肤（必须 `md-btn` 等套件类）；把本轮临时文件留在业务项目里交付。

## 写产物纪律

先清单后落盘。含 CJK 的文件整文件 UTF-8 写入，禁止用 StrReplace 改中文块。每页写后执行 UTF-8 验收；全部目标页写完再跑 coverage。失败则重写，不得交付。细则见 [`reference-quality.md`](reference-quality.md)。

**工具路径**：copy-kit / 搜图标 / UTF-8 / coverage / 浏览器冒烟一律执行 **技能包** `<skillDir>/scripts/…`，不要把技能脚本永久拷进 `prdRoot`。浏览器冒烟依赖宿主可解析 `playwright` 与 `pngjs`；依赖只装在宿主或技能仓库，**禁止**为验收在业务 `prdRoot` 初始化 npm 或生成 `node_modules/`。

**临时文件清理（交付前必做）**：过程中若在 `prdRoot` 建了辅助脚本（如 `prdRoot/scripts/`）、草稿、备份、一次性生成器等，**用完后必须删干净**再交付（含空目录）。正式原型只保留根 `prototypes/`；禁止将其复制到 `versions/`。系统临时目录优先于业务根目录。

```text
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/...
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version vX.Y.Z --page PAGE-… --page PAGE-…
node <skillDir>/scripts/verify-prototype-browser.mjs <prdRoot> --page PAGE-… --page PAGE-…
```

浏览器脚本 exit 1 表示页面或交互失败，必须修复；exit 2 表示宿主缺 Node 依赖，须明确回报“浏览器冒烟未执行”并继续人工预览，不得伪报通过。截图仅在排障时用 `--artifacts <系统临时目录>` 输出，禁止写入业务项目。
## 前置条件

已有 `main_spec.md`。若尚无 `ui_manifest` / 目标页 / 根 `pages_prd`（且非 `ui直出`），或台账仍有 `待②`～`待⑤`：先按开笔前补链并通过Q-S，再写原型。不要因此拒绝。

## 输入

```yaml
版本号: v1.0.0
页面编号列表: (可选；指定则一次完成该列表，未指定则一次完成 manifest 当前全部 active 缺页)
只刷总入口: false  # ⑨ 交来或只要更新版本清单时为 true
```

## 只刷总入口

⑨ 估点落盘后、或用户只要更新总入口版本清单时走本节，**不要**走下方全量步骤。

1. Read [`reference-scope.md`](reference-scope.md)。
2. 若尚无任何 `prototypes/{终端}/`：不新建空总入口，回报「无原型可挂」并结束。
3. 覆盖写入唯一总入口 `prototypes/index.html`。版本清单按 **全部** `versions/` 填写。页底右下须保留 SKILL 标注（见 [`reference-scope.md`](reference-scope.md)）。
4. UTF-8 验收该 `index.html`。
5. **禁止**：copy-kit；改各端 `PAGE-*.html` / 端 `index.html` / `map.html`；补 ②③④⑤；把本节当成全量出原型。

## 执行步骤

若输入 `只刷总入口: true` 或由 ⑨ 交来 → 只走上一节。

1. 校验版本目录。有未清委派或缺规格 → 先补链（见开笔前），不要停。
2. 列出本轮目标页：用户给了 `页面编号列表` 时，以其中在 `ui_manifest` 中为 **active** 的业务页为准，可生成缺页或重画已有页；未指定时，选择 `ui_manifest` 中 **active** 且 `prototypes/{终端}/PAGE-*.html` 尚不存在的全部业务页（排除项不计入）。不按数量截取。
3. 复制 kit 到目标页涉及的每个 `prototypes/{终端}/assets/`（assets 已齐可跳过 copy-kit）。
4. **逐页**：对该页完整 Read `pages_prd`（无则须 `ui直出`）+ `ui/PAGE-*` **§2.3** + COMP。按页类型 Read 金样全文，**对标视觉骨架**（密度/类名不得低于金样），再按本页规格换文案并落地 §2.3 与舒适默认。写完立刻过 [`reference-quality.md`](reference-quality.md) **§G.4 / G.5**。禁止凭记忆、禁止按 ASCII 降质、禁止忽略金样、禁止把金样演示功能搬进规格没写的页。
5. 按 [`reference-shell.md`](reference-shell.md) 写/刷新各端 `index.html`（及移动端 `map.html`）：**只挂已落盘**的 `PAGE-*.html`。按 [`reference-scope.md`](reference-scope.md) 写 `prototypes/index.html`。禁止写项目根 `index.html`、`versions/{v}/index.html` 或 `versions/{v}/prototypes/`，不写 `scope.html`。
6. 对全部目标页跑 UTF-8 脚本 + `verify-prototype-coverage.py` + `<checkSkillDir>/scripts/verify-artifact-paths.py` + [`reference-quality.md`](reference-quality.md) §G 自检（含 kit 引用）；宿主依赖可用时，再对全部目标 PAGE 跑 `verify-prototype-browser.mjs`。任一步失败则重写，不得交付；浏览器依赖缺失须按上文披露。
7. **清理临时文件**：删除本轮在 `prdRoot` 留下的辅助脚本/草稿/备份及空的 `scripts/` 等（见写产物纪律）；未建临时文件可跳过。
8. 作者自检全部通过后自动执行 **⑦/Q-P**。Q-P发现纯原型问题则本步同轮修复并重跑；发现规格问题则按总控回到②③④⑤与Q-S，再更新原型。Q-P通过后输出目标页、验收结果与未完成编号，并只在此时询问产品是否进入⑧评审。
