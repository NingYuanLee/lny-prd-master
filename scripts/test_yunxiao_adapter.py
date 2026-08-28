from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "lny-prd-yunxiao" / "scripts" / "build-yunxiao-plan.py"
VALIDATOR = ROOT / "lny-prd-yunxiao" / "scripts" / "validate-export-plan.py"


class YunxiaoAdapterTests(unittest.TestCase):
    def make_project(self, root: Path) -> None:
        (root / "ui").mkdir()
        (root / "api").mkdir()
        (root / "feature").mkdir()
        version = root / "versions" / "v1.0.0"
        version.mkdir(parents=True)
        pages_prd = version / "pages_prd"
        pages_prd.mkdir()
        (root / "main_spec.md").write_text(
            """# 产品规格说明书 - Adapter Fixture

| 模块编号 | 模块名称 | 说明 |
|---|---|---|
| MODULE-001 | 商品 | 商品能力 |

| 终端类型编码 | 终端名称 | 有效页面总数 | 有效局部自定义UI组件数 |
|---|---|---:|---:|
| MP | Mini | 1 | 0 |
| AD | Admin | 1 | 0 |

| 终端类型编码 | 终端名称 | 有效API数 |
|---|---|---:|
| MP | Mini | 1 |

| 统计项 | 数值 |
|---|---:|
| 有效 Feature 个数 | 1 |

| 故事编号 | 关联 FEATURE / 框架承接 |
|---|---|
| STORY-001 | FEATURE-001 |
""",
            encoding="utf-8",
        )
        (root / "ui_manifest.md").write_text(
            """# UI
| 页面编号 | 状态 | 明细路径 |
|---|---|---|
| PAGE-MP-001 | active | ui/PAGE-MP-001.md |
| PAGE-AD-001 | active | ui/PAGE-AD-001.md |
""",
            encoding="utf-8",
        )
        (root / "api_spec.md").write_text(
            """# API
| 接口编号 | 描述 | 明细路径 |
|---|---|---|
| API-MP-001 | List | api/API-MP-001.md |
""",
            encoding="utf-8",
        )
        (root / "feature_spec.md").write_text(
            """# Features
| 功能编号 | 功能名称 | 模块编号 | 所属模块 | 状态 | 评审状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |
|---|---|---|---|---|---|---:|---|---|---|
| FEATURE-001 | 浏览商品 | MODULE-001 | 商品 | active | approved | 2 | PAGE-MP-001, PAGE-AD-001 | API-MP-001 | feature/FEATURE-001.md |
""",
            encoding="utf-8",
        )
        (root / "ui" / "PAGE-MP-001.md").write_text(
            """# PAGE-MP-001
| 属性 | 内容 |
|---|---|
| 页面编号 | PAGE-MP-001 |
API-MP-001 FEATURE-001

| 接口编号 | 用途（一句话） | 触发时机 |
|---|---|---|
| API-MP-001 | 查询商品 | 页面初始化 |
""",
            encoding="utf-8",
        )
        (root / "api" / "API-MP-001.md").write_text(
            """# API-MP-001
| 项目 | 内容 |
|---|---|
| 接口编号 | API-MP-001 |
FEATURE-001 PAGE-MP-001
""",
            encoding="utf-8",
        )
        (root / "ui" / "PAGE-AD-001.md").write_text(
            """# PAGE-AD-001
| 属性 | 内容 |
|---|---|
| 页面编号 | PAGE-AD-001 |
API-MP-001 FEATURE-001

| 接口编号 | 用途（一句话） | 触发时机 |
|---|---|---|
| API-MP-001 | 查询商品 | 页面初始化 |
""",
            encoding="utf-8",
        )
        (root / "feature" / "FEATURE-001.md").write_text(
            """# FEATURE-001 浏览商品
| 属性 | 内容 |
|---|---|
| 功能编号 | FEATURE-001 |
| 功能名称 | 浏览商品 |
| 模块编号 | MODULE-001 |
| 所属模块 | 商品 |
| 状态 | active |
| 评审状态 | approved |
| 分支数 | 2 |

- 关联页面：PAGE-MP-001, PAGE-AD-001
- 关联接口：API-MP-001
- 关联第三方接口：无

| AC 编号 | 验收描述（可验证） | 关联页面 | 关联接口 | 验证方式 |
|---|---|---|---|---|
| AC-1 | 可以浏览 | PAGE-MP-001 | API-MP-001 | UI + API |
| AC-2 | 失败可重试 | PAGE-MP-001 | API-MP-001 | 异常流测试 |
""",
            encoding="utf-8",
        )
        (pages_prd / "PAGE-MP-001.md").write_text(
            """# PAGE-MP-001
## 5. API 交互清单
| 接口编号 | 在本页的用途（一句话） | 触发时机 |
|---|---|---|
| API-MP-001 | 查询商品 | 页面初始化 |
""",
            encoding="utf-8",
        )
        (pages_prd / "PAGE-AD-001.md").write_text(
            """# PAGE-AD-001
## 5. API 交互清单
| 接口编号 | 在本页的用途（一句话） | 触发时机 |
|---|---|---|
| API-MP-001 | 查询商品 | 页面初始化 |
""",
            encoding="utf-8",
        )
        (version / "delivery_scope.md").write_text(
            """# 交付范围 - v1.0.0
## 1. 范围状态
> **产品经理填写说明**
> - `评审状态` 只填一个值；范围确认后填 `approved`。
> - `产品确认项` 全部关闭后填 `0`。

| 属性 | 内容 |
|---|---|
| 版本号 | v1.0.0 |
| 评审状态 | approved |
| 产品确认项 | 0 |

## 2. Feature 范围
> **产品经理填写说明**
> - 只有本期开发且已确认的 Feature 才填 `本期开发` 和 `approved`。

| Feature | 纳入方式 | 评审状态 | 阻塞决策 |
|---|---|---|---:|
| FEATURE-001 | 本期开发 | approved | 0 |

## 3. 未决决策
> **产品经理填写说明**
> - 未形成结论填 `open`，形成结论后填 `closed`。

| 决策编号 | 状态 | 问题 | 影响对象 |
|---|---|---|---|
| 无 | closed | 无 | 无 |
""",
            encoding="utf-8",
        )

    def run_builder(self, root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), str(root), *arguments],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def run_plan_validator(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_validate_and_plan_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-ok-") as temp:
            root = Path(temp)
            self.make_project(root)
            checked = self.run_builder(root, "--mode", "validate", "--version", "v1.0.0")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["selectedFeatures"], ["FEATURE-001"])

            first = self.run_builder(root, "--mode", "plan", "--version", "v1.0.0")
            second = self.run_builder(root, "--mode", "plan", "--version", "v1.0.0")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(first.stdout, second.stdout)
            plan = json.loads(first.stdout)
            self.assertEqual(
                [item["sourceId"] for item in plan["items"]],
                ["MODULE-001", "FEATURE-001", "FEATURE-001:BE", "FEATURE-001:MP", "FEATURE-001:TEST"],
            )
            test_item = next(item for item in plan["items"] if item["sourceId"] == "FEATURE-001:TEST")
            self.assertEqual(test_item["acceptanceCriteria"][0]["verification"], "UI + API")
            be_item = next(item for item in plan["items"] if item["sourceId"] == "FEATURE-001:BE")
            self.assertEqual(be_item["sourceRefs"], ["API-MP-001", "PAGE-AD-001"])
            self.assertEqual(be_item["dependencyRefs"], [])
            self.assertEqual(be_item["pageApiBindings"], [{
                "pageRef": "PAGE-AD-001",
                "interfaceRef": "API-MP-001",
                "purpose": "查询商品",
                "trigger": "页面初始化",
            }])
            self.assertEqual([item["id"] for item in be_item["acceptanceCriteria"]], ["AC-1", "AC-2"])
            mp_item = next(item for item in plan["items"] if item["sourceId"] == "FEATURE-001:MP")
            self.assertEqual(mp_item["sourceRefs"], ["PAGE-MP-001"])
            self.assertEqual(mp_item["dependencyRefs"], ["API-MP-001"])
            self.assertEqual(mp_item["pageApiBindings"], [{
                "pageRef": "PAGE-MP-001",
                "interfaceRef": "API-MP-001",
                "purpose": "查询商品",
                "trigger": "页面初始化",
            }])
            self.assertEqual([item["id"] for item in mp_item["acceptanceCriteria"]], ["AC-1", "AC-2"])
            self.assertEqual(mp_item["acceptanceCriteria"][0]["pageRefs"], ["PAGE-MP-001"])
            self.assertFalse(any(item.get("deliverySurface") == "FE" for item in plan["items"]))
            serialized = json.dumps(plan).lower()
            self.assertNotIn("yunxiaoid", serialized)
            self.assertNotIn("assignee", serialized)
            plan_path = root / "yunxiao-plan.json"
            plan_path.write_text(first.stdout, encoding="utf-8")
            validated = self.run_plan_validator(plan_path)
            self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_missing_scope_requires_explicit_feature(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-scope-") as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "versions" / "v1.0.0" / "delivery_scope.md").unlink()
            blocked = self.run_builder(root, "--mode", "validate")
            self.assertEqual(blocked.returncode, 1)
            self.assertIn("DELIVERY_SCOPE_MISSING", blocked.stderr)
            fallback = self.run_builder(root, "--mode", "validate", "--feature", "FEATURE-001")
            self.assertEqual(fallback.returncode, 0, fallback.stderr)

    def test_unapproved_feature_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-review-") as temp:
            root = Path(temp)
            self.make_project(root)
            for relative in ("feature_spec.md", "feature/FEATURE-001.md"):
                path = root / relative
                path.write_text(path.read_text(encoding="utf-8").replace("approved", "reviewing"), encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("FEATURE_NOT_APPROVED", result.stderr)

    def test_upsert_feature_requires_complete_unique_acceptance_criteria(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-ac-gate-") as temp:
            root = Path(temp)
            self.make_project(root)
            feature = root / "feature" / "FEATURE-001.md"
            text = feature.read_text(encoding="utf-8")
            start = text.index("| AC 编号 |")
            feature.write_text(text[:start], encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("FEATURE_AC_MISSING", result.stderr)

            text = text.replace(
                "| AC-2 | 失败可重试 | PAGE-MP-001 | API-MP-001 | 异常流测试 |",
                "| AC-1 |  | PAGE-MP-001 | API-MP-001 |  |",
            )
            feature.write_text(text, encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("DUPLICATE_AC_ID", result.stderr)
            self.assertIn("AC_DESCRIPTION_MISSING", result.stderr)
            self.assertIn("AC_VERIFICATION_MISSING", result.stderr)

    def test_iteration_page_binding_falls_back_to_root_ui_detail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-page-fallback-") as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "versions" / "v1.0.0" / "pages_prd" / "PAGE-MP-001.md").unlink()
            result = self.run_builder(root, "--mode", "plan")
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            mp = next(item for item in plan["items"] if item["sourceId"] == "FEATURE-001:MP")
            self.assertEqual(mp["pageApiBindings"][0]["interfaceRef"], "API-MP-001")

    def test_page_without_any_api_binding_table_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-page-table-") as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "versions" / "v1.0.0" / "pages_prd" / "PAGE-MP-001.md").unlink()
            page = root / "ui" / "PAGE-MP-001.md"
            text = page.read_text(encoding="utf-8")
            page.write_text(text[:text.index("| 接口编号 |")], encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("PAGE_API_BINDING_TABLE_MISSING", result.stderr)

    def test_page_api_outside_feature_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-page-api-outside-") as temp:
            root = Path(temp)
            self.make_project(root)
            page = root / "versions" / "v1.0.0" / "pages_prd" / "PAGE-MP-001.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace("API-MP-001", "API-MP-999"),
                encoding="utf-8",
            )
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("PAGE_API_OUTSIDE_FEATURE", result.stderr)

    def test_deprecated_feature_generates_close_plan(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-close-") as temp:
            root = Path(temp)
            self.make_project(root)
            previous = self.run_builder(root, "--mode", "plan", "--version", "v1.0.0")
            self.assertEqual(previous.returncode, 0, previous.stderr)
            previous_plan = json.loads(previous.stdout)
            for item in previous_plan["items"]:
                if item.get("workItemType") == "task":
                    item["acceptanceCriteria"] = []
            (root / "versions" / "v1.0.0" / "yunxiao-plan.json").write_text(
                json.dumps(previous_plan, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            v11 = root / "versions" / "v1.1.0"
            v11.mkdir()
            feature_index = root / "feature_spec.md"
            feature_index.write_text(
                feature_index.read_text(encoding="utf-8").replace(
                    "| active | approved |", "| deprecated | approved |"
                ),
                encoding="utf-8",
            )
            feature_detail = root / "feature" / "FEATURE-001.md"
            close_detail = (
                feature_detail.read_text(encoding="utf-8").replace(
                    "| 状态 | active |", "| 状态 | deprecated |"
                )
                .replace("- 关联页面：PAGE-MP-001, PAGE-AD-001", "- 关联页面：无")
                .replace("- 关联接口：API-MP-001", "- 关联接口：无")
            )
            feature_detail.write_text(close_detail[:close_detail.index("| AC 编号 |")], encoding="utf-8")
            feature_index.write_text(
                feature_index.read_text(encoding="utf-8").replace(
                    "| PAGE-MP-001, PAGE-AD-001 | API-MP-001 |",
                    "| 无 | 无 |",
                ),
                encoding="utf-8",
            )
            manifest = root / "ui_manifest.md"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace("| active |", "| deprecated |"),
                encoding="utf-8",
            )
            main = root / "main_spec.md"
            main.write_text(
                main.read_text(encoding="utf-8")
                .replace("| MP | Mini | 1 | 0 |", "| MP | Mini | 0 | 0 |")
                .replace("| AD | Admin | 1 | 0 |", "| AD | Admin | 0 | 0 |")
                .replace("| 有效 Feature 个数 | 1 |", "| 有效 Feature 个数 | 0 |"),
                encoding="utf-8",
            )
            scope = v11 / "delivery_scope.md"
            scope.write_text(
                (root / "versions" / "v1.0.0" / "delivery_scope.md").read_text(encoding="utf-8")
                .replace("v1.0.0", "v1.1.0")
                .replace("| 本期开发 |", "| 本期下线 |"),
                encoding="utf-8",
            )

            policy = root / "close-policy.json"
            policy.write_text(json.dumps({"includeTestTask": False}), encoding="utf-8")
            checked = self.run_builder(
                root, "--mode", "validate", "--version", "v1.1.0", "--policy", str(policy)
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            validation = json.loads(checked.stdout)
            self.assertEqual(validation["selectedFeatures"], ["FEATURE-001"])
            self.assertEqual(validation["featureOperations"], {"FEATURE-001": "close"})

            result = self.run_builder(
                root, "--mode", "plan", "--version", "v1.1.0", "--policy", str(policy)
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            by_id = {item["sourceId"]: item for item in plan["items"]}
            self.assertNotIn("operation", by_id["MODULE-001"])
            self.assertEqual(by_id["FEATURE-001"]["operation"], "close")
            self.assertEqual(
                sorted(source_id for source_id in by_id if source_id.startswith("FEATURE-001:")),
                ["FEATURE-001:BE", "FEATURE-001:MP", "FEATURE-001:TEST"],
            )
            for source_id in ("FEATURE-001:BE", "FEATURE-001:MP", "FEATURE-001:TEST"):
                task = by_id[source_id]
                self.assertEqual(task["operation"], "close")
                self.assertEqual(task["dependencyRefs"], [])
                self.assertEqual(task["pageApiBindings"], [])
                self.assertEqual(task["acceptanceCriteria"], [])
            self.assertEqual(by_id["FEATURE-001:MP"]["sourceRefs"], ["PAGE-MP-001"])
            plan_path = root / "yunxiao-close-plan.json"
            plan_path.write_text(result.stdout, encoding="utf-8")
            validated = self.run_plan_validator(plan_path)
            self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_close_without_previous_plan_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-close-snapshot-") as temp:
            root = Path(temp)
            self.make_project(root)
            for relative in ("feature_spec.md", "feature/FEATURE-001.md"):
                path = root / relative
                path.write_text(path.read_text(encoding="utf-8").replace("active", "deprecated"), encoding="utf-8")
            scope = root / "versions" / "v1.0.0" / "delivery_scope.md"
            scope.write_text(scope.read_text(encoding="utf-8").replace("本期开发", "本期下线"), encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate", "--version", "v1.0.0")
            self.assertEqual(result.returncode, 1)
            self.assertIn("PREVIOUS_PLAN_MISSING", result.stderr)

    def test_downline_scope_requires_deprecated_feature(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-close-gate-") as temp:
            root = Path(temp)
            self.make_project(root)
            scope = root / "versions" / "v1.0.0" / "delivery_scope.md"
            scope.write_text(
                scope.read_text(encoding="utf-8").replace("| 本期开发 |", "| 本期下线 |"),
                encoding="utf-8",
            )
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("SCOPE_FEATURE_LIFECYCLE_MISMATCH", result.stderr)
            self.assertIn("FEATURE_NOT_DEPRECATED", result.stderr)

    def test_open_scope_decision_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-decision-") as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "versions" / "v1.0.0" / "delivery_scope.md"
            text = path.read_text(encoding="utf-8").replace(
                "| 无 | closed | 无 | 无 |", "| DECISION-001 | open | 确认支付范围 | FEATURE-001 |"
            )
            path.write_text(text, encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("OPEN_SCOPE_DECISION", result.stderr)

    def test_undefined_module_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-module-") as temp:
            root = Path(temp)
            self.make_project(root)
            for relative in ("feature_spec.md", "feature/FEATURE-001.md"):
                path = root / relative
                path.write_text(path.read_text(encoding="utf-8").replace("MODULE-001", "MODULE-999"), encoding="utf-8")
            result = self.run_builder(root, "--mode", "validate")
            self.assertEqual(result.returncode, 1)
            self.assertIn("UNDEFINED_MODULE", result.stderr)

    def test_policy_cannot_reintroduce_fe_surface(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-policy-") as temp:
            root = Path(temp)
            self.make_project(root)
            policy = root / "policy.json"
            policy.write_text(json.dumps({
                "pageTerminalSurfaces": {
                    "MP": "FE",
                    "AD": "BE",
                },
                "surfaceOrder": ["BE", "FE", "TEST"],
            }), encoding="utf-8")
            result = self.run_builder(root, "--mode", "plan", "--policy", str(policy))
            self.assertEqual(result.returncode, 2)
            self.assertIn("unsupported page delivery surfaces: FE", result.stderr)

    def test_policy_cannot_assign_api_implementation_to_mp(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-api-owner-") as temp:
            root = Path(temp)
            self.make_project(root)
            policy = root / "policy.json"
            policy.write_text(json.dumps({
                "apiSurface": "MP",
            }), encoding="utf-8")
            result = self.run_builder(root, "--mode", "plan", "--policy", str(policy))
            self.assertEqual(result.returncode, 2)
            self.assertIn("apiSurface must be BE", result.stderr)

    def test_legacy_ac_without_page_refs_is_inferred_from_page_binding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-legacy-ac-") as temp:
            root = Path(temp)
            self.make_project(root)
            feature = root / "feature" / "FEATURE-001.md"
            text = feature.read_text(encoding="utf-8")
            text = text.replace(
                "| AC 编号 | 验收描述（可验证） | 关联页面 | 关联接口 | 验证方式 |\n"
                "|---|---|---|---|---|\n"
                "| AC-1 | 可以浏览 | PAGE-MP-001 | API-MP-001 | UI + API |\n"
                "| AC-2 | 失败可重试 | PAGE-MP-001 | API-MP-001 | 异常流测试 |",
                "| AC 编号 | 验收描述（可验证） | 关联接口 | 验证方式 |\n"
                "|---|---|---|---|\n"
                "| AC-1 | 可以浏览 | API-MP-001 | UI + API |\n"
                "| AC-2 | 失败可重试 | API-MP-001 | 异常流测试 |",
            )
            feature.write_text(text, encoding="utf-8")
            result = self.run_builder(root, "--mode", "plan")
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            mp_item = next(item for item in plan["items"] if item["sourceId"] == "FEATURE-001:MP")
            self.assertEqual([item["id"] for item in mp_item["acceptanceCriteria"]], ["AC-1", "AC-2"])
            self.assertEqual(mp_item["acceptanceCriteria"][0]["pageRefs"], [])

    def test_plan_validator_rejects_instance_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-plan-") as temp:
            path = Path(temp) / "plan.json"
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "adapter": "lny-prd-yunxiao",
                "items": [{
                    "sourceId": "MODULE-001",
                    "parentSourceId": None,
                    "workItemType": "product",
                    "title": "商品",
                    "yunxiaoId": "123",
                }],
            }), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("FORBIDDEN_INSTANCE_FIELDS", result.stderr)

    def test_plan_validator_rejects_invalid_or_product_close_operation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-plan-operation-") as temp:
            path = Path(temp) / "plan.json"
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "adapter": "lny-prd-yunxiao",
                "sourceVersion": "v1.0.0",
                "project": "Fixture",
                "items": [{
                    "sourceId": "MODULE-001",
                    "parentSourceId": None,
                    "workItemType": "product",
                    "title": "商品",
                    "operation": "close",
                }],
            }), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("PRODUCT_CLOSE_UNSUPPORTED", result.stderr)

            plan = json.loads(path.read_text(encoding="utf-8"))
            plan["items"][0]["operation"] = "delete"
            path.write_text(json.dumps(plan), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("OPERATION", result.stderr)

    def test_plan_validator_rejects_close_task_delivery_content(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-close-content-") as temp:
            path = Path(temp) / "plan.json"
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "adapter": "lny-prd-yunxiao",
                "sourceVersion": "v1.1.0",
                "project": "Fixture",
                "items": [
                    {"sourceId": "MODULE-001", "parentSourceId": None, "workItemType": "product", "title": "商品"},
                    {
                        "sourceId": "FEATURE-001", "parentSourceId": "MODULE-001",
                        "workItemType": "business", "title": "浏览商品", "operation": "close",
                    },
                    {
                        "sourceId": "FEATURE-001:MP", "parentSourceId": "FEATURE-001",
                        "workItemType": "task", "title": "[MP] 浏览商品", "operation": "close",
                        "deliverySurface": "MP", "sourceRefs": ["PAGE-MP-001"],
                        "dependencyRefs": ["API-MP-001"],
                        "pageApiBindings": [{
                            "pageRef": "PAGE-MP-001", "interfaceRef": "API-MP-001",
                            "purpose": "查询商品", "trigger": "页面初始化",
                        }],
                        "acceptanceCriteria": [{
                            "id": "AC-1", "description": "可浏览", "verification": "UI 检查",
                            "pageRefs": ["PAGE-MP-001"], "apiRefs": ["API-MP-001"], "extRefs": [],
                        }],
                    },
                ],
            }), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("CLOSE_TASK_CONTENT", result.stderr)

    def test_plan_validator_rejects_invalid_dependencies_and_page_bindings(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-invalid-relations-") as temp:
            path = Path(temp) / "plan.json"
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "adapter": "lny-prd-yunxiao",
                "sourceVersion": "v1.0.0",
                "project": "Fixture",
                "items": [
                    {
                        "sourceId": "MODULE-001",
                        "parentSourceId": None,
                        "workItemType": "product",
                        "title": "商品",
                    },
                    {
                        "sourceId": "FEATURE-001",
                        "parentSourceId": "MODULE-001",
                        "workItemType": "business",
                        "title": "浏览商品",
                    },
                    {
                        "sourceId": "FEATURE-001:MP",
                        "parentSourceId": "FEATURE-001",
                        "workItemType": "task",
                        "title": "[MP] 浏览商品",
                        "deliverySurface": "MP",
                        "sourceRefs": ["PAGE-MP-001"],
                        "dependencyRefs": ["PAGE-MP-001"],
                        "pageApiBindings": [{
                            "pageRef": "API-MP-001",
                            "interfaceRef": "PAGE-MP-001",
                            "purpose": "查询商品",
                            "trigger": "页面初始化",
                        }],
                        "acceptanceCriteria": [],
                    },
                ],
            }), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("DEPENDENCY_REFS", result.stderr)
            self.assertIn("PAGE_API_BINDING_PAGE", result.stderr)
            self.assertIn("PAGE_API_BINDING_INTERFACE", result.stderr)

    def test_plan_validator_rejects_unowned_page_api_bindings_and_self_dependencies(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-yunxiao-binding-owner-") as temp:
            path = Path(temp) / "plan.json"
            path.write_text(json.dumps({
                "schemaVersion": 1,
                "adapter": "lny-prd-yunxiao",
                "sourceVersion": "v1.0.0",
                "project": "Fixture",
                "items": [
                    {
                        "sourceId": "MODULE-001",
                        "parentSourceId": None,
                        "workItemType": "product",
                        "title": "商品",
                    },
                    {
                        "sourceId": "FEATURE-001",
                        "parentSourceId": "MODULE-001",
                        "workItemType": "business",
                        "title": "浏览商品",
                    },
                    {
                        "sourceId": "FEATURE-001:BE",
                        "parentSourceId": "FEATURE-001",
                        "workItemType": "task",
                        "title": "[BE] 浏览商品",
                        "deliverySurface": "BE",
                        "sourceRefs": ["API-AD-001", "PAGE-AD-001"],
                        "dependencyRefs": ["API-AD-001"],
                        "pageApiBindings": [{
                            "pageRef": "PAGE-AD-999",
                            "interfaceRef": "API-AD-999",
                            "purpose": "查询商品",
                            "trigger": "页面初始化",
                        }],
                        "acceptanceCriteria": [],
                    },
                ],
            }), encoding="utf-8")
            result = self.run_plan_validator(path)
            self.assertEqual(result.returncode, 1)
            self.assertIn("DEPENDENCY_OWNERSHIP_OVERLAP", result.stderr)
            self.assertIn("PAGE_API_BINDING_PAGE_OWNERSHIP", result.stderr)
            self.assertIn("PAGE_API_BINDING_INTERFACE_OWNERSHIP", result.stderr)


if __name__ == "__main__":
    unittest.main()
