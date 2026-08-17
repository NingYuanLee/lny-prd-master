# -*- coding: utf-8 -*-
"""Validate skill metadata, scripts, examples, mirrors, and regression contracts."""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    print(
        "PyYAML is required; run: python -m pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = sorted(path for path in ROOT.glob("lny-prd-*") if path.is_dir())
EXPECTED_SKILLS = {
    "lny-prd-api",
    "lny-prd-check",
    "lny-prd-feature",
    "lny-prd-iter",
    "lny-prd-master",
    "lny-prd-page",
    "lny-prd-prototype",
    "lny-prd-sp",
    "lny-prd-ui",
}
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
GENERATED_PROJECT_DOCS = {"api_spec.md", "feature_spec.md", "ui_manifest.md"}
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".mdc", ".mjs", ".py", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitignore", "LICENSE"}
EXCLUDED_PARTS = {".cursor", ".git", "__pycache__", "node_modules"}
QUICK_VALIDATE = ROOT / "scripts" / "quick_validate.py"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def run(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def require_run(command: list[str], errors: list[str], label: str, *, cwd: Path = ROOT) -> None:
    result = run(command, cwd=cwd)
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        fail(errors, f"{label} failed:\n{detail}")


def load_yaml_mapping(path: Path, text: str, errors: list[str]) -> dict | None:
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        fail(errors, f"{path}: invalid YAML: {exc}")
        return None
    if not isinstance(value, dict):
        fail(errors, f"{path}: YAML root must be a mapping")
        return None
    return value


def validate_skill_metadata(errors: list[str]) -> None:
    names = {path.name for path in SKILL_DIRS}
    if names != EXPECTED_SKILLS:
        fail(
            errors,
            "skill directories mismatch: expected "
            + str(sorted(EXPECTED_SKILLS))
            + ", got "
            + str(sorted(names)),
        )

    for skill_dir in SKILL_DIRS:
        require_run(
            [sys.executable, str(QUICK_VALIDATE), str(skill_dir)],
            errors,
            f"quick validation for {skill_dir.name}",
        )

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            fail(errors, f"{skill_dir.name}: SKILL.md missing")
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            fail(errors, f"{skill_file}: invalid or unclosed frontmatter")
            continue
        frontmatter = load_yaml_mapping(skill_file, match.group(1), errors)
        if frontmatter is None:
            continue
        if list(frontmatter) != ["name", "description"]:
            fail(
                errors,
                f"{skill_file}: frontmatter keys must be name, description; got {list(frontmatter)}",
            )
        if frontmatter.get("name") != skill_dir.name:
            fail(errors, f"{skill_file}: name must match directory {skill_dir.name}")

        agent_file = skill_dir / "agents" / "openai.yaml"
        if not agent_file.is_file():
            fail(errors, f"{agent_file}: missing")
            continue
        agent_text = agent_file.read_text(encoding="utf-8")
        agent = load_yaml_mapping(agent_file, agent_text, errors)
        if agent is None:
            continue
        unexpected = set(agent) - {"interface", "dependencies", "policy"}
        if unexpected:
            fail(errors, f"{agent_file}: unexpected top-level keys {sorted(unexpected)}")

        interface = agent.get("interface")
        if not isinstance(interface, dict):
            fail(errors, f"{agent_file}: interface must be a mapping")
            continue
        for field in ("display_name", "short_description", "default_prompt"):
            value = interface.get(field)
            if not isinstance(value, str) or not value.strip():
                fail(errors, f"{agent_file}: interface.{field} must be a non-empty string")
            quoted = re.search(
                rf'^  {re.escape(field)}: "(?:[^"\\]|\\.)*"$',
                agent_text,
                flags=re.M,
            )
            if not quoted:
                fail(errors, f"{agent_file}: interface.{field} must be double-quoted")
        short = interface.get("short_description")
        if isinstance(short, str) and not 25 <= len(short) <= 64:
            fail(errors, f"{agent_file}: short_description must be 25..64 characters")
        prompt = interface.get("default_prompt")
        if isinstance(prompt, str) and f"${skill_dir.name}" not in prompt:
            fail(errors, f"{agent_file}: default_prompt must mention ${skill_dir.name}")

        policy = agent.get("policy")
        if not isinstance(policy, dict):
            fail(errors, f"{agent_file}: policy must be a mapping")
            continue
        implicit = policy.get("allow_implicit_invocation")
        expected = skill_dir.name == "lny-prd-master"
        if not isinstance(implicit, bool) or implicit is not expected:
            fail(
                errors,
                f"{agent_file}: allow_implicit_invocation must be {str(expected).lower()}",
            )

    with tempfile.TemporaryDirectory(prefix="lny-prd-invalid-skill-") as temp:
        bad = Path(temp) / "bad-skill"
        bad.mkdir()
        (bad / "SKILL.md").write_text(
            "---\nname: bad-skill\ndescription: [\n---\n# Broken\n",
            encoding="utf-8",
        )
        result = run([sys.executable, str(QUICK_VALIDATE), str(bad)])
        if result.returncode == 0:
            fail(errors, "quick_validate.py accepted malformed YAML regression fixture")


def markdown_files() -> list[Path]:
    paths = [ROOT / "README.md"]
    for skill_dir in SKILL_DIRS:
        paths.extend(skill_dir.rglob("*.md"))
    return sorted(set(path for path in paths if path.is_file()))


def validate_markdown_links(errors: list[str]) -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw = match.group(1).split("#", 1)[0].strip()
            if not raw or re.match(r"^(?:https?://|mailto:)", raw):
                continue
            if any(char in raw for char in "{}<>*"):
                continue
            if Path(raw).name in GENERATED_PROJECT_DOCS:
                continue
            target = (path.parent / raw).resolve()
            if not target.exists():
                fail(errors, f"{path}: broken Markdown link {raw}")


def repo_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        files.append(path)
    return files


def validate_text_and_yaml(errors: list[str]) -> None:
    for path in repo_files():
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            fail(errors, f"{path}: invalid UTF-8: {exc}")
            continue
        if path.suffix.lower() in {".yaml", ".yml"}:
            load_yaml_mapping(path, text, errors)


def validate_script_syntax(errors: list[str]) -> None:
    for path in repo_files():
        if path.suffix.lower() != ".py":
            continue
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (OSError, SyntaxError) as exc:
            fail(errors, f"{path}: Python syntax error: {exc}")

    node = shutil.which("node")
    js_files = [
        path
        for path in repo_files()
        if path.suffix.lower() in {".js", ".mjs", ".cjs"}
    ]
    if js_files and node is None:
        fail(errors, "Node.js is required to validate JavaScript syntax")
        return
    for path in js_files:
        require_run([node or "node", "--check", str(path)], errors, f"JS syntax {path}")


def file_map(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def validate_example_identity_and_mirror(errors: list[str]) -> None:
    example = ROOT / "examples" / "mini-shop"
    current = example / "prototypes"
    mirror = example / "versions" / "v1.0.0" / "prototypes"
    current_files = file_map(current)
    mirror_files = file_map(mirror)
    if set(current_files) != set(mirror_files):
        missing = sorted(set(current_files) - set(mirror_files))
        extra = sorted(set(mirror_files) - set(current_files))
        fail(errors, f"prototype mirror file set mismatch: missing={missing}, extra={extra}")
    for relative in sorted(set(current_files) & set(mirror_files)):
        if current_files[relative].read_bytes() != mirror_files[relative].read_bytes():
            fail(errors, f"prototype mirror content mismatch: {relative}")

    for root in (current, mirror):
        for path in sorted(root.rglob("PAGE-*.html")):
            text = path.read_text(encoding="utf-8")
            title = re.search(r"<title>\s*([^<]+)</title>", text, flags=re.I)
            if not title or not re.match(rf"^{re.escape(path.stem)}(?:\s|$)", title.group(1)):
                fail(errors, f"{path}: <title> must start with {path.stem}")


def validate_kit_copies(errors: list[str]) -> None:
    kit = ROOT / "lny-prd-prototype" / "kit"
    example = ROOT / "examples" / "mini-shop"
    targets = [ROOT / "lny-prd-prototype" / "gold" / "assets"]
    for prototype_root in (
        example / "prototypes",
        example / "versions" / "v1.0.0" / "prototypes",
    ):
        targets.extend(path for path in prototype_root.glob("*/assets") if path.is_dir())
    for source in sorted(path for path in kit.iterdir() if path.is_file()):
        for target_dir in targets:
            target = target_dir / source.name
            if not target.is_file():
                fail(errors, f"{target}: missing kit mirror file")
            elif target.read_bytes() != source.read_bytes():
                fail(errors, f"{target}: differs from kit/{source.name}")


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_coverage_regressions(module, errors: list[str]) -> None:
    naked = module.PageParser()
    naked.feed("<label class=md-field><input></label><input>")
    if not any("naked <input>" in error for error in naked.errors) or naked.stack:
        fail(errors, "coverage parser failed the void-element ancestor-stack regression")

    detail = module.PageParser()
    detail.feed('<main><article class="md-card md-card--row"></article></main>')
    if module.check_density(Path("detail.html"), detail):
        fail(errors, "coverage density rejected a non-list page with one card")

    card_list = module.PageParser()
    card_list.feed(
        '<header class="md-list-toolbar"></header>'
        '<article class="md-card md-card--row"></article>'
    )
    if not module.check_density(Path("list.html"), card_list):
        fail(errors, "coverage density accepted a list page with fewer than four cards")

    short_table = module.PageParser()
    short_table.feed(
        '<table class="md-table"><tbody><tr><td>A</td></tr><tr><td>B</td></tr></tbody></table>'
    )
    if module.check_density(Path("summary.html"), short_table):
        fail(errors, "coverage density rejected a short non-D1-1 summary table")

    dense_table = module.PageParser()
    dense_table.feed(
        '<div class="md-d1 md-d1--list"><table class="md-table"><tbody>'
        '<tr><td>A</td></tr><tr><td>B</td></tr></tbody></table></div>'
    )
    if not module.check_density(Path("d1-list.html"), dense_table):
        fail(errors, "coverage density accepted a D1-1 table with fewer than four rows")

    wrong_card = module.PageParser()
    wrong_text = (
        '<div class="md-mobile-page md-standard">'
        '<header class="md-list-toolbar"></header><article class="md-card"></article></div>'
    )
    wrong_card.feed(wrong_text)
    visual_errors = module.check_visual_floor(Path("mobile-list.html"), wrong_text, wrong_card)
    if not any("mobile list cards must use md-card--row" in error for error in visual_errors):
        fail(errors, "coverage accepted a non-row card inside a mobile list")


def validate_migration(errors: list[str]) -> None:
    node = shutil.which("node")
    if node is None:
        fail(errors, "Node.js is required to test migrate-prd-structure.mjs")
        return
    script = ROOT / "lny-prd-ui" / "scripts" / "migrate-prd-structure.mjs"
    manifest = """# UI manifest

## 5 页面与组件

### PAGE-MP-001 首页

#### 结构

page body

### COMP-001 卡片

#### 状态

component body

## 6 其它

must not migrate
"""
    with tempfile.TemporaryDirectory(prefix="lny-prd-migrate-") as temp:
        root = Path(temp)
        (root / "ui_manifest.md").write_text(manifest, encoding="utf-8")
        command = [node, str(script), "--root", str(root)]

        dry = run([*command, "--dry-run"])
        if dry.returncode or "would write 2 file(s)" not in dry.stdout:
            fail(errors, "migration dry-run did not report the two planned files")

        first = run(command)
        page = root / "ui" / "PAGE-MP-001.md"
        comp = root / "ui" / "COMP-001.md"
        if first.returncode or not page.is_file() or not comp.is_file():
            fail(errors, "migration failed to create PAGE and COMP detail files")
            return
        page_text = page.read_text(encoding="utf-8")
        if "COMP-001" in page_text or "must not migrate" in page_text:
            fail(errors, "migration PAGE section leaked an adjacent or trailing section")

        page.write_text("local edit\n", encoding="utf-8")
        blocked = run(command)
        if blocked.returncode != 2 or page.read_text(encoding="utf-8") != "local edit\n":
            fail(errors, "migration did not preserve an existing conflicting detail file")

        conflict_dry = run([*command, "--dry-run"])
        if conflict_dry.returncode or "[would overwrite]" not in conflict_dry.stdout:
            fail(errors, "migration dry-run did not identify an overwrite conflict")

        forced = run([*command, "--force"])
        if forced.returncode or "page body" not in page.read_text(encoding="utf-8"):
            fail(errors, "migration --force did not replace the conflicting file")
        leftovers = [path for path in root.rglob("*") if ".lny-prd-" in path.name]
        if leftovers:
            fail(errors, f"migration left transaction files behind: {leftovers}")


def validate_prototypes(errors: list[str]) -> None:
    scripts = ROOT / "lny-prd-prototype" / "scripts"
    utf8 = scripts / "verify-prototype-utf8.py"
    coverage = scripts / "verify-prototype-coverage.py"
    copy_kit = scripts / "copy-kit.py"
    search_icons = scripts / "search-icons.py"
    example = ROOT / "examples" / "mini-shop"
    require_run(
        [sys.executable, str(search_icons), "--list-kit"],
        errors,
        "offline icon index",
    )
    require_run(
        [sys.executable, str(search_icons), "首页", "--local-only"],
        errors,
        "offline icon lookup",
    )
    html = sorted((example / "prototypes").rglob("*.html"))
    html += sorted((example / "versions" / "v1.0.0" / "prototypes").rglob("*.html"))
    require_run(
        [sys.executable, str(utf8), *(str(path) for path in html)],
        errors,
        "UTF-8 validation",
    )

    pages = sorted(
        path.stem
        for path in (example / "versions" / "v1.0.0" / "pages_prd").rglob("PAGE-*.md")
    )
    command = [sys.executable, str(coverage), str(example), "--version", "v1.0.0"]
    for page in pages:
        command.extend(("--page", page))
    require_run(command, errors, "prototype coverage")

    with tempfile.TemporaryDirectory(prefix="lny-prd-kit-") as temp:
        destination = Path(temp) / "MP"
        require_run(
            [sys.executable, str(copy_kit), str(destination)],
            errors,
            "kit copy",
        )
        expected = {
            "icons-extra.js",
            "md-icons.js",
            "mui-kit.css",
            "proto-map.js",
            "proto-page.js",
            "proto-shell.css",
            "proto-shell.js",
        }
        actual = {path.name for path in (destination / "assets").glob("*")}
        if actual != expected:
            fail(errors, f"kit copy files mismatch: expected {sorted(expected)}, got {sorted(actual)}")

    try:
        module = import_module(coverage, "prototype_coverage")
    except RuntimeError as exc:
        fail(errors, str(exc))
        return
    validate_coverage_regressions(module, errors)
    for gold in sorted((ROOT / "lny-prd-prototype" / "gold").glob("*.html")):
        gold_errors = module.check_html(gold, gold.stem, set(), set(), [])
        for error in gold_errors:
            fail(errors, "gold validation: " + error)


def main() -> int:
    errors: list[str] = []
    validate_skill_metadata(errors)
    validate_markdown_links(errors)
    validate_text_and_yaml(errors)
    validate_script_syntax(errors)
    validate_example_identity_and_mirror(errors)
    validate_kit_copies(errors)
    validate_migration(errors)
    validate_prototypes(errors)
    if errors:
        print("skill package validation failed:", file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print(
        f"skill package validation ok: {len(SKILL_DIRS)} skills; real YAML + quick validation; "
        "links; UTF-8; Python/JS; migration; kit/gold; exact mirror; fixture + negative coverage"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
