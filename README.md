# LNY-PRD — 李宁远产品工作流

AI Agent Skills 驱动的产品需求文档（PRD）工作流工具包。以"文档先行、原型后置"为原则，将产品需求从立项到迭代的全生命周期拆分为 **八步标准化流程**，由 AI Agent 按技能边界各司其职、逐步推进。适用于 Cursor、Claude Code、Codex 等支持 Agent Skills 的 AI 编程工具。

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

- 支持 Agent Skills 的 AI 编程工具（Cursor、Claude Code、Codex 等）
- 已将本仓库各 `lny-prd-*/` 目录下的 `SKILL.md` 注册为 Agent Skill

## 快速开始

### 安装

将本仓库克隆到本地，并在 AI 编程工具中将各子目录注册为 Agent Skill（具体方式取决于所用工具）：

**Cursor**：将 `lny-prd-*/` 目录放入 `~/.cursor/skills/` 或在工作区 `.cursor/skills/` 中引用。

**Claude Code / Codex**：按对应工具的 Skill 配置方式，指向各 `lny-prd-*/SKILL.md` 文件。

### 使用

在 AI 编程工具中打开任意空目录（或已有 `main_spec.md` 的 PRD 项目根目录），输入总控命令：

```
@lny-prd-master
```

或直接使用斜杠命令：

```
/lny-prd-master
```

Agent 将自动判定当前状态：

- **空目录**：进入立项对话，引导你描述项目背景和需求（如项目名称、产品定位、目标用户、终端范围等），以自然语言对话式沟通收集完整立项要素，确认后生成初始文档
- **已有项目**：按状态检测找到当前应执行的步骤，自动路由；回复「继续」即可进入下一轮

### 推荐工作流

```text
① 立项 → ②③④ 规格三件套（并行） → ⑤ 单页 PRD → ⑥ 原型生成 → ⑦ 检查验收 → ⑧ 新迭代（重复）
```

每轮只需输入「继续」，Agent 自动推进下一步，无需用户手动选择子指令。

## 产物结构

完整的 PRD 项目生成后，目录结构如下：

```
my-project/                         # PRD 项目根目录
│
├── main_spec.md                    # 产品规格说明书（概述、终端、统计索引）
├── api_spec.md                     # 接口需求索引（§4 终端对齐 + API/EXT 清单）
├── ui_manifest.md                  # UI 设计清单（页面/分包/组件索引）
├── feature_spec.md                 # 功能规格索引（全局规则 + Feature 索引）
│
├── api/                            # 接口需求明细（③ 负责）
│   ├── API-MP-001.md               #   小程序接口
│   ├── API-AD-001.md               #   管理后台接口
│   └── EXT-001.md                  #   第三方接口
│
├── ui/                             # UI 页面与组件明细（② 负责）
│   ├── PAGE-MP-001.md              #   单页面布局与状态描述
│   ├── PAGE-AD-001.md
│   └── COMP-001.md                 #   局部自定义 UI 组件规格
│
├── feature/                        # 功能规格明细（④ 负责）
│   ├── FEATURE-001.md              #   单功能：目标、流程、验收标准、双图
│   └── FEATURE-002.md
│
├── prototypes/                     # 可交互原型（⑥ 负责）
│   ├── MP/                         #   小程序端
│   │   ├── index.html              #     页面导航汇总
│   │   ├── map.html                #     页面关系画布
│   │   └── PAGE-MP-001.html        #     单页原型
│   ├── AD/                         #   管理后台端
│   └── PC/                         #   PC 端
│
├── prototypes-mui-app/             # 桌面端 React + Material UI 源码（⑥ 负责）
│
└── versions/                       # 版本管理（① 立项 / ⑧ 迭代）
    ├── v1.0.0/                     #   首版
    │   ├── iteration_notes.md      #     过程性留痕
    │   ├── pages_prd/              #     单页 PRD（⑤ 负责）
    │   │   └── PAGE-MP-001.md
    │   └── prototypes/             #     原型静态镜像
    └── v1.1.0/                     #   次版（⑧ 创建）
        ├── iteration_notes.md
        ├── ui_changes.md           #     变更台账
        ├── api_changes.md
        └── feature_changes.md
```

## 工具包结构

```
lny-prd-master/                     # 本仓库（工具包，非 PRD 项目）
├── lny-prd-api/SKILL.md            # ③ 接口需求规范
├── lny-prd-check/SKILL.md          # ⑦ 检查与验收
├── lny-prd-feature/SKILL.md        # ④ 功能规格拆分
├── lny-prd-iter/SKILL.md           # ⑧ 迭代管理
├── lny-prd-master/SKILL.md         # ① 总控入口与立项
├── lny-prd-page/SKILL.md           # ⑤ 单页 PRD
├── lny-prd-prototype/SKILL.md      # ⑥ 可交互原型
├── lny-prd-ui/SKILL.md             # ② UI 设计
├── README.md
└── .gitignore
```

## 许可证

MIT License
