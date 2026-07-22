# LNY-PRD — 李宁远产品工作流

Cursor Agent Skills 驱动的产品需求文档（PRD）工作流工具包。以"文档先行、原型后置"为原则，将产品需求从立项到迭代的全生命周期拆分为 **八步标准化流程**，由 AI Agent 按技能边界各司其职、逐步推进。

## 八步工作流

| 步骤 | 命令 | 职责 |
|------|------|------|
| ① | `/lny-prd-master` | 总控入口与立项，生成项目骨架（`main_spec.md` 等） |
| ② | `/lny-prd-ui` | 页面架构与 UI 清单（`ui_manifest.md` + `ui/` 明细） |
| ③ | `/lny-prd-api` | 接口需求（`api_spec.md` + `api/API-*.md`） |
| ④ | `/lny-prd-feature` | 功能规格拆分（`feature_spec.md` + `feature/FEATURE-*.md`） |
| ⑤ | `/lny-prd-page` | 单页 PRD 生成（`versions/{v}/pages_prd/`） |
| ⑥ | `/lny-prd-prototype` | 可交互原型（`prototypes/`，桌面端基于 Material UI） |
| ⑦ | `/lny-prd-check` | 文档一致性检查 + 功能性验收（只读报告） |
| ⑧ | `/lny-prd-iter` | 新迭代管理（建版本壳 + 变更台账 + 委派清单） |

**②③④** 为规格三件套，可并行推进；**⑤→⑥** 文档先行，互不硬阻塞。

## 核心原则

- **只读检查**：⑦ `/lny-prd-check` 不改任何文件，仅输出报告与委派建议
- **版本纪律**：仅 ① 可建 `v1.0.0`，仅 ⑧ 可建新版本并追加变更记录
- **技能边界**：每一步都有明确的"负责"与"禁止"清单，Agent 不得越权
- **框架内置排除**：公司统一框架已有能力（登录、支付、RBAC 等）默认不写入 PRD，避免重复展开

## 前置条件

- Cursor IDE
- 已配置对应的 Agent Skills（将本仓库各 `lny-prd-*/` 目录下的 `SKILL.md` 注册为 Cursor Skill）

## 快速开始

在 Cursor 中打开任意空目录（或已有 `main_spec.md` 的 PRD 项目根目录），输入：

```
/lny-prd-master
```

Agent 将自动判定当前状态：空目录则走立项脚手架，已有项目则按状态检测路由到应执行的下一步。

## 项目结构

```
lny-prd-master/
├── lny-prd-api/SKILL.md         # ③ 接口需求规范
├── lny-prd-check/SKILL.md       # ⑦ 检查与验收
├── lny-prd-feature/SKILL.md     # ④ 功能规格拆分
├── lny-prd-iter/SKILL.md        # ⑧ 迭代管理
├── lny-prd-master/SKILL.md      # ① 总控入口与立项
├── lny-prd-page/SKILL.md        # ⑤ 单页 PRD
├── lny-prd-prototype/SKILL.md   # ⑥ 可交互原型
├── lny-prd-ui/SKILL.md          # ② UI 设计
└── .cursor/rules/               # Cursor 规则（审计日志等）
```

## 许可证

MIT License
