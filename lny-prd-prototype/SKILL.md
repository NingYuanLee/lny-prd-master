---
name: lny-prd-prototype
description: >-
  按规格生成高保真可交互原型。全端静态 HTML + MUI 套件；图标用 kit 闭集，缺则 scripts/search-icons.py。
  每轮最多 3 个业务页；逐页 Read pages_prd 后对照落地。Use when the user mentions
  /lny-prd-prototype, @lny-prd-prototype, 原型, prototypes.
disable-model-invocation: true
---

## 与总控的关系

本步为 **⑥ `/lny-prd-prototype`**。只写 `prototypes/` 与 `versions/.../prototypes/`（含总入口 `index.html`、各端目录）。禁止改根规格与 `iteration_notes`。缺规格时 **本步内** Read ②③④⑤ 对应 SKILL 并落盘，再写 HTML；**禁止**空中楼阁 HTML，**禁止**停下来只说「交总控」。⑨ 交来时只走「只刷总入口」，禁止升级成全量出原型。⑦ 须用户明确要求检查。全流程见 `lny-prd-master/SKILL.md`。

**分批硬顶**：本轮最多生成/重画 **3** 个业务 `PAGE-*.html`（不含各端 `index.html` / `map.html` / 总入口）。未完成的 PAGE 列出编号，下一轮「继续」只续 ⑥（总控 **G-partial**），禁止借机重做 ②③④⑤，禁止同一轮把全部页画完。

# 生成原型 `/lny-prd-prototype`

## Additional resources

- 套件类名与壳数据：[`reference-kit.md`](reference-kit.md)
- 内置图标：[`reference-icons.md`](reference-icons.md)
- 壳层 / 关系图 / 缩放：[`reference-shell.md`](reference-shell.md)
- 原型总入口：[`reference-scope.md`](reference-scope.md)
- UTF-8 与 BUG / 逐页对照：[`reference-quality.md`](reference-quality.md)
- 复制套件：`scripts/copy-kit.py`
- 搜图标：`scripts/search-icons.py`
- UTF-8 校验：`scripts/verify-prototype-utf8.py`
- 规格对照校验：`scripts/verify-prototype-coverage.py`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md`。不生成已排除项的 `PAGE-*.html`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**在原型中实现或展示清单中的能力。

**输入优先级**：默认 Read 对应 `pages_prd`；无则须 `ui直出`（用户确认或台账标明）。缺规格或有 `待②`/`待③`/`待④`/`待⑤` → **本步内补链**：依次完整 Read `lny-prd-ui` / `lny-prd-api` / `lny-prd-feature` / `lny-prd-page` 的 `SKILL.md` 并落盘缺口，然后继续写 HTML。禁止自行编造规格；禁止因缺口停止本步、只把球踢回总控。

埋点：仅当规格已写明点位或 AD 字典条目时才在原型展示；**禁止自拟埋点方案**。

## 一条路径（全端静态 HTML + kit）

所有终端（MP / H5 / APP / PC / AD）均为静态 HTML。观感来自技能包 **`kit/`**。图标：闭集 `md-icons.js`；闭集没有的用 **`scripts/search-icons.py`**（技能自带，不调用 Cursor MCP）。

1. `python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}`
2. Read [`reference-kit.md`](reference-kit.md)：**高保真落地** + `index.html` 只填 `PROTO_SHELL`；单页只用 `md-*` 类；无对应类名时用该文「无类名组合」，**禁止裸 HTML**、禁止「示例 A/B」低保真夹具。
3. 业务图标：Read [`reference-icons.md`](reference-icons.md)。闭集能覆盖则 `data-icon`；否则 `search-icons.py --pick 0 --name … --out …/assets`。
4. 壳层行为（状态演示 / 规格说明 / 缩放 / 关系图）见 [`reference-shell.md`](reference-shell.md)。每批末按 [`reference-scope.md`](reference-scope.md) 覆盖刷新 `prototypes/index.html`。

**禁止**：初始化 npm/Vite/React；查询 mui-mcp；调用 `user-search-iconfont-mcp`（改用本技能 `search-icons.py`）；页内自造主题色、手绘图标 path 或第二套组件 CSS。

## 职责与禁止

- **负责**：按端分批生成/更新 **高保真** 原型与静态镜像；逐页对照 `pages_prd`；UTF-8 与 coverage 验收；BUG 自检。
- **禁止**：用 HTML 编造规格；改根规范或流水；交付已知 BUG；页内保留演示专用按钮（须归位状态演示）；同一轮画完超过 3 个业务页；未 Read 该页 `pages_prd` 就写 HTML。

## 写产物纪律

先清单后落盘。含 CJK 的文件整文件 UTF-8 写入，禁止用 StrReplace 改中文块。每页写后执行 UTF-8 验收；本批全部页写完再跑 coverage。失败则重写，不得交付。细则见 [`reference-quality.md`](reference-quality.md)。

```text
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/...
python <skillDir>/scripts/verify-prototype-coverage.py <prdRoot> --version vX.Y.Z --page PAGE-… --page PAGE-…
```

## 前置条件

已有 `main_spec.md`。若尚无 `ui_manifest` / 目标页 / `pages_prd`（且非 `ui直出`），或台账仍有 `待②`～`待⑤`：先按开笔前补链，再写原型。不要因此拒绝。

## 输入

```yaml
版本号: v1.0.0
页面编号列表: (可选；未指定则按 manifest 缺页优先，本轮仍最多 3 个)
只刷总入口: false  # ⑨ 交来或只要更新版本清单时为 true
```

## 只刷总入口

⑨ 估点落盘后、或用户只要更新总入口版本清单时走本节，**不要**走下方全量步骤。

1. Read [`reference-scope.md`](reference-scope.md)。
2. 若尚无任何 `prototypes/{终端}/`：不新建空总入口，回报「无原型可挂」并结束。
3. 覆盖写入 `prototypes/index.html`，并镜像到 `versions/{v}/prototypes/index.html`（`{v}` 取估点版本，未指定则当前工作版本）。版本清单按 **全部** `versions/` 填写。
4. UTF-8 验收这两个 `index.html`。
5. **禁止**：copy-kit；改各端 `PAGE-*.html` / 端 `index.html` / `map.html`；补 ②③④⑤；把本节当成全量出原型。

## 执行步骤

若输入 `只刷总入口: true` 或由 ⑨ 交来 → 只走上一节。

1. 校验版本目录。有未清委派或缺规格 → 先补链（见开笔前），不要停。
2. 列出本轮目标页：`ui_manifest` 中 **active** 且 `prototypes/{终端}/PAGE-*.html` 尚不存在的页（用户给了 `页面编号列表` 则从其截取）。**截取最多 3 个**。其余记入「本轮不做」。
3. 复制 kit 到本批每个 `prototypes/{终端}/assets/`（续批若 assets 已齐可跳过 copy-kit）。
4. **逐页**：对该页完整 Read `pages_prd`（无则须 `ui直出`）+ `ui/PAGE-*` + 引用的 `ui/COMP-*`，再按 [`reference-kit.md`](reference-kit.md) 写该页 HTML（图标见 [`reference-icons.md`](reference-icons.md)）。写完立刻过 [`reference-quality.md`](reference-quality.md) **§G.4** 对照清单；未过不得写下页。禁止凭记忆一次写多页。
5. 按 [`reference-shell.md`](reference-shell.md) 写/刷新各端 `index.html`（及移动端 `map.html`）：**只挂已落盘**的 `PAGE-*.html`。按 [`reference-scope.md`](reference-scope.md) 写 `prototypes/index.html`。镜像到 `versions/{v}/prototypes/`（各端含 `assets/`，总入口放在该目录根下）。不写 `scope.html`。
6. 对本批页跑 UTF-8 脚本 + `verify-prototype-coverage.py` + [`reference-quality.md`](reference-quality.md) §G 自检（含 kit 引用）。任一步失败则重写，不得交付。
7. 输出：本批路径列表、验收通过说明、**剩余未生成 PAGE 编号**（无则写「全部已齐」）。有剩余时明确下一步：「继续」只续 ⑥。
