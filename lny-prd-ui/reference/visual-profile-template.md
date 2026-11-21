# 项目级视觉档案

`/lny-prd-ui` 在项目缺少统一视觉事实，或已有两个以上页面需要共享视觉语言时，创建或更新以下文件：

```text
ui/visual/visual-profile.md
ui/visual/tokens.json
ui/visual/assets-manifest.md
```

这些文件记录项目级设计事实。页面自身的任务、层级、状态和页面特有决策仍写入 `ui/PAGE-*.md`，组件状态仍写入 `ui/COMP-*.md`。

## visual-profile.md

```markdown
# 项目视觉档案

## 产品气质
- 领域语汇：
- 品牌线索：
- 禁用方向：

## 视觉语言
- 色彩语义：
- 字体层级：
- 间距节奏：
- 边界与圆角：
- 阴影与层次：
- 图标语言：
- 图片和插画语言：
- 状态语言：
- 动效语言：

## 页面模式
- 移动端：
- 桌面端：
- 首页：
- 列表：
- 详情：
- 表单：
- 工作台：

## 已确认决策
| 决策 | 内容 | 来源 | 确认状态 |
|------|------|------|----------|

## 默认假设
| 假设 | 依据 | 可替换点 |
|------|------|----------|
```

## tokens.json

使用 CSS 自定义属性可直接表达的项目令牌。没有项目事实时，技能根据页面任务自动生成一组克制的默认值，并在 `visual-profile.md` 记录依据。

```json
{
  "color": {
    "brand": "",
    "accent": "",
    "background": "",
    "surface": "",
    "text": "",
    "mutedText": "",
    "border": "",
    "success": "",
    "warning": "",
    "danger": ""
  },
  "type": {
    "fontFamily": "",
    "title": "",
    "body": "",
    "caption": ""
  },
  "space": {
    "page": "",
    "section": "",
    "component": "",
    "inline": ""
  },
  "shape": {
    "smallRadius": "",
    "mediumRadius": "",
    "largeRadius": ""
  }
}
```

## assets-manifest.md

```markdown
# 项目视觉素材清单

| 资产 | 类型 | 路径 | 用途 | 比例或约束 | 可替代方案 | 状态 |
|------|------|------|------|------------|------------|------|
```

## 使用规则

- 视觉档案是共享事实，页面不得无理由覆盖项目级决策。
- 页面可以追加局部视觉决策，但必须说明覆盖范围。
- `tokens.json` 只保存令牌，不保存业务字段、接口契约或页面路径。
- 资产清单记录独立素材，不把整页截图当作页面资产。
- 项目已有品牌事实优先于技能默认值。
