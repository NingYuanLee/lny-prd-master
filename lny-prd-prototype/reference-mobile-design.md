# 移动端设计词典落地（⑥ · 套件映射）

写触屏 `PAGE-*.html` 前与 [`reference-kit.md`](reference-kit.md)、[`gold/README.md`](gold/README.md) 一起 Read。对应 ② 侧完整词典：`lny-prd-ui/reference-mobile-design.md`。

本文件把「设计原则 / 视觉 / 组件 / 布局 / 交互」落到 **可复制的类名与金样**，避免只背禁止项而画出合规但丑的页。

## 0. 审美必做（先于禁止项）

写每一页触屏 HTML 时必须做到；做不到则本页未完成：

1. **有层级**：标题 / 副文 / 元信息字重与颜色有差别（用 `__title` `__subtitle` `__text` `__meta`），不要整页一种灰字。  
2. **有节奏**：列表/表单走 `md-module` 间距；列表区点名形态，多行字段分行靠左，勿标题贴价格一团。  
3. **有反馈**：可点有按下态；等待有骨架；空有插画；轻成功 Toast、破坏性确认。  
4. **有安全距**：正文左右下+四角；标准顶栏左右贴边（不预留 96 胶囊空）；overlay/cover 可点右上才避让胶囊；搜索仅左图标。  
5. **对金样**：密度与结构不低于对应 `gold/mobile-*.html`。

规格没有的业务字段仍禁止编造；**有字段时必须按层级排版**，不得为「省事」只留标题+价格。

## 1. 原则 → 金样

| 原则 | 落地 |
|------|------|
| 清晰 | 首屏一件主事；列表搜索+筛选贴顶，卡片区单滚 |
| 一致 | 同页型抄同一金样；顶栏四选一不混用 |
| 反馈 | `md-btn` 按下；`snackbar`；`confirm`；骨架/空态 |

## 2. 视觉 → Token（已在 `mui-kit.css`）

| 维度 | 使用 |
|------|------|
| 色 | `--md-primary` 主操作；`--md-error` 价/危险；`--md-text` / `--md-text-secondary` 主/次文；功能色 success/warning/info |
| 字 | 标题 `__title`；副 `__subtitle`；摘要 `__text`；元信息 `__meta-item`（约 12px 语义） |
| 图标 | `data-icon`；元信息 14px；导航 24px |
| 间距 | `--md-space`（8px）倍数；正文 `--md-safe-*` |
| 圆角 | 桌面控件 `--md-radius`；触屏卡约 12px、缩略图 10px |

禁止页内另起主题色/第二套字体。改观感请改 `kit/` 再 `copy-kit.py`。

## 3. 组件 → 类名

| 规范里的组件 | 套件 |
|--------------|------|
| Button | `md-btn` `--contained`/`--outlined`/`--soft`/`--text`/`--link`；`--sm`/`--lg` |
| Input / Cell | `md-field`；列表区 `--cover` / `--tile` / `--row`（多行，可小图）/ `md-stack`>`md-set-row`（单行独立有缝）；非分组、可无限流；卡统一轻阴影 |
| Checkbox / Radio / Switch | `md-check` `md-radio` `md-switch` |
| Picker | `data-wheel="date|region|daterange"`；下拉 `md-select` |
| Dialog / Toast / Loading | `md-dialog`；触屏 Toast；`md-skeleton` |
| Tag / Avatar / Swipe / Progress | `md-chip`；**`md-card__tag` `--tl/--tr`**（封面角）；`md-card__thumb`；`md-swiper`；`md-progress`/`md-advance`；时间轴 `md-timeline` |
| TabBar / NavBar / 页内签 | `md-tabbar`；`md-appbar--*`；触屏页内签 `md-tabs` 按钮组（禁止下划线） |
| 悬浮胶囊 | `md-pod` 钉在页根、不进滚动层；`--tl` 横向且与标题栏互斥 / `--bl` `--br` 竖向并避开底栏。规格点名才画，不要右上 |
| 功能区 | `md-king` / `md-king--pair`（无阴影）；通栏 `md-set-group`>`md-set-row`；一行两个 `md-set-pair`；右说明可为文字或 **方形 `__thumb`**（`--thumb`，行更高） |

搜索：`md-search` = 左 `search` 图标 + `md-search__input`，无 caption、无右侧搜索按钮。

## 4. 布局与适配 → 结构

| 项 | 落地 |
|----|------|
| 设计逻辑宽 | 预览 **375**；`viewport-fit=cover` |
| 页面骨架 | 状态栏（脚本注入）+ 顶栏/Hero + `md-mobile-body` + Tab/操作条 |
| 沉浸下沉 | `md-immersive`+`md-hero`：Hero 固定底层；`md-mobile-body` > **`md-mobile-sheet` 白底** 上层滚过盖住 Banner（顶距可点穿） |
| 弹性列表卡 | `--cover` / `--tile` 可横可竖或 `--ratio-auto`；`--row` 左图仅 1:1 或竖图 / `md-stack`>`md-set-row` 单行独立有缝 |
| 安全区 | 正文 `--md-safe-l/r` 左右 16；标准顶栏左右 4（不预留 96 胶囊空）；状态栏 28 贴上边框；底栏 48 贴下边框；overlay/cover 仍避让胶囊 |
| 栅格 | 双列 `md-grid-2`（配 `--tile`）；金刚 4/5 列 |
| 树 + 内容 | `md-tree-page` + `md-split`；`md-tree` `__toggle` 展开收起，点节点只换右区 |
| 时间轴 | `md-timeline`；左竖轨 `__rail`，右图文 `md-card--row` |
| 模块间距 | L3 包 `md-module`；`md-mobile-body`/`md-mobile-sheet` 用 `--md-module-gap`（16px） |

金样索引：`gold/README.md`。

## 5. 交互与反馈 → 行为

| 场景 | API / 类 |
|------|----------|
| 按下 | 套件默认 `transform`/`filter` |
| 半屏/弹窗 | `ProtoPage.openDrawer` / `openDialog`（有过渡） |
| 点图放大阅览 | 默认只给详情页图（页根 `data-lightbox`；**轮播 / 图文 / 评论各一组**）与横卡多行卡内图（每卡一组）。封面叠字 / 双列 / Banner / 上传图不可预览 |
| 轻成功 | `ProtoPage.snackbar`（触屏居中） |
| 确认 | `ProtoPage.confirm` |
| 加载/空/失败 | `data-state` + `md-skel-host` / `md-empty` |
| 进度 | 上传/完整度 `md-progress`；分步 `md-advance`；时间轴 `md-timeline` |

禁止：依赖 hover 当唯一态；闪白瞬切浮层；空态只写「暂无数据」。

## 6. 与估点「视觉细节」的关系

`粗糙/标准/精致` **只给 ⑨ 估点**。⑥ **一律按本词典 + 金样高保真**，不得因「粗糙」少画层级、元信息槽位或舒适默认。

## 写页自检（触屏）

- [ ] Read 了本页类型金样并对标视觉下限（密度/类名不得低于金样）；规格需要的控件脚本保留；不要搬金样演示功能  
- [ ] 审美必做 5 条满足  
- [ ] 搜索/顶栏/安全距符合词典  
- [ ] 列表区/功能区与规格一致（列表：非分组无限流、`--cover` / `--tile` / `--row` / 单行独立有缝、轻阴影；功能：成组有限入口、金刚无阴影、通栏连成一片/一行两个轻阴影）  
- [ ] 加载/空/失败/按下可感知  
