#!/usr/bin/env python3
"""Install the LNY-PRD skill bundle into supported user-level hosts."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "skill-bundle.json"
EXPECTED_SKILLS = {
    "lny-prd-api",
    "lny-prd-check",
    "lny-prd-feature",
    "lny-prd-iter",
    "lny-prd-master",
    "lny-prd-page",
    "lny-prd-prototype",
    "lny-prd-review",
    "lny-prd-sp",
    "lny-prd-ui",
    "lny-prd-yunxiao",
}
IGNORED_NAMES = {".DS_Store", ".git", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
FRONTMATTER_NAME_RE = re.compile(r"^name:\s*([^\r\n]+)\s*$", re.MULTILINE)


class InstallError(RuntimeError):
    """A user-actionable installation failure."""


@dataclass(frozen=True)
class HostSpec:
    host_id: str
    display_name: str
    config_dir: str
    aliases: tuple[str, ...] = ()
    trae_config: bool = False


HOSTS = {
    "cursor": HostSpec("cursor", "Cursor", ".cursor"),
    "chatgpt": HostSpec("chatgpt", "ChatGPT", ".agents", ("codex",)),
    "traework-cn": HostSpec(
        "traework-cn",
        "TraeWork CN",
        ".trae-cn",
        ("trae-work", "trae", "trae-cn"),
        True,
    ),
}
HOST_ALIASES = {
    alias: spec.host_id
    for spec in HOSTS.values()
    for alias in (spec.host_id, *spec.aliases)
}


@dataclass(frozen=True)
class Bundle:
    bundle_id: str
    version: str
    skills: tuple[str, ...]
    examples: Path
    digests: dict[str, str]
    frontmatter_names: dict[str, str]


@dataclass(frozen=True)
class Target:
    host: HostSpec
    config_root: Path
    skills_root: Path
    state_root: Path
    state_file: Path
    lock_file: Path
    backups_root: Path
    trae_config_file: Path | None


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InstallError(f"missing JSON file: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallError(f"cannot read JSON file {path}: {exc}") from exc


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def ignored(relative: Path) -> bool:
    return (
        any(part in IGNORED_NAMES for part in relative.parts)
        or relative.suffix.lower() in IGNORED_SUFFIXES
    )


def bundle_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ignored(relative):
            continue
        if path.is_symlink():
            raise InstallError(f"symlinks are not allowed in the source bundle: {path}")
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def directory_digest(root: Path) -> str:
    if not root.is_dir():
        raise InstallError(f"skill directory missing: {root}")
    digest = hashlib.sha256()
    for path in bundle_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def frontmatter_name(skill_file: Path) -> str:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise InstallError(f"cannot read {skill_file}: {exc}") from exc
    if not text.startswith("---"):
        raise InstallError(f"invalid frontmatter in {skill_file}")
    end = text.find("\n---", 3)
    if end < 0:
        raise InstallError(f"unclosed frontmatter in {skill_file}")
    match = FRONTMATTER_NAME_RE.search(text[3:end])
    if not match:
        raise InstallError(f"frontmatter name missing in {skill_file}")
    return match.group(1).strip().strip('"\'')


def load_bundle() -> Bundle:
    raw = read_json(MANIFEST_PATH)
    if not isinstance(raw, dict):
        raise InstallError("skill-bundle.json must contain an object")
    if raw.get("schema_version") != 1 or raw.get("bundle_id") != "lny-prd":
        raise InstallError("unsupported skill-bundle.json schema or bundle_id")
    version = raw.get("bundle_version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        raise InstallError("bundle_version must be a stable X.Y.Z version")
    skills = raw.get("skills")
    if (
        not isinstance(skills, list)
        or any(not isinstance(name, str) for name in skills)
        or len(skills) != len(set(skills))
        or set(skills) != EXPECTED_SKILLS
    ):
        raise InstallError("skill-bundle.json must list the ten core LNY-PRD skills and optional Yunxiao adapter")
    resources = raw.get("optional_resources")
    examples_config = resources.get("examples") if isinstance(resources, dict) else None
    if not isinstance(examples_config, dict) or examples_config.get("audience") != "human":
        raise InstallError("examples must be declared as an optional human resource")
    examples_path = examples_config.get("path")
    if not isinstance(examples_path, str):
        raise InstallError("examples.path must be a string")
    examples = (ROOT / examples_path).resolve()
    if examples != (ROOT / "examples").resolve() or not examples.is_dir():
        raise InstallError("examples.path must resolve to the repository examples directory")

    digests: dict[str, str] = {}
    names: dict[str, str] = {}
    for skill in skills:
        skill_dir = ROOT / skill
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            raise InstallError(f"{skill}: SKILL.md missing")
        name = frontmatter_name(skill_file)
        if name != skill:
            raise InstallError(f"{skill_file}: frontmatter name must be {skill}")
        names[skill] = name
        digests[skill] = directory_digest(skill_dir)
    return Bundle("lny-prd", version, tuple(skills), examples, digests, names)


def normalize_host(value: str) -> HostSpec:
    host_id = HOST_ALIASES.get(value.lower())
    if host_id is None:
        choices = ", ".join(HOSTS)
        raise InstallError(f"unsupported host {value!r}; choose one of: {choices}")
    return HOSTS[host_id]


def resolve_target(host_value: str, destination: str | None = None) -> Target:
    host = normalize_host(host_value)
    if destination:
        skills_root = Path(destination).expanduser().resolve()
        config_root = skills_root.parent
        state_root = config_root / f".lny-prd-{host.host_id}"
    else:
        config_root = (Path.home() / host.config_dir).resolve()
        skills_root = config_root / "skills"
        state_root = config_root / "lny-prd"
    trae_config = config_root / "skill-config.json" if host.trae_config else None
    return Target(
        host=host,
        config_root=config_root,
        skills_root=skills_root,
        state_root=state_root,
        state_file=state_root / "install.json",
        lock_file=state_root / "install.lock",
        backups_root=state_root / "backups",
        trae_config_file=trae_config,
    )


def validate_direct_child(parent: Path, path: Path, expected_name: str) -> None:
    if path.name != expected_name or path.parent.resolve() != parent.resolve():
        raise InstallError(f"refusing unsafe path outside {parent}: {path}")


def remove_tree(path: Path, parent: Path, expected_name: str) -> None:
    validate_direct_child(parent, path, expected_name)
    if path.exists():
        shutil.rmtree(path)


def copy_skill(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".DS_Store", ".git", "__pycache__", "*.pyc", "*.pyo"),
    )


def prepare_stage(bundle: Bundle, target: Target) -> Path:
    target.skills_root.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(prefix=".lny-prd-stage-", dir=str(target.skills_root.parent))
    )
    try:
        for skill in bundle.skills:
            copy_skill(ROOT / skill, stage / skill)
            if directory_digest(stage / skill) != bundle.digests[skill]:
                raise InstallError(f"staged copy digest mismatch for {skill}")
        return stage
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def load_install_state(target: Target, *, required: bool) -> dict | None:
    if not target.state_file.is_file():
        if required:
            raise InstallError(
                f"no managed installation for {target.host.display_name}; run install first"
            )
        return None
    raw = read_json(target.state_file)
    if not isinstance(raw, dict):
        raise InstallError(f"invalid install state: {target.state_file}")
    if (
        raw.get("schema_version") != 1
        or raw.get("bundle_id") != "lny-prd"
        or raw.get("host") != target.host.host_id
        or raw.get("skills_root") != str(target.skills_root)
        or not isinstance(raw.get("skills"), dict)
    ):
        raise InstallError(f"install state does not match this target: {target.state_file}")
    return raw


def current_digests(bundle: Bundle, target: Target) -> tuple[dict[str, str], list[str]]:
    digests: dict[str, str] = {}
    missing: list[str] = []
    for skill in bundle.skills:
        path = target.skills_root / skill
        if not path.is_dir():
            missing.append(skill)
        else:
            digests[skill] = directory_digest(path)
    return digests, missing


def state_drift(bundle: Bundle, target: Target, state: dict) -> list[str]:
    recorded = state.get("skills")
    if not isinstance(recorded, dict):
        return ["install state has no valid skill digests"]
    current, missing = current_digests(bundle, target)
    drift = [f"{skill}: missing" for skill in missing if skill in recorded]
    for skill, digest in current.items():
        if skill not in recorded:
            drift.append(f"{skill}: unmanaged collision")
        elif recorded.get(skill) != digest:
            drift.append(f"{skill}: locally modified")
    return drift


def load_trae_config(path: Path) -> dict:
    if not path.exists():
        return {"managedSkills": {}, "disabledSkills": []}
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise InstallError(f"TraeWork CN config must be a JSON object: {path}")
    managed = raw.get("managedSkills")
    if managed is None:
        raw["managedSkills"] = {}
    elif not isinstance(managed, dict):
        raise InstallError(f"TraeWork CN managedSkills must be an object: {path}")
    disabled = raw.get("disabledSkills")
    if disabled is not None and not isinstance(disabled, list):
        raise InstallError(f"TraeWork CN disabledSkills must be an array: {path}")
    return raw


def update_trae_config(bundle: Bundle, target: Target, *, remove: bool) -> bool:
    path = target.trae_config_file
    if path is None:
        return False
    config = load_trae_config(path)
    managed = config["managedSkills"]
    before = dict(managed)
    for skill in bundle.skills:
        name = bundle.frontmatter_names[skill]
        if remove:
            managed.pop(name, None)
        else:
            managed[name] = "user_upload"
    if managed == before:
        return False
    write_json_atomic(path, config)
    return True


def trae_config_healthy(bundle: Bundle, target: Target) -> bool:
    path = target.trae_config_file
    if path is None:
        return True
    try:
        config = load_trae_config(path)
    except InstallError:
        return False
    managed = config.get("managedSkills", {})
    return all(managed.get(name) == "user_upload" for name in bundle.frontmatter_names.values())


@contextlib.contextmanager
def install_lock(target: Target) -> Iterator[None]:
    target.state_root.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(target.lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise InstallError(f"another installation is active: {target.lock_file}") from exc
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        with contextlib.suppress(FileNotFoundError):
            target.lock_file.unlink()


def backup_name(version: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{timestamp}-{version}-{uuid.uuid4().hex[:8]}"


def create_backup(target: Target, version: str) -> Path:
    target.backups_root.mkdir(parents=True, exist_ok=True)
    backup = target.backups_root / backup_name(version)
    backup.mkdir()
    return backup


def restore_file(path: Path, original: bytes | None) -> None:
    if original is None:
        with contextlib.suppress(FileNotFoundError):
            path.unlink()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.restore")
        temp.write_bytes(original)
        os.replace(temp, path)


def prune_backups(target: Target, keep: int = 1) -> None:
    if not target.backups_root.is_dir():
        return
    backups = sorted(path for path in target.backups_root.iterdir() if path.is_dir())
    for path in backups[:-keep]:
        validate_direct_child(target.backups_root, path, path.name)
        shutil.rmtree(path)


def build_state(bundle: Bundle, target: Target) -> dict:
    digests, missing = current_digests(bundle, target)
    if missing:
        raise InstallError(f"installed bundle is incomplete: {', '.join(missing)}")
    return {
        "schema_version": 1,
        "bundle_id": bundle.bundle_id,
        "bundle_version": bundle.version,
        "host": target.host.host_id,
        "host_display_name": target.host.display_name,
        "skills_root": str(target.skills_root),
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "skills": digests,
    }


def replace_bundle(bundle: Bundle, target: Target, old_state: dict | None) -> None:
    stage = prepare_stage(bundle, target)
    target.skills_root.mkdir(parents=True, exist_ok=True)
    original_state = target.state_file.read_bytes() if target.state_file.exists() else None
    config_path = target.trae_config_file
    original_config = config_path.read_bytes() if config_path and config_path.exists() else None
    backup: Path | None = None
    moved_old: list[str] = []
    installed_new: list[str] = []
    try:
        with install_lock(target):
            old_version = str(old_state.get("bundle_version", "unmanaged")) if old_state else "unmanaged"
            backup = create_backup(target, old_version)
            if original_state is not None:
                (backup / "install.json").write_bytes(original_state)
            if original_config is not None:
                (backup / "skill-config.json").write_bytes(original_config)

            try:
                for skill in bundle.skills:
                    destination = target.skills_root / skill
                    validate_direct_child(target.skills_root, destination, skill)
                    if destination.exists():
                        os.replace(destination, backup / skill)
                        moved_old.append(skill)
                for skill in bundle.skills:
                    destination = target.skills_root / skill
                    os.replace(stage / skill, destination)
                    installed_new.append(skill)
                update_trae_config(bundle, target, remove=False)
                write_json_atomic(target.state_file, build_state(bundle, target))
            except Exception as exc:
                for skill in reversed(installed_new):
                    remove_tree(target.skills_root / skill, target.skills_root, skill)
                for skill in reversed(moved_old):
                    os.replace(backup / skill, target.skills_root / skill)
                restore_file(target.state_file, original_state)
                if config_path is not None:
                    restore_file(config_path, original_config)
                raise InstallError(f"installation failed and was rolled back: {exc}") from exc
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    if backup is not None:
        prune_backups(target)


def semver_tuple(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.fullmatch(value)
    if not match:
        raise InstallError(f"invalid installed bundle version: {value}")
    return tuple(int(part) for part in match.groups())


def print_target(action: str, bundle: Bundle, target: Target, *, dry_run: bool) -> None:
    prefix = "DRY-RUN " if dry_run else ""
    print(f"{prefix}{action}: {target.host.display_name} {bundle.version}")
    print(f"skills: {target.skills_root}")
    if target.trae_config_file:
        print(f"TraeWork CN config: {target.trae_config_file}")


def command_install(args: argparse.Namespace, bundle: Bundle, target: Target) -> int:
    if target.host.trae_config and args.dest is None and not target.config_root.is_dir():
        raise InstallError(
            f"TraeWork CN config root does not exist: {target.config_root}; start TraeWork CN first"
        )
    if load_install_state(target, required=False) is not None:
        raise InstallError("this target is already managed; use update")
    existing = [skill for skill in bundle.skills if (target.skills_root / skill).exists()]
    if existing and not args.force:
        raise InstallError(
            "unmanaged skill directories already exist: "
            + ", ".join(existing)
            + "; use --force to back up and replace them"
        )
    print_target("install", bundle, target, dry_run=args.dry_run)
    for skill in bundle.skills:
        print(f"  {'would install' if args.dry_run else 'install'} {skill}")
    if args.dry_run:
        return 0
    replace_bundle(bundle, target, None)
    print("installation complete")
    return 0


def command_update(args: argparse.Namespace, bundle: Bundle, target: Target) -> int:
    state = load_install_state(target, required=True)
    assert state is not None
    drift = state_drift(bundle, target, state)
    if drift and not args.force:
        raise InstallError(
            "installed skills changed since the last managed install:\n  "
            + "\n  ".join(drift)
            + "\nuse --force to back up and replace the changed installation"
        )
    installed_version = state.get("bundle_version")
    if not isinstance(installed_version, str):
        raise InstallError("install state has no valid bundle_version")
    if semver_tuple(bundle.version) < semver_tuple(installed_version) and not args.allow_downgrade:
        raise InstallError(
            f"refusing downgrade {installed_version} -> {bundle.version}; use --allow-downgrade"
        )
    current, missing = current_digests(bundle, target)
    if (
        not missing
        and current == bundle.digests
        and installed_version == bundle.version
        and trae_config_healthy(bundle, target)
    ):
        print(f"{target.host.display_name}: already current at {bundle.version}")
        return 0
    print_target("update", bundle, target, dry_run=args.dry_run)
    if drift:
        for item in drift:
            print(f"  {'would replace' if args.dry_run else 'replace'} {item}")
    if args.dry_run:
        return 0
    replace_bundle(bundle, target, state)
    print(f"updated {installed_version} -> {bundle.version}")
    return 0


def command_status(args: argparse.Namespace, bundle: Bundle, target: Target) -> int:
    state = load_install_state(target, required=False)
    if state is None:
        existing = [skill for skill in bundle.skills if (target.skills_root / skill).exists()]
        if existing:
            print(f"{target.host.display_name}: unmanaged ({len(existing)}/{len(bundle.skills)} skill directories found)")
            return 1
        print(f"{target.host.display_name}: not installed")
        return 0
    drift = state_drift(bundle, target, state)
    if not trae_config_healthy(bundle, target):
        drift.append("TraeWork CN managedSkills registration is missing or invalid")
    installed_version = state.get("bundle_version", "unknown")
    if drift:
        print(f"{target.host.display_name}: unhealthy at {installed_version}")
        for item in drift:
            print(f"  - {item}")
        return 1
    suffix = " (update available)" if installed_version != bundle.version else ""
    print(f"{target.host.display_name}: healthy at {installed_version}{suffix}")
    print(f"skills: {target.skills_root}")
    return 0


def command_uninstall(args: argparse.Namespace, bundle: Bundle, target: Target) -> int:
    state = load_install_state(target, required=True)
    assert state is not None
    drift = state_drift(bundle, target, state)
    if drift and not args.force:
        raise InstallError(
            "installed skills changed since the last managed install:\n  "
            + "\n  ".join(drift)
            + "\nuse --force to back up and uninstall them"
        )
    print_target("uninstall", bundle, target, dry_run=args.dry_run)
    if args.dry_run:
        return 0

    original_state = target.state_file.read_bytes()
    config_path = target.trae_config_file
    original_config = config_path.read_bytes() if config_path and config_path.exists() else None
    moved: list[str] = []
    with install_lock(target):
        backup = create_backup(target, str(state.get("bundle_version", "unknown")))
        (backup / "install.json").write_bytes(original_state)
        if original_config is not None:
            (backup / "skill-config.json").write_bytes(original_config)
        try:
            for skill in bundle.skills:
                source = target.skills_root / skill
                validate_direct_child(target.skills_root, source, skill)
                if source.exists():
                    os.replace(source, backup / skill)
                    moved.append(skill)
            update_trae_config(bundle, target, remove=True)
            target.state_file.unlink()
        except Exception as exc:
            for skill in reversed(moved):
                os.replace(backup / skill, target.skills_root / skill)
            restore_file(target.state_file, original_state)
            if config_path is not None:
                restore_file(config_path, original_config)
            raise InstallError(f"uninstall failed and was rolled back: {exc}") from exc
    prune_backups(target)
    print("uninstall complete; the last installation is retained in backups")
    return 0


def command_detect(bundle: Bundle) -> int:
    print(f"LNY-PRD bundle {bundle.version}")
    for host in HOSTS.values():
        target = resolve_target(host.host_id)
        state = "managed" if target.state_file.is_file() else "not managed"
        print(
            f"{host.display_name}: {target.skills_root} "
            f"(config root {'exists' if target.config_root.exists() else 'missing'}, {state})"
        )
    return 0


def command_export_examples(args: argparse.Namespace, bundle: Bundle) -> int:
    destination = (
        Path(args.dest).expanduser().resolve()
        if args.dest
        else (Path.home() / ".lny-prd" / "examples").resolve()
    )
    print(f"{'DRY-RUN ' if args.dry_run else ''}export examples: {destination}")
    if destination.exists() and not args.force:
        raise InstallError(f"examples destination already exists: {destination}; use --force")
    if args.dry_run:
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".lny-prd-examples-", dir=str(destination.parent)))
    staged_examples = stage / "examples"
    backup: Path | None = None
    try:
        shutil.copytree(bundle.examples, staged_examples)
        if destination.exists():
            backup_root = destination.parent / ".lny-prd-example-backups"
            backup_root.mkdir(exist_ok=True)
            backup = backup_root / backup_name(bundle.version)
            os.replace(destination, backup)
        try:
            os.replace(staged_examples, destination)
        except Exception:
            if backup is not None and backup.exists():
                os.replace(backup, destination)
            raise
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    print("examples exported for human reference")
    return 0


def add_target_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", required=True, help="cursor, chatgpt, or traework-cn")
    parser.add_argument("--dest", help="explicit skills directory override")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install the atomic LNY-PRD bundle: ten core skills plus the Yunxiao adapter."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install = subparsers.add_parser("install", help="install an unmanaged bundle")
    add_target_arguments(install)
    install.add_argument("--force", action="store_true", help="back up and replace collisions")
    install.add_argument("--dry-run", action="store_true")

    update = subparsers.add_parser("update", help="update a managed bundle")
    add_target_arguments(update)
    update.add_argument("--force", action="store_true", help="back up and replace local drift")
    update.add_argument("--allow-downgrade", action="store_true")
    update.add_argument("--dry-run", action="store_true")

    status = subparsers.add_parser("status", help="inspect a managed bundle")
    add_target_arguments(status)

    uninstall = subparsers.add_parser("uninstall", help="back up and remove a managed bundle")
    add_target_arguments(uninstall)
    uninstall.add_argument("--force", action="store_true", help="allow uninstall with local drift")
    uninstall.add_argument("--dry-run", action="store_true")

    subparsers.add_parser("detect", help="show supported user-level host paths")

    examples = subparsers.add_parser(
        "export-examples", help="export human-only examples outside skill directories"
    )
    examples.add_argument("--dest", help="destination, default ~/.lny-prd/examples")
    examples.add_argument("--force", action="store_true")
    examples.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        bundle = load_bundle()
        if args.command == "detect":
            return command_detect(bundle)
        if args.command == "export-examples":
            return command_export_examples(args, bundle)
        target = resolve_target(args.host, args.dest)
        if args.command == "install":
            return command_install(args, bundle, target)
        if args.command == "update":
            return command_update(args, bundle, target)
        if args.command == "status":
            return command_status(args, bundle, target)
        if args.command == "uninstall":
            return command_uninstall(args, bundle, target)
        parser.error(f"unsupported command: {args.command}")
    except InstallError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
