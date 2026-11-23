# 项目仓库共享契约

本契约适用于 PRD 项目位于产品代码库、设计代码库或需要多人协作的项目目录时。它只定义交付物的共享边界，不替代项目自身的 Git、权限和发布规则。

## 共享级别

| 级别 | 含义 | 处理方式 |
|---|---|---|
| `shared-required` | 影响产品事实、开发实现、评审或协作，必须进入代码库 | 正式写入项目目录，纳入版本控制 |
| `shared-optional` | 对复盘、视觉复用或团队协作有帮助，可由项目决定是否提交 | 有团队价值时提交，没有则保留本地 |
| `local-only` | 临时过程、机器相关、渲染产物或调试文件 | 不进入代码库，交付前清理或加入 `.gitignore` |

## 必须共享

以下文件是产品事实或可复现交付物，应进入代码库：

- `main_spec.md`
- `ui_manifest.md`、`ui/`
- `api_spec.md`、`api/`
- `feature_spec.md`、`feature/`
- `pages_prd/`
- `prototypes/`，当原型用于评审、验收或团队对齐时
- `product_workspace.md`，当它承担当前项目状态和下一动作的协作入口时
- `evidence_log.md`，当其中的证据影响产品决策时
- `learning_log.md`，当其中的发布学习影响下一轮产品决策时
- `versions/{v}/iteration_notes.md`、`*_changes.md`、`eval_signals.md`
- `versions/{v}/delivery_scope.md`、批准后的 `versions/{v}/pages_prd/`
- `versions/{v}/sp_report.md`，当团队需要共享估点依据时
- 项目确认采用的视觉档案和素材清单，例如 `ui/visual/visual-profile.md`、`tokens.json`、`assets-manifest.md`

## 可选共享

- `prototypes/.design-decisions/`，当视觉决策需要被复用或审阅时
- 产品调研原始材料的脱敏版本
- 竞品截图、流程图和会议纪要
- 团队约定的评审导出物
- 项目级主题 CSS、图标和本地图片素材

原始访谈、含个人信息的材料、授权受限的图片和外部平台导出文件先按项目权限规则处理，不因进入 PRD 项目目录就自动共享。

## 本地文件

以下内容只用于本地生成、调试和验收：

- 浏览器截图、视觉评分结果和临时渲染目录
- `artifacts/`、`.browser-artifacts/`、临时报告和一次性脚本
- `node_modules/`、Python 缓存、Playwright 缓存和系统临时目录
- 编辑器配置、机器路径、个人草稿和本地备份
- 含密钥、令牌、个人信息或未脱敏数据的文件
- 原型生成过程中的草稿、修复脚本和备份文件

正式原型只保留 `prototypes/` 下的交付文件。临时验收产物写入系统临时目录，不能因为验证成功就复制进项目根目录。

## 共享前检查

总控在交付前检查：

1. 正式文件位于本契约或项目规则允许的路径。
2. 共享文件不含密钥、个人信息和机器专属绝对路径。
3. 原型、页面 PRD、UI、API、Feature 和版本范围引用闭合。
4. 本地临时目录、截图、缓存和一次性脚本已清理或被 `.gitignore` 覆盖。
5. 需要团队协作的 `product_workspace.md`、证据和学习记录已提交到代码库。

## 默认判断

项目位于 Git 仓库且用户没有另行说明时，按 `shared-required` 处理正式产品事实和可评审原型，按 `local-only` 处理临时调试文件。无法判断是否含敏感信息时先暂停共享该文件并询问。
