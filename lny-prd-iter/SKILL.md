---
name: lny-prd-iter
description: >-
  创建新版本文件夹、变更台账与委派清单；不写规格正文。
  Use when the user mentions /lny-prd-iter, @lny-prd-iter, 新迭代, 版本迭代, 变更台账.
---

## 与总控的关系

本步为 **⑧ `/lny-prd-iter`**。只建版本壳、台账、根规范「变更记录」一行与委派清单。不写规格正文。完成后「继续」回总控走 **I2-spec / I2-page**（②③④ 同轮批跑，再 ⑤）。⑥ 仅当用户目标为演示/原型时同一轮继续。**⑦ 不自动跑**，须用户明确要求检查。全流程见 `lny-prd-master/SKILL.md`。

# 新迭代 `/lny-prd-iter`

## Additional resources

- 输入 YAML、台账/eval_signals/`iteration_notes` 模板：[`reference.md`](reference.md)
- 正式落点与版本目录白名单：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)

## 角色边界

| 本步只做 | 本步禁止 |
|----------|----------|
| 校验版本号，创建 `versions/{新版本号}/` | 写 `ui/` / `api/` / `feature/` 正文 |
| 写 `iteration_notes.md` 开篇、三类 `*_changes.md`、`eval_signals.md` | 生成 `pages_prd` |
| 新增/修改页面登记 `pages_prd` 目标路径，初始状态 `待②`（② 完成后转 `待⑤`） | 更新索引/统计（留给 ②③④） |
| 根四规范「变更记录」各追加一行（版本号+简述+日期） | 声称已写规格或单页 PRD |
| 输出委派清单（②→③→④→⑤；⑥ 视演示目标；⑦ 不自动） | 初始化 `v1.0.0`（属 ①）；写 `prototypes/index.html`（属 ⑥） |

**独占**：仅本步可新建高于当前最新的 `versions/{新版本号}/` 并追加变更记录行。表内版本须与 `versions/` 一一对应；同版本不得第二行。流水过滤见 master §1.1.1。

## 九类变更与委派

页面/接口/功能 × 新增/修改/废弃。②←页面台账；③←接口；④←功能；⑤←页上可感知变化（`ui_changes.md` 的 `pages_prd目标路径`，规则见 `lny-prd-page`）。废弃 = 索引标 `deprecated`，保留明细文件。

## 前置条件

已立项；`main_spec.md` 有变更记录表。触发时同一条消息给出 YAML 或自然语言（见 [`reference.md`](reference.md)）；版本不合法则对话修正。

## 执行步骤

落盘前 Read [`reference.md`](reference.md) 与 `lny-prd-master/reference-artifact-paths.md`。新版本目录只写本步白名单文件，禁止复制根规范或 `ui/`、`api/`、`feature/`。

1. 以 `versions/` 为准核对当前最新；新版本号须更大，否则失败。
2. 解析输入为九类台账行。
3. 创建目录；按模板写 `iteration_notes.md` 开篇、三类台账、`eval_signals.md`。
4. 根四规范：变更记录各 +1 行；更新「文档版本」「最后更新」；**不**改索引与 §5/§6/§7。
5. 输出委派清单与路径；列出新增/修改页的 `pages_prd目标路径` 供 ⑤/⑦。

台账状态须遵守 master §1.1.3：每行只写一个状态；本步只初始化，不提前标记下游完成。
