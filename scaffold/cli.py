"""Interactive CLI — ask questions, generate project structure."""

import sys
from pathlib import Path

from scaffold.generator import build_context, generate_project
from scaffold.presets import get_preset, list_presets


def _ask(prompt: str, default: str = "") -> str:
    """Prompt the user for input with an optional default."""
    suffix = f" [{default}]" if default else ""
    answer = input(f"{prompt}{suffix}: ").strip()
    return answer if answer else default


def _ask_choice(prompt: str, options: list[tuple[str, str]]) -> str:
    """Prompt the user to pick from numbered options. Returns the key."""
    print(f"\n{prompt}")
    for i, (key, display) in enumerate(options, 1):
        print(f"  {i}. {display}")
    while True:
        raw = input("Enter number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print(f"  Please enter a number between 1 and {len(options)}.")


def _print_banner() -> None:
    """Print the welcome banner."""
    print()
    print("=" * 60)
    print("  AI Dev Scaffold")
    print("  Disciplined project structure for AI-assisted development")
    print("=" * 60)
    print()


def _print_summary(target: Path, files: list[str]) -> None:
    """Print what was created."""
    print()
    print("-" * 60)
    print(f"  Created {len(files)} files in: {target}")
    print("-" * 60)
    for f in sorted(files):
        print(f"    {f}")
    print()
    print("Next steps:")
    print(f"  1. cd {target}")
    print("  2. Open docs/OWNER_TODO.md and complete the prerequisites")
    print("  3. Fill in docs/PRD.md with your requirements")
    print("  4. Fill in docs/ARCHITECTURE.md with your technical design")
    print("  5. Fill in docs/PLAN.md with your phased build plan")
    print("  6. Read docs/GUIDE.md for the full methodology explanation")
    print()
    print("To start your first AI coding session:")
    print("  - Paste the contents of docs/KICKOFF_PROMPT.md as your first message")
    print()


def main() -> None:
    """Entry point for the CLI."""
    _print_banner()

    # --- Gather inputs ---
    project_name = _ask("Project name", "my-project")
    description = _ask("One-line description", "A new project")
    owner_name = _ask("Your name", "Owner")

    preset_key = _ask_choice(
        "Which tech stack?",
        list_presets(),
    )
    preset = get_preset(preset_key)

    ai_tool = _ask_choice(
        "Which AI coding tool?",
        [
            ("claude", "Claude Code"),
            ("cursor", "Cursor"),
            ("windsurf", "Windsurf / Cascade"),
            ("all", "All of the above (generate configs for each)"),
        ],
    )

    target_path = _ask(
        "Output directory",
        str(Path.cwd() / project_name.lower().replace(" ", "-")),
    )
    target = Path(target_path).resolve()

    if target.exists() and any(target.iterdir()):
        confirm = _ask(f"Directory {target} is not empty. Continue? (y/n)", "n")
        if confirm.lower() != "y":
            print("Aborted.")
            sys.exit(0)

    # --- Generate ---
    print(f"\nGenerating project in {target} ...")
    context = build_context(
        project_name=project_name,
        description=description,
        preset=preset,
        ai_tool=ai_tool,
        owner_name=owner_name,
    )
    files = generate_project(target, context)
    _print_summary(target, files)


if __name__ == "__main__":
    main()
