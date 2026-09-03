---
name: lny-prd-feature
description: >-
  维护 feature_spec 领域模块定义与 Feature 索引、feature/FEATURE-*.md 明细，并保持 STORY/AC/PAGE/API/EXT 引用闭环。
  Use when the user mentions /lny-prd-feature, @lny-prd-feature, 功能规格, FEATURE-*.
---

## 与总控的关系

本步为 **④ `/lny-prd-feature`**。产物：`feature_spec.md` + `feature/`。禁止写接口字段表与 UI 线框。下一跳通常 **⑤ page**。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑩ 追加；过程流水见 master §1.1。

# 功能规格 `/lny-prd-feature`

## Additional resources

- 项目产物模板、明细结构与双图规范：[`reference.md`](reference.md)
- 正式落点与镜像禁区：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 与 `lny-prd-master/reference-artifact-paths.md`。不为框架通用已排除项建 Feature；业务流程 Feature 仍须编写且只写差异。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 Feature 或把其写进范围内。

## 职责与禁止

- **负责**：`feature_spec.md` 中少量、稳定、粗粒度的领域模块定义与 Feature 轻量索引，以及 Feature 明细（Story 来源、模块归属、生命周期、产品评审、目标/规则/AC/验证方式/双图）；新增 Module 前执行下文「领域粒度门禁」，优先复用现有边界，具体规则、流程与验收下沉 Feature；索引只登记编号、名称与明细路径，其余 Feature 事实只写明细；每个 Feature 至少关联一个有效 Story 和一个 Module；active Feature 至少一条 AC，且 AC ID 唯一、描述与验证方式非空；FEATURE ↔ PAGE/API/EXT 闭环，并与单页 PRD §6 的 `关联AC` 双向一致；成功自检后推进本次 `feature_changes.md` 对应行状态。
- **禁止**：在 `api_spec` 写字段；在 `ui_manifest` 写线框；写入预览壳机制；根规范「变更记录」表新增行；把 `feature_spec.md` 或 `feature/` 复制到 `versions/{v}/`（含 `versions/{v}/feature/` 与版本根散落文件）。②③④⑤⑥ **禁止**展开「明确不做」。仅当 PM 已说出点位才写埋点；**禁止自拟埋点方案**。
- **AC 证据口径**：`验证方式`只写如何证明结果，例如 `UI + API 联调`、`数据校验`、`异常流测试`；不得写 `FE`、`BE`、`MP`、`AD`、`TEST` 等终端或交付角色。责任归属由 PAGE/API/EXT 引用及外部映射决定，不从验证文案推断。

编号：新增只用 `FEATURE-{三位序号}`。历史 `FEATURE-MP-001` **只读兼容**，新项目禁止再用。

## 写产物纪律

开笔前 Read `main_spec` Story、`feature_spec` Module/索引、`feature/` 与关联规格。先明确 Story 来源与领域边界，再拆 Feature 和 AC。Module 事实只写 `feature_spec.md`，Feature 明细只引用 `MODULE-*`，禁止复制模块名称；Story↔Feature 事实只写 Feature 明细，禁止回写 `main_spec`。索引只作发现与导航，禁止把模块、优先级、生命周期、评审状态、分支数或 PAGE/API/EXT 关联复制回索引。命中双图必画条件则补图（节点用 PAGE/API/EXT 编号）。评审结论只有产品明确给出，或产品确认了 ⑧ `/lny-prd-review` 的最新结论包时才写 `approved`，否则保持 `pending/reviewing`。仅同步评审状态不写 `iteration_notes`；业务正文变更仍按规则追加。

### 领域粒度门禁（仅约束生成过程，不写入项目文档）

默认复用现有 Module。Module 应少量、稳定、粗粒度，并能跨多个版本承载一组 Feature；不能因新增页面、操作或单项需求同步增加 Module。

新建或拆分候选 Module 前依次判断：

1. 候选能力能否归入现有 Module 的范围内且不破坏其职责与核心对象？能则复用。
2. 候选是否拥有稳定核心业务对象、独立业务规则或生命周期，而非现有对象的一次操作？
3. 候选是否能写出清晰的范围内/外，并需要通过明确业务契约与其他 Module 协作？
4. 候选是否能长期承载一组 Feature，而非当前页面、菜单或单个 Feature 的临时分类？

第 1 项能复用，或第 2～4 项缺少实质证据时，不得新建 Module。初期只有一个 Feature 不自动判错，但须有稳定边界与后续能力族，否则并回现有 Module。

页面、菜单、终端、展示区域、CRUD 动作、流程阶段、状态、单个 Feature 的改写名称、技术组件、框架能力和纯目录分类默认都不是 Module。Module 只保留职责、核心对象、范围、对外能力与依赖；`BR-*`、流程分支、状态处理、`STORY/FEATURE/AC/PAGE/API/EXT-*` 及具体交互全部下沉 Feature 明细。只有出现可独立演进的核心对象、规则和对外契约时才拆分。

上述内容是 Agent 的作者治理规则。生成的 `feature_spec.md` 只保留开发 Agent 理解项目所需的文档分工、编号/状态语义、实际 Module 边界、Feature 索引和项目特有跨模块约定；禁止复制门禁步骤、反例清单或写作方法论。

## 并行分片

需要并行时完整 Read [`../lny-prd-master/reference-agent-orchestration.md`](../lny-prd-master/reference-agent-orchestration.md)。Module 边界、Feature ID、依赖方向与 STORY/PAGE/API 输入先由主 Agent 锁定；之后可按单个 `feature/FEATURE-*.md` 分片，每个子 Agent 只写一个独占明细文件。Module 定义、`feature_spec.md` 索引/依赖、跨 Feature AC 去重、台账状态和 `iteration_notes.md` 由主 Agent 单写。无 subagent/Task 时顺序执行同一分片清单。

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
2. 先执行领域粒度门禁：能归入现有 Module 就复用；只有形成独立稳定边界时才在 `feature_spec.md` 新建 Module。边界变化时同步检查受影响 Feature。
3. add：分配编号、写明细、更新 Feature 索引；modify：修改明细，仅在编号、名称或路径变化时同步索引。
4. 补双图或免画理由。
5. 确认每个 Feature 的 Story、Module、AC、PAGE/API/EXT 引用有效，索引与文件双向一致。
6. 自检通过后，将本次 `feature_changes.md` 条目由 `待④` 改为 `已完成`；有缺口或失败则保留 `待④`。
