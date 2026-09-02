---
name: lny-prd-api
description: >-
  维护 api_spec 索引与 api/API-*.md、api/EXT-*.md 业务需求明细；不写路由/JSON/code/域名。
  Use when the user mentions /lny-prd-api, @lny-prd-api, 接口需求, API-*, EXT-*.
---

## 与总控的关系

本步为 **③ `/lny-prd-api`**。产物：`api_spec.md` + `api/`。禁止写 UI 线框与原型。下一跳通常 **④ feature**。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑩ 追加；过程流水见 master §1.1。

# 梳理接口需求 `/lny-prd-api`

## Additional resources

- 索引与单接口/EXT 模板：[`reference.md`](reference.md)
- 正式落点与镜像禁区：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 开笔前

Read `lny-prd-master/framework-exclusions.md` 与 `lny-prd-master/reference-artifact-paths.md`。不为框架通用已排除项建 `API-*`/`EXT-*`；业务 API/EXT 仍须建档且只写差异。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 `API-*`/`EXT-*`。

本层是 **接口需求**（要什么能力、连哪些页、业务字段与规则），不是 OpenAPI。不写域名、path、HTTP 方法、JSON、响应 code。禁止落盘 `待补充` 等 meta 占位。

## 职责与禁止

- **负责**：`api_spec.md` §1～§4 跨接口规则与轻量索引；API/EXT 索引只登记编号、名称（用途）与明细路径，其余接口事实只写 `api/API-*.md` / `api/EXT-*.md`；成功自检后推进本次 `api_changes.md` 对应行状态。
- **禁止**：写 UI 线框；改 `prototypes/`；实现向内容；根规范「变更记录」表新增行；把 `api_spec.md` 或 `api/` 复制到 `versions/{v}/`（含 `versions/{v}/api/` 与版本根散落文件）。仅当 PM 已说出点位或 AD 字典条目才写埋点；**禁止自拟埋点方案**。

**新立项只走目录化**。旧 `api_spec` §5 单体大段只提示迁移，禁止双轨扩写。

## 写作要点

- 终端小节仅按 `main_spec` 第4章划分。
- 响应形态三选一：基础对象 / 无分页列表 / 分页列表。
- 字段表用中文业务名 + 类型语义；不写 snake_case。
- API 必填：服务对象、数据操作形态、第三方联动、特殊通道、响应形态。联动为「是」须挂 `EXT-*`。
- EXT **联调门槛必须由人工提供**，禁止 AI 自填；交互方向/业务敏感度证据不足则询问。

## 写产物纪律

开笔前 Read `api_spec` + `ui_manifest`/`ui/`。先清单后落盘。旧版宽索引在本次修改涉及对应表时收敛到当前三列，禁止把涉及页面、服务商或人工统计复制回索引。收尾核对 API↔PAGE；`iteration_notes` 文末追加业务变更。

## 前置条件

已有 `main_spec.md`；建议已有页面索引。⑩ 委派进入时 Read `api_changes.md` 中 `待③`。

## 输入

见对话 YAML：版本号、add/modify、接口信息、第三方（含 `联调门槛`）。未指定版本号时按 master §1.1。

## 执行步骤

1. 缺 `api_spec.md` / `api/` 时按 [`reference.md`](reference.md) 创建骨架。
2. 按页面与第4章终端梳理接口；写 EXT 前过联调门槛门禁。
3. 更新 §2 / §4 索引与明细文件。
4. 文末追加 `iteration_notes`（若有业务变更）。
5. 索引、明细与引用自检通过后，将本次 `api_changes.md` 条目由 `待③` 改为 `已完成`；有缺口或失败则保留 `待③`。
