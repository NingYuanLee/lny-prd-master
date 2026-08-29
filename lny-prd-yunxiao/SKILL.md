---
name: lny-prd-yunxiao
description: >-
  只读校验 LNY-PRD 交付范围并生成云效工作项导出计划，不创建或修改云效工作项。
  Use when the user mentions /lny-prd-yunxiao, @lny-prd-yunxiao, 云效导出, 云效需求映射, Yunxiao plan.
---

# 云效导出适配器 `/lny-prd-yunxiao`

这是十步 LNY-PRD 工作流之外的**可选集成技能**。它读取稳定的产品来源编号，校验本期交付门禁，并生成可审阅的云效工作项计划；不改变 PRD 产品事实，不承担实时研发状态管理。

## Additional resources

- 输入契约：[`references/lny-prd-input-contract.md`](references/lny-prd-input-contract.md)
- 工作项计划结构：[`references/yunxiao-work-item-schema.md`](references/yunxiao-work-item-schema.md)
- 默认映射与覆盖方式：[`references/mapping-policy.md`](references/mapping-policy.md)
- 计划生成器：`scripts/build-yunxiao-plan.py`
- 计划结构校验器：`scripts/validate-export-plan.py`

## 边界

- **负责**：选择显式版本；读取 `delivery_scope.md` 或用户显式 Feature 清单；执行导出门禁；为 `本期开发` 生成更新计划、为 `本期下线` 生成关闭计划；生成稳定、确定性的 JSON 工作项树。
- **禁止**：调用云效写接口；创建、更新、关闭工作项；把云效实际 ID、负责人或实时状态回写 PRD；默认导出全部 active Feature；把本技能称为第十步。
- **公司角色契约**：`API-*` / `EXT-*` / `PAGE-AD-*` → `BE`；其余客户端 `PAGE-*` → `MP`；每个 Feature → `TEST`。云效 `MP` 对应 ⑨ SP 口径中的 `FE`，但适配器只改任务面名称，不改 `FE_SP`，也不生成 `FE` 任务。
- PRD 保存产品事实与来源 ID；云效保存实际工作项、负责人和研发状态；Git 保存提交与发布关联。

## 执行方式

工作目录为 PRD 根目录。默认 `plan`；未指定版本时选择 `versions/` 中最大 semver。

```text
python <skillDir>/scripts/build-yunxiao-plan.py <prdRoot> --mode validate --version v1.0.0
python <skillDir>/scripts/build-yunxiao-plan.py <prdRoot> --mode plan --version v1.0.0
```

历史项目尚无 `delivery_scope.md` 时，只有用户明确给出 Feature ID 才可使用兼容入口：

```text
python <skillDir>/scripts/build-yunxiao-plan.py <prdRoot> --mode plan --version v1.0.0 --feature FEATURE-001
```

兼容入口只替代“范围选择”，不会跳过 Feature `active + approved`、模块来源 ID、引用闭环等门禁。公司角色分工明确调整时才使用 `--policy <json>` 调整终端归 `BE` 或 `MP`、以及是否生成 `TEST`；策略不能引入其他任务面，也不得改写 Feature 产品事实来迎合任务分工。

## 门禁与输出

先运行 `validate`。任一阻塞项存在时退出码为 1，禁止宣称可导入；输入或参数错误退出码为 2。通过后运行 `plan`，将标准输出 JSON 交给用户审阅，再用 `validate-export-plan.py` 校验结构。用户明确要求保存计划时，规范落点为 `versions/{v}/yunxiao-plan.json`；它是可重新生成的审阅快照，不回写任何云效实例字段。

计划必须满足：

- 每个模块生成一个 `product`；每个 Feature 生成一个 `business`；研发面按策略生成 `task`。
- `本期开发 + active` 生成缺省 `upsert`；`本期下线 + deprecated` 从最近更早版本的 `yunxiao-plan.json` 读取实际业务子任务并生成 `operation=close`，模块项不关闭。缺上一版计划快照时阻塞，禁止按当前引用或当前 policy 猜测。旧计划缺少 `operation` 时按 `upsert`。
- API/EXT 的实现引用只进入 `BE.sourceRefs`；所有带数据交互的页面任务均通过 `pageApiBindings` 承担 API 调用实现。MP 调用 BE API 时另以 `dependencyRefs` 表达跨任务依赖；AD 页面与 API 同归 BE 时保留调用绑定但不制造 BE 对自身的依赖。
- `本期开发` Feature 至少一条完整 AC；AC ID 唯一，描述和验证方式非空。AC 按 `关联页面` 投影到对应页面任务，按 `关联接口` 同时投影到 BE；旧 AC 缺页面时可用页面/API 绑定反推。全部 AC 始终完整保留在 TEST。
- PAGE→API/EXT 绑定优先读当前版本单页 PRD §5，缺页时回退根 `ui/PAGE-*.md` 稳定接口表；两处均无接口表，或某绑定无法归属到任何同时关联该 PAGE 和接口的 Feature 时阻塞。聚合页按 Feature 接口集合分别投影，不得把其他 Feature 的绑定误塞入当前任务。
- 来源 ID 仅使用 `MODULE-###`、`FEATURE-###` 与 `FEATURE-###:{SURFACE}`。
- 同一输入得到字节级稳定输出；不得包含 `yunxiaoId`、负责人和实时状态。
- 当前版本只到计划。`close` 只是供后续 reconcile 使用的声明，不代表云效已关闭；用户要求实际写入时，明确说明 `apply/reconcile` 尚未提供，不得自行拼写云效写 API。
