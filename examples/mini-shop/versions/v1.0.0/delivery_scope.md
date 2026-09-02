# 交付范围 - v1.0.0

## 1. 范围状态

> **产品经理填写说明**
> - `评审状态` 只填一个值：尚未发起评审填 `pending`；正在评审填 `reviewing`；存在阻塞、暂不能确认范围填 `blocked`；本期范围已明确且不存在未关闭问题时填 `approved`。
> - `产品确认项` 填仍未关闭且影响本期范围确认的问题数量。每关闭一项同步递减，全部关闭后改为 `0`。
> - 推荐流转：`pending` -> `reviewing` -> `approved`；评审中发现阻塞时改为 `blocked`，解除阻塞后回到 `reviewing`，重新确认后再改为 `approved`。

| 属性 | 内容 |
|------|------|
| 版本号 | v1.0.0 |
| 评审结论 | 通过 |
| 评审状态 | approved |
| 产品确认项 | 0 |

## 2. Feature 范围

> **产品经理填写说明**
> - `Feature` 填根 `feature_spec.md` 中已登记的 `FEATURE-###`；尚未确定时保留阻塞壳，不能从全部 `active` Feature 自动推断。
> - `纳入方式`：确定本期实现时填 `本期开发`；迭代中明确废弃并需关闭外部研发工作项时填 `本期下线`；尚未确定时填 `待确认`；其余 Feature 不保留在本表中。
> - 生命周期必须匹配：`本期开发` 对应 Feature `状态=active`，`本期下线` 对应 `状态=deprecated`；废弃只改状态并保留历史明细文件。
> - 行级 `评审状态` 与范围级使用同一组状态，但表示该 Feature 的开发或下线结论是否已经确认；只有已确认的本期 Feature 才改为 `approved`。
> - `阻塞决策` 填下方仍为 `open` 且影响该 Feature 的决策数量；相关决策关闭后同步递减，全部关闭后改为 `0`。

| Feature | 纳入方式 | 评审状态 | 阻塞决策 |
|---------|----------|----------|----------|
| FEATURE-001 | 本期开发 | approved | 0 |
| FEATURE-002 | 本期开发 | approved | 0 |
| FEATURE-003 | 本期开发 | approved | 0 |

## 3. PAGE 发布映射

| PAGE | 终端 | 工作源 | 页面路由 | 快照路径 |
|------|------|--------|----------|----------|
| PAGE-MP-001 | MP | pages_prd/MP/PAGE-MP-001.md | pages/index/index | versions/v1.0.0/pages_prd/MP/pages/index/index/PAGE-MP-001.md |
| PAGE-MP-002 | MP | pages_prd/MP/PAGE-MP-002.md | pages/goods/index | versions/v1.0.0/pages_prd/MP/pages/goods/index/PAGE-MP-002.md |
| PAGE-MP-003 | MP | pages_prd/MP/PAGE-MP-003.md | pages/goods/detail | versions/v1.0.0/pages_prd/MP/pages/goods/detail/PAGE-MP-003.md |
| PAGE-MP-004 | MP | pages_prd/MP/PAGE-MP-004.md | pages/kit/form | versions/v1.0.0/pages_prd/MP/pages/kit/form/PAGE-MP-004.md |
| PAGE-AD-001 | AD | pages_prd/AD/PAGE-AD-001.md | views/goods/index | versions/v1.0.0/pages_prd/AD/views/goods/index/PAGE-AD-001.md |
| PAGE-AD-002 | AD | pages_prd/AD/PAGE-AD-002.md | views/goods/form | versions/v1.0.0/pages_prd/AD/views/goods/form/PAGE-AD-002.md |
| PAGE-AD-008 | AD | pages_prd/AD/PAGE-AD-008.md | views/goods/detail | versions/v1.0.0/pages_prd/AD/views/goods/detail/PAGE-AD-008.md |

> 本表仅列 `FEATURE-001`～`FEATURE-003` 已批准 AC 实际覆盖的业务页；版本快照不包含 `_shell` 或夹具专用页面。

## 4. 未决决策

> **产品经理填写说明**
> - 每个待确认问题单独一行：未形成结论填 `open`，形成明确结论并已同步相关 PRD 后改为 `closed`。
> - `影响对象` 填受影响的 `FEATURE-###`；影响多个 Feature 时用逗号分隔。没有未决问题时仅保留 `| 无 | closed | 无 | 无 |`。
> - 所有决策均为 `closed` 后，才可把上方对应的 `阻塞决策` 归零；其他门禁也满足后，再将评审状态改为 `approved`。

| 决策编号 | 状态 | 问题 | 影响对象 |
|----------|------|------|----------|
| 无 | closed | 无 | 无 |
