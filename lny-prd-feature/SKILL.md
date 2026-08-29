---
name: lny-prd-feature
description: >-
  维护 feature_spec 索引与 feature/FEATURE-*.md 明细，并与 PAGE/API/EXT 保持引用闭环。
  Use when the user mentions /lny-prd-feature, @lny-prd-feature, 功能规格, FEATURE-*.
---

## 与总控的关系

本步为 **④ `/lny-prd-feature`**。产物：`feature_spec.md` + `feature/`。禁止写接口字段表与 UI 线框。下一跳通常 **⑤ page**。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑩ 追加；过程流水见 master §1.1。

# 功能规格 `/lny-prd-feature`

## Additional resources

- 索引、明细、双图规范：[`reference.md`](reference.md)
- 正式落点与镜像禁区：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 与 `lny-prd-master/reference-artifact-paths.md`。不为框架通用已排除项建 Feature；业务流程 Feature 仍须编写且只写差异。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 Feature 或把其写进范围内。

## 职责与禁止

- **负责**：Feature 索引与明细（模块来源、生命周期、产品评审、目标/规则/AC/验证方式/双图）；active Feature 至少一条 AC，且 AC ID 唯一、描述与验证方式非空；FEATURE ↔ PAGE/API/EXT 闭环，并与单页 PRD §6 的 `关联AC` 双向一致；`main_spec` §3.3 模块注册表与 §7 统计；成功自检后推进本次 `feature_changes.md` 对应行状态。
- **禁止**：在 `api_spec` 写字段；在 `ui_manifest` 写线框；写入预览壳机制；根规范「变更记录」表新增行；把 `feature_spec.md` 或 `feature/` 复制到 `versions/{v}/`（含 `versions/{v}/feature/` 与版本根散落文件）。②③④⑤⑥ **禁止**展开「明确不做」。仅当 PM 已说出点位才写埋点；**禁止自拟埋点方案**。
- **AC 证据口径**：`验证方式`只写如何证明结果，例如 `UI + API 联调`、`数据校验`、`异常流测试`；不得写 `FE`、`BE`、`MP`、`AD`、`TEST` 等终端或交付角色。责任归属由 PAGE/API/EXT 引用及外部映射决定，不从验证文案推断。

编号：新增只用 `FEATURE-{三位序号}`。历史 `FEATURE-MP-001` **只读兼容**，新项目禁止再用。

## 写产物纪律

开笔前 Read 索引 + `feature/` + 根规格校验引用，并确认 `main_spec` 模块注册表。先清单后落盘。命中双图必画条件则补图（节点用 PAGE/API/EXT 编号）。评审结论只有产品明确给出，或产品确认了 ⑧ `/lny-prd-review` 的最新结论包时才写 `approved`，否则保持 `pending/reviewing`。仅同步评审状态不写 `iteration_notes`；业务正文变更仍按规则追加。

## 前置条件

已有 `main_spec.md`、`api_spec.md`、`ui_manifest.md`。⑩ 委派进入时 Read `feature_changes.md` 中 `待④`。

## 输入

```yaml
版本号: v1.1.0
操作模式: add 或 modify
功能信息:
  - 功能编号: FEATURE-001
    功能名称: 商品筛选与排序
    关联页面: [PAGE-MP-002]
    关联接口: [API-MP-003]
```

## 执行步骤

1. 缺 `feature_spec.md` / `feature/` 时按 [`reference.md`](reference.md) 创建骨架。
2. add：分配编号、写明细、更新 §3；modify：同步明细与索引。
3. 补双图或免画理由；更新 `main_spec` §7。
4. 确认索引有文件、文件有索引、关联 ID 有定义。
5. 自检通过后，将本次 `feature_changes.md` 条目由 `待④` 改为 `已完成`；有缺口或失败则保留 `待④`。
