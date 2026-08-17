#!/usr/bin/env python3
"""Integration tests for the multi-host LNY-PRD installer."""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = ROOT / "scripts" / "install-skills.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("lny_prd_installer", INSTALLER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {INSTALLER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


installer = load_installer()


def options(**values) -> argparse.Namespace:
    defaults = {
        "dest": None,
        "dry_run": False,
        "force": False,
        "allow_downgrade": False,
    }
    defaults.update(values)
    return argparse.Namespace(**defaults)


@contextlib.contextmanager
def quiet_output():
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        yield


class InstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = installer.load_bundle()

    def test_host_names_and_official_user_paths(self) -> None:
        self.assertEqual(installer.normalize_host("codex").host_id, "chatgpt")
        self.assertEqual(installer.normalize_host("trae").host_id, "traework-cn")
        self.assertEqual(
            installer.resolve_target("chatgpt").skills_root,
            Path.home() / ".agents" / "skills",
        )
        self.assertEqual(
            installer.resolve_target("traework-cn").skills_root,
            Path.home() / ".trae-cn" / "skills",
        )

    def test_cursor_install_drift_update_and_uninstall(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-installer-cursor-") as temp:
            destination = Path(temp) / "cursor" / "skills"
            target = installer.resolve_target("cursor", str(destination))
            args = options(dest=str(destination))
            with quiet_output():
                self.assertEqual(installer.command_install(args, self.bundle, target), 0)
            self.assertTrue(target.state_file.is_file())
            for skill in self.bundle.skills:
                self.assertTrue((destination / skill / "SKILL.md").is_file())
            self.assertFalse((destination / "examples").exists())

            edited = destination / "lny-prd-master" / "SKILL.md"
            edited.write_text(edited.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
            with self.assertRaises(installer.InstallError):
                with quiet_output():
                    installer.command_update(args, self.bundle, target)

            force_args = options(dest=str(destination), force=True)
            with quiet_output():
                self.assertEqual(installer.command_update(force_args, self.bundle, target), 0)
                self.assertEqual(installer.command_status(args, self.bundle, target), 0)
                self.assertEqual(installer.command_uninstall(args, self.bundle, target), 0)
            for skill in self.bundle.skills:
                self.assertFalse((destination / skill).exists())
            backups = [path for path in target.backups_root.iterdir() if path.is_dir()]
            self.assertEqual(len(backups), 1)
            self.assertTrue((backups[0] / "lny-prd-master" / "SKILL.md").is_file())

    def test_traework_config_merge_and_remove_preserves_other_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-installer-trae-") as temp:
            root = Path(temp) / ".trae-cn"
            destination = root / "skills"
            root.mkdir()
            config_path = root / "skill-config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "managedSkills": {"Other Skill": "user_upload"},
                        "disabledSkills": ["disabled-skill"],
                        "futureField": {"preserve": True},
                    }
                ),
                encoding="utf-8",
            )
            target = installer.resolve_target("traework-cn", str(destination))
            args = options(dest=str(destination))
            with quiet_output():
                installer.command_install(args, self.bundle, target)
            installed = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(installed["managedSkills"]["Other Skill"], "user_upload")
            self.assertEqual(installed["disabledSkills"], ["disabled-skill"])
            self.assertEqual(installed["futureField"], {"preserve": True})
            for name in self.bundle.frontmatter_names.values():
                self.assertEqual(installed["managedSkills"][name], "user_upload")

            with quiet_output():
                installer.command_uninstall(args, self.bundle, target)
            removed = json.loads(config_path.read_text(encoding="utf-8"))
            self.assertEqual(removed["managedSkills"], {"Other Skill": "user_upload"})
            self.assertEqual(removed["futureField"], {"preserve": True})

    def test_failed_install_restores_unmanaged_directories(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-installer-rollback-") as temp:
            destination = Path(temp) / "cursor" / "skills"
            destination.mkdir(parents=True)
            for skill in self.bundle.skills:
                skill_dir = destination / skill
                skill_dir.mkdir()
                (skill_dir / "original.txt").write_text(skill, encoding="utf-8")
            target = installer.resolve_target("cursor", str(destination))
            args = options(dest=str(destination), force=True)
            original_write = installer.write_json_atomic

            def fail_state_write(path: Path, value: object) -> None:
                if path == target.state_file:
                    raise OSError("simulated state write failure")
                original_write(path, value)

            with mock.patch.object(installer, "write_json_atomic", side_effect=fail_state_write):
                with self.assertRaises(installer.InstallError):
                    with quiet_output():
                        installer.command_install(args, self.bundle, target)
            self.assertFalse(target.state_file.exists())
            for skill in self.bundle.skills:
                marker = destination / skill / "original.txt"
                self.assertEqual(marker.read_text(encoding="utf-8"), skill)

    def test_dry_run_and_collision_do_not_write(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-installer-dry-") as temp:
            destination = Path(temp) / "skills"
            target = installer.resolve_target("cursor", str(destination))
            with quiet_output():
                installer.command_install(
                    options(dest=str(destination), dry_run=True), self.bundle, target
                )
            self.assertFalse(destination.exists())

            collision = destination / "lny-prd-master"
            collision.mkdir(parents=True)
            with self.assertRaises(installer.InstallError):
                with quiet_output():
                    installer.command_install(options(dest=str(destination)), self.bundle, target)
            self.assertFalse(target.state_file.exists())

    def test_examples_export_is_separate_from_skills(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lny-prd-installer-examples-") as temp:
            destination = Path(temp) / "human-examples"
            with quiet_output():
                installer.command_export_examples(
                    options(dest=str(destination)), self.bundle
                )
            self.assertTrue((destination / "mini-shop" / "main_spec.md").is_file())
            self.assertFalse(any(destination.glob("lny-prd-*")))


if __name__ == "__main__":
    unittest.main()
