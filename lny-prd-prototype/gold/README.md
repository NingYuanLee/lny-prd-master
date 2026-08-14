# 原型视觉金样（地板，不是业务内容）

⑥ 写任何 `PAGE-*.html` **之前**必须 Read 下表对应文件，**复制骨架再换文案/条数/跳转**。

`pages_prd` 的 ASCII 线框只定**分区顺序**。金样定**控件密度与套件类名**。二者冲突时以金样为准。

金样 HTML 写 `assets/mui-kit.css`（以及 `md-icons.js` / `icons-extra.js` / `proto-page.js`）是**故意**的：复制到 `prototypes/{终端}/` 后与 `copy-kit.py` 写入的 `assets/` 对齐。禁止改成 `../kit/`，否则业务页会丢样式。本目录 `gold/assets/` 只供直接打开金样预览；改过 `kit/` 后执行：

```text
python <skillDir>/scripts/copy-kit.py <skillDir>/gold
```

| 本页类型 | 必读 |
|----------|------|
| 移动宫格 / 推荐 / 双列卡片 | `mobile-grid.html`（**沉浸式**透明状态栏 + 下沉 Banner + 金刚区） |
| 移动列表 / 动态流 / 横卡 | `mobile-list.html`（**标准**不透明状态栏 + **搜索行+筛选行贴顶** + 1:1 横卡 + 左/右半屏） |
| 移动展示 / 详情 | `mobile-detail.html`（**沉浸式**下沉 **16:9** 图 + 返回叠图上 + 图文介绍 + 评论 + 贴底次要操作） |
| 移动表单 | `mobile-form.html`（**标准**不透明状态栏 + 返回顶栏 + 输入独立成行且右侧安全距 + 五步/无极滑动条 + 下拉 + 底半屏日期/省市区三级联动 + 单图更换/多图可删/文件上传 + 贴底提交） |
| 桌面表格 / 筛选列表 / 弹窗维护 | `desktop-list.html`（内容区顶面包屑无大标题；页内签在筛选上方整区切换；分页与表横条贴底；勾选左冻 / 操作右冻定宽「更多」下拉；汇总左分页右；**列宽按字段语义**；**紧凑密度一屏多行**；隐藏骨架+插画空态） |
| 桌面整页表单 | `desktop-form.html`（内容区顶面包屑无大标题；字段 `md-field--sm`） |
| 工作台 / 仪表盘 | `desktop-dashboard.html`（`md-stat-grid` 指标卡 + `md-chart-ph` + 短表。禁止拿 `desktop-list` 硬套） |
| 树 + 内容 / 分栏 | `desktop-split.html`（`md-d1--split` 左树右内容，点树只换右区） |
| 桌面设置 | `desktop-settings.html`（分组 `md-set-group`，一行一项开关） |
| 桌面向导 | `desktop-wizard.html`（`md-stepper`，最后一步才提交） |
| 移动设置 / 偏好 | `mobile-settings.html`（分组列表，一行一项） |
| 其它桌面页 | 先按上表选最接近的金样；对不上再读 `desktop-list.html` 只借控件，禁止整页套成商品表 |
| 其它移动页 | 先读 `mobile-list.html`；宫格叠加 `mobile-grid.html`；展示/表单/设置用上表对应金样 |

复制时 **整份含 `<script>`**：轮盘 `data-wheel`、更多 `data-menu`、页内签 `data-panel` 由 `proto-page.js` 驱动，禁止删成静态壳。§2.3 漏写时仍须落地舒适默认（骨架、空态插图、失败可重试、按下态、浮层过渡、语义列宽）。

禁止：

- 按 ASCII 画出带边框的空盒子
- 因 `ui/PAGE`「视觉细节=粗糙」而少画控件
- 重画已有页时删掉 Chip、面包屑、横卡、图标、弹窗套件、金样脚本
- 从零手写一套比金样更瘦的布局
- 用 `desktop-list.html` 硬套工作台 / 树 / 设置 / 向导
