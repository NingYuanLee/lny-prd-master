# 原型视觉金样（地板，不是业务内容）

⑥ 写任何 `PAGE-*.html` **之前**必须 Read 下表对应文件，**复制骨架再换文案/条数/跳转**。触屏另扫 [`../reference-mobile-design.md`](../reference-mobile-design.md) 审美必做。

`pages_prd` 的 ASCII 线框只定**分区顺序**。金样定**控件密度与套件类名**。二者冲突时以金样为准。

金样 HTML 写 `assets/mui-kit.css`（以及 `md-icons.js` / `icons-extra.js` / `proto-page.js`）是**故意**的：复制到 `prototypes/{终端}/` 后与 `copy-kit.py` 写入的 `assets/` 对齐。禁止改成 `../kit/`，否则业务页会丢样式。本目录 `gold/assets/` 只供直接打开金样预览；改过 `kit/` 后执行：

```text
python <skillDir>/scripts/copy-kit.py <skillDir>/gold
```

| 本页类型 | 必读 |
|----------|------|
| 移动宫格 / 推荐 / 双列卡片 | `mobile-grid.html`（**沉浸式**；`md-hero` 钉底层；`md-mobile-sheet`；`md-module`；**封面叠字** `md-card--cover` + **双列瓷砖** `md-card--tile`；金刚 5 列或 `md-king--pair`） |
| 移动列表 / 动态流 / 横卡 | `mobile-list.html`（**标准** + 搜索/筛选贴顶；**横卡** `md-card--row` / 头像 / **纯文** `--plain`+`__photos`；左/右半屏；`data-wheel="daterange"`） |
| 移动展示 / 详情 | `mobile-detail.html`（**沉浸式**；16:9 `md-hero` 钉底层 + 返回叠层；`md-mobile-sheet` 白底正文上层滚过；评论 + 贴底次要操作；点图灯箱同页一组翻页不循环） |
| 移动表单 | `mobile-form.html`（夹具 `PAGE-MP-004.html`；**套件样例**，一页铺齐触屏表单控件：文本/选择/滑动条/单日/日期段/省市区/三类上传 + 贴底提交；进度条见步骤向导） |
| 桌面表格 / 筛选列表 / 弹窗维护 | `desktop-list.html`（内容区顶面包屑无大标题；页内签在筛选上方整区切换；分页与表横条贴底；勾选左冻 / 操作右冻定宽「更多」下拉；汇总左分页右；**列宽按字段语义**；**紧凑密度一屏多行**；隐藏骨架+插画空态；筛选用 `md-field--daterange`） |
| 桌面整页表单 | `desktop-form.html`（夹具 `PAGE-AD-009.html`；**套件样例**，一页铺齐桌面表单控件：文本/选择/滑动条/单日/时间/日期段/省市区/三类上传。业务商品表单 `PAGE-AD-002` 按规格裁字段；进度条见步骤向导） |
| 桌面展示 / 详情 | `desktop-detail.html`（夹具 `PAGE-AD-008.html`；面包屑；16:9 `md-swiper--wide`；图文介绍；`md-comment` 时间行 + 附图；点图灯箱同页一组翻页不循环。禁止沉浸式叠层，禁止拿列表卡 1:1） |
| 工作台 / 仪表盘 | `desktop-dashboard.html`（夹具 `PAGE-AD-004.html`；`md-stat-grid` 指标卡 + `md-chart-ph` + 短表。禁止拿 `desktop-list` 硬套） |
| 树 + 内容 / 分栏 | `desktop-split.html`（夹具 `PAGE-AD-005.html`；`md-d1--split` 左树右内容；箭头展开收起，点树只换右区） |
| 桌面设置 | `desktop-settings.html`（夹具 `PAGE-AD-006.html`；分组 `md-set-group`，一行一项开关） |
| 桌面向导 | `desktop-wizard.html`（夹具 `PAGE-AD-003.html`；`md-stepper` + 分段 `md-advance`，最后一步才提交） |
| 移动设置 / 偏好 | `mobile-settings.html`（夹具 `PAGE-MP-006.html`；**沉浸式**；`md-appbar--cover` 两倍标题栏高度背景图+标题；分组列表一行一项） |
| 移动步骤向导 | `mobile-wizard.html`（夹具 `PAGE-MP-005.html`；横向 `md-stepper` + 分段 `md-advance--lg` + 无极 `md-progress` + 当前步表单，贴底上一步/下一步） |
| 移动时间轴 | `mobile-timeline.html`（夹具 `PAGE-MP-009.html`；`md-timeline` 左竖轨右图文） |
| 桌面时间轴 | `desktop-timeline.html`（夹具 `PAGE-AD-007.html`；面包屑 + `md-timeline` 左竖轨右图文） |
| 移动按钮样例 | `mobile-buttons.html`（夹具 `PAGE-MP-007.html`；小/中/大三档：线框、色块、线框置灰、色块置灰、带角标） |
| 移动树 + 内容 | `mobile-tree.html`（夹具 `PAGE-MP-008.html`；`md-tree-page` 左树右内容；箭头展开收起，点节点只换右区） |
| 其它桌面页 | 先按上表选最接近的金样；对不上再读 `desktop-list.html` 只借控件，禁止整页套成商品表 |
| 其它移动页 | 先读 `mobile-list.html`；宫格叠加 `mobile-grid.html`；展示/表单/设置/步骤向导/时间轴/树用上表对应金样 |

触屏顶栏四种（⑥ 按规格点名复制对应金样）：

1. **16:9 + slogan**：`mobile-grid.html`（`md-hero`，无页内顶栏）
2. **16:9 + 返回和标题**：`mobile-detail.html`（`md-appbar--overlay`）
3. **标准高度 + 返回和标题**：`mobile-form.html` / `mobile-wizard.html` / `mobile-tree.html` / `mobile-timeline.html`（`md-appbar--mobile`）
4. **两倍标准高度 + 背景 + 标题**：`mobile-settings.html`（`md-appbar--cover`）

复制时 **整份含 `<script>`**：轮盘 `data-wheel`、更多 `data-menu`、页内签 `data-panel` 由 `proto-page.js` 驱动，禁止删成静态壳。§2.3 漏写时仍须落地舒适默认（骨架、空态插图、失败可重试、按下态、浮层过渡、语义列宽）。

禁止：

- 按 ASCII 画出带边框的空盒子
- 因 `ui/PAGE`「视觉细节=粗糙」而少画控件
- 重画已有页时删掉 Chip、面包屑、横卡、图标、弹窗套件、金样脚本
- 从零手写一套比金样更瘦的布局
- 用 `desktop-list.html` 硬套工作台 / 树 / 设置 / 向导 / 详情；用 `mobile-list.html` 硬套触屏树
