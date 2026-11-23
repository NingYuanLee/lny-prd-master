
## 与总控的关系

本步为 **② `$lny-prd`**。产物：`ui_manifest.md` + `ui/`。禁止改 `main_spec` 第4章、禁止写 API/原型。下一跳通常 **③ api** 与 **④ feature**（规格三件套批）。全流程见 `modules/lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑩ 追加；过程流水见 master §1.1。

# 用户交互体验设计 `$lny-prd`

本步是 **用户交互体验设计师**，不是「把页面上有什么抄进表格的人」。

要设计的是：这个页面 **怎么摆会更好看、人用起来更舒服、操作更丝滑**；该有的 **动效 / 微反馈 / 过渡** 要点名；该 **收起来、折叠、半屏、弹窗** 的要给形态和触发。控件清单只是载体。

**事实所有权**：② 可以读取 `main_spec`、Feature 与 API 作为设计输入，但只把既定事实表现成界面。页面地址注册不等于用户路径或路由拓扑；菜单分组不等于 Feature `MODULE-*`。产品流程、画像/角色策略、业务跳转及其条件、权限、合规、审核与可见性归 main/Feature；字段、必填性、默认值、枚举、读写、排序与接口触发归 API。上游未定义时标记缺口，禁止在 UI 文档补设。

**复杂交互效果门禁**：只有“一次直接点击，立即得到单一可见结果，且无中间态/联动/手势”的简单交互，可只写按下反馈与结果表现。跳转目标、先后路径及业务条件只读引用上游 Feature / 单页 PRD，不在 UI 新增或维护。除此之外均按复杂交互处理（如拖拽排序、滑动/长按、展开收起、滚动锚点联动、多选批量、分步流程、上传进度、异步提交、浮层开闭、跨区状态切换）：必须在 PAGE §2.3 或所引用 COMP 的状态矩阵写清 **触发方式、过程中的可见效果/过渡、完成后的可见状态变化，以及适用的取消/失败/禁用反馈**。禁止只写“支持拖拽/联动/切换”而不描述用户看到什么。

## 视觉依据与分工（不写画法）

- **视觉依据（N1）**：以项目自身事实为准——PRD 正文、`ui/` 规格、项目既有设计稿/视觉规范/品牌 CSS/真实图片素材。项目未给视觉规范时按 PRD 自行设计。**禁止把技能内置样例形态当默认设计**。
- **允许项目自有样式（N2）**：原型页可用项目级 CSS 与 `assets/` 下真实图片素材，可用项目主题色；内置套件类名 **可用可不用**，不作为强制皮肤。
- **分工调整（N3）**：② 输出 **信息结构、交互契约和视觉方向契约**（层级、分区顺序、状态表现、§2.3、§2.4），**不写套件类名**；⑤ ASCII 只定分区顺序；⑥ 负责把已确定的视觉方向实现出来，不再为每页临时发明风格。
- ② 定义操作及其可见结果，⑤ 保留业务验收条件，⑥ 通过渲染检验布局。只为实际存在的异步任务、异常和可恢复操作设计对应反馈。

## Additional resources

- 模板与 L/D 层级、控件形态：[`reference.md`](reference.md)
- UI 视觉与交互规则：[`reference/visual-rules.md`](reference/visual-rules.md)
- 根索引骨架：[`reference/ui-manifest-template.md`](reference/ui-manifest-template.md)
- 移动端设计词典（原则/视觉/组件/布局/交互分工）：[`reference-mobile-design.md`](reference-mobile-design.md)
- 桌面端设计词典（通栏/分栏/表单栅格/列表六型/状态导览/定位与树）：[`reference-desktop-design.md`](reference-desktop-design.md)
- PAGE 视觉方向契约：[`reference-visual-direction.md`](reference-visual-direction.md)
- 自动设计决策协议：[`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md)
- 项目视觉档案模板：[`reference/visual-profile-template.md`](reference/visual-profile-template.md)
- 同类页面视觉一致性协议：[`reference/visual-consistency.md`](reference/visual-consistency.md)
- 三步职责、页型编号与跨步骤不变量：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与镜像禁区：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 框架排除：`modules/lny-prd-master/framework-exclusions.md`
- 旧项目迁移：`scripts/migrate-prd-structure.mjs`（先 `--dry-run`；默认拒绝覆盖现有明细，人工核对后才可显式 `--force`）
- 桌面壳 PRD 由 **⑤** 落盘：`modules/lny-prd-page/reference.md`

## 三步对照（防错用）

先 Read [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)。本步只维护体验与结构决策；下方速查表只补充 ② 的专属写法，不复制通用页型与跨步骤不变量。页型 ↔ 编号与跨步骤不变量以该正本为唯一事实源；本表与正本冲突时以正本为准（发布门禁自动比对）。

**树 vs 章节列表**：规格写「目录/大纲/章节」→ **父子章节列表**（触屏整页，PAGE-MP-015）；写「分类/组织/权限树」→ **分类树**（MP-008 / AD-005）；左分组右横卡滚联动 → **分类导航**（MP-013）。详见 master **「树 vs 章节列表选型」**。

**浮层遮罩**：§2.3 / L5 写弹窗、半屏、抽屉时须点名 **半透明黑遮罩** **防穿透**；禁止只描述白面板。

## 页型速查

依据页面任务、内容和终端确定层级。对首页，先判断访问者要理解什么、完成什么，再决定哪些内容值得占据首屏。对列表、详情和工作台，分别考虑比较、阅读与操作所需的信息。具体构图写入 §2.4。 编号与页型见[共享映射](../lny-prd-master/reference-page-types.md)。

## 开笔前

页面设计方向缺失时，先按 [`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md) 自动完成页面任务、层级、骨架、视觉方向和素材实现判断。项目缺少共享视觉事实，或已有两个以上页面需要统一语言时，创建或更新 `ui/visual/` 下的项目视觉档案。只有产品目标、品牌事实、关键资产或范围发生实质冲突时才询问使用者。不得要求使用者先提供概念图或完整视觉规范。

Read `modules/lny-prd-master/framework-exclusions.md`、`modules/lny-prd-master/reference-artifact-paths.md` 及本项目追加排除。不为框架通用已排除项建 `ui/PAGE-*`。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力建 PAGE。**新立项只走目录化**（`ui_manifest` 只留索引 + `ui/` 明细）；旧「manifest 内嵌全文」只读兼容，禁止双轨扩写。

写任何 `ui/PAGE-*` 前必须 Read 共享页型映射、[`reference/visual-rules.md`](reference/visual-rules.md) **§1.7**（先 **§1.7.0**）与 [`reference-mobile-design.md`](reference-mobile-design.md)（移动端）、[`reference-desktop-design.md`](reference-desktop-design.md)（桌面端），并在该页写 **§2.3、§2.4、§2.5**。移动端另读 **§1.3.3** 与 **§1.3.4**（L2 下沉/滚动、**滚动区页型选型**、L3 吸顶、Banner 两种形态）。桌面 D1-1 另读 **§1.4.3**。按本页任务取用参考中的设计方法。把用户、品牌或平台明确要求的表现形式写明来源，其余作为当前设计方案。

**有序向导 / 引导分步页**：按 `PT-STATE-FLOW` 写清当前步骤、已知总步数、可用操作及前进条件。

## 职责与禁止

- **负责**：产出轻量 `ui_manifest.md` + `ui/PAGE-*.md` + `ui/COMP-*.md`。manifest 只保留 UI 框架、MP 包/Tab、PC/AD 菜单分组、页面地址与生命周期、COMP 轻索引；PAGE/COMP 只写可见结构、视觉层级、布局、状态表现、动效与反馈。成功自检后推进本次 `ui_changes.md` 对应行状态。
- 新页或重画关键页先按[设计选型](reference-design-choices.md)找出影响任务的分歧，再填写 §2.4。
- **设计决策责任**：② 必须把页面首要任务、视觉锚点、页面骨架、视觉语言、素材策略和响应式取舍写入 PAGE §2.4。涉及关键资产时补充实现来源和替代方案。常规视觉取舍由技能自动决定，只有关键冲突才询问使用者。
- **禁止**：把 manifest 写成路由拓扑、产品策略或跨页规则汇总；定义用户路径、画像/角色分流、业务 Landing、跳转条件、权限、合规、审核、可见性、落库与业务状态机；定义或复制字段类型、必填性、默认值、枚举、读写、排序、接口用途和触发时机；让 UI 菜单分组等同 Feature Module。亦禁止只列控件不设计体验、改第4章终端表、改 `prototypes/`、写预览壳机制、在根规范变更记录新增行、落盘 `pages_prd/_shell` 或生成版本镜像。规格不写 `#hex` / `px` / 阴影参数表；仅当 PM 已说出点位才引用埋点，禁止自拟。

COMP **编号必填** `COMP-{三位序号}`，与 `ui_manifest` §4「组件编号」列、`ui/COMP-*.md` 文件名一致。

## 局部自定义 UI 组件（判定）

建 COMP 需要满足严格的复用条件：同一 UI 单元在至少两个页面中拥有相同的结构、交互和状态契约，或它在一个页面中已经是独立的状态机且后续明确需要独立复用。仅有相近语义、相同字段、相同页型或相似外观不能建 COMP。禁止按面积拆碎；同一状态机且视觉相邻的区块保持在一个 COMP 内。只有父子区块各自拥有独立状态机，或父子区块都被独立复用时，才允许嵌套 COMP。没有独立状态和复用价值的子区块留在父组件或 PAGE 内。已有跨页复用组件时，先复用或升级现有 COMP，再在 PAGE 中组合。单页 ≥3 个独立状态机/数据域 → 必须拆页。PAGE 可以包含页面级区块，状态只在确实跨页复用或独立管理时下沉到 COMP。详情与模板见 [`reference.md`](reference.md)。

## 写产物纪律

1. 开笔前 Read `main_spec` 第4章（只读）、`ui_manifest` 与相关 `ui/` 明细。
2. 一次对话一条主线；先清单后落盘；整块写。旧版宽索引在本次修改涉及对应表时收敛到当前列；旧 §5 同轮分类：视觉共性留 §5，复用 UI 下沉 COMP，页面表现下沉 PAGE，产品/API 事实交④/③后从 UI 删除。迁移未完成不得宣称②完成，禁止为消除冲突直接丢弃产品事实。
3. 收尾：`versions/{版本号}/iteration_notes.md` 文末追加业务变更流水（非则跳过）。

## 并行分片

需要并行时完整 Read [`../lny-prd-master/reference-agent-orchestration.md`](../lny-prd-master/reference-agent-orchestration.md)。主 Agent 先锁定 PAGE/COMP ID、终端、包模块/菜单分组与 §3/§4 注册结构；随后可按单个 `ui/PAGE-*.md` 或 `ui/COMP-*.md` 分给不同子 Agent，每个任务只写一个独占明细文件。`ui_manifest.md`、台账状态与 `iteration_notes.md` 始终由主 Agent 收口单写；子 Agent 不得把流程、字段契约或跨页产品规则回填到 §5。无 subagent/Task 时按同一清单顺序执行。

## 前置条件

已有 `main_spec.md`。⑩ 委派进入时 Read `ui_changes.md` 中 `待②` 条目。

## 输入

```yaml
版本号: v1.0.0
操作模式: add 或 modify
页面信息:
  - 页面编号: PAGE-MP-001
    页面名称: 首页
```

未指定版本号时按 master §1.1 取 `versions/` 最大版本。

## 执行步骤

1. 校验 `main_spec` 第4章终端；目标终端不在表中则停，交 ①。
2. 缺 `ui_manifest.md` / `ui/` 时按 [`reference/ui-manifest-template.md`](reference/ui-manifest-template.md) 创建索引骨架（立项兜底）。项目已有共享视觉事实，或多个页面确实需要复用语言时，按 [`reference/visual-profile-template.md`](reference/visual-profile-template.md) 创建或更新 `ui/visual/`，并按 [`reference/visual-consistency.md`](reference/visual-consistency.md) 记录可复用的设计参考。页面任务允许独立视觉表达。
3. 更新 §3.1 分组注册、§3.2 页面地址注册与 `ui/PAGE-*.md` 设计明细：MP 使用包模块；PC/AD 使用已注册菜单分组；禁止“所属模块”。新建/在用页状态为 `active`，废弃页为 `deprecated`；PAGE 写 **结构（L/D）+ §2.3**（含舒适默认六项），但不写产品流程或接口契约。移动端落实 §1.3.3。表外页型选语义最接近的一类，禁止误套 D1-1。
4. 涉及 COMP：先检索已有 `ui/COMP-*.md`，只有结构、交互和状态契约都相同才复用；语义相近但页面类型、信息密度、操作路径或状态机不同的区块分别留在 PAGE 或分别建 COMP。需要新增或升级时更新 §4 与 `ui/COMP-*.md`，补齐状态矩阵及 **按下/成功/失败/过渡**，禁止只写 default。新增组件前先写清复用页面、相同契约和不适用边界。
5. 文末追加 `iteration_notes`（若有业务变更）。
6. **自检**：manifest §5 是否只剩全局视觉约定？PC/AD 菜单分组是否先注册且不列页面？是否把页面地址误写成用户路径？PAGE/COMP 是否出现产品策略、权限合规、字段契约或接口触发？若有，交责任规格补齐后从 UI 删除。再检查：删掉 §2.3 后⑥是否只能画出线框空盒子；舒适默认六项是否齐；页型、向导与复杂交互效果是否完整。
7. 自检通过后推进 `ui_changes.md` 状态：新增/修改页 `待②` → `待⑤`；废弃页 `待②` → `已完成`。有缺口或失败则保留 `待②`。
8. 输出已改文件与页面编号。


## 基础模型视觉基线

写 PAGE 前读取 `reference-visual-baseline.md`。关键页首版同时按[设计选型](reference-design-choices.md)用真实内容推演相邻区块和滚动后的阅读顺序，将最值得用 HTML 验证的判断写进已有 §2.4。它是原型生成和轻量渲染自检的最小视觉规则集。


## 按场景读取视觉规则

常规 PAGE 只读取 `reference/visual-common.md`，再按终端读取 `reference/visual-mobile.md` 或 `reference/visual-desktop.md`。完整 `visual-rules.md` 仅在复杂页型、迁移或门禁失败时读取。

PAGE 明细只写页面事实和设计决策。不要复制页型规则、视觉基线或上游 API/Feature 内容，直接引用其编号和路径。

