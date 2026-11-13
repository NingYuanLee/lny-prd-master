# 原型写盘与 BUG 预防（§F–G）

### F. 中文 UTF-8 写盘纪律（必做，防乱码）

乱码是写盘方式问题。写后跑验收，失败则整文件重写。

#### F.1 根因与正确写盘

| 现象 | 根因 | 正确做法 | 禁止 |
|------|------|---------|------|
| 页面出现 `?`/半拉中文 | StrReplace 破坏 UTF-8 多字节中文 | 整文件 UTF-8 写入；仅改 ASCII 可用 StrReplace | StrReplace 含 CJK / >3 行区块 |
| `UnicodeDecodeError: invalid continuation byte` | 文件已是无效 UTF-8 | 从同端已验收页复制再改 | `read_text(errors='replace')` 后写回 |
| PowerShell `python -c` 失败 | Windows GBK 与 UTF-8 混用 | 中文写在 `.py` 源码内（`# -*- coding: utf-8 -*-`） | `python -c "…中文…"` / Shell heredoc |
| 出现版本原型副本 | 旧流程或 Agent 自创镜像 | 只写根 `prototypes/`；历史回看用 Git commit/tag | 写 `versions/{v}/prototypes/`；根与版本目录双写 |

#### F.2 写后验收（必做）

```bash
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/MP/PAGE-MP-010.html
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version v1.0.0 --page PAGE-MP-010
node <skillDir>/scripts/verify-prototype-browser.mjs <prdRoot> --page PAGE-MP-010
```

前两项 exit 0 才可继续；exit 1 不得交付，按 F.1 整文件重写（coverage 失败则按 G.4 补控件/跳转/COMP）。浏览器脚本检查真实渲染、离线资源、控制台、横向溢出、截图非空及常见交互；exit 1 必须修复，exit 2 仅表示宿主缺 `playwright` / `pngjs`，须披露未执行并人工预览。依赖只装在宿主或技能仓库，禁止在业务 `prdRoot` 初始化 npm。禁止未跑验收就汇报「已更新」；禁止把 `repair-*` 当常规步骤。

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

规则见 [`reference-shell.md`](reference-shell.md) 状态演示。搜索 `demo-` / `setDemo` / `mock-` / `alert('原型`；模拟后端 → 移入状态演示；用户操作保留。状态演示用壳层提供的开关控件。

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
| G3.13 | 资源引用 | `mui-kit.css` + `md-icons.js` + `icons-extra.js` + `proto-page.js`；index 另引 shell；无 `prototypes-mui-app/`；无 `versions/` 副本 |
| G3.14 | 业务图标 | `data-icon` 属闭集或 extras 已 register；未调 Cursor iconfont MCP（项目自有图标素材不受限） |
| G3.15 | 无裸控件 | 可点操作的 `button` / `input type="submit"` 不得露出浏览器原生皮肤；套件类与项目自有样式均可 |
| G3.16 | 规格对照脚本 | `verify-prototype-coverage.py --page …` exit 0 |
| G3.17 | 浏览器冒烟 | 宿主依赖可用时，`verify-prototype-browser.mjs --page …` exit 0；失败截图写系统临时目录，不污染业务项目 |

#### G.4 逐页对照清单（必做，未过不得交付、不得写下页）

每写一个 `PAGE-*.html` 之前，必须已经 Read 该页 `pages_prd`（`ui直出` 除外）+ `ui/PAGE-*` + 引用 COMP。对照下表逐项勾选；**G4.6 脚本失败 = 本页未完成**。

| 序号 | 对照源 | 通过标准 |
|------|--------|----------|
| G4.1 | 本页 `pages_prd` | 本页文件已 Read；未用其它页或记忆顶替 |
| G4.1b | `ui/PAGE` §2.3 | 动效/微反馈/收纳已按体验规格落地，未另发明交互 |
| G4.2 | §3 ASCII 线框与 `###` 分区 | 每个内容分区在 HTML 有对应区块；`data-section` 即足够。Markdown `###` 只用于编写结构，不自动成为可见文案；仅当 §2.3 /「结构与控件」明确声明准确的用户可见标题时才渲染该标题，禁止只为通过校验添加区块标题；禁止只画顶栏+一张空表 |
| G4.3 | 各分区「结构与控件」 | 每个按钮/输入/Tab/卡片/列均已落地；可用套件类名，也可用项目自有样式 |
| G4.4 | §4 跳转清单 | 每个目标 `PAGE-*` 有可点 `href`（本页自身与「无」除外） |
| G4.5 | `ui/COMP-*` 状态矩阵 | `data-comp` + `data-state`；`empty`/`error` 有空态标记；`loading` 有骨架标记 |
| G4.6 | 脚本 | `verify-prototype-coverage.py` 对根 `prototypes/` 本页 exit 0 |
| G4.7 | 浏览器行为 | 宿主依赖可用时，本页浏览器冒烟 exit 0；菜单、页签、抽屉、轮盘等已有交互至少完成首个控件的真实点击验收 |

#### G.5 视觉与结构自检（必做，未过不得交付）

与估点「视觉细节」档位无关。视觉依据见 SKILL.md「视觉依据与样式边界」：优先取项目自带设计事实（PRD 正文、`ui/` 规格、既有设计稿/品牌 CSS/真实素材），没有时按 PRD 自行设计。

| 序号 | 检查项 | 通过标准 |
|------|--------|----------|
| G5.1 | 数据像真 | 无「示例商品 A/B」「测试数据」；名称/价格像业务数据 |
| G5.2 | 密度 | 直接执行共享 `PT-DENSITY`；不得把其中的列表门槛扩大到详情附属区或摘要短表，规格/API 明示条数优先 |
| G5.3 | 图片素材 | 有真实素材时用真实素材；无素材时用项目自定的占位样式。禁止把规格没写的图片预览（灯箱 / 上传缩略）加进页 |
| G5.4 | 移动端 | 状态栏由 `proto-page.js` 注入；页根声明布局形态（沉浸式 / 标准）；固定区在滚动区之外；列表按 `PT-MOBILE-LIST`；悬浮控件按 `PT-FLOAT` |
| G5.5 | 桌面端 | 有面包屑、无页内大标题；D1-1 按 `PT-DESKTOP-LIST` 实现（语义列宽、冻结、操作列定宽）；向导步骤可点跳步；悬浮控件按 `PT-FLOAT` |
| G5.6 | 视觉依据 | 视觉取自项目自带设计事实；无项目设计事实时按 PRD 自行设计；未把技能内置样例形态当默认设计 |
| G5.7 | 不残缺 | 重画不得删掉规格要求的 Chip / 面包屑 / 横卡 / 图标 / 弹窗 |
| G5.8 | 舒适默认 | 列表/卡片页含隐藏骨架与插画空态；失败可重试；D1-1 有语义列宽；评论有时间行和附图槽。§2.3 漏写也要落地，不算发明业务 |
| G5.9 | 控件行为 | 本页规格需要的轮盘 / 更多菜单 / 页内签行为必须保留，禁止只剩静态壳；图片预览按规格给，不给规格没写的预览 |
| G5.10 | 易误套页型 | 按页型选骨架；禁止拿列表页硬套工作台、拿表单窄双列冒充页面分栏、拿一排按钮冒充功能区 |
| G5.11 | SKILL 标注 | 总入口 `prototypes/index.html` 页底右下有技能包地址小字（见 `reference-scope.md`）；各端 `index.html` 由 `proto-shell.js` 注入，禁止手写或删 |
| G5.12 | 控件皮肤 | 可点操作不得使用浏览器原生 `button` / `input type="submit"`；用套件类或项目自有样式均可 |
| G5.13 | 触屏结构 | 每页恰有一个滚动容器，其唯一直接内容层放内容块；固定区在滚动容器之外；父级 gap 与块内 padding 不叠成双倍缝 |
| G5.14 | 浮层遮罩 | 每个浮层（弹窗 / 抽屉）须配对遮罩层；打开用壳层提供的方法；禁止只有白面板无遮罩、`alert()` |

禁止：对照未过就汇报「已更新」；把 G.3（UTF-8/控制台）当成功能齐套。
