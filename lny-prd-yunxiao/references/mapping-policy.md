# 映射策略

默认策略把产品事实映射为交付面，不把组织结构写回 PRD：

| 来源 | 默认交付面 |
|------|------------|
| `API-*`、`EXT-*` | `BE` |
| `PAGE-AD-*` | `BE` |
| `PAGE-MP-*`、`PAGE-APP-*`、`PAGE-H5-*`、`PAGE-PC-*` | `MP` |
| 每个 Feature | `TEST` |

这是当前公司的统一云效角色口径：管理后台由后端/全栈侧承担，客户端页面统一由 `MP` 承担；云效 `MP` 对应 SP 技能的 `FE` 侧，但不改写 `FE_SP` 字段。`TEST` 默认开启。若同一 Feature 同时命中多个来源，按 `BE, MP, TEST` 去重排序。

映射只决定实现所有权。每个页面交付面都要实现其单页 PRD §5 的 `PAGE → API` 调用绑定：客户端页面在 MP 任务中以 `pageApiBindings + dependencyRefs` 表达调用 BE API；AD 页面在 BE 任务中以 `pageApiBindings` 表达调用，同时 API 位于同一任务的 `sourceRefs`，因此不再写成 BE 对自身的依赖。这不会生成第二条 API 开发任务，也不会遗漏页面侧的调用工作。

组织差异通过 `--policy policy.json` 覆盖：

```json
{
  "schemaVersion": 1,
  "apiSurface": "BE",
  "externalApiSurface": "BE",
  "pageTerminalSurfaces": {
    "MP": "MP",
    "APP": "MP",
    "H5": "MP",
    "PC": "MP",
    "AD": "BE"
  },
  "includeTestTask": true,
  "surfaceOrder": ["BE", "MP", "TEST"]
}
```

策略文件必须是 JSON 对象；未知字段、空交付面、重复 `surfaceOrder` 会被拒绝。默认策略是公司专用契约；`--policy` 只能调整 `pageTerminalSurfaces` 中的页面归 `BE` 或 `MP`，以及是否生成 `TEST`。`apiSurface` 与 `externalApiSurface` 为结构兼容字段，若覆盖也只能填 `BE`，不能把 API/EXT 实现责任转移给 `MP`；策略也不能引入 `FE`、`APP`、`H5` 等新任务面。公司页面分工明确调整时才覆盖，并在导出计划审阅时显式说明。
