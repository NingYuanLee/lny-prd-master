
## 与总控的关系

本步为 **⑤ `$lny-prd`**。产物：根 `pages_prd/{终端}/PAGE-*.md` 与桌面 `pages_prd/_shell/` 工作源；不写版本快照，不依赖原型。②③④完成后由总控先做⑤前置自检，通过即自动执行本步；本步完成后自动进入 **⑦/Q-S**，通过后自动进入⑥。全流程见 `modules/lny-prd-master/SKILL.md`。变更记录表仅①首行/⑩追加；仅改根 `pages_prd` 且未改根四规范时可省略流水。

# 产出单页 PRD `$lny-prd`

## Additional resources

- 产出具约束、单页模板、桌面壳模板：[`reference.md`](reference.md)
- 自动设计决策协议：[`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md)
- 三步职责、页型编号与映射：[`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)
- 正式落点与禁止副本范围：[`../lny-prd-master/reference-artifact-paths.md`](../lny-prd-master/reference-artifact-paths.md)
- 框架排除：`modules/lny-prd-master/framework-exclusions.md`

## 三步对照（防错用）

先 Read [`../lny-prd-master/reference-page-types.md`](../lny-prd-master/reference-page-types.md)。本步只维护 ASCII 分区顺序和单页 PRD 表达；下方速查表只保留 ⑤ 的专属措辞。页型 ↔ 编号 ↔ 映射与跨步骤不变量以该正本为唯一事实源；本表与正本冲突时以正本为准（发布门禁自动比对）。

**树 vs 章节列表**：ASCII 与「结构与控件」须跟 master 选型一致——章节目录写父子章节列表（PAGE-MP-015）；分类树写左多级树右内容（PAGE-MP-008）；左分组右横卡写分类导航（PAGE-MP-013）。禁止三者混名。

**浮层遮罩**：规格或 ASCII 出现弹窗/半屏/抽屉时，「结构与控件」须写**遮罩层 + 浮层形态（弹窗 / 半屏 / 抽屉）**与**壳层浮层接口（`ProtoPage.openDialog` / `openDrawer`）**，禁止只写无遮罩的白面板。

## 页型速查

线框表达内容关系、主次操作与必要的阅读顺序。尺寸、列数、滚动方式等若是用户或平台要求，带上来源；自动选择的构图沿用 UI 的当前方案，允许依据真实渲染调整。 编号与页型见[共享映射](../lny-prd-master/reference-page-types.md)。

## 开笔前

Read `modules/lny-prd-master/framework-exclusions.md` 与 `modules/lny-prd-master/reference-artifact-paths.md`。不为已排除项生成单页 PRD。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力写单页 PRD。落盘前 **完整 Read [`reference.md`](reference.md)**。

## 职责与禁止

- **负责**：按页生成根 `pages_prd/{终端}/` 工作源；§6 用 `关联AC` 反向登记本页承接的 Feature AC（只写 AC ID，不复制正文）；**项目含 PC 或 AD 时必须**落盘 `pages_prd/_shell/{终端编码}-shell.md`；成功自检后推进本次 `ui_changes.md` 对应行状态。
- **禁止**：抄 `api/` 字段表；编造未立项 PAGE；把约束说明写入产物；单页罗列壳层换页。仅当 PM 已说出点位才写埋点；**禁止自拟埋点方案**。

## 前置条件

已执行①②③④；目标 `PAGE-*` 已在 `ui/` 登记。总控在进入⑤前执行轻量输入自检：核对页面、接口、Feature/AC及必要产品事实是否足以生成逐页规格。可自动修复的缺口定向返回②③④并同轮重检；缺产品事实才询问用户。该自检不是正式Q-S。

## 输入

```yaml
版本号: v1.0.0
页面编号: PAGE-MP-001
页面名称: 首页
接口编号列表: [API-MP-001]
```

未指定版本号时按 master §1.1。

## 并行分片

需要并行时完整 Read [`../lny-prd-master/reference-agent-orchestration.md`](../lny-prd-master/reference-agent-orchestration.md)。⑤输入自检通过且 PAGE ID、路由与引用已锁定后，可按每个 `pages_prd/{终端}/PAGE-*.md` 启动一个独占子任务；同一 PAGE 不拆给多个 Agent。`pages_prd/_shell/`、跨页导航一致性、台账 `待⑤→已完成` 与最终全量自检由主 Agent 单写/汇总。子任务必须返回实际文件、自检和未决问题；无 subagent/Task 时顺序生成全部目标页。

## 执行步骤

1. 校验版本目录与页面编号；有台账则核对目标路径。
2. Read `ui/PAGE-*` + 引用 COMP、`api/API-*`、`feature/`、`main_spec` §1.2（仅作背景）。
3. 按 [`reference.md`](reference.md) 模板落盘；§1 表后写根规格依赖引用块；§3 顶 ASCII 线框默认必填（按本页内容关系）；§6 反查 Feature AC 的 `关联页面`，写入本页对应的 AC ID 集合并核对双向一致。交互、动效、收纳从 `ui/PAGE-*` **§2.3** 带入，视觉方向从 **§2.4** 带入，素材和实现约束从 **§2.5** 带入，禁止降级成「有个按钮」。
4. 工作源路径固定为 `pages_prd/{终端编码}/{PAGE-ID}.md`，例如 `pages_prd/MP/PAGE-MP-001.md`、`pages_prd/AD/PAGE-AD-001.md`。页面真实路由写入基本信息，不参与工作源文件寻址。
5. 若终端含 PC/AD：按壳模板写 `_shell/{编码}-shell.md`（尚无则创建）。
6. 单页 PRD 与桌面壳自检通过后，将本次 `ui_changes.md` 条目由 `待⑤` 改为 `已完成`；有缺口或失败则保留 `待⑤`。
7. 若改了根四规范：`iteration_notes` 文末追加；否则省略。
8. 自动进入 **⑦/Q-S**。Q-S通过后自动进入⑥；失败则按责任定向返修②③④或⑤并重跑。仅当用户明确要求“只要规格/不要原型”时，在Q-S通过后停止。

## 产物长度

正式产物遵守 `../lny-prd-master/reference-common.md` 的产物精简规范。只写本步骤新增的事实和决策，重复内容用编号或路径引用。
