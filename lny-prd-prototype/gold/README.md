# 原型视觉金样（视觉下限，不是业务功能）

⑥ 写任何 `PAGE-*.html` **之前**必须 Read 下表对应文件，**对标视觉下限**（密度、比例、套件类名、顶栏/底栏）。金样方便快速对照，保证不画出比它更瘦的线框。

`pages_prd` 的 ASCII 线框只定**分区顺序**。金样定**控件密度与套件类名**。视觉冲突以金样为准；**功能**以本页 `pages_prd` / `ui` §2.3 / feature 为准。

**按页类型打开金样，不要按 PAGE 序号左右对齐**：`PAGE-MP-003` 是详情（`mobile-detail`），`PAGE-AD-003` 是向导（`desktop-wizard`）。完整编号对照见 `lny-prd-ui` / `lny-prd-page` / `lny-prd-prototype` 的「三步对照」。

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
| 移动展示 / 详情 | `mobile-detail.html`（含 `md-profile` 店铺资料示例；组件亦用于个人/公司资料） |
| 移动字段详情 | `mobile-fields.html`（浅灰底+白底分组；`md-desc` 左名右值；标准顶栏；非图文、非表单） |
| 移动表单 | `mobile-form.html`（**套件样例**；`md-form-page` 浅灰底+白底分组；一页铺齐触屏表单控件：文本/选择/滑动条/单日/日期段/省市区/三类上传 + 贴底提交；进度条见步骤向导） |
| 桌面列表四型 | `desktop-lists.html`（分页标准 / 分页树表 / 分组字段 / 只读树；**写列表先读**） |
| 桌面标准列表落地 | `desktop-list.html`（`PT-DESKTOP-LIST` 分页标准列表完整交互；操作列按钮数定宽；`md-cell-stack`；语义 `md-col-*`） |
| 桌面卡片列表 | `desktop-cards.html`（`md-d1--cards` + `md-card-grid`；不进四型页签） |
| 桌面页面布局 | `desktop-layout.html`（通栏/双列/三列/品字；**禁止**用 `md-d1__form` 窄双列冒充分栏） |
| 桌面整页表单 | `desktop-form.html`（**套件样例**；双列栅格有行距，`--cols-1/3` 可选。业务表单按规格裁；进度条见状态导览/向导） |
| 桌面展示 / 详情 | `desktop-detail.html`（整页浅灰+白底区块；资料卡片；灯箱分区；右下目录+回顶。禁止沉浸式） |
| 桌面字段详情 | `desktop-fields.html`（分组 `md-desc`；桌面可双列；禁止沉浸式、禁止当表单） |
| 工作台 / 仪表盘 | `desktop-dashboard.html`（`md-stat-grid` 指标卡 + `md-chart-ph` + 短表。禁止拿 `desktop-list` 硬套） |
| 树 + 内容（不分页） | `desktop-split.html`（`md-d1--split` 左树右内容；总控展开/收起/增根；节点维护与拖到上/中/下。**不是**分类钮） |
| 表内父子嵌套 | `desktop-tree-nest.html`（分页树形列表深挖；四型总览见 `desktop-lists`） |
| 定位导航（章节大纲） | `desktop-locator.html`（左大纲右全文，点左滚右；与时间轴同构；与树分离） |
| 桌面设置 | `desktop-settings.html`（**设置项**：当页当行直接操作；左图标可有可无） |
| 桌面我的 / 服务 | `desktop-menu.html`（功能入口；右可为文字或方形配图 `--thumb`） |
| 桌面向导 | `desktop-wizard.html`（`md-stepper` + 分段 `md-advance`；数字步骤可点跳步；当前步吃表单双列间距） |
| 桌面状态导览合览 | `desktop-state-flow.html`（页签 + 步骤 + 进步/进度同族说明） |
| 移动设置 / 偏好 | `mobile-settings.html`（**设置项**：当页当行直接操作；沉浸式封面顶栏；左图标可有可无） |
| 移动我的 / 服务 | `mobile-menu.html`（功能入口；右可为文字或方形配图 `--thumb`） |
| 移动步骤向导 | `mobile-wizard.html`（`md-form-page`；横向 `md-stepper` + 分段 `md-advance--lg` + 无极 `md-progress` + 当前步表单，贴底上一步/下一步） |
| 移动时间轴 | `mobile-timeline.html`（`md-timeline` 左竖轨右图文） |
| 桌面时间轴 | `desktop-timeline.html`（左节点右全文，点左滚右；属定位导航族。触屏见 `mobile-timeline`） |
| 移动按钮样例 | `mobile-buttons.html`（小/中/大三档：线框、色块、浅底 `--soft`、线框/色块/浅底置灰、带角标；页签按钮组） |
| 触屏悬浮胶囊 | `mobile-pod.html`（钉在页根、不进滚动层；左上横向且与标题栏互斥；左下/右下竖向并避开 TabBar/操作条；单个圆形、多个成组细线分割。规格点名才画，不要右上） |
| 桌面悬浮按钮 | `desktop-pod.html`（语义按共享 `PT-FLOAT`，实现用 `md-pod--desk` / `md-pod--fold`） |
| 移动树 + 内容 | `mobile-tree.html`（`md-tree-page` 左树右内容；箭头展开收起，点节点只换右区） |
| 其它桌面页 | 先按上表选最接近的金样；对不上再读 `desktop-list.html` **只借控件**，禁止整页套成商品表 |
| 其它移动页 | 先按上表选最接近的金样（设置/我的/向导/时间轴/树/详情/字段详情各有专页）；对不上再读 `mobile-list.html` **只借列表卡**，禁止整页套成商品列表 |

触屏顶栏四种（⑥ 按规格点名复制对应金样）：

1. **16:9 + slogan**：`mobile-grid.html`（`md-hero`，无页内顶栏）
2. **16:9 + 返回和标题**：`mobile-detail.html`（`md-appbar--overlay`）
3. **标准高度 + 返回和标题**：`mobile-form.html` / `mobile-wizard.html` / `mobile-tree.html` / `mobile-timeline.html`（`md-appbar--mobile`）
4. **两倍标准高度 + 背景 + 标题**：`mobile-settings.html`（`md-appbar--cover`）

对标时抄**视觉骨架**（类名、密度、本页规格需要的控件脚本：轮盘 `data-wheel`、更多 `data-menu`、页内签 `data-panel`）。禁止把金样演示交互整页搬来；禁止删掉本页规格需要的套件行为。§2.3 漏写时仍须落地舒适默认（骨架、空态插图、失败可重试、按下态、浮层过渡、语义列宽）。点图预览只默认给详情页与横卡多行。

禁止：

- 按 ASCII 画出带边框的空盒子
- 因 `ui/PAGE`「视觉细节=粗糙」而少画控件
- 重画已有页时删掉 Chip、面包屑、横卡、图标、弹窗套件、金样脚本
- 从零手写一套比金样更瘦的布局
- 用 `desktop-list.html` 硬套工作台 / 树 / 设置 / 我的服务 / 向导 / 详情；用 `mobile-list.html` 硬套触屏树；用金刚或一排按钮冒充列表卡单行
