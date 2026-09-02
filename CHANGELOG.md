# 变更日志

LNY-PRD 技能包（`bundle_id: lny-prd`）的显著变更记录于此文件。

- 版本号必须与 `skill-bundle.json` 的 `bundle_version`、`README.md` 的「工具包版本」保持一致（`scripts/validate-skill-package.py` 强制）。
- 升版使用 `python scripts/bump_version.py <X.Y.Z>`：同步上述位置并预置本节模板。
- 2.14.0 之前的历史未追溯（早期提交以 `v2.8.x` 系列编号留言，无语义版本标签），详见 git 历史。

## Unreleased

## 2.18.0 - 2026-09-02

- ④ 新增领域粒度门禁：Module 默认复用现有边界，只有具备稳定核心对象、独立规则/生命周期、清晰范围与跨域契约时才允许新建；页面、终端、CRUD、流程阶段、技术组件和单 Feature 改名不得充当领域。
- 明确 Module 少量、稳定、粗粒度，Module 只写边界级短句/短列表；业务规则、流程、验收及 STORY/FEATURE/AC/PAGE/API/EXT 细节统一下沉 Feature。
- ⑦ 新增 Module 功能级编号泄漏、孤立 Module 和循环依赖校验与负例；单 Feature Module、Module/Feature 数量接近等只作为语义复核信号，不设僵硬数量阈值。

## 2.17.0 - 2026-09-02

- 建立规格、Story、Module、Feature/AC 四驱动模型：Story 扩展到用户价值、运营、合规、迁移和技术使能，所有正式 Feature 必须具备明确 Story 来源、唯一 Module 归属和可验证 AC。
- Story↔Feature 映射统一以 `feature/FEATURE-*.md` 为事实源；`main_spec.md` Story 表移除 Feature 反向列，检查器由 Feature 明细反查 Story 覆盖。
- Module 领域边界迁入 `feature_spec.md` 并由④统一维护，不新增技能或 `module/` 目录；`main_spec.md` 删除模块注册表，Feature 明细只引用 `MODULE-*`，不复制模块名称。
- 收敛三类根索引的事实源边界：Feature 与 API/EXT 仅保留编号、名称和明细路径；UI manifest 只保留全局页面注册、路由、包类型和生命周期，PAGE/COMP 设计事实回归明细。
- ⑦ 语义扫描器直接从明细验证生命周期、评审、Story、Module、分支及 PAGE/API/EXT 关联，并新增 Story 覆盖、Module 边界与依赖负例；旧宽索引、旧 Story 表和旧 Module 注册表保留只读兼容。

## 2.16.1 - 2026-09-01

- ⑥ 金样速查门禁校验一行内全部 PAGE 编号（不再只看第一个），并内置「第二编号非法」负例。
- Cursor 宿主同步改为走 `install-skills.py update --host cursor`，禁止只拷目录导致 `install.json` 落后。

## 2.16.0 - 2026-09-01

- 立项确认摘要必须列出 `lny-default` 将不展开的类别闭集；看不见清单不得请用户确认。确认仍等于沿用。
- 总控 §3 改为用户意图短树；完整条件表下沉 `lny-prd-master/reference-routing.md`。
- ②⑤⑥ 速查只留本步增量（体验 / 线框词 / 关键类）；金样文件名以 `reference-page-types.md` 为正本。`validate_page_type_consistency` 不再要求 ⑥ 每行自带金样文件名。
- README 新增 5.4 换栈（`profile: none`）最小立项示例；`examples/` 仍是回归夹具。
- ⑨ 对话回报固定五行：FE_SP / BE_SP / 合计、校准系数（默认 `1.0（暂定）`）、非日历工期声明。

## 2.15.0 - 2026-09-01

- 修复 6 处已发布技能内的「仓库 README」死链（改指随包可达位置或删除指针）。
- 新增防复发门禁 `validate_skill_references`：禁止技能文件在 prose 中引用仓库根文件（README/LICENSE/skill-bundle.json/CHANGELOG/requirements）。
- `reference-kit.md` 拆分索引化：索引保留全局 token（67K 字符 → 8.4K），类名字典分为 `reference-kit/` 下 5 个分域分片，入站引用同步更新。
- 页型速查表与正本 `reference-page-types.md` 建立发布门禁比对（`validate_page_type_consistency`）；三份速查表加入「冲突以正本为准」优先级规则。
- 新增 `CHANGELOG.md` 与 `scripts/bump_version.py`（版本号单一命令同步三处，`validate_changelog` 强制顶版一致）。
- 安装器健康检查区分 `unreadable` 与 `locally modified`，`unreadable` 时拒绝 `update/uninstall --force`（`UnreadableSkillError` fail-loud）。
- `.cursor/rules` 本地规则去重并声明仅 Cursor 宿主生效。
- `lny-prd-ui/reference.md` 拆分索引化：索引保留落地/初始化约定与分片表；`ui_manifest.md` / `ui/COMP-*.md` / `ui/PAGE-*.md` 三份模板分别落 `lny-prd-ui/reference/` 下三片，入站 §x.y 指针同步更新。
- ⑦ 语义扫描器 `validate-prd-project.py` 输出机器可读 `NEXT_STEP_ROUTE:`（issue 码 → 建议委派技能，供 ① 总控路由消费）。
- `examples/` 定位为**回归夹具**单一身份（供 ⑦ 检查类 AI 自检与作者验收对照）：`skill-bundle.json` audience 改 `regression`，README 与 `export-examples` 文案同步，撤「人类样例」表述（2026-09-01 决议：不做样例/夹具分目录，单一身份即收口）。
- 框架排除 profile 立项交互显式化：确认摘要中明确「要不要改」询问，**用户未主动要求更改即按 `lny-default` 默认沿用**（2026-09-01 决议：作者为主要使用者，默认不变，仅显式展示询问）。
- CI 缓存：`.github/workflows/validate-skills.yml` 用 `actions/cache@v4` 按版本键缓存 `~/.cache/ms-playwright` 与 `~/.npm`，命中时浏览器不再全量下载。至此原 P3 三项全部收口（profile 显式化、examples 单一身份、CI 缓存）。

## 2.14.0 - 2026-08-29

- 新增 ⑧ `lny-prd-review` 需求与交付范围评审技能：拟定结论 / 确认落盘两段式；`delivery_scope.md` 仅由 ⑧ 在产品确认后创建或更新（`272e5d3`）。
- 精化评审与交付门禁：⑧ 结论包、⑨ 已确认范围估点、⑩ 前版保底检查对齐（`b79f823`）。
- 移除原型每轮三页上限：⑥ 按目标页面范围一次完成、逐页对照金样与质量门禁（`52176d2`）。
- 移除云效（Yunxiao）交付导出适配器（`f21d64c`）；`main_spec` 展开为共享阅读指南并去掉根级冗余统计（`785f107`、`4818d4e`）。
