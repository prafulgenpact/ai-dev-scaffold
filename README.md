# AI Dev Scaffold

**Disciplined project structure for AI-assisted development.**

A CLI tool + template repo that generates everything you need to build software with AI coding assistants (Claude Code, Cursor, Windsurf) — without falling into context rot or doom loops.

## What It Does

Run the CLI, answer 5 questions, get a fully structured project with:

- **9 document templates** — PRD, Architecture, Plan, Verification, Evals, Owner TODO, Kickoff Prompt, AI Operating Manual, README
- **verify.sh** — single verification script adapted to your stack (Python, React, Node.js)
- **Stop hook** — blocks the AI from declaring "done" without passing verification
- **QA agent** — independent agent that tests the builder's work with fresh eyes
- **Pre-commit hooks** — linting + secrets scanning on every commit
- **AI tool configs** — Claude Code, Cursor, and/or Windsurf rules

## Quick Start

```bash
git clone <repo-url>
cd ai-dev-scaffold
python -m scaffold.cli
```

The CLI asks:
1. Project name
2. One-line description
3. Your name
4. Tech stack preset (Python · Python+React · Node+React · Node)
5. AI tool (Claude Code · Cursor · Windsurf · All)
6. Output directory

Then generates all files, ready to go.

## What Gets Generated

```
your-project/
├── CLAUDE.md                    # AI reads this every session
├── README.md
├── .gitignore
├── .pre-commit-config.yaml      # Gitleaks secrets scanning
├── scripts/verify.sh            # Single gate: lint + typecheck + tests
├── docs/
│   ├── PRD.md                   # Requirements + non-goals (fill in)
│   ├── ARCHITECTURE.md          # Technical design (fill in)
│   ├── PLAN.md                  # Build plan (Phase 0 pre-filled)
│   ├── VERIFICATION.md          # Testing regime (pre-filled)
│   ├── EVALS.md                 # Accuracy measurement (fill in)
│   ├── OWNER_TODO.md            # Your prerequisites checklist
│   └── KICKOFF_PROMPT.md        # First message for AI sessions
├── qa/reports/                  # QA evidence goes here
└── .claude/ (or .cursorrules)   # AI tool configuration + Stop hook
```

## Supported Stacks

| Preset | Linter | Type Checker | Tests | Extra |
|--------|--------|-------------|-------|-------|
| **Python** | Ruff | Mypy | Pytest | — |
| **Python + React** | Ruff + tsc | Mypy + tsc | Pytest | Playwright, Tailwind |
| **Node + React** | ESLint + tsc | tsc | Vitest | Playwright, Tailwind |
| **Node** | ESLint | tsc | Vitest | — |

## Supported AI Tools

| Tool | Config File | Stop Hook | QA Agent |
|------|------------|-----------|----------|
| **Claude Code** | `.claude/settings.json` | ✅ Native | ✅ `.claude/agents/qa.md` |
| **Cursor** | `.cursorrules` | Manual (run verify.sh) | Manual |
| **Windsurf** | `.windsurfrules` | Manual (run verify.sh) | Manual |

> **Note:** Only Claude Code currently supports native Stop hooks (automatic verification on task completion). For Cursor and Windsurf, the rules file instructs the AI to run `verify.sh` manually — but it's a prompt instruction, not a mechanical gate.

## Learn the Methodology

Read **[docs/GUIDE.md](docs/GUIDE.md)** — a comprehensive, beginner-friendly guide that explains every concept from scratch:

- What Git, linters, type checkers, and tests are
- What context rot and doom loops are
- How documents prevent them
- How the 5-layer enforcement chain works
- How to detect AI deviation
- How to use the scaffold tool

No prior knowledge assumed.

## Philosophy

Three principles drive this tool:

1. **Enforcement is mechanical, not aspirational.** Rules enforced by tools (hooks, scripts, gates) beat rules that depend on the AI "remembering."
2. **Documents are contracts, not chores.** Written before code, read every session, enforced by tests.
3. **Thin slices prevent doom loops.** Small changes (~30 min) can't cascade far. If something breaks, revert one commit.
