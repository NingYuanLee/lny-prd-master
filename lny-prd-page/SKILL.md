---
name: lny-prd-page
description: >-
  生成单页 PRD 至 versions/{v}/pages_prd/；含 ASCII 线框与估点信号。PC/AD 必产 _shell。
  Use when the user mentions /lny-prd-page, @lny-prd-page, 单页 PRD, pages_prd.
disable-model-invocation: true
---

## 与总控的关系

本步为 **⑤ `/lny-prd-page`**。产物：`versions/{v}/pages_prd/`（含桌面 `_shell`）。不依赖原型。完成后建议 **⑥ 原型**；⑦ 须用户明确要求检查。全流程见 `lny-prd-master/SKILL.md`。变更记录表仅 ① 首行 / ⑧ 追加；仅改 `pages_prd` 且未改根规格时可省略流水。

# 产出单页 PRD `/lny-prd-page`

## Additional resources

- 产出具约束、单页模板、桌面壳模板：[`reference.md`](reference.md)
- 框架排除：`lny-prd-master/framework-exclusions.md`

## 夹具速查（写单页前扫一眼）

夹具 `examples/mini-shop/` 的 ASCII / 分区措辞模板。线框 **只定分区顺序**；⑥ 视觉以 `gold/` 为准。体验细则见 `lny-prd-ui` **§1.3.3 / §1.4.3**。

**移动端 ASCII 自上而下**

| 页型 | 夹具 | 线框顺序 | 「结构与控件」须带到的词 |
|------|------|----------|--------------------------|
| TabBar 宫格 | PAGE-MP-001 | 下沉 Banner → 金刚 → 双列卡 → TabBar | 沉浸式；无页内顶栏；封面 1:1 |
| 列表 | PAGE-MP-002 | 搜索行+筛选行贴顶 → 1:1 横卡 | 搜索/筛选不进滚动区；半屏方向 |
| 详情 | PAGE-MP-003 | 返回叠 16:9 → 图文介绍 → 评论 → 贴底次要操作 | 时间行；附图 1:1、一排最多五张 |
| 表单 | PAGE-MP-004 | 返回顶栏 → 独立成行输入 → 贴底提交 | 右侧安全距；滑动条/轮盘/上传点名 |

**桌面端 ASCII 自上而下**

| 页型 | 夹具 | 线框顺序 | 「结构与控件」须带到的词 |
|------|------|----------|--------------------------|
| D1-1 | PAGE-AD-001 | 面包屑 → 签 → 筛 → 功能 → 表 → 汇总左+分页右贴底 | 无页内大标题；勾选左冻/操作右冻「更多」；**列宽按语义**（名称吃剩余，售价/状态/日期窄）；**紧凑多看行** |
| D1-2 | PAGE-AD-002 | 面包屑 → 字段分区 → 保存/取消 | 无页内大标题；不要写 D1-1 紧凑行高 |

禁止：ASCII 漏掉「贴顶/贴底/左冻/右冻/语义列宽/紧凑」，把这些留给 ⑥ 去猜。

## 开笔前

Read `lny-prd-master/framework-exclusions.md`。不为已排除项生成单页 PRD。Read `main_spec` §1.5「明确不做」（若有）：**禁止**为清单中的能力写单页 PRD。落盘前 **完整 Read [`reference.md`](reference.md)**。

## 职责与禁止

- **负责**：按页生成 `pages_prd`；**项目含 PC 或 AD 时必须**落盘 `pages_prd/_shell/{终端编码}-shell.md`。
- **禁止**：抄 `api/` 字段表；编造未立项 PAGE；把约束说明写入产物；单页罗列壳层换页。仅当 PM 已说出点位才写埋点；**禁止自拟埋点方案**。

## 前置条件

已执行 ①②③；目标 `PAGE-*` 已在 `ui/` 登记。⑧ 委派时以 `ui_changes.md` 的 `pages_prd目标路径` 为准。

## 输入

```yaml
版本号: v1.0.0
页面编号: PAGE-MP-001
页面名称: 首页
接口编号列表: [API-MP-001]
```

未指定版本号时按 master §1.1。

## 执行步骤

1. 校验版本目录与页面编号；有台账则核对目标路径。
2. Read `ui/PAGE-*` + 引用 COMP、`api/API-*`、`feature/`、`main_spec` §1.2（仅作背景）。
3. 按 [`reference.md`](reference.md) 模板落盘；§1 表后写根规格依赖引用块；§3 顶 ASCII 线框默认必填（页型顺序见上方夹具速查）。交互、动效、收纳从 `ui/PAGE-*` **§2.3** 带入，禁止降级成「有个按钮」。桌面 D1-1 须写列宽语义与紧凑密度。
4. 路径：`pages/{m}` → `pages_prd/pages/{m}/`；`subpackages/{m}` → `pages_prd/subpackages/{m}/`；`views/{m}` → `pages_prd/views/{m}/`。
5. 若终端含 PC/AD：按壳模板写 `_shell/{编码}-shell.md`（尚无则创建）。
6. 若改了根四规范：`iteration_notes` 文末追加；否则省略。
7. 提示下一步：**⑥ `/lny-prd-prototype`**。⑦ 须用户明确要求检查，不自动跑。
