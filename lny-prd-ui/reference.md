# UI 模板与层级约定

落盘前 Read 本节。COMP 编号 **必填** `COMP-{三位序号}`。

## 分片索引

| 分片 | 内容 | 何时 Read |
|------|------|-----------|
| [`reference/ui-manifest-template.md`](reference/ui-manifest-template.md) | `ui_manifest.md` 轻量索引骨架模板 | ① 立项 / ② 续跑生成或更新 `ui_manifest.md` 时 |
| [`reference/visual-rules.md`](reference/visual-rules.md) | UI 视觉、页型与交互表现作者规则；不复制进项目 manifest | ② 写 PAGE/COMP 与⑥对齐视觉时 |
| [`reference/component-template.md`](reference/component-template.md) | `ui/COMP-*.md` 明细模板 | 写组件详述时 |
| [`reference/page-template.md`](reference/page-template.md) | `ui/PAGE-*.md` 明细模板 | 写页面详述时 |

> §1 分层/滚动/交互等完整约定在 [`reference/ui-manifest-template.md`](reference/ui-manifest-template.md)；视觉实现边界见 `lny-prd-prototype` 的 `reference-kit.md` 与 `gold/`，不在本文件重复。

## 立项落盘与 `ui/` 目录初始化

**`/lny-prd-master` 立项时**：创建空目录 **`ui/`**，按 [`reference/ui-manifest-template.md`](reference/ui-manifest-template.md) 生成根目录 **`ui_manifest.md`**（索引骨架；**§2 UI 框架** 按 `main_spec` 第4章预填终端行）。

**`/lny-prd-ui` 续跑时**：

1. 若 **`ui_manifest.md` 不存在**：按 [`reference/ui-manifest-template.md`](reference/ui-manifest-template.md) 在根目录创建；同步创建 **`ui/`**（若不存在）。
2. 若 **`ui/` 不存在**：创建空目录；旧版 manifest 内大段页面/组件正文须 **迁移** 至 `ui/PAGE-*.md`、`ui/COMP-*.md` 后 manifest **只留索引**。
3. 新增 **`PAGE-*`**：更新 **§3.2**（及 MP **§3.1** 若涉及）→ 按 [`reference/page-template.md`](reference/page-template.md) 创建 **`ui/PAGE-{终端}-{序号}.md`**。
4. 新增 **`COMP-*`**：更新 **§4** → 按 [`reference/component-template.md`](reference/component-template.md) 创建 **`ui/COMP-{序号}.md`**。
5. **禁止**在 `ui/` 存放 API 字段表、Feature 流程正文、原型 HTML。

## 明细模板（放在本技能维护）

`ui_manifest.md` 作为索引清单，不再内嵌明细模板引用；单组件模板见 [`reference/component-template.md`](reference/component-template.md)，单页面模板见 [`reference/page-template.md`](reference/page-template.md)。
