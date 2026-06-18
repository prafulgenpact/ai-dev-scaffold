"""Git + GitHub operations — init, commit, create remote, push."""

import shutil
import subprocess
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a command in the target directory and return the result."""
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=60, check=False,
    )


def has_git() -> bool:
    """Check if git is available on PATH."""
    return shutil.which("git") is not None


def has_gh_cli() -> bool:
    """Check if GitHub CLI (gh) is installed and authenticated."""
    if not shutil.which("gh"):
        return False
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True, text=True, timeout=10, check=False,
    )
    return result.returncode == 0


def init_and_commit(target: Path, project_name: str) -> bool:
    """Initialize a git repo and make the initial commit. Returns True on success."""
    result = _run(["git", "init"], cwd=target)
    if result.returncode != 0:
        print(f"  git init failed: {result.stderr.strip()}")
        return False

    _run(["git", "add", "-A"], cwd=target)

    result = _run(
        ["git", "commit", "-m", f"Initial commit: {project_name} scaffolded by ai-dev-scaffold"],
        cwd=target,
    )
    if result.returncode != 0:
        print(f"  git commit failed: {result.stderr.strip()}")
        return False

    print("  Git repo initialized with initial commit.")
    return True


def create_github_repo_and_push(
    target: Path,
    project_slug: str,
    description: str,
    private: bool = True,
) -> bool:
    """Create a GitHub repo with gh CLI and push. Returns True on success."""
    visibility = "--private" if private else "--public"
    result = _run(
        [
            "gh", "repo", "create", project_slug,
            visibility,
            "--source", ".",
            "--remote", "origin",
            "--push",
            "--description", description,
        ],
        cwd=target,
    )
    if result.returncode != 0:
        print(f"  GitHub repo creation failed: {result.stderr.strip()}")
        return False

    for line in result.stdout.strip().splitlines():
        if "github.com" in line:
            print(f"  GitHub repo: {line.strip()}")
            break

    print("  Code pushed to GitHub.")
    return True
