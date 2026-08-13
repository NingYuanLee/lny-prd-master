# 原型套件（MUI 视觉等价）

生成/更新原型时 Read。套件在技能包 `lny-prd-prototype/kit/`，**禁止**另起主题、禁止 `prototypes-mui-app/`、禁止 Ant Design / Bootstrap / 页内自造皮肤。

观感对齐 **Material UI v5 默认 light theme**（primary `#1976d2`、圆角 4px、Roboto、elevation 阴影）。不是 React 运行时；类名以 `md-` / `proto-` 为准。

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。镜像 `versions/{v}/prototypes/{终端}/` 时 **须连同 `assets/`**（含 extras 与 `icons/`）。禁止改 kit 源文件来迁就某一页。

## 引用（硬性）

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | `assets/mui-kit.css` + `assets/md-icons.js` + `assets/icons-extra.js` + `assets/proto-page.js` |
| `index.html` 汇总壳 | 上表 + `assets/proto-shell.css` + `assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |
| `map.html` | 建议 `assets/mui-kit.css` 做工具栏；画布逻辑仍按 `reference-shell.md` §E |

禁止：页内 `<style>` 改 `--md-primary` / 另写一套按钮色；内联 `style` 仅允许布局占位（宽高/显示），不得当主题。

## `index.html`（数据驱动壳）

只填 `PROTO_SHELL`，**不要**手写侧栏/顶栏/状态演示/规格说明 DOM。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>MP 原型</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="assets/mui-kit.css">
  <link rel="stylesheet" href="assets/proto-shell.css">
</head>
<body>
  <div id="proto-root"></div>
  <script>
    window.PROTO_SHELL = {
      terminal: "MP",
      mode: "mobile",
      title: "小程序原型",
      pages: [
        {
          id: "PAGE-MP-001",
          name: "首页",
          module: "首页",
          file: "PAGE-MP-001.html",
          tabBarExempt: true,
          comps: [],
          spec: {
            layout: "依据 ui/PAGE-MP-001.md …",
            comps: "COMP-001 · 商品卡片 · 状态见页内/豁免",
            apis: "API-MP-001 · 查询推荐\n进页请求；失败 Toast。",
            features: "FEATURE-001 · … · 本页关联点",
            actions: "点击 · 卡片无出页（夹具）"
          },
          brief: "首页展示推荐商品，可从底栏进入商品列表。"
        }
      ]
    };
  </script>
  <script src="assets/md-icons.js"></script>
  <script src="assets/icons-extra.js"></script>
  <script src="assets/proto-shell.js"></script>
</body>
</html>
```

| 字段 | 规则 |
|------|------|
| `mode` | MP/H5/APP → `mobile`（手机框 + `fitPhoneFrame`）；PC/AD → `desktop`（iframe 铺满，无手机框） |
| `tabBarExempt` | 页内已有 TabBar/Tabs 承担 COMP 切态时 `true`，壳层隐藏状态演示 |
| `brief` | 当前页范围说明（人话，无 API 编号） |
| `comps[].states` | 与 `ui/COMP-*.md` 状态矩阵 **逐字一致** |
| `spec` 五项 | 顺序固定；接口首行 `API-* · 描述`，交互另起一行 |

## 单页类名（只许用这些，禁止自造皮肤类）

**桌面 D1-1**

```html
<div class="md-d1">
  <div class="md-d1__search">
    <label class="md-field md-field--sm">
      <span class="md-field__label">商品名称</span>
      <input class="md-field__input" type="text">
    </label>
    <button type="button" class="md-btn md-btn--contained">查询</button>
  </div>
  <div class="md-toolbar md-toolbar--dense"></div>
  <div class="md-d1__table">
    <div class="md-table-wrap">
      <table class="md-table">…</table>
    </div>
  </div>
  <div class="md-d1__footer">
    <span class="md-caption">共 2 条</span>
    <nav class="md-pagination">
      <button type="button" class="md-page-btn is-active">1</button>
    </nav>
  </div>
</div>
```

**移动页**

```html
<div class="md-mobile-page">
  <header class="md-appbar md-appbar--mobile">
    <div class="md-appbar__title">首页</div>
  </header>
  <main class="md-mobile-body">…</main>
  <nav class="md-tabbar">
    <a class="is-active" href="PAGE-MP-001.html">
      <span class="md-icon" data-icon="home" aria-hidden="true"></span>
      <span>首页</span>
    </a>
    <a href="PAGE-MP-002.html">
      <span class="md-icon" data-icon="goods" aria-hidden="true"></span>
      <span>商品</span>
    </a>
  </nav>
</div>
<script src="assets/md-icons.js"></script>
<script src="assets/icons-extra.js"></script>
<script src="assets/proto-page.js"></script>
```

**COMP 切态**（iframe 内）

```html
<article class="md-card" data-comp="COMP-001" data-state="default">…</article>
<p class="md-empty is-hidden" data-empty-for="COMP-001"></p>
```

壳层 `postMessage({ type:'comp-state', compId, state })` 由 `proto-page.js` 写到 `data-state`。`loading` 显示骨架；`empty`/`error` 隐藏卡片并显示 `.md-empty`。

## 组件速查

| 用途 | 类名 |
|------|------|
| 主/线/字按钮 | `md-btn md-btn--contained` / `--outlined` / `--text`；`--sm` `--lg` |
| 图标 | `span.md-icon` + `data-icon`（闭集见 [`reference-icons.md`](reference-icons.md)） |
| 图标按钮 | `md-icon-btn` 内放 `span.md-icon` |
| 输入 | `md-field` + `md-field__label` + `md-field__input` |
| 卡片 | `md-card` `md-card__media` `md-card__body` `md-card__title` `md-price` |
| 纸面/表格 | `md-paper` `md-table` `md-pagination` `md-page-btn` |
| 弹窗 | `md-backdrop` + `md-dialog`（`is-open`）；`ProtoPage.openDialog(id)` |
| Toast | `ProtoPage.snackbar('…')` |
| 状态组 | `md-toggle md-toggle--vert`（状态演示已内置） |
| Chip/Alert | `md-chip` `md-alert md-alert--error` |

D5 弹窗用 `md-dialog`，禁止 `alert('原型：…')`。
