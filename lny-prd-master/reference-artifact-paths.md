# 产物路径契约

所有会写 PRD 项目的步骤在列目标文件或委派子任务前 Read 本文件。这里是根规格、版本产物和原型镜像范围的单一事实源。

## 正式落点

| 归属 | 唯一正式落点 |
|------|--------------|
| 根规格 | `main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md` |
| UI 明细 | `ui/PAGE-*.md`、`ui/COMP-*.md` |
| API 明细 | `api/API-*.md`、`api/EXT-*.md` |
| Feature 明细 | `feature/FEATURE-*.md` |
| 当前原型 | `prototypes/index.html`、`prototypes/{终端}/**` |
| 版本过程 | `versions/{v}/iteration_notes.md`；迭代版可有三类 `*_changes.md` 与 `eval_signals.md` |
| 单页 PRD | `versions/{v}/pages_prd/**` |
| 原型镜像 | `versions/{v}/prototypes/**` |
| 标准工时点 | `versions/{v}/sp_report.md` |

`当前工作版本`只决定流水、台账、单页 PRD、原型镜像和标准工时点落在哪个 `versions/{v}/`，不把根规格搬进版本目录。

## 唯一允许的镜像

协议内唯一成树镜像是：

```text
prototypes/** -> versions/{v}/prototypes/**
```

同步时以 `prototypes/` 为源根，逐项保留相对路径。目标必须能解析到 `versions/{v}/prototypes/` 内；不得把不同来源的文件批量复制到 `versions/{v}/` 根。

以下均不是 LNY-PRD 产物，禁止创建或继续同步：

- `versions/{v}/main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md`
- `versions/{v}/ui/`、`api/`、`feature/`
- `versions/{v}/API-*.md`、`EXT-*.md`、`FEATURE-*.md`、`PAGE-*.md`、`COMP-*.md`
- 项目根 `index.html`、`versions/{v}/index.html`

历史项目已有上述副本时，以正式落点为事实源；不要更新副本。涉及删除或迁移时先由 ⑦ 报告，再取得用户授权交对应责任技能处理。

## 委派与写前校验

父 Agent 的 Task 提示只能列本表中的目标。不得增加 `mirror to versions/...`、双写或“以防万一”的副本要求；子技能收到冲突委派时遵守本契约并报告冲突。

落盘前把目标路径逐项归类；无法归入「正式落点」则不写。⑥ 镜像后、⑦ 检查时运行：

```text
python <checkSkillDir>/scripts/verify-artifact-paths.py <prdRoot>
```
