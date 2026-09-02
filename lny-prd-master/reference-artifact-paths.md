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
| 版本过程 | `versions/{v}/iteration_notes.md`；迭代版可有三类 `*_changes.md` 与 `eval_signals.md` |
| 产品评审决议 | `versions/{v}/delivery_scope.md`（仅⑧在产品确认后创建或更新；评审前可不存在） |
| 当前单页 PRD 工作源 | `pages_prd/{终端}/PAGE-{终端}-*.md`；桌面业务壳仅在 `pages_prd/_shell/{终端}-shell.md` |
| 已批准单页 PRD 快照 | `versions/{v}/pages_prd/{终端}/{页面路由目录}/PAGE-{终端}-*.md`（仅⑧最终“通过”确认后发布；不含 `_shell`） |
| 标准工时点 | `versions/{v}/sp_report.md` |

`当前工作版本`只决定流水、交付范围、台账、批准快照和标准工时点落在哪个 `versions/{v}/`；根 `pages_prd/` 与 `prototypes/` 始终表示当前工作状态。`delivery_scope.md` 维护本期 Feature 选择、PAGE 发布映射、产品评审与未决决策，由⑧在产品确认后落盘，不由①/⑩预建；旧版本范围与 `pages_prd/` 快照是只读历史事实，不因根工作源或 Feature 后续变化而改写。

## 单页 PRD 工作源与版本发布

- ⑤只写根 `pages_prd/`：业务页按终端平铺，以 PAGE 编号稳定寻址；不得按小程序主包/分包或前端路由组织工作源。
- ⑥与 Q-P 只读取根 `pages_prd/`，不得把版本快照当作当前原型依据。
- ⑧只有在产品确认最终“通过”后，才按 `delivery_scope.md` 的 PAGE 发布映射，把批准业务页发布到 `versions/{v}/pages_prd/`。`附条件通过`、`退回补充`、`不进入本期`均不发布页面快照。
- MP 快照目录按 `ui_manifest.md` 中批准时的完整页面路由投影；其它终端按其页面路由投影。文件名仍为 PAGE ID，文档基本信息中的路由、发布映射与快照目录须一致。
- 根 `_shell` 是跨页面当前规格，不进入任何版本快照。壳层历史依赖该版本 Git commit/tag；壳层变更可写台账和范围影响，但不得复制到 `versions/{v}/pages_prd/_shell/`。
- 快照是生成物且只读：发布后不得由⑤或⑥继续编辑。同一版本重新发布只允许发生在最终批准尚未形成前；批准后改变范围或正文须重新打开⑧，必要时进入⑩新版本。
- ⑧发布前必须通过PAGE版本范围原子性门禁：同一PAGE的本版受影响Feature不得部分纳入、部分不纳入。首版检查该页全部待发布active Feature；非首版只检查三类change文档直接登记或反查到的本版受影响Feature，上一版已批准且本期未变的Feature作为存量基线保留。
- 禁止靠裁剪快照解决本版Feature范围冲突。产品可在⑧调整范围使同页受影响Feature一致纳入/不纳入；坚持拆分则返回②③④重划页面、依赖或Feature/AC，再重走⑤→Q-S→⑥→Q-P→⑧。

## 不生成版本原型镜像

`versions/{v}/prototypes/` 不是 LNY-PRD 产物。日常生成和更新只写根 `prototypes/**`，不按版本复制 HTML、套件和图片。需要回看历史原型时使用项目 Git commit/tag；需要交付独立历史包时，由用户明确要求后另行导出，不回写 `versions/` 作日常事实源。

以下均不是 LNY-PRD 产物，禁止创建或继续同步：

- `versions/{v}/main_spec.md`、`ui_manifest.md`、`api_spec.md`、`feature_spec.md`
- `versions/{v}/ui/`、`api/`、`feature/`
- `versions/{v}/prototypes/`
- `versions/{v}/API-*.md`、`EXT-*.md`、`FEATURE-*.md`、`PAGE-*.md`、`COMP-*.md`
- 项目根 `index.html`、`versions/{v}/index.html`

允许的版本 `pages_prd/` 仅为⑧批准发布快照；其下出现 `_shell/`、未列入 PAGE 发布映射的页面、与映射路由不一致的页面，均属于路径或范围错误。

历史项目已有上述副本时，以正式落点为事实源；不要更新副本。涉及删除或迁移时先由 ⑦ 报告，再取得用户授权交对应责任技能处理。

## 委派与写前校验

父 Agent 的 Task 提示只能列本表中的目标。不得增加 `mirror to versions/...`、双写或“以防万一”的副本要求；子技能收到冲突委派时遵守本契约并报告冲突。

落盘前把目标路径逐项归类；无法归入「正式落点」则不写。⑥ 交付后、⑦ 检查时运行：

```text
python <checkSkillDir>/scripts/verify-artifact-paths.py <prdRoot>
```
