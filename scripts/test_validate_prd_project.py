from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "lny-prd-check" / "scripts" / "validate-prd-project.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("prd_validator", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProjectSemanticValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def make_project(self, root: Path) -> None:
        (root / "ui").mkdir()
        (root / "api").mkdir()
        (root / "feature").mkdir()
        (root / "versions" / "v1.0.0" / "pages_prd").mkdir(parents=True)
        (root / "main_spec.md").write_text(
            """# Product
| 故事编号 | 故事类型 | 角色 / 利益相关方 | 画像 / 背景 | 需求故事 |
|---|---|---|---|---|
| STORY-001 | 用户价值 | 买家 | 浏览商品的消费者 | 作为买家，我需要浏览商品，以便选择商品 |
""",
            encoding="utf-8",
        )
        (root / "ui_manifest.md").write_text(
            """# UI
| 页面编号 | 状态 | 明细路径 |
|---|---|---|
| PAGE-MP-001 | active | ui/PAGE-MP-001.md |

| 组件编号 | 适用终端 | 明细路径 |
|---|---|---|
| COMP-001 | MP | ui/COMP-001.md |
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
### MODULE-001 商品
| 属性 | 内容 |
|---|---|
| 模块编号 | MODULE-001 |
| 模块名称 | 商品 |
| 领域职责 | 管理商品浏览能力 |
| 核心业务对象 | 商品 |
| 范围内 | 商品查询 |
| 范围外 | 订单交易 |
| 对外提供能力 | 商品信息查询 |
| 依赖模块 | 无 |
| 跨模块交互 | 无 |

| 功能编号 | 功能名称 | 明细路径 |
|---|---|---|
| FEATURE-001 | Browse | feature/FEATURE-001.md |
""",
            encoding="utf-8",
        )
        (root / "ui" / "PAGE-MP-001.md").write_text(
            """# PAGE-MP-001
| 属性 | 内容 |
|---|---|
| 页面编号 | PAGE-MP-001 |
API-MP-001 COMP-001
""",
            encoding="utf-8",
        )
        (root / "ui" / "COMP-001.md").write_text(
            """# COMP-001
| 属性 | 内容 |
|---|---|
| 组件编号 | COMP-001 |
PAGE-MP-001
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
        (root / "feature" / "FEATURE-001.md").write_text(
            """# FEATURE-001
| 属性 | 内容 |
|---|---|
| 功能编号 | FEATURE-001 |
| 模块编号 | MODULE-001 |
| 关联 STORY | STORY-001（主） |
| 状态 | active |
| 评审状态 | pending |
| 分支数 | 2 |
- 关联页面：PAGE-MP-001
- 关联接口：API-MP-001
| AC 编号 | 验收描述（可验证） | 关联页面 | 关联接口 | 验证方式 |
|---|---|---|---|---|
| AC-1 | Works | PAGE-MP-001 | API-MP-001 | UI + API 联调 |
| AC-2 | Retries | PAGE-MP-001 | API-MP-001 | 异常流测试 |
""",
            encoding="utf-8",
        )
        (root / "versions" / "v1.0.0" / "pages_prd" / "PAGE-MP-001.md").write_text(
            """# PAGE-MP-001
## 6. Feature 关联清单
| Feature编号 | Feature名称 | 关联AC | 本页关联点 | 来源路径 |
|---|---|---|---|---|
| FEATURE-001 | Browse | AC-1, AC-2 | Browse | feature/FEATURE-001.md |
""",
            encoding="utf-8",
        )
        (root / "versions" / "v1.0.0" / "sp_report.md").write_text(
            """# SP
| FEATURE编号 | 分支数 | AC条数（只审计） |
|---|---:|---:|
| FEATURE-001 | 2 | 2 |
""",
            encoding="utf-8",
        )

    def test_valid_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-ok-") as temp:
            root = Path(temp)
            self.make_project(root)
            self.assertEqual(self.validator.validate_project(root), [])

    def test_detail_paths_accept_both_directory_separators(self) -> None:
        root = Path("project")
        fallback = root / "fallback.md"
        for value in ("ui/PAGE-MP-001.md", r"ui\PAGE-MP-001.md"):
            with self.subTest(value=value):
                self.assertEqual(
                    self.validator.detail_path(
                        root,
                        {"明细路径": value},
                        "明细路径",
                        fallback,
                    ),
                    root / "ui" / "PAGE-MP-001.md",
                )

    def test_detects_count_reference_and_sp_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-bad-") as temp:
            root = Path(temp)
            self.make_project(root)
            feature = (root / "feature" / "FEATURE-001.md").read_text(encoding="utf-8")
            (root / "feature" / "FEATURE-001.md").write_text(
                feature.replace("- 关联接口：API-MP-001", "- 关联接口：API-MP-999"),
                encoding="utf-8",
            )
            report = (root / "versions" / "v1.0.0" / "sp_report.md").read_text(encoding="utf-8")
            (root / "versions" / "v1.0.0" / "sp_report.md").write_text(
                report.replace("| FEATURE-001 | 2 | 2 |", "| FEATURE-001 | 1 | 1 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertTrue(
                {"UNDEFINED_API_REF", "SP_FEATURE_INPUT_DRIFT"}
                <= codes
            )

    def test_detects_detail_identity_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-identity-") as temp:
            root = Path(temp)
            self.make_project(root)
            replacements = (
                (root / "ui" / "PAGE-MP-001.md", "PAGE-MP-001", "PAGE-MP-002"),
                (root / "ui" / "COMP-001.md", "COMP-001", "COMP-002"),
                (root / "api" / "API-MP-001.md", "API-MP-001", "API-MP-002"),
            )
            for path, source, target in replacements:
                path.write_text(
                    path.read_text(encoding="utf-8").replace(source, target),
                    encoding="utf-8",
                )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertTrue(
                {"PAGE_DETAIL_ID", "COMP_DETAIL_ID", "API_DETAIL_ID"}
                <= codes
            )

    def test_reports_invalid_detail_utf8_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-utf8-") as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "ui" / "COMP-001.md").write_bytes(b"COMP-001\xff")
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INVALID_UTF8", codes)

    def test_rejects_invalid_feature_status(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-status-") as temp:
            root = Path(temp)
            self.make_project(root)
            detail_path = root / "feature" / "FEATURE-001.md"
            detail_path.write_text(
                detail_path.read_text(encoding="utf-8").replace(
                    "| 状态 | active |", "| 状态 | enabled |"
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INVALID_FEATURE_STATUS", codes)

    def test_legacy_feature_index_mirrors_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-legacy-index-") as temp:
            root = Path(temp)
            self.make_project(root)
            (root / "feature_spec.md").write_text(
                """# Features
| 属性 | 内容 |
|---|---|
| 模块编号 | MODULE-001 |
| 模块名称 | 商品 |
| 领域职责 | 管理商品浏览能力 |
| 核心业务对象 | 商品 |
| 范围内 | 商品查询 |
| 范围外 | 订单交易 |
| 对外提供能力 | 商品信息查询 |
| 依赖模块 | 无 |
| 跨模块交互 | 无 |

| 功能编号 | 功能名称 | 模块编号 | 所属模块 | 优先级 | 状态 | 评审状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |
|---|---|---|---|---|---|---|---:|---|---|---|
| FEATURE-001 | Stale | MODULE-999 | Stale | P2 | deprecated | blocked | 99 | PAGE-MP-999 | API-MP-999 | feature/FEATURE-001.md |
""",
                encoding="utf-8",
            )
            self.assertEqual(self.validator.validate_project(root), [])

    def test_rejects_delivery_roles_in_ac_verification(self) -> None:
        for leaked_role in ("MP", "FE", "BE", "AD", "PC", "APP", "H5", "TEST"):
            with self.subTest(leaked_role=leaked_role), tempfile.TemporaryDirectory(
                prefix="lny-prd-semantic-ac-role-"
            ) as temp:
                root = Path(temp)
                self.make_project(root)
                detail_path = root / "feature" / "FEATURE-001.md"
                detail_path.write_text(
                    detail_path.read_text(encoding="utf-8").replace(
                        "UI + API 联调", f"{leaked_role} + API 联调"
                    ),
                    encoding="utf-8",
                )
                codes = {issue.code for issue in self.validator.validate_project(root)}
                self.assertIn("AC_VERIFICATION_ROLE_LEAK", codes)

    def test_rejects_missing_duplicate_or_incomplete_active_feature_ac(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-ac-shape-") as temp:
            root = Path(temp)
            self.make_project(root)
            detail = root / "feature" / "FEATURE-001.md"
            original = detail.read_text(encoding="utf-8")
            start = original.index("| AC 编号 |")
            detail.write_text(original[:start], encoding="utf-8")
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("FEATURE_AC_MISSING", codes)

            detail.write_text(
                original.replace(
                    "| AC-2 | Retries | PAGE-MP-001 | API-MP-001 | 异常流测试 |",
                    "| AC-1 |  | PAGE-MP-001 | API-MP-001 |  |",
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertTrue({"DUPLICATE_AC_ID", "AC_DESCRIPTION_MISSING", "AC_VERIFICATION_MISSING"} <= codes)

    def test_detects_feature_page_acceptance_criterion_drift(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-page-ac-") as temp:
            root = Path(temp)
            self.make_project(root)
            page = root / "versions" / "v1.0.0" / "pages_prd" / "PAGE-MP-001.md"
            page.write_text(page.read_text(encoding="utf-8").replace("AC-1, AC-2", "AC-1, AC-9"), encoding="utf-8")
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("PAGE_AC_UNKNOWN_AC", codes)
            self.assertIn("PAGE_AC_DRIFT", codes)

    def test_fixture_status_is_reserved(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-fixture-") as temp:
            root = Path(temp)
            self.make_project(root)
            manifest = (root / "ui_manifest.md").read_text(encoding="utf-8")
            (root / "ui_manifest.md").write_text(
                manifest.replace("| PAGE-MP-001 | active |", "| PAGE-MP-001 | fixture |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INVALID_PAGE_STATUS", codes)

    def test_delivery_contract_validates_module_review_and_scope(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-delivery-") as temp:
            root = Path(temp)
            self.make_project(root)
            main_path = root / "main_spec.md"
            detail_path = root / "feature" / "FEATURE-001.md"
            detail_path.write_text(
                detail_path.read_text(encoding="utf-8").replace(
                    "| 状态 | active |",
                    "| 状态 | active |\n| 评审状态 | approved |",
                ),
                encoding="utf-8",
            )
            scope_path = root / "versions" / "v1.0.0" / "delivery_scope.md"
            scope_path.write_text(
                """# Scope
| 属性 | 内容 |
|---|---|
| 版本号 | v1.0.0 |
| 评审状态 | approved |
| 产品确认项 | 0 |

| Feature | 纳入方式 | 评审状态 | 阻塞决策 |
|---|---|---|---:|
| FEATURE-001 | 本期开发 | approved | 0 |

| 决策编号 | 状态 | 问题 | 影响对象 |
|---|---|---|---|
| 无 | closed | 无 | 无 |
""",
                encoding="utf-8",
            )
            self.assertEqual(self.validator.validate_project(root), [])

            approved_scope = scope_path.read_text(encoding="utf-8")
            scope_path.write_text(
                approved_scope.replace("| 评审状态 | approved |", "| 评审结论 | 待定 |\n| 评审状态 | approved |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INVALID_SCOPE_REVIEW_CONCLUSION", codes)
            scope_path.write_text(approved_scope, encoding="utf-8")

            scope_path.write_text(
                approved_scope.replace("| 本期开发 |", "| 本期下线 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("SCOPE_FEATURE_LIFECYCLE_MISMATCH", codes)
            scope_path.write_text(approved_scope, encoding="utf-8")

            active_detail = detail_path.read_text(encoding="utf-8")
            active_manifest = (root / "ui_manifest.md").read_text(encoding="utf-8")
            active_main = main_path.read_text(encoding="utf-8")
            v11 = root / "versions" / "v1.1.0"
            v11.mkdir()
            (v11 / "delivery_scope.md").write_text(
                approved_scope
                .replace("v1.0.0", "v1.1.0")
                .replace("| 本期开发 |", "| 本期下线 |"),
                encoding="utf-8",
            )
            detail_path.write_text(active_detail.replace("| 状态 | active |", "| 状态 | deprecated |"), encoding="utf-8")
            (root / "ui_manifest.md").write_text(
                active_manifest.replace("| PAGE-MP-001 | active |", "| PAGE-MP-001 | deprecated |"),
                encoding="utf-8",
            )
            main_path.write_text(active_main, encoding="utf-8")
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertNotIn("SCOPE_FEATURE_LIFECYCLE_MISMATCH", codes)

            detail_path.write_text(active_detail, encoding="utf-8")
            (root / "ui_manifest.md").write_text(active_manifest, encoding="utf-8")
            main_path.write_text(active_main, encoding="utf-8")
            (v11 / "delivery_scope.md").unlink()
            v11.rmdir()

            detail_path.write_text(
                detail_path.read_text(encoding="utf-8").replace("MODULE-001", "MODULE-999"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("UNDEFINED_MODULE_REF", codes)

    def test_story_feature_mapping_is_owned_by_feature_detail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-story-") as temp:
            root = Path(temp)
            self.make_project(root)
            detail_path = root / "feature" / "FEATURE-001.md"
            original = detail_path.read_text(encoding="utf-8")
            detail_path.write_text(
                original.replace("| 关联 STORY | STORY-001（主） |", "| 关联 STORY | 无 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("FEATURE_STORY_MISSING", codes)
            self.assertIn("STORY_WITHOUT_FEATURE", codes)

            detail_path.write_text(
                original.replace("STORY-001（主）", "STORY-999（主）"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("UNDEFINED_STORY_REF", codes)

    def test_module_boundary_is_owned_by_feature_spec(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-module-") as temp:
            root = Path(temp)
            self.make_project(root)
            feature_spec = root / "feature_spec.md"
            original = feature_spec.read_text(encoding="utf-8")
            feature_spec.write_text(
                original.replace("| 领域职责 | 管理商品浏览能力 |\n", ""),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INCOMPLETE_MODULE_BOUNDARY", codes)

            feature_spec.write_text(
                original.replace("| 依赖模块 | 无 |", "| 依赖模块 | MODULE-999 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("UNDEFINED_MODULE_DEPENDENCY", codes)

    def test_module_granularity_objective_guards(self) -> None:
        module_two = """
### MODULE-002 订单
| 属性 | 内容 |
|---|---|
| 模块编号 | MODULE-002 |
| 模块名称 | 订单 |
| 领域职责 | 管理订单生命周期 |
| 核心业务对象 | 订单 |
| 范围内 | 订单处理 |
| 范围外 | 商品维护 |
| 对外提供能力 | 订单状态查询 |
| 依赖模块 | 无 |
| 跨模块交互 | 读取商品快照 |

"""
        with tempfile.TemporaryDirectory(prefix="lny-prd-semantic-module-granularity-") as temp:
            root = Path(temp)
            self.make_project(root)
            feature_spec = root / "feature_spec.md"
            original = feature_spec.read_text(encoding="utf-8")

            feature_spec.write_text(
                original.replace("| 对外提供能力 | 商品信息查询 |", "| 对外提供能力 | 通过 API-MP-001 查询商品 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("MODULE_DETAIL_LEAK", codes)

            feature_spec.write_text(
                original.replace("| 功能编号 | 功能名称 | 明细路径 |", module_two + "| 功能编号 | 功能名称 | 明细路径 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("MODULE_WITHOUT_FEATURE", codes)

            cyclic_module_two = module_two.replace("| 依赖模块 | 无 |", "| 依赖模块 | MODULE-001 |")
            feature_spec.write_text(
                original.replace("| 依赖模块 | 无 |", "| 依赖模块 | MODULE-002 |", 1).replace(
                    "| 功能编号 | 功能名称 | 明细路径 |",
                    cyclic_module_two + "| 功能编号 | 功能名称 | 明细路径 |",
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("CYCLIC_MODULE_DEPENDENCY", codes)


    def test_suggested_routes_returns_distinct_sorted_skills(self) -> None:
        issue = self.validator.Issue
        issues = [
            issue("FEATURE_AC_MISSING", Path("a.md"), "x"),
            issue("UNDEFINED_PAGE_REF", Path("b.md"), "y"),
            issue("INVALID_FEATURE_STATUS", Path("c.md"), "z"),
            issue("UNKNOWN_CODE", Path("d.md"), "w"),
        ]
        self.assertEqual(self.validator.suggested_routes(issues), ["feature", "page"])

    def test_next_step_route_mapping_is_complete(self) -> None:
        source = Path(self.validator.__file__).read_text(encoding="utf-8")
        inline = set(re.findall(r"add\(\s*issues,\s*\"([A-Z][A-Z0-9_]+)\"", source))
        multiline = set(re.findall(r"^\s*\"([A-Z][A-Z0-9_]+)\"," r"""\s*$""", source, flags=re.M))
        variable = set(re.findall(r"(?:missing|identity)_code=\"([A-Z][A-Z0-9_]+)\"", source))
        labels = re.findall(r"[A-Z]+_RE,\s*\"([A-Z]+)\"", source)
        fstring = {f"UNDEFINED_{label}_REF" for label in labels}
        codes = inline | multiline | variable | fstring
        mapped = set(self.validator.NEXT_ROUTE)
        self.assertFalse(codes - mapped, f"unmapped issue codes: {sorted(codes - mapped)}")


if __name__ == "__main__":
    unittest.main()
