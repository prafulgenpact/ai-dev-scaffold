"""Stack presets — each preset defines tools, linters, test runners, and verify.sh commands."""

from dataclasses import dataclass, field


@dataclass
class Preset:
    name: str
    display: str
    language: str
    package_manager: str
    linter: str
    type_checker: str
    test_runner: str
    formatter: str
    extra_tools: list[str] = field(default_factory=list)
    has_frontend: bool = False
    frontend_framework: str = ""
    css_framework: str = ""
    frontend_build_tool: str = ""
    frontend_type_checker: str = ""


PRESETS: dict[str, Preset] = {
    "python": Preset(
        name="python",
        display="Python (FastAPI / Flask / CLI)",
        language="python",
        package_manager="uv",
        linter="ruff",
        type_checker="mypy",
        test_runner="pytest",
        formatter="ruff format",
    ),
    "python-react": Preset(
        name="python-react",
        display="Python backend + React/TypeScript frontend",
        language="python",
        package_manager="uv",
        linter="ruff",
        type_checker="mypy",
        test_runner="pytest",
        formatter="ruff format",
        has_frontend=True,
        frontend_framework="react",
        css_framework="tailwindcss",
        frontend_build_tool="vite",
        frontend_type_checker="tsc",
        extra_tools=["playwright"],
    ),
    "node-react": Preset(
        name="node-react",
        display="Node.js backend + React/TypeScript frontend",
        language="node",
        package_manager="npm",
        linter="eslint",
        type_checker="tsc",
        test_runner="vitest",
        formatter="prettier",
        has_frontend=True,
        frontend_framework="react",
        css_framework="tailwindcss",
        frontend_build_tool="vite",
        frontend_type_checker="tsc",
        extra_tools=["playwright"],
    ),
    "node": Preset(
        name="node",
        display="Node.js / Express / CLI (TypeScript)",
        language="node",
        package_manager="npm",
        linter="eslint",
        type_checker="tsc",
        test_runner="vitest",
        formatter="prettier",
    ),
}


def list_presets() -> list[tuple[str, str]]:
    """Return (key, display_name) pairs for all presets."""
    return [(k, v.display) for k, v in PRESETS.items()]


def get_preset(key: str) -> Preset:
    """Look up a preset by key. Raises KeyError if not found."""
    return PRESETS[key]
