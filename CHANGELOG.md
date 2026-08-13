# Changelog

## 2.2.1 — 2026-08-13

- 总控 §3：I2 / ⑦ / ⑨ / ⑧ 排在 GoalProto 之前；演示措辞不得压过未清委派或明确检查。
- ⑥ 缺规格时本步内补 ②③④⑤ 再写 HTML，禁止停下来只交总控。
- ②③④⑤⑥ 开笔过滤「明确不做」；⑦ 委派改为删超范围实现，禁止为过检查改「明确不做」列表。
- ⑤ 壳归属与预览壳「规格说明」用词对齐；⑧「继续」不自动跑 ⑦。
- README：对人补链；对 Agent 禁止用 HTML 代替规格（取代「对 Agent 不跳步」）。
- 夹具 mini-shop：补 AD `pages_prd` 与 `versions/v1.0.0/prototypes/` 镜像。

## 2.2.0 — 2026-08-13

- 总控：目标驱动静默补 ②③④⑤⑥（要原型不再拒绝跳步）；禁止静默 ⑧。
- 排除表改为立项确认的个性化 profile；未确认不得按默认表删需求。
- 立项可选「成功怎么算 / 明确不做」；禁止自拟埋点。
- ⑥ 刷新 PRD 根 `scope.html`；壳层文案改为状态演示 / 关系图 / 规格说明，并加当前页「范围说明」。不区分 audience。
- ⑦ 功能性改为规格外 / 文案 / 主路径 + 实现符合规格。
- ⑨ 可选压缩候选附录；不换算人天。

## 2.1.3 — 2026-08-13

- 技能说明书瘦身：⑧ 模板下沉 `reference.md`；⑥ 壳层 A–D 改为套件已实现（保留 §E map）；① 版本纪律去重；⑦ 估点因子改指针 ⑨；删除旧补丁工作流说明。

## 2.1.2 — 2026-08-13

- ⑥ 缺闭集图标时用技能包 `scripts/search-icons.py` 直连 iconfont 检索并写入 `assets/icons-extra.js`；不依赖 Cursor MCP。

## 2.1.1 — 2026-08-13

- ⑥ 图标改为技能包内置 `kit/md-icons.js`（`data-icon` 闭集）。

## 2.1.0 — 2026-08-13

- 原型改为全端静态 HTML；技能包新增 `lny-prd-prototype/kit/`（Material UI v5 默认主题视觉等价 CSS/壳层 JS），生成时拷到 `prototypes/{终端}/assets/`。
- 删除 `prototypes-mui-app/` / npm / mui-mcp 工程路径；⑥ 禁止另起主题。
- `examples/mini-shop` 夹具改为引用套件（含 AD D1-1 样例）。

## 2.0.0 — 2026-08-13

技能包结构与总控纪律重构。旧 PRD 项目跟版时注意：

- 交互体验 / 视觉细节：旧值 `低/中/高` 分别对应 `简单/标准/较复杂` 与 `粗糙/标准/精致`；新开页只用新枚举。
- EXT：停写「对接复杂度」；须补交互方向、业务敏感度、联调门槛（联调门槛须人工给定）。
- COMP：编号 `COMP-{三位序号}` 必填，并写入 `ui_manifest` §4「组件编号」列。
- 桌面壳 PRD：改由 **⑤** 落盘 `pages_prd/_shell/{终端编码}-shell.md`。
- 框架排除：默认 `lny-default`；换栈立项声明 `框架排除 profile: none`。

### 正确性

- 总控 §3：I2-spec / I2-page 提到 G2 之前；有未清 `待②③④⑤` 或无 `pages_prd`/`ui直出` 时拒绝先出原型。（**2.2.0 起废止「拒绝先出原型」**：对人要原型则静默补链；**2.2.1** 起 GoalProto 不得压过 I2 / ⑦。）
- 修复 `lny-prd-sp` YAML frontmatter。
- 脚本改放技能包内：`lny-prd-prototype/scripts/verify-prototype-utf8.py`、`lny-prd-ui/scripts/migrate-prd-structure.mjs`。
- 修正 L0～L5 交叉引用；`ui_manifest` 示例枚举与 PAGE 明细对齐。

### 技能写法

- 各步 SKILL 只留执行与边界；模板/权重/检查表下沉到同目录 `reference*.md`（一层）。
- `name` 统一为目录名；除 master 外 `disable-model-invocation: true`。
- 版本纪律只在 master §1.1；子技能一句指针。

### 产品

- 框架排除可配置（`framework-exclusions.md`）。
- 原型：MP/H5/APP 默认静态 HTML；仅 PC/AD 才创建 `prototypes-mui-app/`（2.1.0 已废止该工程）。
- 新增回归夹具 `examples/mini-shop/`。
