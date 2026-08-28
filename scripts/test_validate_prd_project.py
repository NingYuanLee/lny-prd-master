from __future__ import annotations

import importlib.util
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
| 终端类型编码 | 终端名称 | 有效页面总数 | 有效局部自定义UI组件数 |
|---|---|---:|---:|
| MP | Mini | 1 | 1 |

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
| 功能编号 | 状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |
|---|---|---:|---|---|---|
| FEATURE-001 | active | 2 | PAGE-MP-001 | API-MP-001 | feature/FEATURE-001.md |
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
| 状态 | active |
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
            main = (root / "main_spec.md").read_text(encoding="utf-8")
            (root / "main_spec.md").write_text(
                main.replace("| MP | Mini | 1 | 1 |", "| MP | Mini | 9 | 1 |"),
                encoding="utf-8",
            )
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
                {"PAGE_COUNT_DRIFT", "FEATURE_API_DRIFT", "UNDEFINED_API_REF", "SP_FEATURE_INPUT_DRIFT"}
                <= codes
            )

    def test_detects_detail_identity_and_feature_status_drift(self) -> None:
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
            feature_path = root / "feature" / "FEATURE-001.md"
            feature_path.write_text(
                feature_path.read_text(encoding="utf-8").replace(
                    "| 状态 | active |", "| 状态 | deprecated |"
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertTrue(
                {"PAGE_DETAIL_ID", "COMP_DETAIL_ID", "API_DETAIL_ID", "FEATURE_STATUS_DRIFT"}
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
            index_path = root / "feature_spec.md"
            index_path.write_text(
                index_path.read_text(encoding="utf-8").replace(
                    "| FEATURE-001 | active |", "| FEATURE-001 | enabled |"
                ),
                encoding="utf-8",
            )
            detail_path = root / "feature" / "FEATURE-001.md"
            detail_path.write_text(
                detail_path.read_text(encoding="utf-8").replace(
                    "| 状态 | active |", "| 状态 | enabled |"
                ),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("INVALID_FEATURE_STATUS", codes)

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
            main_path.write_text(
                main_path.read_text(encoding="utf-8")
                + """
| 模块编号 | 模块名称 | 说明 |
|---|---|---|
| MODULE-001 | 商品 | 商品能力 |
""",
                encoding="utf-8",
            )
            index_path = root / "feature_spec.md"
            index_path.write_text(
                index_path.read_text(encoding="utf-8")
                .replace(
                    "| 功能编号 | 状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |",
                    "| 功能编号 | 模块编号 | 所属模块 | 状态 | 评审状态 | 分支数 | 关联页面 | 关联接口 | 明细路径 |",
                )
                .replace(
                    "|---|---|---:|---|---|---|",
                    "|---|---|---|---|---|---:|---|---|---|",
                )
                .replace(
                    "| FEATURE-001 | active | 2 | PAGE-MP-001 | API-MP-001 | feature/FEATURE-001.md |",
                    "| FEATURE-001 | MODULE-001 | 商品 | active | approved | 2 | PAGE-MP-001 | API-MP-001 | feature/FEATURE-001.md |",
                ),
                encoding="utf-8",
            )
            detail_path = root / "feature" / "FEATURE-001.md"
            detail_path.write_text(
                detail_path.read_text(encoding="utf-8").replace(
                    "| 状态 | active |",
                    "| 模块编号 | MODULE-001 |\n| 所属模块 | 商品 |\n| 状态 | active |\n| 评审状态 | approved |",
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
                approved_scope.replace("| 本期开发 |", "| 本期下线 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertIn("SCOPE_FEATURE_LIFECYCLE_MISMATCH", codes)
            scope_path.write_text(approved_scope, encoding="utf-8")

            active_index = index_path.read_text(encoding="utf-8")
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
            index_path.write_text(active_index.replace("| active | approved |", "| deprecated | approved |"), encoding="utf-8")
            detail_path.write_text(active_detail.replace("| 状态 | active |", "| 状态 | deprecated |"), encoding="utf-8")
            (root / "ui_manifest.md").write_text(
                active_manifest.replace("| PAGE-MP-001 | active |", "| PAGE-MP-001 | deprecated |"),
                encoding="utf-8",
            )
            main_path.write_text(
                active_main
                .replace("| MP | Mini | 1 | 1 |", "| MP | Mini | 0 | 1 |")
                .replace("| 有效 Feature 个数 | 1 |", "| 有效 Feature 个数 | 0 |"),
                encoding="utf-8",
            )
            codes = {issue.code for issue in self.validator.validate_project(root)}
            self.assertNotIn("SCOPE_FEATURE_LIFECYCLE_MISMATCH", codes)

            index_path.write_text(active_index, encoding="utf-8")
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
            self.assertIn("FEATURE_MODULE_ID_DRIFT", codes)


if __name__ == "__main__":
    unittest.main()
