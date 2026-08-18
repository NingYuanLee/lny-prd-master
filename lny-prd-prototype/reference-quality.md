# 原型写盘与 BUG 预防（§F–G）

### F. 中文 UTF-8 写盘纪律（必做，防乱码）

乱码是写盘方式问题。写后跑验收，失败则整文件重写。

#### F.1 根因与正确写盘

| 现象 | 根因 | 正确做法 | 禁止 |
|------|------|---------|------|
| 页面出现 `?`/半拉中文 | StrReplace 破坏 UTF-8 多字节中文 | 整文件 UTF-8 写入；仅改 ASCII 可用 StrReplace | StrReplace 含 CJK / >3 行区块 |
| `UnicodeDecodeError: invalid continuation byte` | 文件已是无效 UTF-8 | 从同端已验收页复制再改 | `read_text(errors='replace')` 后写回 |
| PowerShell `python -c` 失败 | Windows GBK 与 UTF-8 混用 | 中文写在 `.py` 源码内（`# -*- coding: utf-8 -*-`） | `python -c "…中文…"` / Shell heredoc |
| 原型镜像不一致 | 对主路径和镜像分次 StrReplace | 同时写 `prototypes/` + `versions/.../prototypes/`，或 `shutil.copy2` | 对两路径分别 StrReplace |

#### F.2 写后验收（必做）

```bash
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/MP/PAGE-MP-010.html <prdRoot>/versions/v1.0.0/prototypes/MP/PAGE-MP-010.html
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version v1.0.0 --page PAGE-MP-010
```

exit 0 才可继续；exit 1 不得交付，按 F.1 整文件重写（coverage 失败则按 G.4 补控件/跳转/COMP）。禁止未跑验收就汇报「已更新」；禁止把 `repair-*` 当常规步骤。

#### F.3 临时文件清理（交付前）

过程中可在 `prdRoot` 建辅助脚本（如 `scripts/`）、草稿、备份；**交付前必须删干净**（含空目录）。工具脚本始终跑 `<skillDir>/scripts/…`，不要把技能包脚本永久留在业务项目。

### G. 原型 BUG 预防规则（必守）

交付前消除已知 BUG。

#### G.1 代码变更引用检查（必做）

删除或重命名函数/变量/类/id/DOM 前，先全文件搜索引用并修复：

| 变更类型 | 须搜索 |
|---------|--------|
| 删除函数 `foo()` | `foo(` |
| 删除变量/类/id | 单词边界；`getElementById` |
| `<script src>` | 须有对应 `</script>`；Network 200；Console 无 ReferenceError |
| 新增全局调用 | `assets/` 下确有 `var XXX` / `global.XXX`；禁止凭记忆写 `ProtoApiClient` |
| 壳层菜单超出视口 | `.proto-sidebar__nav` 有 `overflow-y: auto` |

#### G.2 状态演示按钮归位（必做）

规则见 [`reference-shell.md`](reference-shell.md) 状态演示。搜索 `demo-` / `setDemo` / `mock-` / `alert('原型`；模拟后端 → 移入状态演示；用户操作保留。状态演示用套件 `.md-toggle`。

#### G.3 自检清单（逐页过）

| 序号 | 检查项 | 通过标准 |
|------|--------|---------|
| G3.1 | JS 控制台 | 无红色报错 |
| G3.2 | 渲染完整 | 无意外 `display:none` |
| G3.3 | 演示按钮归位 | 无后端模拟用的 `demo-*` / `setDemo*` |
| G3.4 | 状态演示选项 | 与 `ui/COMP-*.md` 状态矩阵逐字一致 |
| G3.5 | 链接可操作 | `href` / `location.href` / `postMessage` 有效 |
| G3.6 | UTF-8 | `verify-prototype-utf8.py` exit 0 |
| G3.7 | 版本演示标记 | 无 `v{版}` 开头的演示 id |
| G3.8 | alert 桩位 | 无 `alert('原型：…')`；接口模拟须标 `// 接口桩位-待接入` |
| G3.9 | 无重复监听 | 同一操作无全局 click + 局部 onclick 两套 |
| G3.10 | script 闭合 | 外部脚本均有 `</script>` |
| G3.11 | 全局变量存在 | `assets/` 有定义；`rg "ProtoApiClient" prototypes/` 为 0 |
| G3.12 | 侧栏可滚动 | `.proto-sidebar__nav` `overflow-y: auto` |
| G3.13 | 套件引用 | `mui-kit.css` + `md-icons.js` + `icons-extra.js`；index 另引 shell；无 `prototypes-mui-app/`；无自造主题 |
| G3.14 | 业务图标 | `data-icon` 属闭集或 extras 已 register；无手绘 path；未调 Cursor iconfont MCP |
| G3.15 | 无裸控件 | 每个 `button`/`input`/`table` 使用 `md-*`（或「无类名组合」）；无页内 `<style>`；无主题向内联 `background`/`color` |
| G3.16 | 规格对照脚本 | `verify-prototype-coverage.py --page …` exit 0 |

#### G.4 逐页对照清单（必做，未过不得交付、不得写下页）

每写一个 `PAGE-*.html` 之前，必须已经 Read 该页 `pages_prd`（`ui直出` 除外）+ `ui/PAGE-*` + 引用 COMP。对照下表逐项勾选；**G4.6 脚本失败 = 本页未完成**。

| 序号 | 对照源 | 通过标准 |
|------|--------|----------|
| G4.1 | 本页 `pages_prd` | 本页文件已 Read；未用其它页或记忆顶替 |
| G4.1b | `ui/PAGE` §2.3 | 动效/微反馈/收纳已按体验规格落地，未另发明交互 |
| G4.2 | §3 ASCII 线框与 `###` 分区 | 每个内容分区在 HTML 有对应可见区块（`data-section` 或可见标题）；禁止只画顶栏+一张空表 |
| G4.3 | 各分区「结构与控件」 | 每个按钮/输入/Tab/卡片/列均用 `md-*` 落地；套件无类名 → [`reference-kit.md`](reference-kit.md)「无类名组合」 |
| G4.4 | §4 跳转清单 | 每个目标 `PAGE-*` 有可点 `href`（本页自身与「无」除外） |
| G4.5 | `ui/COMP-*` 状态矩阵 | `data-comp` + `data-state`；`empty`/`error` 有 `.md-empty`；`loading` 有骨架（卡片态或 `md-skel-host`） |
| G4.6 | 脚本 | `verify-prototype-coverage.py` 对本页（及镜像）exit 0 |

#### G.5 高保真（必做，未过不得交付）

与估点「视觉细节」档位无关。对照 [`reference-kit.md`](reference-kit.md)「高保真落地」。

| 序号 | 检查项 | 通过标准 |
|------|--------|----------|
| G5.1 | 数据像真 | 无「示例商品 A/B」「测试数据」；名称/价格像业务数据 |
| G5.2 | 密度 | 直接执行共享 `PT-DENSITY`；不得把其中的列表门槛扩大到详情附属区或摘要短表，规格/API 明示条数优先 |
| G5.3 | 封面 | `md-media-ph--1`～`--6` 轮换，无纯灰块。灯箱默认给详情页图（页根 `data-lightbox`；轮播/图文/评论各一组）、横卡多行卡内图（每卡一组）、**单图/多图/视频上传缩略**。封面叠字 / 双列 / Banner / 文件上传不可预览 |
| G5.4 | 移动端 | 状态栏由 `proto-page.js` 注入；页根 `md-immersive` 或 `md-standard`；分区用 `md-module` + `md-section-head`；列表实现共享 `PT-MOBILE-LIST`，多行卡根必须有 `md-card--row` 且左图宽高双锁，单行用 `md-stack`>`md-set-row`；功能区明确 `md-king` / `--pair` / `md-set-group` / `md-set-pair`；详情非列表图默认 16:9；评论有时间行与最多五张约 40px 附图；有 TabBar 则无 `md-appbar`；MP 用 `md-mp` 和 `viewport-fit=cover`；悬浮控件实现共享 `PT-FLOAT` |
| G5.5 | 桌面端 | 有 `md-breadcrumb`、无页内大标题；表格有 `md-thumb`/`md-chip`；表单字段 `md-field--sm`；D1-1 用 `md-d1--list` + 语义 `md-col-*` 并实现共享 `PT-DESKTOP-LIST`；向导数字步骤可点跳步，不要只留上一步/下一步；悬浮控件实现共享 `PT-FLOAT` |
| G5.6 | 金样 | 写前已 Read `gold/` 对应文件并对标视觉下限（密度/类名不得低于金样）；未把金样演示功能（凡图即灯箱、全套表单样例）搬进规格没写的页；未给封面叠字 / 双列 / Banner / 文件上传加预览；HTML 无 `┌│└` 线框残留 |
| G5.7 | 不降质 | 重画不得删 Chip / 面包屑 / 横卡 / 图标 / `md-dialog`；不得因「粗糙」档简化 |
| G5.8 | 舒适默认 | 列表/卡片页含隐藏骨架与插画空态；失败可重试；D1-1 有 `md-d1--list` + 语义 `md-col-*`；评论有时间行和附图槽。§2.3 漏写也要落地，不算发明业务 |
| G5.9 | 金样脚本 | 本页规格需要的 `data-wheel` / `data-menu` + `md-menu--fixed` / `md-tabs--page` + `data-panel` 换业务时必须保留，禁止只剩静态壳。详情页根保留 `data-lightbox`；横卡多行图自动可预览，列表页不要整页加 `data-lightbox` |
| G5.10 | 易误套页型 | 按页类型打开金样，禁止按 MP/AD 序号对齐。工作台/树/设置/我的/向导/时间轴/桌面详情用对应金样；禁止拿 `desktop-lists` / `mobile-list` 整页硬套；禁止一排按钮冒充功能区 |
| G5.11 | SKILL 标注 | 总入口 `prototypes/index.html` 页底右下有技能包地址小字（见 `reference-scope.md`）；各端 `index.html` 由 `proto-shell.js` 注入，禁止手写或删 |
| G5.12 | 控件皮肤 | 可点操作用 `md-btn`（含 `--contained` / `--outlined` / `--soft` / `--text` / `--link`）或 `md-icon-btn` / `md-tab` / `md-menu__item` / `md-page-btn` / `md-tree__item`；无 `md-*` 的 `<button>` / `<input type="submit">` 不得交付（浏览器灰钮） |

禁止：对照未过就汇报「已更新」；把 G.3（UTF-8/控制台）当成功能齐套；按 ASCII 线框从零手写一页更瘦的布局。
