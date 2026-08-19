# 原型视觉金样（视觉下限，不是业务功能）

⑥ 写任何 `PAGE-*.html` **之前**必须 Read 下表对应文件，**对标视觉下限**（密度、比例、套件类名、顶栏/底栏）。金样方便快速对照，保证不画出比它更瘦的线框。

`pages_prd` 的 ASCII 线框只定**分区顺序**。金样定**控件密度与套件类名**。视觉冲突以金样为准；**功能**以本页 `pages_prd` / `ui` §2.3 / feature 为准。

**按页类型打开金样，不要按 PAGE 序号左右对齐**：`PAGE-MP-003` 是详情（`mobile-detail`），`PAGE-AD-003` 是向导（`desktop-wizard`）。完整编号、金样文件与夹具 PAGE 对照见 [`lny-prd-master/reference-page-types.md`](../../lny-prd-master/reference-page-types.md)「mini-shop 夹具 · 金样 · 套件对照」。套件样例夹具可整页对标金样；业务夹具按规格裁（桌面列表夹具含筛+功能栏，金样六型只对标列表区）。

**库存**：触屏金样 **14** 个 `mobile-*.html`；桌面金样 **14** 个 `desktop-*.html`（含 `desktop-state-flow.html` 合览，无独立夹具）；mini-shop 各端夹具各 **14** 页；套件源 `kit/mui-kit.css` 等经 `copy-kit.py` 同步到 `gold/assets/` 与各端 `prototypes/*/assets/`。

禁止两个极端：

1. **照搬**：套件样例铺了全控件就把整页搬进业务表单。点图预览 **只默认给详情页图片和横卡多行卡内图**；不要给封面叠字 / 双列 / Banner / 表单上传加灯箱。
2. **忽略**：按 ASCII 空盒子、不 Read 对应金样、密度低于金样。未 Read = 本页未完成。

金样 HTML 写 `./assets/mui-kit.css`（以及 `md-icons.js` / `icons-extra.js` / `proto-page.js`）是**故意**的：复制到 `prototypes/{终端}/` 后与 `copy-kit.py` 写入的 `assets/` 对齐。禁止改成 `../kit/`，否则业务页会丢样式。本目录 `gold/assets/` 只供直接打开金样预览；改过 `kit/` 后执行：

```text
python <skillDir>/scripts/copy-kit.py <skillDir>/gold
```

| 本页类型 | 必读 |
|----------|------|
| 移动宫格 / 推荐 / 双列卡片 | `mobile-grid.html`（**沉浸式**；`md-hero` 钉底层；`md-mobile-sheet`；`md-module`；**封面叠字** `md-card--cover` + **双列瓷砖** `md-card--tile`；金刚 5 列或 `md-king--pair`） |
| 移动列表 / 动态流 / 横卡 | `mobile-list.html`（语义按共享 `PT-MOBILE-LIST`；多行 `md-card--row`、长值 `md-card--long`、单行 `md-stack`>`md-set-row`；左/右半屏；`data-wheel="daterange"`） |
| 移动订单列表 | `mobile-order-list.html`（顶栏返回+搜索；下划线可滚动页签+筛选遮罩；店名后 `chevron-right`；`md-card--order` 推广条/商品行价量/实付款/浅底操作） |
| 移动展示 / 详情 | `mobile-detail.html`（含 `md-profile` 店铺资料示例；组件亦用于个人/公司资料） |
| 移动字段列表 | `mobile-fields.html`（sheet safe + `md-group-list` 白卡浮灰；标准顶栏；非图文、非横卡列表、非表单） |
| 桌面字段列表 | `desktop-fields.html`（`md-d1--list` + `md-group-list` + `md-desc--cols-2`；面包屑；多条按组。六型合览见 `desktop-lists.html` 第三签；夹具 `PAGE-AD-012`） |
| 移动表单 | `mobile-form.html`（**套件样例**；`md-form-page` 浅灰底+白底分组；一页铺齐触屏表单控件：文本/选择/滑动条/单日/日期段/省市区/三类上传 + 贴底提交；进度条见步骤向导） |
| 桌面列表六型 | `desktop-lists.html`（只对标列表区：分页标准 / **分页树表** / 分组字段 / 只读树 / **分页无图卡片列表** / **分页有图卡片列表**；树表含 `md-table--nest` 嵌套行；卡片同一行等高、底栏统计分页；操作列按钮形态与数量定宽。筛区/功能栏按规格另加。夹具 `PAGE-AD-001` 是分页标准列表且含筛+功能栏） |
| 桌面页面布局 | `desktop-layout.html`（通栏/均分双列/左定右填/左填右定/三列/品字；**禁止**用 `md-d1__form` 窄双列冒充分栏。夹具 `PAGE-AD-014`） |
| 桌面整页表单 | `desktop-form.html`（**套件样例**；通栏 1～4 列栅格有行距；`md-combo` 七种下拉 + `md-select`；多图上传 80×80。业务表单按规格裁；进度条见状态导览/向导） |
| 桌面展示 / 详情 | `desktop-detail.html`（图文签 + 字段签；整页浅灰+白底区块；资料卡片；灯箱；右下目录+回顶。字段签=详情内单组 `md-desc` 排版参考。禁止沉浸式、禁止当表单。夹具图文 `PAGE-AD-008`；**字段列表** `PAGE-AD-012` → `desktop-fields.html`） |
| 工作台 / 仪表盘 | `desktop-dashboard.html`（`md-stat-grid` 指标卡 + `md-chart-ph` + 短表。禁止拿 `desktop-lists` 硬套） |
| 树 + 内容（不分页） | `desktop-split.html`（`md-d1--split` 左树右内容；总控展开/收起/增根；节点维护与拖到上/中/下。**不是**分类钮。夹具 `PAGE-AD-005`） |
| 定位导航（章节大纲） | `desktop-locator.html`（左侧可收缩 / 右侧悬浮可收起；**收起后点线轨**，滚正文当前点高亮；与树分离。夹具 `PAGE-AD-013`） |
| 桌面设置 | `desktop-settings.html`（**设置项**：当页当行直接操作；左图标可有可无） |
| 桌面我的 / 服务 | `desktop-menu.html`（**`md-svc-strip--desk`** 待办/概览条 + 功能入口；右可为文字或方形配图 `--thumb`） |
| 桌面向导 | `desktop-wizard.html`（`md-stepper` + 分段 `md-advance`；数字步骤可点跳步；当前步吃表单双列间距） |
| 桌面状态导览合览 | `desktop-state-flow.html`（页签 + 步骤 + 进步/进度同族说明） |
| 移动设置 / 偏好 | `mobile-settings.html`（**设置项**：当页当行直接操作；沉浸式封面顶栏；左图标可有可无） |
| 移动我的 / 服务 | `mobile-menu.html`（功能入口；右可为文字或方形配图 `--thumb`） |
| 移动步骤向导 | `mobile-wizard.html`（`md-form-page`；横向 `md-stepper` + 分段 `md-advance--lg` + 无极 `md-progress` + 当前步表单，贴底上一步/下一步） |
| 移动物流时间轴 | `mobile-timeline.html`（`md-timeline--static` 左竖轨右横卡文本；**仅已发生节点**、倒序、竖轨主色；夹具 PAGE-MP-009） |
| 桌面时间轴 | `desktop-timeline.html`（通栏 `md-timeline--static` 物流只读：仅已发生节点、倒序、竖轨主色；下方示例可点切换的交互轴。触屏见 `mobile-timeline`） |
| 移动按钮样例 | `mobile-buttons.html`（小/中/大三档：线框、色块、浅底 `--soft`、线框/色块/浅底置灰、带角标；页签按钮组） |
| 触屏悬浮胶囊 | `mobile-pod.html`（钉在页根、不进滚动层；左上横向且与标题栏互斥；左下/右下竖向并避开 TabBar/操作条；单个圆形、多个成组细线分割。规格点名才画，不要右上） |
| 桌面悬浮按钮 | `desktop-pod.html`（语义按共享 `PT-FLOAT`，实现用 `md-pod--desk` / `md-pod--fold`） |
| 移动分类树 | `mobile-tree.html`（`md-tree-page`；左多级树右 **图文介绍** `md-cat-intro`；点节点换右区） |
| 移动分类导航 | `mobile-locator.html`（`md-locator-page`；左一级分组右 **分组横卡**；滚动联动；对标 desktop-locator 左栏） |
| 移动树 + 内容（历史名） | 已拆为 `mobile-tree`（图文）与 `mobile-locator`（横卡导航）；勿混写 |
| 其它桌面页 | 先按上表选最接近的金样；对不上再读 `desktop-lists.html` **只借控件**，禁止整页套成商品表 |
| 其它移动页 | 先按上表选最接近的金样（设置/我的/向导/时间轴/树/详情/字段列表各有专页）；对不上再读 `mobile-list.html` **只借列表卡**，禁止整页套成商品列表 |

**触屏滚动 sheet（L2）**：凡 `md-mobile-body` 内 **必有** `md-mobile-sheet`（唯一直接子层）。**没有 sheet 的**：L1 固定区、下沉 `md-hero`、TabBar、贴底条、浮层——均在 body **外**并列。默认 sheet 带左右 safe；详情/字段/树用 `--flush-x`；表单/设置靠页根 `md-form-page` / `md-set-page` 自动 lr0。详见 `reference-kit.md`「何时有 sheet」与 `reference.md` §1.3.4。

触屏顶栏六种（⑥ 按规格点名复制对应金样）：

1. **L1 无顶栏 + 自定义顶区**（TabBar）：`mobile-grid.html`（`md-hero`）；或 `md-list-toolbar` 搜索/筛选/页签
2. **L2 居中标题**（TabBar，无返回）：`mobile-list.html`（`md-appbar--center`）
3. **L3 透明叠图 + 滚变实底**：`mobile-detail.html`（`md-appbar--overlay`）
4. **L4 无顶栏 + 左上胶囊**：`mobile-pod.html`（`md-pod--tl`，与页内顶栏互斥）
5. **L5 标准返回 + 左标题**：`mobile-form.html` / `mobile-menu.html` / `mobile-wizard.html` 等（`md-appbar--mobile`）
6. **L6 双层封面顶栏**：`mobile-settings.html`（`md-appbar--cover`，返回可选）

对标时抄**视觉骨架**（类名、密度、本页规格需要的控件脚本：轮盘 `data-wheel`、更多 `data-menu`、页内签 `data-panel`）。禁止把金样演示交互整页搬来；禁止删掉本页规格需要的套件行为。§2.3 漏写时仍须落地舒适默认（骨架、空态插图、失败可重试、按下态、浮层过渡、语义列宽）。点图预览只默认给详情页与横卡多行。

禁止：

- 按 ASCII 画出带边框的空盒子
- 因 `ui/PAGE`「视觉细节=粗糙」而少画控件
- 重画已有页时删掉 Chip、面包屑、横卡、图标、弹窗套件、金样脚本
- 从零手写一套比金样更瘦的布局
- 用 `desktop-lists.html` 硬套工作台 / 树 / 设置 / 我的服务 / 向导 / 详情；用 `mobile-list.html` 硬套触屏树；用金刚或一排按钮冒充列表卡单行
- 把 `desktop-detail` 字段签整页套成 MP-012；或把 MP-012 做成 flush 浅灰壳单对象 `md-module`
