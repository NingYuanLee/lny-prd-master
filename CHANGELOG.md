# 变更日志

LNY-PRD 技能包（`bundle_id: lny-prd`）的显著变更记录于此文件。

- 版本号必须与 `skill-bundle.json` 的 `bundle_version`、`README.md` 的「工具包版本」保持一致（`scripts/validate-skill-package.py` 强制）。
- 升版使用 `python scripts/bump_version.py <X.Y.Z>`：同步上述位置并预置本节模板。
- 2.14.0 之前的历史未追溯（早期提交以 `v2.8.x` 系列编号留言，无语义版本标签），详见 git 历史。

## Unreleased

- 修复 6 处已发布技能内的「仓库 README」死链（改指随包可达位置或删除指针）。
- 新增防复发门禁 `validate_skill_references`：禁止技能文件在 prose 中引用仓库根文件（README/LICENSE/skill-bundle.json/CHANGELOG/requirements）。
- `reference-kit.md` 拆分索引化：索引保留全局 token（67K 字符 → 8.4K），类名字典分为 `reference-kit/` 下 5 个分域分片，入站引用同步更新。
- 页型速查表与正本 `reference-page-types.md` 建立发布门禁比对（`validate_page_type_consistency`）；三份速查表加入「冲突以正本为准」优先级规则。
- 新增 `CHANGELOG.md` 与 `scripts/bump_version.py`（版本号单一命令同步三处，`validate_changelog` 强制顶版一致）。
- 安装器健康检查区分 `unreadable` 与 `locally modified`，`unreadable` 时拒绝 `update/uninstall --force`（`UnreadableSkillError` fail-loud）。
- `.cursor/rules` 本地规则去重并声明仅 Cursor 宿主生效。
- `lny-prd-ui/reference.md` 拆分索引化：索引保留落地/初始化约定与分片表；`ui_manifest.md` / `ui/COMP-*.md` / `ui/PAGE-*.md` 三份模板分别落 `lny-prd-ui/reference/` 下三片，入站 §x.y 指针同步更新。
- ⑦ 语义扫描器 `validate-prd-project.py` 输出机器可读 `NEXT_STEP_ROUTE:`（issue 码 → 建议委派技能，供 ① 总控路由消费）。
- 评审决议（2026-08-31 收敛，显式后置非遗漏）：`lny-default` 默认 profile 弱化、`examples` 样例/夹具分离、CI Playwright/npm 缓存（P3）。

## 2.14.0 - 2026-08-29

- 新增 ⑧ `lny-prd-review` 需求与交付范围评审技能：拟定结论 / 确认落盘两段式；`delivery_scope.md` 仅由 ⑧ 在产品确认后创建或更新（`272e5d3`）。
- 精化评审与交付门禁：⑧ 结论包、⑨ 已确认范围估点、⑩ 前版保底检查对齐（`b79f823`）。
- 移除原型每轮三页上限：⑥ 按目标页面范围一次完成、逐页对照金样与质量门禁（`52176d2`）。
- 移除云效（Yunxiao）交付导出适配器（`f21d64c`）；`main_spec` 展开为共享阅读指南并去掉根级冗余统计（`785f107`、`4818d4e`）。
