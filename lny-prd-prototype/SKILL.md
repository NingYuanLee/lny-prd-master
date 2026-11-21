---
name: lny-prd-prototype
description: >-
  按规格生成可交互原型。只对文件结构、壳层机制、产物落点与可校验性负责，视觉与交互表现以项目自身事实为准。
  全端静态 HTML，按目标页面范围一次完成并逐页验收。Use when the user mentions
  /lny-prd-prototype, @lny-prd-prototype, 原型, prototypes.
---

## 与总控的关系

本步为 **⑥ `/lny-prd-prototype`**。只写根 `prototypes/`（含总入口 `index.html`、各端目录），只读取根 `pages_prd/` 工作源，禁止读取版本快照作为当前依据，禁止生成 `versions/{v}/prototypes/`。禁止改根规格与 `iteration_notes`。缺规格时 **本步内** Read ②③④⑤ 对应 SKILL 并落盘，再经⑦/Q-S通过后写 HTML；**禁止**空中楼阁 HTML，**禁止**停下来只说“交总控”。⑨交来时只走“只刷总入口”。完成作者自检后自动进入 **⑦/Q-P**；Q-P通过才询问是否进入⑧。全流程见 `lny-prd-master/SKILL.md`。

**页面范围**：用户给出 `页面编号列表` 时，一次生成/重画该列表中的业务 `PAGE-*.html`；未指定时，一次完成 `ui_manifest` 中当前全部 active 缺页（排除项不计入）。数量不设固定上限，但每一页都必须独立读取规格并通过验收，禁止以页面较多为由合并或跳过质量门禁。因失败中断时列出未完成 PAGE，下一轮「继续」只补 ⑥（总控 **G-partial**），禁止借机重做 ②③④⑤。

# 生成原型 `/lny-prd-prototype`

## Additional resources

- 壳层 / 关系图 / 缩放：[`reference-shell.md`](reference-shell.md)
- 原型总入口：[`reference-scope.md`](reference-scope.md)
- UTF-8 与 BUG / 逐页对照：[`reference-quality.md`](reference-quality.md)
- 内置图标：[`reference-icons.md`](reference-icons.md)
- 桌面端设计词典（② 同源）：[`../lny-prd-ui/reference-desktop-design.md`](../lny-prd-ui/reference-desktop-design.md)
- 自动设计决策协议：[`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md)
- 三步职责与跨步骤不变量：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 复制套件：`<skillDir>/scripts/copy-kit.py`
- 关系图画布：`kit/proto-map.js`（`map.html` 只 boot 数据）
- 搜图标：`<skillDir>/scripts/search-icons.py`
- UTF-8 校验：`<skillDir>/scripts/verify-prototype-utf8.py`
- 规格对照校验：`<skillDir>/scripts/verify-prototype-coverage.py`
- 浏览器冒烟验收：`<skillDir>/scripts/verify-prototype-browser.mjs`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 三步对照（防错用）

先 Read [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)。本步只维护壳层结构、产物落点与 HTML 行为；跨步骤不变量（页型语义、密度、状态导览、定位导航等）以该正本为唯一事实源；本表与正本冲突时以正本为准。

**树 vs 章节列表**：写 HTML 前若页含可展开层级列表，先读 master **「树 vs 章节列表选型」**——分类/组织 → 可展开层级树；章节目录 → 父子章节列表；左分组右横卡滚联动 → 分类定位导航。三者禁止混用。

## 壳层与结构约束

本步只对 **文件结构 / 壳层机制 / 产物落点 / 可校验性** 负责；**不对“页面长什么样、怎么画”负责**。

- **R1 落点结构**：`prototypes/index.html`（唯一总入口）+ `prototypes/{终端}/PAGE-*.html` + `prototypes/{终端}/assets/` + 各端 `index.html`、`map.html`。禁止项目根 index.html、禁止 `versions/{v}/prototypes/` 副本。
- **R2 壳层资源**：`kit/` 全部资产（`mui-kit.css`、`proto-shell.css`、`proto-shell.js`、`proto-page.js`、`proto-map.js`、`md-icons.js`）与 `scripts/copy-kit.py` 保留可用；壳层仍支持 `PROTO_SHELL` 状态演示与关系图。**kit 是可选工具箱，不是强制皮肤。**
- **R3 路径规则**：本地相对路径必须带 `./`；禁绝对路径、站点根路径、裸相对名；`#` 锚点与 `https://` 外链除外。
- **R4 校验链**：`verify-prototype-utf8.py`、`verify-prototype-coverage.py`（规格对照 + 结构类检查）、`lny-prd-check/scripts/verify-artifact-paths.py`、`verify-prototype-browser.mjs`。
- **R5 纪律**：禁 npm/Vite/React、禁在业务项目装依赖、禁改根规格与 `iteration_notes`、禁 HTML 编造规格、临时文件必须清理、⑨ 只刷总入口、并行分片时主 Agent 单写共享产物。

壳层与总入口细则见 [`reference-shell.md`](reference-shell.md) 与 [`reference-scope.md`](reference-scope.md)。

## 视觉依据与样式边界

- **N1 视觉依据**：项目自带设计事实优先（PRD 正文、`ui/` 规格、既有设计稿/视觉规范/品牌 CSS/真实图片素材）；没有时按 PRD 自行设计。**禁止**把技能内置样例形态当默认设计。
- **N2 允许项目自有样式**：原型页可用项目级 CSS（如 `brand.css`）与 `assets/` 下真实图片素材，可用项目主题色；套件类名可用可不用，套件资源仍默认引用以保证壳层与状态演示可用。
- **N3 分工不变**：② 输出信息结构、交互契约和 PAGE §2.4 视觉方向契约；⑤ ASCII 只定分区顺序；⑥ 实现已确定的视觉方向，但必须满足 ⑤ 的结构与交互契约与本页规格。

## 自动设计决策与实现策略

- 进入本步后先读取 [`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md)，检查 PAGE §2.4 是否已经包含页面任务、视觉锚点、素材策略和响应式取舍。
- 缺少这些判断时，本步自动根据上游产品事实、页型规则、终端设计词典和项目现有素材补齐，并在 `prototypes/.design-decisions/PAGE-*.md` 记录默认假设。不得因为缺少概念图而停下。
- 原型默认 **HTML 优先**。页面结构、文字、组件、状态、跳转和响应式表现直接用 HTML/CSS 实现，再通过浏览器真实渲染调整。
- 概念图是可选的内部探索材料。仅在视觉方向未定且探索能改变方向时生成；主视觉、插画、纹理和建筑场景可生成独立素材。整页生图不得作为正式页面来源。
- 关键视觉元素必须有可追溯实现路径。缺少指定字体、Logo 或品牌图片时，使用可替换占位并记录，不得凭空改变页面任务或伪造最终资产；只有交付被关键资产阻塞时才询问使用者。
- 只在产品目标冲突、品牌事实冲突、关键资产不可替代或不可逆范围变化时询问使用者。常规布局、间距、边框、阴影、按钮层级和装饰收纳由本步自动决定。

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 与 `lny-prd-master/reference-artifact-paths.md`。不生成已排除项的 `PAGE-*.html`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**在原型中实现或展示清单中的能力。

**输入优先级**：默认 Read 根 `pages_prd/{终端}/{PAGE-ID}.md` 工作源；无则须 `ui直出`（用户确认或台账标明）。缺规格或有 `待②`/`待③`/`待④`/`待⑤` → **本步内补链**：只读取责任步骤的 `SKILL.md` 和相关参考，落盘缺口，执行 Q-S，通过后继续写 HTML。禁止自行编造规格；禁止因缺口停止本步、只把球踢回总控。

埋点：仅当规格已写明点位或 AD 字典条目时才在原型展示；**禁止自拟埋点方案**。

**向导 / 引导分步页（`PT-STATE-FLOW`）开笔 checklist**：

- [ ] `ui/PAGE` **步骤区**已三选一点名 + **共 N 步**（L3 只写一种）
- [ ] 业务页不得使用只用于演示的签切换面板结构（`data-wizard-panel` / `data-panel="*Wiz*"`）
- [ ] 同页只出现一种步骤指示形态（`verify-prototype-coverage.py` 会拦叠加）

## 一条路径（全端静态 HTML + kit）

所有终端（MP / H5 / APP / PC / AD）均为静态 HTML。观感由项目自身设计事实决定；套件 `kit/` 提供可用的控件与壳层能力，**可选不强制**。图标：套件闭集 `md-icons.js`；闭集没有的用 **`scripts/search-icons.py`**（技能自带，不调用 Cursor MCP）；项目自有图标素材可直接引用。**本地 URL 一律相对路径且带 `./`**：静态资源（如 `./assets/mui-kit.css`）、页面跳转与 `<a href>`（如 `./PAGE-MP-001.html`）、`iframe`/`script`/`link` 的 `src`/`href`、壳层 `PROTO_SHELL.pages[].file`、关系图 `map` 数据里的 `file` 等；禁止绝对路径、站点根路径（`/…`）或省略 `./` 的裸相对名。`#` 锚点与 `https://` 外链除外。

**本地预览**：在 `prototypes/` 目录执行 `python -m http.server`（不要用 `npx serve`，也**禁止**在业务项目生成 `serve.json`）。

1. `python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}`
2. Read `reference-shell-quick.md` 与 `reference-quality-quick.md`；复杂壳层或门禁失败时再读取完整参考；页面结构与交互契约按本页规格与 `ui/PAGE` §2.3 落地，控件可用套件类名、也可按项目自有 CSS 落地，不强制套件形态。
3. 业务图标：Read [`reference-icons.md`](reference-icons.md)。闭集能覆盖则 `data-icon`；否则 `search-icons.py --pick 0 --name … --out …/assets`。无网或接口失败时按该文选择闭集近义项并记录替代，**不中止本轮**。
4. 壳层行为（状态演示 / 规格说明 / 缩放 / 关系图）见 [`reference-shell.md`](reference-shell.md)。目标页完成后按 [`reference-scope.md`](reference-scope.md) 覆盖刷新 `prototypes/index.html`（含页底右下 SKILL 标注）。各端 `index.html` 的同类标注由 `proto-shell.js` 注入，禁止手写。

**状态机硬约束**：`PROTO_SHELL.pages[].comps[].states` 只能从对应 `ui/COMP-*.md` 的 UI 状态矩阵复制，逐字且按行顺序一致；禁止凭空补 `edit` / `disabled` / `pending` 等状态。`loading` / `empty` / `error` 必须分别落地 `data-skel-for` / `data-empty-for` 视觉实现，其它状态必须有 `data-state-for` + `data-state` 视觉块。默认显示壳层状态演示；只有页内产品控件明确承担同一 COMP 切态时才写 `stateDemo: false`，不要再用 `tabBarExempt` 隐藏有组件的页面。覆盖验收会同时检查状态矩阵、壳层枚举和页面视觉实现。

**禁止**：初始化 npm/Vite/React；查询 mui-mcp；调用 `user-search-iconfont-mcp`（改用本技能 `search-icons.py`）。

## 职责与禁止

- **负责**：按目标范围生成/更新根 `prototypes/` 下的当前原型；逐页对照 `pages_prd`；UTF-8 与 coverage 验收；BUG 自检。
- **禁止**：用 HTML 编造规格；改根规范或流水；交付已知 BUG；页内保留演示专用按钮（须归位状态演示）；因目标页较多而跳过逐页规格读取或验收；未 Read 该页 `pages_prd` 就写 HTML；把规格没写的功能画进业务页；裸 `<button>` / `<input type="submit">` 露出浏览器原生皮肤；把本轮临时文件留在业务项目里交付。

## 写产物纪律

先清单后落盘。含 CJK 的文件整文件 UTF-8 写入，禁止用 StrReplace 改中文块。每页写后执行 UTF-8 验收；全部目标页写完再跑 coverage。失败则重写，不得交付。细则见 [`reference-quality.md`](reference-quality.md)。

**工具路径**：copy-kit / 搜图标 / UTF-8 / coverage / 浏览器冒烟一律执行 **技能包** `<skillDir>/scripts/…`，不要把技能脚本永久拷进 `prdRoot`。浏览器冒烟依赖宿主可解析 `playwright` 与 `pngjs`；依赖只装在宿主或技能仓库，**禁止**为验收在业务 `prdRoot` 初始化 npm 或生成 `node_modules/`。

**临时文件清理（交付前必做）**：过程中若在 `prdRoot` 建了辅助脚本（如 `prdRoot/scripts/`）、草稿、备份、一次性生成器等，**用完后必须删干净**再交付（含空目录）。正式原型只保留根 `prototypes/`；禁止将其复制到 `versions/`。系统临时目录优先于业务根目录。

```text
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/...
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version vX.Y.Z --page PAGE-… --page PAGE-…
node <skillDir>/scripts/verify-prototype-browser.mjs <prdRoot> --page PAGE-… --page PAGE-…
```

浏览器脚本 exit 1 表示页面或交互失败，必须修复；exit 2 表示宿主缺 Node 依赖，须明确回报“浏览器冒烟未执行”并继续人工预览，不得伪报通过。截图仅在排障时用 `--artifacts <系统临时目录>` 输出，禁止写入业务项目。

## 并行分片

需要并行时完整 Read [`../lny-prd-master/reference-agent-orchestration.md`](../lny-prd-master/reference-agent-orchestration.md)。主 Agent 必须先完成目标页清单、kit、共享 assets、壳层约束和跨页跳转表；随后可按每个业务 `PAGE-*.html` 启动一个独占子任务，任务只写该页面文件并逐页对照 `pages_prd`、`ui/PAGE`、引用 COMP 与本页结构契约。共享 kit/assets、各端 `index.html`、移动端 `map.html`、`prototypes/index.html`、LINKS 汇总与浏览器整体验收由主 Agent 单写/执行。页面数超过可用并发槽时分波；无 subagent/Task 时顺序生成，质量门禁不变。

## 前置条件

已有 `main_spec.md`。若尚无 `ui_manifest` / 目标页 / 根 `pages_prd`（且非 `ui直出`），或台账仍有 `待②`～`待⑤`：先按开笔前补链并通过Q-S，再写原型。不要因此拒绝。

## 输入

```yaml
版本号: v1.0.0
页面编号列表: (可选；指定则一次完成该列表，未指定则一次完成 manifest 当前全部 active 缺页)
只刷总入口: false  # ⑨ 交来或只要更新版本清单时为 true
```

## 只刷总入口

⑨ 估点落盘后、或用户只要更新总入口版本清单时走本节，**不要**走下方全量步骤。

1. Read [`reference-scope.md`](reference-scope.md)。
2. 若尚无任何 `prototypes/{终端}/`：不新建空总入口，回报「无原型可挂」并结束。
3. 覆盖写入唯一总入口 `prototypes/index.html`。版本清单按 **全部** `versions/` 填写。页底右下须保留 SKILL 标注（见 [`reference-scope.md`](reference-scope.md)）。
4. UTF-8 验收该 `index.html`。
5. **禁止**：copy-kit；改各端 `PAGE-*.html` / 端 `index.html` / `map.html`；补 ②③④⑤；把本节当成全量出原型。

## 执行步骤

若输入 `只刷总入口: true` 或由 ⑨ 交来 → 只走上一节。

1. 校验版本目录。有未清委派或缺规格 → 先补链（见开笔前），不要停。
2. 列出本轮目标页：用户给了 `页面编号列表` 时，以其中在 `ui_manifest` 中为 **active** 的业务页为准，可生成缺页或重画已有页；未指定时，选择 `ui_manifest` 中 **active** 且 `prototypes/{终端}/PAGE-*.html` 尚不存在的全部业务页（排除项不计入）。不按数量截取。
3. 复制 kit 到目标页涉及的每个 `prototypes/{终端}/assets/`（assets 已齐可跳过 copy-kit）。
4. **逐页**：对该页完整 Read `pages_prd`（无则须 `ui直出`）+ `ui/PAGE-*` **§2.3 + §2.4** + COMP。视觉先按 PAGE §2.4 取项目设计事实（PRD 正文、`ui/` 规格、既有设计稿/品牌 CSS/真实素材），无项目设计事实时按 PRD 自行设计；结构与交互契约以 ⑤ 的分区顺序和本页规格为准。写完立刻过 [`reference-quality.md`](reference-quality.md) **§G.4 / G.5**。禁止凭记忆、禁止把规格没写的功能画进页。
5. 按 `reference-shell-quick.md` 写/刷新各端 `index.html`（及移动端 `map.html`）：**只挂已落盘**的 `PAGE-*.html`。按 [`reference-scope.md`](reference-scope.md) 写 `prototypes/index.html`。禁止写项目根 `index.html`、`versions/{v}/index.html` 或 `versions/{v}/prototypes/`，不写 `scope.html`。
6. 对全部目标页跑 UTF-8 脚本 + `verify-prototype-coverage.py` + `<checkSkillDir>/scripts/verify-artifact-paths.py` + [`reference-quality.md`](reference-quality.md) §G 自检（含 kit 引用）；宿主依赖可用时，再对全部目标 PAGE 跑 `verify-prototype-browser.mjs`。任一步失败则重写，不得交付；浏览器依赖缺失须按上文披露。
7. **清理临时文件**：删除本轮在 `prdRoot` 留下的辅助脚本/草稿/备份及空的 `scripts/` 等（见写产物纪律）；未建临时文件可跳过。
8. 作者自检全部通过后，提示用户是否执行 **⑦/Q-P**。用户明确执行后，Q-P发现纯原型问题则本步同轮修复并重跑；发现规格问题则按总控回到②③④⑤与Q-S，再更新原型。Q-P通过后输出目标页、验收结果与未完成编号，并询问产品是否进入⑧评审。


## 基础模型视觉基线

原型逐页读取 `../lny-prd-ui/reference-visual-baseline.md`。页面完成后先做一次真实渲染自检，检查首屏主次、层级、密度、横向溢出、图片比例、移动端滚动、桌面端对齐、空态和失败态。发现明显问题先修复，再报告原型完成。Q-P 仍是用户可选择的正式门禁。

## 按场景读取原型规则

常规业务页读取 `reference-page-implementation.md` 和 `reference-quality-quick.md`。只有维护壳层、总入口或关系图时读取 `reference-shell-quick.md`，只有复杂门禁或失败复核时读取完整 `reference-shell.md` 与 `reference-quality.md`。

## 产物长度

正式产物遵守 `../lny-prd-master/reference-common.md` 的产物精简规范。只写本步骤新增的事实和决策，重复内容用编号或路径引用。

