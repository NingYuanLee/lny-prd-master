# 组件速查（reference-kit 分片）
> 本文件是 `reference-kit.md` 的分片。索引与全局 token（圆角阴影 / 高保真落地 / 间距 / 滚动容器）见 [../reference-kit.md](../reference-kit.md)。

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/浅底/字/链接按钮 | `md-btn md-btn--contained` / `--outlined` / **`--soft`（无边框浅底色字）** / `--text` / **`--link`（纯文字无线框无背景，查看更多/了解全部）**；`--sm` `--lg`；置灰 `disabled`；角标内嵌 `md-badge`。**`--text`/`--link` 字色须区别紧邻正文**（默认主色，禁止跟正文同色） |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](../reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input`；不可编辑一项即可：`md-field--readonly` + `readonly` 或 `disabled`（**视觉相同、灰底淡字**）。日期段 `readonly` 触发器不要加 `--readonly` |
| 卡片 | `md-card` **`--cover` / `--tile`（可横可竖或 `--ratio-auto` 定宽随图）`--row`（左图仅 1:1 或竖图 `--ratio-3x4/2x3`；字段少因值长再加 `--long`）**；列表单行 `md-set-row`。`md-card__media` `md-card__leading` `--avatar` `md-card__body` `md-card__main` `md-card__title` `md-card__subtitle` `md-card__text` `md-card__chips` `md-card__rail` `md-card__aside` `md-card__dist` `md-card__actions` `--bar` `md-card__time` `md-card__foot` `md-card__meta` `md-card__photos` `md-card__photo` `md-card__tag` `--tl/--tr` `md-price` |
| 资料卡片 | `md-profile`（店铺/个人/公司；**默认平铺**无圆角/轻阴影）；**最精简**=仅 `__head`（`__media` + `__title` + `__subtitle`）；完整再加 `__side` / `__meta` / `__tags` / `__stats` / `__foot`；**页顶**加 `--top` |
| 详情页 | 页根 `md-detail-page`（整页浅灰）；内容壳透底；标题/图文 **白底区块**、间隙露灰；`md-detail-head`；`md-article` 四级标题；短段不缩进、大段 `__body` 缩进、多项目 `__list`；`__figures--1/2`+居中 `__caption`+表格可横滑；**评论列表卡**；可嵌平铺 **资料卡片**；触屏溢出长页默认右下导航（至少 2 个有标题分区才含目录，短页不注入）；桌面 **`md-split--outline-right` 右定宽目录** |
| 字段详情 | 同 `md-detail-page` 壳；分组 `md-module`+`md-section-head`；`md-desc` 左名右值（`--stack` 上下、桌面 `--cols-2/3`、跨列 `--span`）；金样 `mobile-fields` / `desktop-detail` 字段签 |
| 分区 / 模块 | `md-module`（L3，模块间距 `--md-module-gap`）；**列表/表单/详情等须区分的内容分区**才加 `md-section-head` + `md-section-head__title`（产品文案）；**金刚/通栏/服务条等功能区默认不加**（§1.3.5 / 金样 `mobile-grid` 金刚 module） |
| 系统栏 | `md-status-bar`（`proto-page.js` 固定顶注入；页内禁止手写；时间/信号靠顶略放大，左右各收一个图标身位，不为胶囊留空） |
| 触屏顶栏 | L1 无栏+自定义顶区 · L2 `--center` 居中无返回 · L3 `--overlay` 透明滚变实 · L4 无栏+`md-pod--tl` · L5 标准返回+左标题 · L6 `--cover` 双层封面 |
| 桌面面包屑 | `md-breadcrumb`（D1 内容区顶部，禁止再写 `md-page-head`） |
| 操作列 | 阈值与收纳执行 `PT-DESKTOP-LIST`。`md-col-actions` **按直出按钮形态+数量钉 px 列宽**（colgroup + `--md-col-actions-w`；表头 th 与 td 同宽；`ProtoPage.syncActionColWidths` 按图标 28px / 文字钮测字宽取各行 max，**不随浏览器 resize 变化**；tbody 变更才重算）；常规动作 `md-icon-btn` + `title`/`aria-label`；删除加 `md-icon--danger`；「更多」用 `data-menu` + `md-menu md-menu--fixed`（`md-select-wrap` 不计子节点档位） |
| 语义列宽 | `md-col-check` 勾选；`md-col-name` 名称硬锁定宽；`md-col-label` 长分类标题/值（136–160px）；`md-col-desc` / `md-col-note` 说明吃剩余；`md-col-date` / 最后数据列规则同前；`md-col-price` / `md-col-status` / `md-col-id` / `md-col-num`。**多字段单元格**用 `md-cell-stack`（`__primary` / `__secondary`）。长值省略不得溢出叠邻列；悬停看全文、点击复制 |
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
| 纸面/表格 | `md-paper`（内含平铺 `md-set-group` 时加 `md-paper--clip` 裁住圆角）`md-table` `md-table-wrap` `md-col-check` `md-col-name` `md-col-label` `md-col-desc` `md-col-note` `md-col-price` `md-col-status` `md-col-date` `md-col-actions` `md-pagination` `md-page-btn` |
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
