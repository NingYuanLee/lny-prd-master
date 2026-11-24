# LNY PRD Workflow

LNY PRD Workflow（LNY-PRD-WF）是一个统一入口的全量产品方案工作流。它把产品发现、立项、UI、API、Feature、单页 PRD、原型、检查、评审、估点、发布学习和迭代规则收在一个可安装的 `lny-prd` 技能下，内部模块根据用户意图、项目状态和变更影响智能选路。

## 目录

```text
lny-prd/
├── SKILL.md
├── agents/openai.yaml
└── modules/
    ├── lny-prd-master/
    ├── lny-prd-ui/
    ├── lny-prd-api/
    ├── lny-prd-feature/
    ├── lny-prd-page/
    ├── lny-prd-prototype/
    ├── lny-prd-check/
    ├── lny-prd-review/
    ├── lny-prd-sp/
    └── lny-prd-iter/
```

`lny-prd/SKILL.md` 是唯一公开入口。`modules/*/SKILL.md` 是内部步骤说明，不单独安装或触发。

当前工作流不是固定直线。路由图见 [`lny-prd/modules/lny-prd-master/reference-workflow-map.md`](lny-prd/modules/lny-prd-master/reference-workflow-map.md)。PM 视图压缩为理解与决策、规格与原型、自动验证、交付准备、发布学习五个阶段，内部模块仍按影响范围自动选取。

小范围可逆修改按 [`lny-prd/modules/lny-prd-master/reference-flexible-execution.md`](lny-prd/modules/lny-prd-master/reference-flexible-execution.md) 走快速路径，不要求完整链或完整记录。

宿主能力可用 `python .\scripts\probe-host-capabilities.py --json` 探测。探测器识别 Codex、Claude Code、Cursor、DeepSeek Harness、WorkBuddy、豆包工作、千问办公和 Trae 等宿主，`unknown` 只表示未被当前探测器确认，不表示能力不存在。

## 安装

在 Windows 上从仓库根目录执行：

```powershell
pwsh -NoProfile -File .\lny-prd\scripts\install-skill.ps1
```

默认会在 `$env:USERPROFILE\.agents\skills\lny-prd` 创建指向本仓库 `lny-prd` 目录的 junction。可以显式指定源目录和安装目录：

```powershell
pwsh -NoProfile -File .\lny-prd\scripts\install-skill.ps1 `
  -SourceRoot (Resolve-Path .) `
  -InstallRoot "$env:USERPROFILE\.agents\skills"
```

安装位是链接，修改源目录会立即生效。脚本不会覆盖同名实体目录或非 junction 链接。

## 验证

```powershell
python .\scripts\validate-skill-package.py
python .\scripts\run-regression.py
```

第一条命令检查 bundle 元数据、入口 frontmatter、Agent 配置、内部模块路径、技能文档中的本地引用和脚本路径。第二条命令运行产品无关的运行时回归，验证 UTF-8、产物路径和 kit 复制，不读取固定业务页面，也不把任何视觉样例当作原型标准。

原型反馈可先运行 `python .\scripts\classify-change.py "反馈原文" --page-id PAGE-...` 获取 A～D 影响分类和最小检查范围。反馈记录格式与视觉前后截图要求分别见 `lny-prd/modules/lny-prd-master/reference-feedback-record.md` 和 `lny-prd/modules/lny-prd-prototype/reference-visual-self-review.md`。

## 使用

在 PRD 项目目录中使用 `$lny-prd`，并说明目标步骤，例如“用 UI 步骤设计页面”或“继续生成原型”。完整入口规则见 [`lny-prd/SKILL.md`](lny-prd/SKILL.md)。

## 版本

当前统一入口迁移版本为 **3.1.4**。展示名为 **LNY PRD Workflow**，技术调用仍使用 `$lny-prd`。旧的 `/lny-prd-master`、`/lny-prd-ui` 等名称不再作为独立安装入口。

默认输入可以是碎片化自然语言、文件、截图、链接或局部修改意见。模型会自动提取事实、补齐高可信推断、记录可逆假设，并按最小依赖路径推进全量产品能力。只有冲突、关键事实缺失、范围变化或正式批准动作才暂停询问。
