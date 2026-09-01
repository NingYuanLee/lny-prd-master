# -*- coding: utf-8 -*-
"""Validate skill metadata, scripts, examples, and regression contracts."""
from __future__ import annotations

import importlib.util
import json
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
        "PyYAML is required in the active interpreter. Create the repository "
        ".venv and install requirements-dev.txt; see README.md section 10.",
        file=sys.stderr,
    )
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = sorted(path for path in ROOT.glob("lny-prd-*") if path.is_dir())
EXPECTED_SKILL_ORDER = (
    "lny-prd-master",
    "lny-prd-ui",
    "lny-prd-api",
    "lny-prd-feature",
    "lny-prd-review",
    "lny-prd-page",
    "lny-prd-prototype",
    "lny-prd-check",
    "lny-prd-iter",
    "lny-prd-sp",
)
EXPECTED_SKILLS = set(EXPECTED_SKILL_ORDER)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.S)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXAMPLES_PATH_RE = re.compile(r"(?:^|[\s(\"'`])(?:\.\./)*examples[\\/]", re.M)
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
GENERATED_PROJECT_DOCS = {"api_spec.md", "feature_spec.md", "ui_manifest.md"}
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".mdc", ".mjs", ".py", ".txt", ".yaml", ".yml"}
TEXT_NAMES = {".gitignore", "LICENSE"}
EXCLUDED_PARTS = {".cursor", ".git", "__pycache__", "node_modules"}
QUICK_VALIDATE = ROOT / "scripts" / "quick_validate.py"
INSTALLER_TESTS = ROOT / "scripts" / "test_install_skills.py"
ARTIFACT_PATH_CHECKER = ROOT / "lny-prd-check" / "scripts" / "verify-artifact-paths.py"
PRD_SEMANTIC_CHECKER = ROOT / "lny-prd-check" / "scripts" / "validate-prd-project.py"
PRD_SEMANTIC_TESTS = ROOT / "scripts" / "test_validate_prd_project.py"


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


def validate_bundle_contract(errors: list[str]) -> None:
    manifest_path = ROOT / "skill-bundle.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{manifest_path}: invalid bundle manifest: {exc}")
        return
    if not isinstance(manifest, dict):
        fail(errors, f"{manifest_path}: root must be an object")
        return
    if manifest.get("schema_version") != 1 or manifest.get("bundle_id") != "lny-prd":
        fail(errors, f"{manifest_path}: expected schema_version 1 and bundle_id lny-prd")
    version = manifest.get("bundle_version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        fail(errors, f"{manifest_path}: bundle_version must be stable X.Y.Z")
    if manifest.get("skills") != list(EXPECTED_SKILL_ORDER):
        fail(errors, f"{manifest_path}: skills must list ten ordered core skills")
    expected_resources = {"examples": {"path": "examples", "audience": "regression"}}
    if manifest.get("optional_resources") != expected_resources:
        fail(errors, f"{manifest_path}: optional_resources must declare regression-only examples")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    match = re.search(r"\*\*工具包版本：([^*]+)\*\*", readme)
    readme_version = match.group(1).strip() if match else None
    if isinstance(version, str) and readme_version != version:
        fail(errors, f"README version {readme_version!r} does not match bundle {version!r}")

    prototype_skill = (ROOT / "lny-prd-prototype" / "SKILL.md").read_text(encoding="utf-8")
    master_skill = (ROOT / "lny-prd-master" / "SKILL.md").read_text(encoding="utf-8")
    prototype_contract_files = {
        "README.md": readme,
        "lny-prd-master/SKILL.md": master_skill,
        "lny-prd-prototype/SKILL.md": prototype_skill,
    }
    fixed_page_cap_patterns = ("每轮最多 3", "截取最多 3", "超过 3 个业务页")
    for label, text in prototype_contract_files.items():
        for pattern in fixed_page_cap_patterns:
            if pattern in text:
                fail(errors, f"{label}: prototype workflow must not restore fixed three-page cap {pattern!r}")
    if "不按数量截取" not in prototype_skill or "全部 active 缺页" not in prototype_skill:
        fail(errors, "lny-prd-prototype/SKILL.md: missing unbounded target-page selection contract")
    if "逐页执行金样对照与质量门禁" not in master_skill:
        fail(errors, "lny-prd-master/SKILL.md: missing per-page prototype quality contract")

    for skill_dir in SKILL_DIRS:
        for path in skill_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8")
            if EXAMPLES_PATH_RE.search(text):
                fail(errors, f"{path}: skill runtime must not reference repository examples/")


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


def validate_example_prototype_identity(errors: list[str]) -> None:
    current = ROOT / "examples" / "mini-shop" / "prototypes"
    for path in sorted(current.rglob("PAGE-*.html")):
        text = path.read_text(encoding="utf-8")
        title = re.search(r"<title>\s*([^<]+)</title>", text, flags=re.I)
        if not title or not re.match(rf"^{re.escape(path.stem)}(?:\s|$)", title.group(1)):
            fail(errors, f"{path}: <title> must start with {path.stem}")
        parts = path.stem.split("-")
        terminal = parts[1] if len(parts) >= 3 else ""
        if path.parent.name != terminal:
            fail(errors, f"{path}: terminal directory must be {terminal}")


def validate_kit_copies(errors: list[str]) -> None:
    kit = ROOT / "lny-prd-prototype" / "kit"
    example = ROOT / "examples" / "mini-shop"
    targets = [ROOT / "lny-prd-prototype" / "gold" / "assets"]
    prototype_root = example / "prototypes"
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
    _, _, labels = module.parse_prd(
        "## 3. 页面模块详述\n"
        "```\n节点「仅示意」\n```\n"
        "- **结构与控件**：按钮「提交」\n"
        "## 4. 交互\n"
    )
    if labels != ["提交"]:
        fail(errors, "coverage label parser treated fenced wireframe copy as a label contract")

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
    visual_errors = module.check_visual_floor(
        Path("mobile-list.html"), "PAGE-MP-002", wrong_text, wrong_card
    )
    if not any("mobile list cards must use md-card--row or md-card--order" in error for error in visual_errors):
        fail(errors, "coverage accepted a non-row card inside a mobile list")

    order_list = module.PageParser()
    order_text = (
        '<div class="md-mobile-page md-standard">'
        '<header class="md-list-toolbar"></header>'
        '<article class="md-card md-card--order"></article></div>'
    )
    order_list.feed(order_text)
    order_errors = module.check_visual_floor(
        Path("mobile-order-list.html"), "PAGE-MP-014", order_text, order_list
    )
    if any("mobile list cards must use" in error for error in order_errors):
        fail(errors, "coverage rejected md-card--order as a supported mobile list card")

    generic_mobile = module.PageParser()
    generic_mobile.feed('<div class="md-mobile-page md-standard"></div>')
    if not module.mobile_section_head_required(generic_mobile):
        fail(errors, "coverage stopped requiring section heads on generic mobile pages")
    for page_class in ("md-tree-page", "md-form-page"):
        typed_mobile = module.PageParser()
        typed_mobile.feed(
            f'<div class="md-mobile-page md-standard {page_class}"></div>'
        )
        if module.mobile_section_head_required(typed_mobile):
            fail(errors, f"coverage required a section head on {page_class}")
    for content_class in (
        "md-card md-card--cover",
        "md-card md-card--tile",
        "md-card md-card--row",
        "md-card md-card--order",
        "md-grid-2",
        "md-comment-list",
        "md-group-list",
    ):
        typed_mobile = module.PageParser()
        typed_mobile.feed(
            '<div class="md-mobile-page md-standard">'
            f'<div class="{content_class}"></div></div>'
        )
        if module.mobile_section_head_required(typed_mobile):
            fail(errors, f"coverage required a section head on {content_class}")

    wizard_demo = (
        '<div class="md-form-page"><div data-wizard-panel="stepper">'
        '<div class="md-stepper"></div><div class="md-advance"></div>'
        '</div></div>'
    )
    fixture_errors = module.check_wizard_nav(
        Path("gold/mobile-wizard.html"), "mobile-wizard", wizard_demo, fixture=True
    )
    if fixture_errors:
        fail(errors, "coverage rejected a declared gold wizard fixture")
    business_errors = module.check_wizard_nav(
        Path("business.html"), "PAGE-MP-099", wizard_demo
    )
    if not any("business page must not copy" in error for error in business_errors):
        fail(errors, "coverage accepted gold wizard demo markup on a business page")

    matrix = module.parse_comp_states(
        "## 5. UI 状态矩阵（必填）\n"
        "| 状态 | 触发条件 | 展示要点 | 可执行操作 |\n"
        "|------|----------|----------|------------|\n"
        "| loading | 请求中 | 骨架 | 无 |\n"
        "| default | 已加载 | 内容 | 点击 |\n"
        "## 6. 关联页面索引\n"
    )
    if matrix != ["loading", "default"]:
        fail(errors, "coverage state matrix parser failed the documented table")

    shell = module.parse_shell_page(
        "window.PROTO_SHELL = { pages: [{ id: 'PAGE-MP-001', stateDemo: true, "
        "comps: [{ id: 'COMP-001', states: ['loading', 'default'] }] }] };",
        "PAGE-MP-001",
    )
    if not shell or shell["comps"][0]["states"] != ["loading", "default"]:
        fail(errors, "coverage shell parser failed the PROTO_SHELL state contract")

    state_parser = module.PageParser()
    state_parser.feed(
        '<article data-comp="COMP-001" data-state="default"></article>'
        '<div class="is-hidden" data-state-for="COMP-001" data-state="pending">处理中</div>'
    )
    if state_parser.state_views.get("COMP-001") != {"pending"}:
        fail(errors, "coverage parser failed custom state visual markers")


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


def validate_artifact_path_checker(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="lny-prd-artifact-paths-") as temp:
        root = Path(temp)
        version = root / "versions" / "v1.0.0"
        (root / "api").mkdir()
        (root / "ui").mkdir()
        (root / "feature").mkdir()
        (root / "prototypes" / "MP").mkdir(parents=True)
        (version / "pages_prd" / "pages" / "index").mkdir(parents=True)
        for name in ("main_spec.md", "ui_manifest.md", "api_spec.md", "feature_spec.md"):
            (root / name).write_text("# spec\n", encoding="utf-8")
        (root / "api" / "API-MP-001.md").write_text("# API\n", encoding="utf-8")
        (root / "ui" / "PAGE-MP-001.md").write_text("# PAGE\n", encoding="utf-8")
        (root / "feature" / "FEATURE-001.md").write_text("# Feature\n", encoding="utf-8")
        (root / "prototypes" / "index.html").write_text("ok\n", encoding="utf-8")
        clean = run([sys.executable, str(ARTIFACT_PATH_CHECKER), str(root)])
        if clean.returncode:
            fail(errors, "artifact path checker rejected a canonical project:\n" + clean.stderr.strip())

        (root / "index.html").write_text("wrong\n", encoding="utf-8")
        (version / "index.html").write_text("wrong\n", encoding="utf-8")
        (version / "main_spec.md").write_text("copy\n", encoding="utf-8")
        (version / "api").mkdir()
        (version / "api" / "API-MP-001.md").write_text("copy\n", encoding="utf-8")
        (version / "prototypes" / "MP").mkdir(parents=True)
        (version / "prototypes" / "index.html").write_text("copy\n", encoding="utf-8")
        (version / "FEATURE-001.md").write_text("copy\n", encoding="utf-8")
        invalid = run([sys.executable, str(ARTIFACT_PATH_CHECKER), str(root)])
        output = invalid.stdout + invalid.stderr
        expected_codes = {
            "ROOT_INDEX",
            "VERSION_ROOT_INDEX",
            "VERSION_SPEC_COPY",
            "VERSION_SPEC_TREE",
            "VERSION_PROTOTYPE_TREE",
            "VERSION_LOOSE_DETAIL",
        }
        missing = sorted(code for code in expected_codes if code not in output)
        if invalid.returncode != 1 or missing:
            fail(
                errors,
                "artifact path checker missed forbidden project artifacts: "
                f"returncode={invalid.returncode}, missing={missing}\n{output.strip()}",
            )


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
    for fixture in ("PAGE-AD-003", "PAGE-MP-005"):
        command.extend(("--fixture", fixture))
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
        gold_errors = module.check_html(
            gold, gold.stem, set(), set(), [], fixture=True
        )
        for error in gold_errors:
            fail(errors, "gold validation: " + error)


CANONICAL_PAGE_TYPES = ROOT / "lny-prd-master" / "reference-page-types.md"
GOLD_BASENAME_RE = re.compile(r"([a-z][a-z0-9]*(?:-[a-z0-9]+)*\.html)")
PAGE_ID_RE = re.compile(r"PAGE-(MP|AD)-(\d{3})")


def section_between(text: str, start_heading: str, end_heading: str) -> str | None:
    start = text.find(start_heading)
    if start == -1:
        return None
    end = text.find(end_heading, start + len(start_heading))
    if end == -1:
        return None
    return text[start:end]


def parse_canonical_page_map(errors: list[str]) -> dict[str, set[str]] | None:
    text = CANONICAL_PAGE_TYPES.read_text(encoding="utf-8")
    section = section_between(text, "## 页型映射", "## 金样边界")
    if section is None:
        fail(errors, "reference-page-types.md: 页型映射 / 金样边界 sections missing")
        return None
    mapping: dict[str, set[str]] = {}
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5 or cells[0] == "页型":
            continue
        _page_type, mp_cell, ad_cell, mp_gold, ad_gold = cells[:5]
        for num in re.findall(r"MP-\d{3}", mp_cell):
            mapping.setdefault(num, set()).update(GOLD_BASENAME_RE.findall(mp_gold))
        for num in re.findall(r"AD-\d{3}", ad_cell):
            mapping.setdefault(num, set()).update(GOLD_BASENAME_RE.findall(ad_gold))
    if not mapping:
        fail(errors, "reference-page-types.md: 页型映射 table parsed empty")
        return None
    return mapping


def prototype_quick_row_errors(
    mapping: dict[str, set[str]],
    all_canonical_golds: set[str],
    proto_quick: str,
    *,
    label: str = "lny-prd-prototype/SKILL.md 金样速查",
) -> list[str]:
    """Check every PAGE id on every prototype quick-ref table row."""
    found: list[str] = []
    for line in proto_quick.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        ids = PAGE_ID_RE.findall(stripped)
        row_golds = set(GOLD_BASENAME_RE.findall(stripped))
        unknown = row_golds - all_canonical_golds
        if unknown:
            found.append(f"{label}: gold file(s) unknown to canonical mapping: {sorted(unknown)}")
        if not ids:
            continue
        row_canonical: set[str] = set()
        for terminal, num in ids:
            key = f"{terminal}-{num}"
            canonical = mapping.get(key)
            if canonical is None:
                found.append(f"{label}: PAGE-{key} missing from canonical 页型映射")
                continue
            row_canonical.update(canonical)
        if row_canonical:
            extra = row_golds - row_canonical
            if extra:
                found.append(
                    f"{label}: gold file(s) not in canonical mapping for this row: {sorted(extra)}"
                )
    return found


def validate_page_type_consistency(errors: list[str]) -> None:
    """②⑤⑥ quick-reference tables may list PAGE ids; they must exist in the canonical map.

    Gold filenames belong in reference-page-types.md. If a ⑥ row still names a
    ``*.html`` file, it must be a known canonical gold and belong to that PAGE.
    """
    mapping = parse_canonical_page_map(errors)
    if mapping is None:
        return
    all_canonical_golds: set[str] = set().union(*mapping.values())

    second_id_errors = prototype_quick_row_errors(
        mapping,
        all_canonical_golds,
        "| PAGE-MP-001 / PAGE-MP-999 | md-hero |\n",
    )
    if not any("PAGE-MP-999" in item for item in second_id_errors):
        fail(
            errors,
            "page-type gate missed a second illegal PAGE id on a prototype quick-ref row",
        )

    for skill_name in ("lny-prd-ui", "lny-prd-page", "lny-prd-prototype"):
        skill_text = (ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        if "reference-page-types.md" not in skill_text:
            fail(errors, f"{skill_name}/SKILL.md: missing canonical reference-page-types.md pointer")

    ui_quick = section_between((ROOT / "lny-prd-ui" / "SKILL.md").read_text(encoding="utf-8"), "## 页型速查", "## 开笔前")
    page_quick = section_between((ROOT / "lny-prd-page" / "SKILL.md").read_text(encoding="utf-8"), "## 页型速查", "## 开笔前")
    if ui_quick is None or page_quick is None:
        fail(errors, "lny-prd-ui/lny-prd-page SKILL.md: 页型速查 section missing")
    else:
        for label, quick in (("lny-prd-ui", ui_quick), ("lny-prd-page", page_quick)):
            for terminal, num in PAGE_ID_RE.findall(quick):
                if f"{terminal}-{num}" not in mapping:
                    fail(errors, f"{label}/SKILL.md 速查表: PAGE-{terminal}-{num} missing from canonical 页型映射")

    proto_quick = section_between((ROOT / "lny-prd-prototype" / "SKILL.md").read_text(encoding="utf-8"), "## 金样速查", "## 开笔前")
    if proto_quick is None:
        fail(errors, "lny-prd-prototype/SKILL.md: 金样速查 section missing")
        return
    for item in prototype_quick_row_errors(mapping, all_canonical_golds, proto_quick):
        fail(errors, item)


REPO_ROOT_REF_RE = re.compile(
    r"仓库\s*根?\s*[`「『(（]?\s*(?:README|LICENSE\b|skill-bundle\.json|CHANGELOG\.md|requirements[^\s`」』)）]*\.txt)",
    re.IGNORECASE,
)


def validate_skill_references(errors: list[str]) -> None:
    """Skill prose must not point at repository-root files that are never installed.

    Anchored on 仓库/仓库根 + root-file name so legitimate in-skill references
    (e.g. gold/README.md) and PRD-project wording ("PRD 仓库根目录") pass through.
    """
    for skill_dir in SKILL_DIRS:
        for path in sorted(skill_dir.rglob("*.md")):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), start=1):
                match = REPO_ROOT_REF_RE.search(line)
                if match:
                    rel = path.relative_to(ROOT).as_posix()
                    fail(
                        errors,
                        f"{rel}:{lineno}: references repository root file "
                        f"({match.group(0)!r}); repo-root files are not installed with the skill",
                    )


def validate_changelog(errors: list[str]) -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        fail(errors, "CHANGELOG.md missing at repository root")
        return
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## (\d+\.\d+\.\d+)\b", text, flags=re.M)
    if match is None:
        fail(errors, "CHANGELOG.md: no '## X.Y.Z' version section found")
        return
    manifest = json.loads((ROOT / "skill-bundle.json").read_text(encoding="utf-8"))
    version = manifest.get("bundle_version")
    if match.group(1) != version:
        fail(errors, f"CHANGELOG.md top version {match.group(1)!r} != skill-bundle.json bundle_version {version!r}")


def main() -> int:
    errors: list[str] = []
    validate_bundle_contract(errors)
    validate_skill_metadata(errors)
    validate_markdown_links(errors)
    validate_text_and_yaml(errors)
    validate_script_syntax(errors)
    validate_example_prototype_identity(errors)
    validate_kit_copies(errors)
    validate_page_type_consistency(errors)
    validate_changelog(errors)
    validate_skill_references(errors)
    validate_migration(errors)
    validate_artifact_path_checker(errors)
    validate_prototypes(errors)
    require_run(
        [sys.executable, str(PRD_SEMANTIC_TESTS), "-v"],
        errors,
        "PRD semantic validator tests",
    )
    require_run(
        [
            sys.executable,
            str(PRD_SEMANTIC_CHECKER),
            str(ROOT / "examples" / "mini-shop"),
            "--allow-fixture-status",
        ],
        errors,
        "mini-shop semantic validation",
    )
    require_run(
        [sys.executable, str(INSTALLER_TESTS), "-v"],
        errors,
        "atomic bundle installer tests",
    )
    if errors:
        print("skill package validation failed:", file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print(
        f"skill package validation ok: {len(SKILL_DIRS)} skills (10 core); bundle/version contract; "
        "runtime examples isolation; real YAML + quick validation; links; UTF-8; Python/JS; "
        "installer transactions; migration; artifact paths; semantic consistency; kit/gold; "
        "prototype identity; fixture + negative coverage"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
