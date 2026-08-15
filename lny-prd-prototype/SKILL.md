---
name: lny-prd-prototype
description: >-
  按规格生成高保真可交互原型。写每一页前必须 Read gold/ 金样以对标视觉下限（密度/类名），
  禁止按 ASCII 线框降质，也禁止把金样里的演示功能整页搬进业务页。
  全端静态 HTML + MUI 套件；每轮最多 3 个业务页。Use when the user mentions
  /lny-prd-prototype, @lny-prd-prototype, 原型, prototypes.
disable-model-invocation: true
---

## 与总控的关系

本步为 **⑥ `/lny-prd-prototype`**。只写 `prototypes/` 与 `versions/.../prototypes/`（含总入口 `index.html`、各端目录）。禁止改根规格与 `iteration_notes`。缺规格时 **本步内** Read ②③④⑤ 对应 SKILL 并落盘，再写 HTML；**禁止**空中楼阁 HTML，**禁止**停下来只说「交总控」。⑨ 交来时只走「只刷总入口」，禁止升级成全量出原型。⑦ 须用户明确要求检查。全流程见 `lny-prd-master/SKILL.md`。

**分批硬顶**：本轮最多生成/重画 **3** 个业务 `PAGE-*.html`（不含各端 `index.html` / `map.html` / 总入口）。未完成的 PAGE 列出编号，下一轮「继续」只续 ⑥（总控 **G-partial**），禁止借机重做 ②③④⑤，禁止同一轮把全部页画完。

# 生成原型 `/lny-prd-prototype`

## Additional resources

- 套件类名与壳数据：[`reference-kit.md`](reference-kit.md)
- 移动端设计词典落地（原则→金样/Token）：[`reference-mobile-design.md`](reference-mobile-design.md)
- 内置图标：[`reference-icons.md`](reference-icons.md)
- 壳层 / 关系图 / 缩放：[`reference-shell.md`](reference-shell.md)
- 原型总入口：[`reference-scope.md`](reference-scope.md)
- 视觉金样（写页前必读）：[`gold/README.md`](gold/README.md)
- UTF-8 与 BUG / 逐页对照：[`reference-quality.md`](reference-quality.md)
- 复制套件：`scripts/copy-kit.py`
- 关系图画布：`kit/proto-map.js`（`map.html` 只 boot 数据）
- 搜图标：`scripts/search-icons.py`
- UTF-8 校验：`scripts/verify-prototype-utf8.py`
- 规格对照校验：`scripts/verify-prototype-coverage.py`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 三步对照（防错用）

同一套页型，②⑤⑥ 各看一层，**禁止串用、禁止按编号左右对齐**。

| 步 | 看 | 用来 | 禁止 |
|----|----|------|------|
| ② | `ui/PAGE` §2.3 + 夹具页型 | 体验与结构 | 规格里堆 `md-*` |
| ⑤ | `pages_prd` ASCII | 分区上下 | ⑥ 按线框画空盒子 |
| ⑥ 本步 | 下方金样全文 | 密度/类名下限 | 整页搬样例；按号猜金样（MP-003≠AD-003） |

**编号不对齐**（先对页型再打开金样）：详情 MP-003→`mobile-detail` / AD-008→`desktop-detail`；向导 MP-005 / AD-003；树 MP-008 / AD-005；时间轴 MP-009 / AD-007；表单铺齐 MP-004 / AD-009；业务表单 AD-002 只借 `desktop-form` 控件并按规格裁。设置碰巧都是 006，我的碰巧都是 010。

**套件样例 ≠ 业务必有页**：MP-004 / MP-007 / MP-011 / AD-009 / AD-011 只在本页规格写了「铺齐/演示」时整页用。业务表单按规格裁字段。触屏胶囊对标 `mobile-pod.html`，桌面悬浮按钮对标 `desktop-pod.html`，不要每个项目都做样例页。

**列表页**用 `md-list-toolbar`（搜索+筛选），不要套返回标题栏 `md-appbar`。

## 夹具速查（写 HTML 前扫一眼）

夹具 `examples/mini-shop/` → 金样 + 套件类。金样用来**快速对标视觉下限**（密度、比例、类名），不是业务功能清单。按**页类型**对照金样，不要按 PAGE 序号左右对齐。再按本页规格换文案/跳转/控件。夹具还须落地舒适默认与 [`reference-mobile-design.md`](reference-mobile-design.md) **审美必做**。类名细则 [`reference-kit.md`](reference-kit.md)。

**移动端**

| 夹具页 | 金样 | 关键类 / 调用 |
|--------|------|----------------|
| PAGE-MP-001 首页 | `gold/mobile-grid.html` | `md-immersive` `md-hero`；`md-module`；`md-card--cover` 精选 + `md-card--tile` 双列推荐；`md-king` 5 列 + `--pair`；有 TabBar 则无 `md-appbar` |
| PAGE-MP-002 列表 | `gold/mobile-list.html` | `md-standard`；搜索+筛选贴顶；页签按钮组；**列表区**横卡多行 `md-card--row`（字段多或值长；文本靠左，`__rail` 价格/距离右上，单按钮右下或 `--bar` 底栏；**卡内图默认可预览**；竖图定宽只加高）+ 横卡单行 `md-stack`>`md-set-row`（仅字段≤3 且值都短；每行独立有缝，不要 `md-set-group`）；非分组、数据可无限（分页无页边界）；卡统一 `--md-shadow-surface`；底角 `md-pod`（有顶栏故无左上）；筛选半屏 `data-wheel="daterange"` |
| PAGE-MP-003 详情 | `gold/mobile-detail.html` | `md-swiper--wide` 主图 16:9；图文介绍；`md-comment` 时间行 + `__photos` 约 40px、一排最多五张。**本页图片默认可点预览**（页根 `data-lightbox`） |
| PAGE-MP-004 表单（套件样例） | `gold/mobile-form.html` | **样例才整页铺齐**。返回顶栏；全部触屏表单控件；`md-action-bar` 贴底。业务表单按规格裁字段。进度条见步骤向导 |
| PAGE-MP-005 步骤向导 | `gold/mobile-wizard.html` | 横向 `md-stepper`；分段 `md-advance md-advance--lg`；无极 `md-progress md-progress--lg`；当前步表单；`md-action-bar` 贴底，最后一步才提交 |
| PAGE-MP-006 设置 | `gold/mobile-settings.html` | 沉浸式；`md-appbar--cover`；**设置项**：开关可点；`md-set-picks` 选项面文字/图标/图片均可，未选显示 `radio-off`、已选 `check`；左图标可有可无；无极 / `data-menu` 改值 |
| PAGE-MP-010 我的/服务 | `gold/mobile-menu.html` | 标准顶栏；**功能入口**（只跳转或开半屏/弹窗）：通栏 `md-set-group`>`md-set-row` 或 `md-set-pair`；常带箭头。金刚见首页（无阴影）。禁止一排 `md-btn` |
| PAGE-MP-007 按钮（套件样例） | `gold/mobile-buttons.html` | 小 `--sm` / 中 / 大 `--lg`；线框、色块、**浅底 `--soft`**、文字、**`--link`**、置灰、`md-badge`。禁止当业务首页。禁止裸 `<button>` |
| PAGE-MP-011 悬浮胶囊（套件样例） | `gold/mobile-pod.html` | 规格点名才画到**业务页**，不要每个项目都做本页。`md-pod` + `--tl` / `--bl` / `--br`；写在页根。不要右上，不要用 `md-fab` 冒充成组 |
| PAGE-MP-008 分类 | `gold/mobile-tree.html` | `md-tree-page`；`md-split` 左树右内容；`md-tree` `__toggle` 展开收起；点节点只换右区 |
| PAGE-MP-009 时间轴 | `gold/mobile-timeline.html` | `md-timeline` 左 `__rail` 竖轨，右 `md-card--row` 图文；`is-done` / `is-active`；点节点切高亮 |

**桌面端**

| 夹具页 | 金样 | 关键类 / 调用 |
|--------|------|----------------|
| PAGE-AD-001 列表 | `gold/desktop-list.html` | `md-d1 md-d1--list`（**紧凑密度**）；`md-breadcrumb` 无 `md-page-head`；签 `md-tabs--page` 在筛上整区切换；列类 `md-col-check` `md-col-name` `md-col-price` `md-col-status` `md-col-date` `md-col-actions`（**按字段语义，禁止均分**）；筛选用 `md-field--daterange`；「更多」`md-menu--fixed`；`md-d1__stats` 左 / `md-d1__pager` 右 |
| PAGE-AD-002 商品表单 | `gold/desktop-form.html` | `md-breadcrumb`；`md-field--sm`。**按规格裁字段**，不要把套件样例整页搬来；进度条不在本页，见步骤向导 |
| PAGE-AD-009 表单（套件样例） | `gold/desktop-form.html` | **样例才整页铺齐**。全部桌面表单控件。业务页用 AD-002 按规格裁。**不要**加 `md-d1--list`，不要触屏 `data-wheel` |
| PAGE-AD-008 详情 | `gold/desktop-detail.html` | `md-breadcrumb`；`md-swiper--wide` 主图 16:9；图文介绍；`md-comment` 时间行 + `__photos` 约 40px、一排最多五张。**本页图片默认可点预览**。不要 `md-d1--list`、不要沉浸式叠层 |
| PAGE-AD-003 向导 | `gold/desktop-wizard.html` | `md-stepper` + 分段 `md-advance`；当前步 `[data-step]` 包在 `md-d1__form` 内（套件会给步进容器双列间距，禁止裸堆字段贴死）；**数字步骤可点跳步**；最后一步才提交 |
| PAGE-AD-004 工作台 | `gold/desktop-dashboard.html` | 指标卡 `md-stat-grid`；趋势 `md-chart-ph`；下面短表 |
| PAGE-AD-005 分类 | `gold/desktop-split.html` | `md-d1--split` 左树右内容；`md-tree` `__toggle` 展开收起；点树只换右区 |
| PAGE-AD-006 设置 | `gold/desktop-settings.html` | **设置项**：开关可点；`md-set-picks` 文字/图标/图片 + 未选空圈；左图标可有可无；无极 / `data-menu` 改值 |
| PAGE-AD-010 我的/服务 | `gold/desktop-menu.html` | **功能入口**（只跳转或开抽屉/弹窗）：通栏 `md-set-group`>`md-set-row` 或 `md-set-pair`。不要 `md-d1--list`、不要一排按钮 |
| PAGE-AD-007 时间轴 | `gold/desktop-timeline.html` | `md-breadcrumb`；`md-timeline` 左竖轨右图文；点节点切高亮 |
| PAGE-AD-011 悬浮按钮（套件样例） | `gold/desktop-pod.html` | 规格点名才画到**业务页**。`md-pod md-pod--desk` 只右下、`position:fixed`。单个圆形；多个独立圆钮竖排（不要细线胶囊）。满 4 个写 `md-pod--fold` + `__toggle`（脚本也会补），点「+」错开弹出、再点收起。功能钮按下下沉/加深，不要缩放回弹。不要 `--tl/--bl`，不要 `md-fab` |
| 关系图 | `prototypes/{端}/map.html` | `ProtoMap.boot`；预览区 **375×812**；连线端口错开 + 线中 `label`；底部色线图例；拖动写入 localStorage；「导出图片」 |

## 开笔前

Read `lny-prd-master/framework-exclusions.md`。不生成已排除项的 `PAGE-*.html`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**在原型中实现或展示清单中的能力。

**输入优先级**：默认 Read 对应 `pages_prd`；无则须 `ui直出`（用户确认或台账标明）。缺规格或有 `待②`/`待③`/`待④`/`待⑤` → **本步内补链**：依次完整 Read `lny-prd-ui` / `lny-prd-api` / `lny-prd-feature` / `lny-prd-page` 的 `SKILL.md` 并落盘缺口，然后继续写 HTML。禁止自行编造规格；禁止因缺口停止本步、只把球踢回总控。

埋点：仅当规格已写明点位或 AD 字典条目时才在原型展示；**禁止自拟埋点方案**。

## 一条路径（全端静态 HTML + kit）

所有终端（MP / H5 / APP / PC / AD）均为静态 HTML。观感来自技能包 **`kit/`**。图标：闭集 `md-icons.js`；闭集没有的用 **`scripts/search-icons.py`**（技能自带，不调用 Cursor MCP）。

1. `python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}`
2. Read [`reference-kit.md`](reference-kit.md)：**高保真落地** + `index.html` 只填 `PROTO_SHELL`；单页只用 `md-*` 类；无对应类名时用该文「无类名组合」，**禁止裸 HTML**、禁止「示例 A/B」低保真夹具。
3. 业务图标：Read [`reference-icons.md`](reference-icons.md)。闭集能覆盖则 `data-icon`；否则 `search-icons.py --pick 0 --name … --out …/assets`。
4. 壳层行为（状态演示 / 规格说明 / 缩放 / 关系图）见 [`reference-shell.md`](reference-shell.md)。每批末按 [`reference-scope.md`](reference-scope.md) 覆盖刷新 `prototypes/index.html`（含页底右下 SKILL 标注）。各端 `index.html` 的同类标注由 `proto-shell.js` 注入，禁止手写。

**禁止**：初始化 npm/Vite/React；查询 mui-mcp；调用 `user-search-iconfont-mcp`（改用本技能 `search-icons.py`）；页内自造主题色、手绘图标 path 或第二套组件 CSS。

## 金样怎么用（视觉下限，不是功能清单）

金样只做一件事：**方便快速对标，保证视觉效果下限**（密度、图文比例、套件类名、顶栏/底栏结构）。不是业务功能清单，也不是可以跳过的参考图。

禁止两个极端：

1. **照搬功能**：金样表单铺了全套控件就把样例整页搬进业务页。点图预览 **只默认给详情页图片和横卡多行卡内图**；不要给封面叠字 / 双列 / Banner / 表单上传加灯箱。一页铺齐控件只在本页规格写了才用。
2. **忽略金样**：按 ASCII 画空盒子、比金样更瘦、不 Read 对应金样。未 Read 金样 = 本页未完成。

该对标的：分区疏密、卡片形态与图文比例（叠字/瓷砖可横可竖或定宽随图；横卡左图 1:1 或竖图；详情非列表图 16:9）、Chip / 面包屑 / 横卡、`md-*` 类名、本页规格需要的控件行为（轮盘 / 下拉 / 签）。
不该搬的：夹具商品名与跳转、套件样例才有的演示交互。

真实项目没有样例店可看时，模型会按 ASCII 线框画出空盒子。用 `gold/` 钉死视觉下限，用 [`reference-mobile-design.md`](reference-mobile-design.md) 钉死审美必做，再用舒适默认抬高：

1. 写页前：Read [`gold/README.md`](gold/README.md) → Read **本页类型**金样全文 → **按视觉骨架落地**（类名与密度不得低于金样）。禁止凭记忆、禁止按 ASCII 从零画。
2. 只替换业务文案、条数、跳转、本页规格里的分区。规格需要的套件行为要保留（轮盘 `data-wheel`、`data-menu` 更多、页内签 `data-panel`）。规格没有的金样演示交互不要搬；换业务时禁止把本页需要的 JS 删成静态壳。
3. ASCII = 分区顺序；金样 = 视觉密度。功能以本页规格为准。`ui/PAGE`「视觉细节」只给 ⑨ 估点，⑥ 视觉不降档。触屏 §1.3.3；桌面 D1-1 §1.4.3。
4. **舒适默认（§2.3 漏写也要落地）**：按 `lny-prd-ui` **§1.7.0**。骨架、空态插图、失败可重试、一个主按钮、按下态、浮层过渡、D1-1 语义列宽+`md-d1--list`、评论时间行+附图约 40px、一排最多五张。禁止发明新跳转/新字段/新弹窗。**有字段时必须按层级排版**。用户未给设计规范 ≠ 可以画线框。点图预览只默认给详情页与横卡多行，不是凡图都预览。
5. 重画不得删 Chip / 面包屑 / 横卡 / `data-icon` / `md-dialog`。未 Read 金样 = 本页未完成。
6. 不是夹具表里已有的页型：按金样表选最接近的金样（dashboard / split / settings / menu / wizard / timeline），禁止拿 `desktop-list` 硬套工作台，禁止拿一排按钮硬套功能区。

## 职责与禁止

- **负责**：按端分批生成/更新 **高保真** 原型与静态镜像；逐页对照 `pages_prd`；UTF-8 与 coverage 验收；BUG 自检。
- **禁止**：用 HTML 编造规格；改根规范或流水；交付已知 BUG；页内保留演示专用按钮（须归位状态演示）；同一轮画完超过 3 个业务页；未 Read 该页 `pages_prd` 或未 Read `gold/` 就写 HTML；按 ASCII 线框降质；把金样演示功能（如凡图即灯箱、全套表单样例）搬进规格没写的业务页；给封面叠字 / 双列 / Banner / 上传图加预览；裸 `<button>` / `<input type="submit">` 露出浏览器原生皮肤（必须 `md-btn` 等套件类）。

## 写产物纪律

先清单后落盘。含 CJK 的文件整文件 UTF-8 写入，禁止用 StrReplace 改中文块。每页写后执行 UTF-8 验收；本批全部页写完再跑 coverage。失败则重写，不得交付。细则见 [`reference-quality.md`](reference-quality.md)。

```text
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/...
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version vX.Y.Z --page PAGE-… --page PAGE-…
```

## 前置条件

已有 `main_spec.md`。若尚无 `ui_manifest` / 目标页 / `pages_prd`（且非 `ui直出`），或台账仍有 `待②`～`待⑤`：先按开笔前补链，再写原型。不要因此拒绝。

## 输入

```yaml
版本号: v1.0.0
页面编号列表: (可选；未指定则按 manifest 缺页优先，本轮仍最多 3 个)
只刷总入口: false  # ⑨ 交来或只要更新版本清单时为 true
```

## 只刷总入口

⑨ 估点落盘后、或用户只要更新总入口版本清单时走本节，**不要**走下方全量步骤。

1. Read [`reference-scope.md`](reference-scope.md)。
2. 若尚无任何 `prototypes/{终端}/`：不新建空总入口，回报「无原型可挂」并结束。
3. 覆盖写入 `prototypes/index.html`，并镜像到 `versions/{v}/prototypes/index.html`（`{v}` 取估点版本，未指定则当前工作版本）。版本清单按 **全部** `versions/` 填写。页底右下须保留 SKILL 标注（见 [`reference-scope.md`](reference-scope.md)）。
4. UTF-8 验收这两个 `index.html`。
5. **禁止**：copy-kit；改各端 `PAGE-*.html` / 端 `index.html` / `map.html`；补 ②③④⑤；把本节当成全量出原型。

## 执行步骤

若输入 `只刷总入口: true` 或由 ⑨ 交来 → 只走上一节。

1. 校验版本目录。有未清委派或缺规格 → 先补链（见开笔前），不要停。
2. 列出本轮目标页：`ui_manifest` 中 **active** 且 `prototypes/{终端}/PAGE-*.html` 尚不存在的页（用户给了 `页面编号列表` 则从其截取）。**截取最多 3 个**。其余记入「本轮不做」。
3. 复制 kit 到本批每个 `prototypes/{终端}/assets/`（续批若 assets 已齐可跳过 copy-kit）。
4. **逐页**：对该页完整 Read `pages_prd`（无则须 `ui直出`）+ `ui/PAGE-*` **§2.3** + COMP。按页类型 Read 金样全文，**对标视觉骨架**（密度/类名不得低于金样），再按本页规格换文案并落地 §2.3 与舒适默认。写完立刻过 [`reference-quality.md`](reference-quality.md) **§G.4 / G.5**。禁止凭记忆、禁止按 ASCII 降质、禁止忽略金样、禁止把金样演示功能搬进规格没写的页。
5. 按 [`reference-shell.md`](reference-shell.md) 写/刷新各端 `index.html`（及移动端 `map.html`）：**只挂已落盘**的 `PAGE-*.html`。按 [`reference-scope.md`](reference-scope.md) 写 `prototypes/index.html`。镜像到 `versions/{v}/prototypes/`（各端含 `assets/`，总入口放在该目录根下）。不写 `scope.html`。
6. 对本批页跑 UTF-8 脚本 + `verify-prototype-coverage.py` + [`reference-quality.md`](reference-quality.md) §G 自检（含 kit 引用）。任一步失败则重写，不得交付。
7. 输出：本批路径列表、验收通过说明、**剩余未生成 PAGE 编号**（无则写「全部已齐」）。有剩余时明确下一步：「继续」只续 ⑥。
