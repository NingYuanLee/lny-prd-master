# 壳层与总入口（reference-kit 分片）
> 本文件是 `reference-kit.md` 的分片。索引与全局 token（圆角阴影 / 高保真落地 / 间距 / 滚动容器）见 [../reference-kit.md](../reference-kit.md)。

## 复制

每个终端目录执行一次（可多端并列）：

```text
python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}
```

写入 `prototypes/{终端}/assets/`：`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`proto-map.js`、`md-icons.js`；若尚无 `icons-extra.js` 则补空文件（已有 extras 不覆盖）。禁止改 kit 源文件来迁就某一页，也禁止将套件副本写到 `versions/{v}/prototypes/`。禁止生成 `serve.json`。本地预览：在 `prototypes/` 目录执行 `python -m http.server`。

## 引用（硬性）

| 文件 | 必引 |
|------|------|
| 所有 `PAGE-*.html` | `./assets/mui-kit.css` + `./assets/md-icons.js` + `./assets/icons-extra.js` + `./assets/proto-page.js` |
| `index.html` 汇总壳 | 上表 + `./assets/proto-shell.css` + `./assets/proto-shell.js`（`md-icons.js` → `icons-extra.js` → `proto-shell.js`） |
| `map.html` | `./assets/mui-kit.css` + `./assets/proto-shell.css` + `./assets/proto-map.js`；只填 `ProtoMap.boot({ project, terminal, pages, links })`，禁止手写拖拽/缩放/导出 |

禁止：页内 `<style>` 改 `--md-primary` / 另写一套按钮色；内联 `style` 仅允许布局占位（宽高/显示），不得当主题。

## `index.html`（数据驱动壳）

只填 `PROTO_SHELL`，**不要**手写侧栏/顶栏/状态演示/规格说明 DOM。右下角 SKILL 标注由 `proto-shell.js` 注入，不要写进本页 HTML。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>MP 原型</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <link rel="stylesheet" href="./assets/mui-kit.css">
  <link rel="stylesheet" href="./assets/proto-shell.css">
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
          file: "./PAGE-MP-001.html",
          stateDemo: true,
          comps: [],
          spec: {
            layout: "依据 ui/PAGE-MP-001.md …",
            comps: "COMP-001 · 商品卡片 · 状态见页内/豁免",
            apis: "API-MP-001 · 查询推荐\n进页请求；失败 Toast。",
            features: "FEATURE-001 · … · 本页关联点",
            actions: "点击 · 卡片无出页（当前演示）"
          }
        }
      ]
    };
  </script>
  <script src="./assets/md-icons.js"></script>
  <script src="./assets/icons-extra.js"></script>
  <script src="./assets/proto-shell.js"></script>
</body>
</html>
```

| 字段 | 规则 |
|------|------|
| `mode` | MP/H5/APP → `mobile`（手机框 + `fitPhoneFrame`）；PC/AD → `desktop`（iframe 铺满，无手机框） |
| `stateDemo` | 默认显示状态演示；仅当页内 TabBar/Tabs/SegmentedControl 明确承担同一 COMP 切态时才写 `false` |
| `tabBarExempt` | 已废弃兼容字段，不控制状态演示；禁止用它隐藏有 COMP 的页面 |
| `comps[].states` | 与 `ui/COMP-*.md` 状态矩阵 **逐字、按行顺序一致**；每个状态必须有页面视觉实现 |
| `spec` 五项 | 顺序固定；接口首行 `API-* · 描述`，交互另起一行 |
