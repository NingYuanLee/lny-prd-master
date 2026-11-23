# 原型壳层快速规则

只有维护终端 `index.html`、总入口或 `map.html` 时读取。业务单页无需读取完整壳层参考。

- `index.html` 只填 `PROTO_SHELL`。
- 共享 kit 和 assets 由壳层统一提供。
- 壳层、总入口和关系图沿用 kit 的固定样式与交互。业务 `PAGE-*.html` 可以完全使用项目自有 CSS，不要求继承壳层皮肤。
- 移动端同步维护 `index.html` 与 `map.html`。
- 不在业务页复制侧栏、顶栏、状态演示或关系图逻辑。

完整结构见 [`reference-shell.md`](reference-shell.md)。
