# 桌面 AD 常用控件（reference-kit 分片）
> 本文件是 `reference-kit.md` 的分片。索引与全局 token（圆角阴影 / 高保真落地 / 间距 / 滚动容器）见 [../reference-kit.md](../reference-kit.md)。

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
