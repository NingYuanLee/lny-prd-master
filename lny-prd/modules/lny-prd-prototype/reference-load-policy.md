# 原型模块加载策略

原型模块默认按最小上下文读取，失败或场景复杂时再升级。

## 默认读取

- `SKILL.md`
- `reference-page-implementation.md`
- `reference-demo-fidelity.md`
- `reference-quality-quick.md`
- `../lny-prd-ui/reference/visual-consistency.md`
- `../lny-prd-master/reference-decision-walkthrough.md`
- 当前页面的 `pages_prd`、UI 明细和 COMP 明细

## 按需升级

| 场景 | 再读取 |
|---|---|
| 壳层或总入口 | `reference-shell-quick.md`，失败后 `reference-shell.md` |
| 规格覆盖或结构门禁失败 | `reference-quality.md` 对应章节 |
| 视觉方向不清或需要返修 | `reference-visual-improvement.md`、`reference-visual-self-review.md` |
| 图标缺失 | `reference-icons.md` |
| 复杂状态、路径或资源问题 | `reference-shell.md`、`reference-quality.md` |

不要因为页面进入原型步骤就预加载全部参考文件。当前页无关的终端词典、壳层细节、完整质量表和截图差异规则延迟到确实需要时再读取。

