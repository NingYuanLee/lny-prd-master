# 原型页面实现规则

写业务 PAGE 时读取。先读 `pages_prd`、`ui/PAGE §2.3 + §2.4`、引用 COMP、UI 视觉基线、[`reference-demo-fidelity.md`](reference-demo-fidelity.md) 和 [`../lny-prd-ui/reference/visual-consistency.md`](../lny-prd-ui/reference/visual-consistency.md)。

- 默认先完成设计决策再实现页面。若 PAGE 缺少任务、视觉锚点、素材策略或响应式取舍，依据 [`../lny-prd-master/reference-design-decision.md`](../lny-prd-master/reference-design-decision.md) 自动补齐，并记录默认假设。
- 只实现规格已确定的结构、字段、状态和跳转。
- 读取已有 `visual-lock.md`、`project-theme.css`、引用的 `COMP-*` 和 PAGE §2.4 作为设计参考。页面依据任务、项目事实和设计判断选择视觉方向，可以发展页面族或单页的独立表达。已有 COMP 的结构、交互和状态语义优先复用。
- 页面必须有主次、合理密度、真实或可信素材、加载/空/失败状态。默认态使用自洽的业务数据和用户文案，禁止开发说明、规格编号、占位词和草稿化填充。
- 以 HTML 的真实渲染结果作为最终视觉验收对象。概念图只用于视觉探索，独立图片素材可以进入页面，整页生图不得代替页面结构和交互。
- 对字体、边框、装饰、纹理和阴影逐项确定来源或实现路径。不可获得的关键资产使用本地 CSS、SVG 或主题一致的图形化处理，并记录实现路径。业务页不显示“占位”文字或灰色空块。
- 生成后先做一次真实渲染自检，再报告完成。

壳层、关系图和完整质量门禁按需读取对应参考文件。
