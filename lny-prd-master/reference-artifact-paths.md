# 产物路径契约

所有会写 PRD 项目的步骤在列目标文件或委派子任务前 Read 本文件。这里是根规格、版本产物和原型落点的单一事实源。

## 正式落点

| 归属 | 唯一正式落点 |
|------|--------------|
| 根规格 | `main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md` |
| UI 明细 | `ui/PAGE-*.md`、`ui/COMP-*.md` |
| API 明细 | `api/API-*.md`、`api/EXT-*.md` |
| Feature 明细 | `feature/FEATURE-*.md` |
| 当前原型 | `prototypes/index.html`、`prototypes/{终端}/**` |
| 版本过程 | `versions/{v}/iteration_notes.md`、`versions/{v}/delivery_scope.md`；迭代版可有三类 `*_changes.md` 与 `eval_signals.md` |
| 单页 PRD | `versions/{v}/pages_prd/**` |
| 标准工时点 | `versions/{v}/sp_report.md` |
| 可选集成产物 | `versions/{v}/yunxiao-plan.json`（仅用户明确要求保存云效计划时生成） |

`当前工作版本`只决定流水、交付范围、台账、单页 PRD、标准工时点和可选集成产物落在哪个 `versions/{v}/`；原型始终以根 `prototypes/` 表示当前状态。`delivery_scope.md` 只维护本期 Feature 选择、产品评审与未决决策，不保存云效实际 ID 或研发实时状态；旧版本范围是历史事实，不因根 Feature 后续变为 `deprecated` 而改写。`yunxiao-plan.json` 是由当前 PRD 确定性生成的审阅快照，不是产品事实源，也不得包含云效实际 ID、负责人或实时状态。

## 不生成版本原型镜像

`versions/{v}/prototypes/` 不是 LNY-PRD 产物。日常生成和更新只写根 `prototypes/**`，不按版本复制 HTML、套件和图片。需要回看历史原型时使用项目 Git commit/tag；需要交付独立历史包时，由用户明确要求后另行导出，不回写 `versions/` 作日常事实源。

以下均不是 LNY-PRD 产物，禁止创建或继续同步：

- `versions/{v}/main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md`
- `versions/{v}/ui/`、`api/`、`feature/`
- `versions/{v}/prototypes/`
- `versions/{v}/API-*.md`、`EXT-*.md`、`FEATURE-*.md`、`PAGE-*.md`、`COMP-*.md`
- 项目根 `index.html`、`versions/{v}/index.html`

历史项目已有上述副本时，以正式落点为事实源；不要更新副本。涉及删除或迁移时先由 ⑦ 报告，再取得用户授权交对应责任技能处理。

## 委派与写前校验

父 Agent 的 Task 提示只能列本表中的目标。不得增加 `mirror to versions/...`、双写或“以防万一”的副本要求；子技能收到冲突委派时遵守本契约并报告冲突。

落盘前把目标路径逐项归类；无法归入「正式落点」则不写。⑥ 交付后、⑦ 检查时运行：

```text
python <checkSkillDir>/scripts/verify-artifact-paths.py <prdRoot>
```
