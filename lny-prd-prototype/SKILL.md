---
name: lny-prd-prototype
description: >-
  按规格生成可交互原型。全端静态 HTML + MUI 套件；图标用 kit 闭集，缺则 scripts/search-icons.py（不依赖 Cursor MCP）。
  Use when the user mentions /lny-prd-prototype, @lny-prd-prototype, 原型, prototypes.
disable-model-invocation: true
---

## 与总控的关系

本步为 **⑥ `/lny-prd-prototype`**。只写 `prototypes/` 与 `versions/.../prototypes/`（含总入口 `index.html`、各端目录）。禁止改根规格与 `iteration_notes`。缺规格时 **本步内** Read ②③④⑤ 对应 SKILL 并落盘，再写 HTML；**禁止**空中楼阁 HTML，**禁止**停下来只说「交总控」。⑦ 须用户明确要求检查。全流程见 `lny-prd-master/SKILL.md`。

# 生成原型 `/lny-prd-prototype`

## Additional resources

- 套件类名与壳数据：[`reference-kit.md`](reference-kit.md)
- 内置图标：[`reference-icons.md`](reference-icons.md)
- 壳层 / 关系图 / 缩放：[`reference-shell.md`](reference-shell.md)
- 原型总入口：[`reference-scope.md`](reference-scope.md)
- UTF-8 与 BUG 清单：[`reference-quality.md`](reference-quality.md)
- 复制套件：`scripts/copy-kit.py`
- 搜图标：`scripts/search-icons.py`
- 校验脚本：`scripts/verify-prototype-utf8.py`
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md`。不生成已排除项的 `PAGE-*.html`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**在原型中实现或展示清单中的能力。

**输入优先级**：默认 Read 对应 `pages_prd`；无则须 `ui直出`（用户确认或台账标明）。缺规格或有 `待②`/`待③`/`待④`/`待⑤` → **本步内补链**：依次完整 Read `lny-prd-ui` / `lny-prd-api` / `lny-prd-feature` / `lny-prd-page` 的 `SKILL.md` 并落盘缺口，然后继续写 HTML。禁止自行编造规格；禁止因缺口停止本步、只把球踢回总控。

埋点：仅当规格已写明点位或 AD 字典条目时才在原型展示；**禁止自拟埋点方案**。

## 一条路径（全端静态 HTML + kit）

所有终端（MP / H5 / APP / PC / AD）均为静态 HTML。观感来自技能包 **`kit/`**。图标：闭集 `md-icons.js`；闭集没有的用 **`scripts/search-icons.py`**（技能自带，不调用 Cursor MCP）。

1. `python <skillDir>/scripts/copy-kit.py <prdRoot>/prototypes/{终端}`
2. Read [`reference-kit.md`](reference-kit.md)：`index.html` 只填 `PROTO_SHELL`；单页只用 `md-*` 类。
3. 业务图标：Read [`reference-icons.md`](reference-icons.md)。闭集能覆盖则 `data-icon`；否则 `search-icons.py --pick 0 --name … --out …/assets`。
4. 壳层行为（状态演示 / 规格说明 / 缩放 / 关系图）见 [`reference-shell.md`](reference-shell.md)。轮末按 [`reference-scope.md`](reference-scope.md) 覆盖刷新 `prototypes/index.html`。

**禁止**：初始化 npm/Vite/React；查询 mui-mcp；调用 `user-search-iconfont-mcp`（改用本技能 `search-icons.py`）；页内自造主题色、手绘图标 path 或第二套组件 CSS。

## 职责与禁止

- **负责**：按端生成/更新原型与静态镜像；UTF-8 验收；BUG 自检。
- **禁止**：用 HTML 编造规格；改根规范或流水；交付已知 BUG；页内保留演示专用按钮（须归位状态演示）。

## 写产物纪律

先清单后落盘。含 CJK 的文件整文件 UTF-8 写入，禁止用 StrReplace 改中文块。写后执行：

```text
python <skillDir>/scripts/verify-prototype-utf8.py <prdRoot>/prototypes/...
```

失败则重写，不得交付。细则见 [`reference-quality.md`](reference-quality.md)。

## 前置条件

已有 `main_spec.md`。若尚无 `ui_manifest` / 目标页 / `pages_prd`（且非 `ui直出`），或台账仍有 `待②`～`待⑤`：先按开笔前补链，再写原型。不要因此拒绝。

## 输入

```yaml
版本号: v1.0.0
页面编号列表: (可选)
```

## 执行步骤

1. 校验版本目录。有未清委派或缺规格 → 先补链（见开笔前），不要停。
2. Read 相关规格与（默认）`pages_prd`；核对未触碰「明确不做」。
3. 复制 kit 到本批每个 `prototypes/{终端}/assets/`。
4. 按 [`reference-kit.md`](reference-kit.md) 写单页（图标见 [`reference-icons.md`](reference-icons.md)）；按 [`reference-shell.md`](reference-shell.md) 写各端 `index.html`（及移动端 `map.html`）；按 [`reference-scope.md`](reference-scope.md) 写 `prototypes/index.html`；镜像到 `versions/{v}/prototypes/`（各端含 `assets/`，总入口放在该目录根下）。不写 `scope.html`。
5. UTF-8 脚本验收 + [`reference-quality.md`](reference-quality.md) §G 自检（含 kit 引用）。
6. 输出路径列表；附验收通过说明。
