"""Interactive CLI — ask questions, generate project structure."""

import sys
from pathlib import Path

from scaffold.generator import build_context, generate_project
from scaffold.git import create_github_repo_and_push, has_gh_cli, has_git, init_and_commit
from scaffold.presets import get_preset, list_presets

PRESET_OPTIONS = list_presets()
AI_TOOL_OPTIONS: list[tuple[str, str]] = [
    ("claude", "Claude Code"),
    ("cursor", "Cursor"),
    ("windsurf", "Windsurf / Cascade"),
    ("all", "All of the above (generate configs for each)"),
]


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


def _display_name_for_key(key: str, options: list[tuple[str, str]]) -> str:
    """Look up display name for a given key in an options list."""
    for k, display in options:
        if k == key:
            return display
    return key


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


def _gather_inputs() -> dict[str, str]:
    """Collect all user inputs and return as a dict."""
    answers: dict[str, str] = {}
    answers["project_name"] = _ask("Project name", "my-project")
    answers["description"] = _ask("One-line description", "A new project")
    answers["owner_name"] = _ask("Your name", "Owner")
    answers["preset_key"] = _ask_choice("Which tech stack?", PRESET_OPTIONS)
    answers["ai_tool"] = _ask_choice("Which AI coding tool?", AI_TOOL_OPTIONS)
    answers["target_path"] = _ask(
        "Output directory",
        str(Path.cwd() / answers["project_name"].lower().replace(" ", "-")),
    )
    return answers


def _print_review(answers: dict[str, str]) -> None:
    """Print all answers for the user to review."""
    print()
    print("-" * 60)
    print("  Review your choices:")
    print("-" * 60)
    print(f"  1. Project name:    {answers['project_name']}")
    print(f"  2. Description:     {answers['description']}")
    print(f"  3. Your name:       {answers['owner_name']}")
    print(f"  4. Tech stack:      {_display_name_for_key(answers['preset_key'], PRESET_OPTIONS)}")
    print(f"  5. AI tool:         {_display_name_for_key(answers['ai_tool'], AI_TOOL_OPTIONS)}")
    print(f"  6. Output directory: {answers['target_path']}")
    print("-" * 60)


def _edit_answer(answers: dict[str, str], field_num: int) -> dict[str, str]:
    """Re-ask a single field and return updated answers."""
    if field_num == 1:
        answers["project_name"] = _ask("Project name", answers["project_name"])
        answers["target_path"] = _ask(
            "Output directory",
            str(Path.cwd() / answers["project_name"].lower().replace(" ", "-")),
        )
    elif field_num == 2:
        answers["description"] = _ask("One-line description", answers["description"])
    elif field_num == 3:
        answers["owner_name"] = _ask("Your name", answers["owner_name"])
    elif field_num == 4:
        answers["preset_key"] = _ask_choice("Which tech stack?", PRESET_OPTIONS)
    elif field_num == 5:
        answers["ai_tool"] = _ask_choice("Which AI coding tool?", AI_TOOL_OPTIONS)
    elif field_num == 6:
        answers["target_path"] = _ask("Output directory", answers["target_path"])
    return answers


def _confirm_loop(answers: dict[str, str]) -> dict[str, str]:
    """Show review, let user fix fields or confirm. Returns final answers."""
    while True:
        _print_review(answers)
        print()
        choice = _ask("Enter a number (1-6) to change, or 'y' to proceed", "y")
        if choice.lower() == "y":
            return answers
        if choice.isdigit() and 1 <= int(choice) <= 6:
            answers = _edit_answer(answers, int(choice))
        else:
            print("  Enter a number 1-6 to edit a field, or 'y' to confirm.")


def main() -> None:
    """Entry point for the CLI."""
    _print_banner()

    answers = _gather_inputs()
    answers = _confirm_loop(answers)

    preset = get_preset(answers["preset_key"])
    target = Path(answers["target_path"]).resolve()

    if target.exists() and any(target.iterdir()):
        confirm = _ask(f"Directory {target} is not empty. Continue? (y/n)", "n")
        if confirm.lower() != "y":
            print("Aborted.")
            sys.exit(0)

    # --- Generate ---
    print(f"\nGenerating project in {target} ...")
    context = build_context(
        project_name=answers["project_name"],
        description=answers["description"],
        preset=preset,
        ai_tool=answers["ai_tool"],
        owner_name=answers["owner_name"],
    )
    files = generate_project(target, context)
    _print_summary(target, files)

    # --- Git init ---
    if has_git():
        print("Setting up Git...")
        git_ok = init_and_commit(target, answers["project_name"])

        if git_ok and has_gh_cli():
            push = _ask("Create a GitHub repo and push? (y/n)", "y")
            if push.lower() == "y":
                visibility = _ask("Repo visibility — private or public? (private/public)", "private")
                slug = answers["project_name"].lower().replace(" ", "-")
                create_github_repo_and_push(
                    target=target,
                    project_slug=slug,
                    description=answers["description"],
                    private=(visibility.lower() != "public"),
                )
        elif git_ok:
            print("  GitHub CLI (gh) not found — skipping remote creation.")
            print("  You can push manually: gh repo create <name> --source . --push")
    else:
        print("  Git not found — skipping repo initialization.")


if __name__ == "__main__":
    main()
