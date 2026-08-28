# 云效工作项计划结构

计划为 UTF-8 JSON，`schemaVersion` 固定为 `1`。工作项可选 `operation`：缺省或 `upsert` 表示创建/更新，`close` 表示按稳定来源 ID 关闭；缺省规则保证旧计划兼容。

```json
{
  "schemaVersion": 1,
  "adapter": "lny-prd-yunxiao",
  "sourceVersion": "v1.0.0",
  "project": "Mini Shop",
  "items": [
    {
      "sourceId": "MODULE-001",
      "parentSourceId": null,
      "workItemType": "product",
      "title": "商品"
    },
    {
      "sourceId": "FEATURE-001",
      "parentSourceId": "MODULE-001",
      "workItemType": "business",
      "title": "浏览在售商品"
    },
    {
      "sourceId": "FEATURE-001:BE",
      "parentSourceId": "FEATURE-001",
      "workItemType": "task",
      "title": "[BE] 浏览在售商品",
      "deliverySurface": "BE",
      "sourceRefs": ["API-MP-001"],
      "dependencyRefs": [],
      "pageApiBindings": [],
      "acceptanceCriteria": [
        {
          "id": "AC-1",
          "description": "首页初始化后展示推荐商品",
          "verification": "UI + API",
          "pageRefs": ["PAGE-MP-001"],
          "apiRefs": ["API-MP-001"],
          "extRefs": []
        }
      ]
    },
    {
      "sourceId": "FEATURE-001:MP",
      "parentSourceId": "FEATURE-001",
      "workItemType": "task",
      "title": "[MP] 浏览在售商品",
      "deliverySurface": "MP",
      "sourceRefs": ["PAGE-MP-001"],
      "dependencyRefs": ["API-MP-001"],
      "pageApiBindings": [
        {
          "pageRef": "PAGE-MP-001",
          "interfaceRef": "API-MP-001",
          "purpose": "拉取推荐商品",
          "trigger": "页面初始化"
        }
      ],
      "acceptanceCriteria": [
        {
          "id": "AC-1",
          "description": "首页初始化后展示推荐商品",
          "verification": "UI + API",
          "pageRefs": ["PAGE-MP-001"],
          "apiRefs": ["API-MP-001"],
          "extRefs": []
        }
      ]
    }
  ]
}
```

下线 Feature 示例：

```json
{
  "sourceId": "FEATURE-002",
  "parentSourceId": "MODULE-001",
  "workItemType": "business",
  "title": "旧版商品预约",
  "operation": "close"
}
```

其既有子任务使用上一版 `yunxiao-plan.json` 中实际存在的 `FEATURE-002:*` 稳定来源 ID 输出 `operation: "close"`；模块项仍为 `upsert`，单个 Feature 下线不得关闭整个产品模块。不得根据下线后可能已清理的当前引用或变化后的映射策略重建关闭集合。

约束：

- `items` 按模块编号、Feature 编号、研发面固定顺序输出。
- `sourceId` 全局唯一；`parentSourceId` 必须引用同计划中已存在的父项。
- `operation` 只允许 `upsert` / `close`；缺省按 `upsert`。父业务项为 `close` 时，计划内子任务也必须为 `close`；本适配器暂不支持关闭 `product` 模块项。
- `product → business → task` 是唯一层级。
- 计划不得出现 `yunxiaoId`、`assignee`、实时研发状态或其他云效实例字段。
- `sourceRefs` 表示该任务负责实现或历史上承接的 PRD 对象；`upsert` 时 API/EXT 只归 `BE`，客户端 PAGE 归 `MP`。`close` 任务保留来源引用供审阅，但依赖、页面调用绑定与 AC 均为空，不产生开发工作。
- `dependencyRefs` 表示任务消费但不负责实现的 API/EXT。MP 调用 BE API 时，两边可引用同一 API，但所有权不重复；BE 同时负责 AD 页面和 API 时不得把自有 API 重复写成依赖。
- `pageApiBindings` 来自当前版本单页 PRD §5，保存 PAGE、接口、本页用途与触发时机。MP 和 BE 的页面任务都必须保留各自页面的调用绑定：绑定中的 PAGE 必须位于本任务 `sourceRefs`，接口必须位于本任务 `dependencyRefs`（跨任务调用）或 `sourceRefs`（同任务实现）；旧计划可缺省为空数组。
- `acceptanceCriteria` 保存 Feature AC 的编号、描述、验证方式及 PAGE/API/EXT 来源引用。同一 AC 可投影到 BE、MP，并完整保留在 TEST；TEST 的 AC 集合必须与 Feature 完全一致，且包含其他交付面出现的全部 AC。这是同一来源的多角色证据责任，不是复制 AC。
- `close` task 的 `dependencyRefs`、`pageApiBindings`、`acceptanceCriteria` 必须均为空数组；`sourceRefs` 保留上一版计划快照中的历史承接对象供审阅。
