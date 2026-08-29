---
name: lny-prd-iter
description: >-
  核验上一版本评审终态后，创建新版本文件夹、变更台账与委派清单；不创建或修改交付范围，不写规格正文。
  Use when the user mentions /lny-prd-iter, @lny-prd-iter, 新迭代, 版本迭代, or 变更台账.
---

## 与总控的关系

本步为 **⑩ `/lny-prd-iter`**。先只读核验当前最新版本已由 ⑧ 形成终态结论；结论为“通过”且有交付范围时还须已有有效 ⑨ SP；随后确认不存在未清台账，再创建版本壳、台账、根规范「变更记录」一行与委派清单。不创建或修改任何 `delivery_scope.md`，不写规格正文。完成后「继续」回总控走 **I2-spec / I2-page**（②③④ 同轮批跑，再 ⑤）。⑥ 仅当用户目标为演示/原型时同一轮继续。**⑦ 检查与 ⑧ 评审不自动跑**，须用户明确要求。全流程见 `lny-prd-master/SKILL.md`。

# 新迭代 `/lny-prd-iter`

## Additional resources

- 输入 YAML、台账/eval_signals/`iteration_notes` 模板：[`reference.md`](reference.md)
- 正式落点与版本目录白名单：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)

## 角色边界

| 本步只做 | 本步禁止 |
|----------|----------|
| 校验版本号，创建 `versions/{新版本号}/` | 写 `ui/` / `api/` / `feature/` 正文 |
| 只读核验前版 `delivery_scope.md` 的终态结论与未清台账 | 创建、初始化或修改任何版本的 `delivery_scope.md`（专属 ⑧） |
| 写 `iteration_notes.md` 开篇、三类 `*_changes.md`、`eval_signals.md` | 生成 `pages_prd` |
| 新增/修改页面登记 `pages_prd` 目标路径，初始状态 `待②`（② 完成后转 `待⑤`） | 更新索引/统计（留给 ②③④） |
| 根四规范「变更记录」各追加一行（版本号+简述+日期） | 声称已写规格或单页 PRD |
| 输出委派清单（②→③→④→⑤；⑥ 视演示目标；⑦⑧ 不自动） | 初始化 `v1.0.0`（属 ①）；写 `prototypes/index.html`（属 ⑥） |

**独占**：仅本步可新建高于当前最新的 `versions/{新版本号}/` 并追加变更记录行。表内版本须与 `versions/` 一一对应；同版本不得第二行。流水过滤见 master §1.1.1。

## 九类变更与委派

页面/接口/功能 × 新增/修改/废弃。②←页面台账；③←接口；④←功能；⑤←页上可感知变化（`ui_changes.md` 的 `pages_prd目标路径`，规则见 `lny-prd-page`）。废弃 = 索引标 `deprecated`，保留明细文件。

## 前置条件

已立项；`main_spec.md` 有变更记录表；当前最新版本已完成 ⑧ 评审闭环。触发时同一条消息给出 YAML 或自然语言（见 [`reference.md`](reference.md)）；版本不合法则对话修正。

## 执行步骤

落盘前 Read [`reference.md`](reference.md) 与 `lny-prd-master/reference-artifact-paths.md`。新版本目录只写本步白名单文件，禁止复制根规范或 `ui/`、`api/`、`feature/`。

1. 以 `versions/` 为准核对当前最新；新版本号须更大，否则失败。
2. **前版保底检查（只读）**：当前最新版本须存在由 ⑧ 记录的 `delivery_scope.md`。允许进入下一版本的终态仅为：`评审结论=通过` 且 `评审状态=approved`，或 `评审结论=不进入本期` 且 `评审状态=approved`；两者均要求 `产品确认项=0`、无 `open` 决策。旧文件缺 `评审结论` 时，仅在范围及所有 Feature 行均为 `approved`、计数为 0、无 `open` 决策时按“通过”兼容读取。
3. 前版结论为“通过”且范围含 `本期开发` 或 `本期下线` 时，必须存在有效 `sp_report.md`，且 FE_SP、BE_SP、合计不得为 `—`；否则停止建版并建议 ⑨。结论为“不进入本期”且范围为空时免 SP。
4. 若当前最新版本存在三类 `*_changes.md`，不得残留 `待②` / `待③` / `待④` / `待⑤`。任一保底条件不满足时不得创建目录或追加变更记录；列出缺口，并建议对应的 ⑦、⑧ 或 ⑨。缺原型只提示，不阻塞建版。
5. 解析输入为九类台账行。
6. 创建目录；按模板只写 `iteration_notes.md` 开篇、三类台账、`eval_signals.md`，明确不创建 `delivery_scope.md`。
7. 根四规范：变更记录各 +1 行；更新「文档版本」「最后更新」；**不**改索引与 §5/§6/§7。
8. 输出委派清单与路径；列出新增/修改页的 `pages_prd目标路径` 供 ⑤/⑦。该新版本完成规格与原型后，由 ⑦ 检查并建议是否发起 ⑧；⑧ 经产品确认后才创建本版本 `delivery_scope.md`，有交付范围则再执行 ⑨。

台账状态须遵守 master §1.1.3：每行只写一个状态；本步只初始化，不提前标记下游完成。
