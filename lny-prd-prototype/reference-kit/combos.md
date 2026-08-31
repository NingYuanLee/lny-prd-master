# 无类名组合（reference-kit 分片）
> 本文件是 `reference-kit.md` 的分片。索引与全局 token（圆角阴影 / 高保真落地 / 间距 / 滚动容器）见 [../reference-kit.md](../reference-kit.md)。

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
