# 原型质量快速规则

常规单页完成后先执行：规格覆盖、真实渲染、视觉评分、首屏层级、密度、溢出、图片比例、滚动、状态和演示内容检查。直接打开业务 `PAGE-*.html`，确认没有说明性文案、开发词、占位词、草稿数据和不自洽的字段关系。

需要保留截图时运行：

```text
node <skillDir>/modules/lny-prd-prototype/scripts/render-prototype.mjs <prdRoot> --page PAGE-… --output <reviewDir>
node <skillDir>/modules/lny-prd-prototype/scripts/score-visual-quality.mjs <prdRoot> --render-dir <reviewDir>
```

已有基准截图时可运行 `compare-prototype-shot.mjs <baseline.png> <current.png>` 生成像素差异报告。视觉评分用于发现客观实现问题，不能替代产品对品牌方向的最终判断。

Q-P 或复杂问题复核时再读取 [`reference-quality.md`](reference-quality.md) 的完整 G.3～G.5。
