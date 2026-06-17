"""File generator — reads templates, fills placeholders, writes to target directory."""

from pathlib import Path

from scaffold.presets import Preset


TEMPLATE_DIR = Path(__file__).parent / "templates"


def _fill(template_text: str, context: dict[str, str]) -> str:
    """Replace {{KEY}} placeholders with values from context."""
    result = template_text
    for key, value in context.items():
        result = result.replace("{{" + key + "}}", value)
    return result


def _read_template(relative_path: str) -> str:
    """Read a .tpl file from the templates directory."""
    return (TEMPLATE_DIR / relative_path).read_text()


def _write_file(target_dir: Path, relative_path: str, content: str) -> Path:
    """Write content to target_dir/relative_path, creating parents as needed."""
    out = target_dir / relative_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)
    return out


def _make_executable(path: Path) -> None:
    """Set the executable bit on a file."""
    path.chmod(path.stat().st_mode | 0o111)


def build_context(
    project_name: str,
    description: str,
    preset: Preset,
    ai_tool: str,
    owner_name: str,
) -> dict[str, str]:
    """Build the template substitution context from user inputs."""
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": project_name.lower().replace(" ", "-").replace("_", "-"),
        "DESCRIPTION": description,
        "OWNER_NAME": owner_name,
        "PRESET_NAME": preset.name,
        "PRESET_DISPLAY": preset.display,
        "LANGUAGE": preset.language,
        "PACKAGE_MANAGER": preset.package_manager,
        "LINTER": preset.linter,
        "TYPE_CHECKER": preset.type_checker,
        "TEST_RUNNER": preset.test_runner,
        "FORMATTER": preset.formatter,
        "HAS_FRONTEND": "yes" if preset.has_frontend else "no",
        "FRONTEND_FRAMEWORK": preset.frontend_framework,
        "CSS_FRAMEWORK": preset.css_framework,
        "FRONTEND_BUILD_TOOL": preset.frontend_build_tool,
        "FRONTEND_TYPE_CHECKER": preset.frontend_type_checker,
        "AI_TOOL": ai_tool,
        "EXTRA_TOOLS": ", ".join(preset.extra_tools) if preset.extra_tools else "none",
    }


def generate_project(target_dir: Path, context: dict[str, str]) -> list[str]:
    """Generate all project files. Returns list of created file paths (relative)."""
    created: list[str] = []
    preset_name = context["PRESET_NAME"]
    ai_tool = context["AI_TOOL"]

    # --- Documentation ---
    doc_templates = [
        "docs/PRD.md.tpl",
        "docs/ARCHITECTURE.md.tpl",
        "docs/PLAN.md.tpl",
        "docs/VERIFICATION.md.tpl",
        "docs/EVALS.md.tpl",
        "docs/OWNER_TODO.md.tpl",
        "docs/KICKOFF_PROMPT.md.tpl",
    ]
    for tpl_path in doc_templates:
        content = _fill(_read_template(tpl_path), context)
        out_path = tpl_path.replace(".tpl", "")
        _write_file(target_dir, out_path, content)
        created.append(out_path)

    # --- Root files ---
    for tpl in ["CLAUDE.md.tpl", "README.md.tpl"]:
        content = _fill(_read_template(tpl), context)
        _write_file(target_dir, tpl.replace(".tpl", ""), content)
        created.append(tpl.replace(".tpl", ""))

    # --- verify.sh (stack-specific) ---
    verify_tpl = f"scripts/verify-{preset_name}.sh.tpl"
    if not (TEMPLATE_DIR / verify_tpl).exists():
        verify_tpl = f"scripts/verify-{context['LANGUAGE']}.sh.tpl"
    content = _fill(_read_template(verify_tpl), context)
    out = _write_file(target_dir, "scripts/verify.sh", content)
    _make_executable(out)
    created.append("scripts/verify.sh")

    # --- Pre-commit config ---
    content = _fill(_read_template("pre-commit-config.yaml.tpl"), context)
    _write_file(target_dir, ".pre-commit-config.yaml", content)
    created.append(".pre-commit-config.yaml")

    # --- AI tool configuration ---
    if ai_tool in ("claude", "all"):
        content = _fill(_read_template("ai/claude/settings.json.tpl"), context)
        _write_file(target_dir, ".claude/settings.json", content)
        created.append(".claude/settings.json")

        content = _fill(_read_template("ai/claude/agents/qa.md.tpl"), context)
        _write_file(target_dir, ".claude/agents/qa.md", content)
        created.append(".claude/agents/qa.md")

    if ai_tool in ("cursor", "all"):
        content = _fill(_read_template("ai/cursor/cursorrules.tpl"), context)
        _write_file(target_dir, ".cursorrules", content)
        created.append(".cursorrules")

    if ai_tool in ("windsurf", "all"):
        content = _fill(_read_template("ai/windsurf/windsurfrules.tpl"), context)
        _write_file(target_dir, ".windsurfrules", content)
        created.append(".windsurfrules")

    # --- QA reports directory ---
    (target_dir / "qa" / "reports").mkdir(parents=True, exist_ok=True)
    _write_file(target_dir, "qa/reports/.gitkeep", "")
    created.append("qa/reports/.gitkeep")

    # --- .gitignore ---
    content = _fill(_read_template("gitignore.tpl"), context)
    _write_file(target_dir, ".gitignore", content)
    created.append(".gitignore")

    return created
