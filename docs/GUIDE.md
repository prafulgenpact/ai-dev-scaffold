# The Complete Guide to Disciplined AI-Assisted Development

> **Who this is for:** Anyone building software with AI coding assistants (Claude Code, Cursor, Windsurf, GitHub Copilot, etc.). No prior knowledge of engineering methodology is assumed. Every concept is explained from scratch.

> **What you'll learn:** How to structure a project so that AI assistants produce reliable, high-quality code — and how to prevent the two most common failure modes: **context rot** and **doom loops**.

---

## Table of Contents

1. [Foundations — The Tools You Need to Know](#part-1-foundations)
2. [The Problem — Why AI-Assisted Coding Goes Wrong](#part-2-the-problem)
3. [The Solution — Documents as Executable Contracts](#part-3-the-solution)
4. [The Documents — What Each One Does](#part-4-the-documents)
5. [Planning — Why Sequence Matters More Than Speed](#part-5-planning)
6. [Execution — Mechanical Gates, Not Willpower](#part-6-execution)
7. [Enforcement — How the AI Is Forced to Follow the Rules](#part-7-enforcement)
8. [Deviation Detection — The Owner's Watchlist](#part-8-deviation-detection)
9. [Determinism — Making Development Reproducible](#part-9-determinism)
10. [Using the Scaffold Tool](#part-10-using-the-scaffold-tool)

---

## Part 1: Foundations

Before we talk about methodology, let's make sure we share a common vocabulary. If you already know these concepts, skip to Part 2.

### What is Git?

**Git** is a version control system. Think of it as an "infinite undo" for your entire project.

Every time you save a meaningful change (called a **commit**), Git takes a snapshot of every file in your project. You can go back to any snapshot at any time. If something breaks, you can rewind to the last working version in seconds.

**Key concepts:**
- **Repository (repo):** Your project folder, tracked by Git
- **Commit:** A saved snapshot with a message describing what changed
- **Branch:** A parallel copy of your project where you can make changes without affecting the main version
- **Merge:** Combining changes from one branch into another
- **Revert:** Undoing a commit by creating a new commit that reverses the changes

**Why it matters for AI development:** AI assistants make many changes quickly. Without Git, a bad AI-generated change could destroy hours of work. With Git, you can always go back.

### What is a Linter?

A **linter** is a tool that reads your code and flags problems — *without running it*. It's like a spell-checker for code.

Examples of what a linter catches:
- Variables you created but never used (probably a typo)
- Code that can never be reached (dead code)
- Style inconsistencies (tabs vs spaces, missing commas)
- Importing a library you don't need

**Common linters:**
- **Ruff** (Python) — extremely fast, catches hundreds of issue types
- **ESLint** (JavaScript/TypeScript) — the standard JS linter

**Why it matters:** Linters catch bugs in milliseconds that would take minutes to debug at runtime. They are the cheapest, fastest check you can run.

### What is a Type Checker?

Most programming languages let you write code without specifying what *type* of data each variable holds. A type checker enforces this.

Example without types:
```python
def add(a, b):
    return a + b

add("hello", 5)  # Crashes at runtime — you can't add a string and a number
```

Example with types:
```python
def add(a: int, b: int) -> int:
    return a + b

add("hello", 5)  # Type checker catches this BEFORE you run it
```

**Common type checkers:**
- **Mypy** (Python)
- **tsc** (TypeScript) — TypeScript IS a type system for JavaScript

**Why it matters:** Type errors are one of the most common bugs AI assistants introduce. A type checker catches them instantly, before any test runs.

### What is a Test?

A **test** is code that checks whether your code works correctly. You write a test once, and it runs automatically every time you make a change.

```python
def add(a, b):
    return a + b

# This is a test:
def test_add():
    assert add(2, 3) == 5      # Should be 5
    assert add(-1, 1) == 0     # Should be 0
    assert add(0, 0) == 0      # Should be 0
```

If someone (or an AI) accidentally changes `add` to subtract, the test fails immediately.

**Types of tests (from fastest to most thorough):**
- **Unit tests** — test one function in isolation. Very fast (~seconds).
- **Integration tests** — test multiple components working together (~seconds).
- **End-to-end (E2E) tests** — test the entire application as a user would (~minutes).

**Common test runners:**
- **Pytest** (Python) — the standard Python test framework
- **Vitest** (JavaScript/TypeScript) — fast, modern JS test framework
- **Playwright** — automates a real browser for E2E testing

**Why it matters:** Tests are your safety net. When an AI changes code, tests tell you immediately if something broke. Without tests, you won't know until a user finds the bug.

### What is a Pre-commit Hook?

A **hook** is code that runs automatically at a specific point in your workflow. A **pre-commit hook** runs every time you try to save a Git commit.

Example: You set up a pre-commit hook that runs the linter. Now, every time you (or the AI) commit code, the linter checks it first. If there are lint errors, the commit is blocked. You cannot save broken code.

**Why it matters:** Hooks turn "please remember to lint" into "you physically cannot commit without linting." This is the difference between a suggestion and an enforcement.

### What is an API?

An **API** (Application Programming Interface) is a way for two programs to talk to each other. When your web browser loads a webpage, it's calling the website's API.

In web development, an API typically means:
- Your **frontend** (what the user sees — the website) sends a request to your **backend** (the server that does the work)
- The backend processes the request and sends back a response
- The response contains data (usually in JSON format)

Example:
```
Frontend: "Hey backend, give me all blog posts"
  → GET /api/posts
Backend: "Here are 10 posts"
  → [{"title": "Hello World", "date": "2024-01-01"}, ...]
```

### What is an Environment Variable (.env)?

An **environment variable** is a piece of configuration that lives *outside* your code. You store them in a `.env` file, which is never committed to Git.

```
# .env file — NEVER commit this to Git
API_KEY=sk-abc123def456
DATABASE_URL=sqlite:///data/app.db
PORT=8000
```

**Why it matters:** API keys are secrets. If they get into Git, anyone with access to your repo can use (and abuse) them. The `.env` file keeps secrets out of code.

---

## Part 2: The Problem — Why AI-Assisted Coding Goes Wrong

AI coding assistants are remarkably capable. They can write entire features, fix bugs, refactor code, and even set up projects from scratch. But they have two fundamental failure modes that, if left unchecked, will waste more time than they save.

### Context Rot

**Context rot** is the gradual loss of project understanding over time.

Here's how it happens:
1. **Session 1:** You and the AI discuss the architecture. You decide on SQLite for the database, FastAPI for the backend, and agree that user authentication is out of scope for v1. The AI writes great code.
2. **Session 2:** The AI starts fresh — it has no memory of Session 1. It reads your code and makes assumptions. Maybe it adds a PostgreSQL migration because "that's more scalable." Maybe it starts building a login page because "most apps need one."
3. **Session 5:** The project is a mess. Some code assumes SQLite, some assumes PostgreSQL. There's a half-built auth system nobody asked for. The AI is confused by the inconsistencies it created.

**The root cause:** Decisions were made in conversation but never written down. Each new session starts from scratch and re-discovers (or contradicts) old decisions.

### Doom Loops

A **doom loop** is a cycle where fixing one thing breaks another, and the fix for that breaks the original:

```
Bug found → Fix attempt → New bug introduced → Fix that → Original bug returns → ...
```

Here's a real example:
1. AI writes a feature. Tests pass.
2. You notice a bug in the UI. You describe it to the AI.
3. The AI "fixes" the bug by changing a function. But it doesn't understand *why* the function was written that way.
4. The fix breaks two other features. The AI tries to fix those.
5. Those fixes break the original feature. You're back where you started — but now the code is more complex.
6. After 3 hours, you have more bugs than when you started.

**The root cause:** The AI treats symptoms instead of root causes. It makes large, interconnected changes. It weakens tests to get a "passing" result instead of fixing the actual bug.

### Why These Problems Are Worse with AI

Human developers also suffer from context rot and doom loops. But AI makes them worse because:

1. **No memory between sessions.** A human developer remembers yesterday's decisions. An AI starts completely fresh.
2. **Confident hallucination.** An AI will confidently invent an API endpoint that doesn't exist, a database column that was never created, or a library function with the wrong signature.
3. **Pressure to be "helpful."** AI assistants want to produce output. They will write code even when the right answer is "I need to read the docs first."
4. **Speed amplifies mistakes.** An AI can introduce 50 changes in a minute. Without guardrails, that's 50 potential bugs in a minute.

---

## Part 3: The Solution — Documents as Executable Contracts

The solution is not "use AI less" — it is **structure the project so the AI cannot go wrong easily.**

Most developers think of documentation as something you write *after* the code, for other people to read. In disciplined AI-assisted development, documentation is written *before* the code, and it serves as **executable contracts** — rules the AI must follow, boundaries it cannot cross, and criteria it must meet.

The key insight:

> **Documents, tests, and tools form a three-layer defense. Documents provide structure for *decisions*. Tests provide structure for *behavior*. Tools provide structure for *process*. When all three are in place and enforced mechanically, context rot and doom loops become structurally impossible — not just unlikely.**

### How This Works in Practice

Instead of telling the AI "please follow the architecture," you:
1. **Write the architecture in a document** the AI reads every session
2. **Write tests** that verify the code matches the architecture
3. **Use tools** (hooks, scripts) that prevent the AI from skipping the tests

The AI doesn't need to "remember" your architecture decisions. It re-reads them every session. It doesn't need to "try hard" to pass tests. The tests run automatically and block it from proceeding if they fail. It doesn't need "willpower" to follow the process. The process is enforced by tools it cannot bypass.

---

## Part 4: The Documents — What Each One Does

This scaffold generates 9 documents (plus AI tool configuration files). Each has a specific job, and removing any one creates a gap.

### 4.1 CLAUDE.md — The AI's Operating Manual

**What it is:** The first file the AI reads every session. Named `CLAUDE.md` because Claude Code reads it automatically from the project root — but it works as a context file for any AI tool.

**What goes in it:**
- A one-line description of the project
- Ranked priorities (when two goals conflict, which one wins?)
- Stack decisions (language, framework, database — so the AI doesn't change them)
- Hard invariants (rules that are NEVER violated, even if tests pass)
- Working rules (how to develop: thin slices, evidence before claims)
- Commands (how to run the dev server, how to run tests)
- A document map (pointers to every other document)

**Why it matters:** Without this file, every AI session starts from zero. With it, the AI begins every session already knowing the project's boundaries, rules, and decisions. It prevents context rot at the most fundamental level.

### 4.2 PRD.md — The "What & Why"

**PRD** stands for **Product Requirements Document**. It answers: What are we building? Why? What are we NOT building?

**Critical sections:**
- **Problem:** What problem does this project solve?
- **Priorities (ranked):** When two goals conflict, which wins? (e.g., "accuracy > speed")
- **Requirements:** Numbered, testable requirements (R1, R2, ...). Each traces to an acceptance test.
- **Non-goals:** What are we explicitly NOT building? This is the most important section for AI development — it prevents scope creep. If "mobile support" is a non-goal, the AI cannot add responsive design.
- **Success criteria:** How do we know the project is done? Concrete, testable.

**Why it matters:** The AI will happily add features you didn't ask for. The PRD, especially the non-goals section, is the fence that keeps scope under control.

### 4.3 ARCHITECTURE.md — The "How"

**What it is:** The technical blueprint. Components, data schemas, API contracts, key decisions.

**Why it matters:** Without this, the AI invents its own architecture — differently each session. With it, the AI has a single source of truth for "how things connect." When the AI proposes adding a new endpoint, you can check: is it in ARCHITECTURE.md? If not, discuss it first.

### 4.4 PLAN.md — The "When"

**What it is:** A phased build plan with thin slices (~30 min each), acceptance criteria per slice, and a "Current state" block that's updated every session.

**Why it matters:** This is the single source of truth for progress. The AI reads it to know: What phase are we in? What's the next slice? What are the acceptance criteria? Without this, the AI might re-implement something already done, skip ahead to a later phase, or work on the wrong thing entirely.

### 4.5 VERIFICATION.md — The "Proof"

**What it is:** The testing regime. What tests exist, how they're organized, what "done" means, and the mechanical gates that enforce it.

**Why it matters:** This document defines the contract between "the AI says it works" and "it actually works." Without it, the AI self-certifies quality — which is like grading your own exam.

### 4.6 EVALS.md — The "Accuracy"

**What it is:** How you measure whether the *outputs* are correct — not just whether the code runs. Tests verify the machine works; evals verify the outputs are right.

**Why it matters:** A search feature can pass all tests (it returns results, doesn't crash, renders correctly) but still be inaccurate (the results are wrong, irrelevant, or fabricated). Evals catch this.

### 4.7 OWNER_TODO.md — The "Blockers"

**What it is:** A list of things only the human can do. Prerequisites, blocking inputs, ongoing responsibilities.

**Why it matters:** It makes human dependencies explicit. The AI cannot fill in your API keys, write your test cases, or decide your success criteria. This document tells the AI: "Stop and ask me for this — do not invent it."

### 4.8 KICKOFF_PROMPT.md — The "Bootstrap"

**What it is:** The exact message you paste as the first message in every new AI coding session.

**It forces the AI to:**
1. Read ALL project documents
2. Restate in its own words what it's building (comprehension check)
3. List anything ambiguous or contradictory (catch stale docs)
4. Confirm the next slice before writing any code

**Why it matters:** Reading a document is not the same as understanding it. The "restate in your own words" step forces processing, not just scanning. The "list ambiguities" step surfaces stale information before it causes bugs.

### 4.9 QA Agent (qa.md)

**What it is:** Instructions for a separate QA agent that tests the builder's work.

**The builder/judge separation principle:** The session that wrote the code has the same blind spots that wrote the bug. A separate agent, with fresh context and no knowledge of HOW the code was written, tests it purely against the written criteria.

**Why it matters:** Without this, the builder AI grades its own work. With this, an independent agent tries to break it — and files evidence (screenshots, error logs) when it does.

---

## Part 5: Planning — Why Sequence Matters More Than Speed

### Phases

Instead of building everything at once, you build in **phases**. Each phase has a clear goal:

1. **Phase 0 — Guardrails.** Before writing any real code, set up linting, testing, the Stop hook, and pre-commit hooks. This ensures every future change is verified automatically.
2. **Phase 1 — Walking skeleton.** The thinnest possible end-to-end path. A "hello world" that crosses every layer (frontend → backend → database). This proves the architecture works.
3. **Phase 2+ — Features.** Each subsequent phase adds real functionality on top of the working skeleton.

**Why Phase 0 is mandatory:** If you skip guardrails, every future phase is unverified. Bugs accumulate silently. By the time you notice, the codebase is too tangled to fix. The 30 minutes spent on Phase 0 saves hours of debugging later.

### Thin Vertical Slices

A "slice" is NOT a horizontal layer ("build the database"). It is a **thin vertical cut** through ALL layers:

> "User can type a message and see a response" — not "build the API layer"

**Rules:**
- Each slice takes ~30 minutes of AI coding time
- Each slice produces a testable, demonstrable increment
- Each slice has written acceptance criteria BEFORE coding starts
- One Git branch per slice
- If a slice grows beyond 30 minutes, stop and split it

**Why this matters:**
- A 30-minute slice cannot waste hours
- If it breaks, you revert one small commit — not a week of work
- Each slice is small enough to review and verify
- You can demo progress after every slice

### Acceptance Criteria — Written Before Coding

Every slice has criteria written BEFORE the AI starts coding. Example:

> **Acceptance:** User types a task in the input box, presses Submit, sees a loading state, then sees the result rendered below. Console shows no errors. Refreshing the page does not lose the result.

This eliminates ambiguity about what "done" means. The AI cannot declare victory by passing tests alone — it must meet the written criteria, with evidence.

---

## Part 6: Execution — Mechanical Gates, Not Willpower

### The Testing Pyramid

Tests are organized in layers, from fastest to most thorough:

| Layer | Speed | What It Catches |
|-------|-------|-----------------|
| **Linting** | ~1 second | Style errors, unused variables, typos |
| **Type checking** | ~3 seconds | Type mismatches, wrong function signatures |
| **Unit tests** | ~5 seconds | Broken individual functions |
| **Integration tests** | ~10 seconds | Components that don't work together |
| **E2E tests** | ~30 seconds | Broken user journeys |
| **Exploratory QA** | ~2 minutes | Visual bugs, UX issues, edge cases |

**The key insight:** Each layer is faster and cheaper than the next. Most bugs die at linting or type checking. Some survive to unit tests. Very few make it to E2E. This is intentional — the cheapest check catches the most bugs.

### verify.sh — The Single Gate

Instead of running each tool separately, you have ONE script that runs everything:

```bash
scripts/verify.sh        # Full verification
scripts/verify.sh --hook  # Fast mode (used by Stop hook)
```

**Why a single script matters:**
- One command to remember, not five
- Same checks run locally, in hooks, in CI
- No "it passed on my machine" — same script everywhere
- Tolerant: skips suites that don't exist yet
- Strict: fails loudly on any existing failure

### The Stop Hook — The AI Cannot Say "Done" Without Proof

This is the most important enforcement mechanism.

**How it works:**
1. The AI finishes coding and tries to declare the task complete
2. The AI tool (Claude Code, etc.) automatically runs `verify.sh --hook`
3. If the script fails (exit code 2), the AI is **physically blocked** from completing
4. The AI must fix the failure and try again

**The AI cannot bypass this.** It is not a suggestion in a prompt — it is a system-level hook that executes regardless of what the AI "decides" to do.

**What the hook runs (fast mode):**
- Linting (catches style errors instantly)
- Type checking (catches type mismatches)
- Unit/integration tests (catches broken behavior)
- NOT E2E tests (those need live servers and would make the hook too slow)

### Tests Are Append-Only

A critical rule: **tests are never weakened, skipped, or deleted without explicit owner approval.**

Why? Because AI agents under pressure to get a "green" result will weaken tests instead of fixing bugs. Example:

```python
# Original test
def test_login():
    response = client.post("/login", json={"email": "test@test.com"})
    assert response.status_code == 200
    assert response.json()["token"] is not None  # Must return a token

# AI "fixes" the failing test by removing the assertion
def test_login():
    response = client.post("/login", json={"email": "test@test.com"})
    assert response.status_code == 200
    # Token assertion removed — test passes, but login is broken
```

The append-only rule makes this escape hatch unavailable. The AI must fix the bug, not the test.

### Pre-commit Hooks — Cannot Commit Broken Code

Every `git commit` automatically triggers:
1. **Linting** — catches style and code quality issues
2. **Secrets scanning (gitleaks)** — blocks commits containing API keys

The AI cannot commit code with lint errors or leaked secrets. Period.

---

## Part 7: Enforcement — How the AI Is Forced to Follow the Rules

The hardest problem is not "can the AI write code?" — it is "can you *constrain* the AI to write the *right* code?"

Left unconstrained, an AI assistant will:
- Invent endpoints that don't exist
- Skip tests to get green faster
- Ignore architectural decisions from earlier sessions
- Declare "done" without evidence

This scaffold uses a **5-layer enforcement chain** where each layer catches what the previous one misses:

### Layer 1: Automatic Context Loading

**What happens:** The AI tool reads `CLAUDE.md` from the project root at the start of every session. This is automatic — it's how Claude Code, Cursor rules, and Windsurf rules work.

**What it loads:** Stack decisions, hard invariants, working rules, document map.

**What it prevents:** Context rot. The AI re-reads the rules every session. It cannot "forget."

### Layer 2: Forced Comprehension (Kickoff Prompt)

**What happens:** The human pastes the kickoff prompt. The AI reads ALL documents and restates its understanding.

**What it prevents:** The AI building the wrong thing. Restating understanding forces processing, not just scanning.

### Layer 3: Runtime Gates (Stop Hook + Pre-commit)

**What happens:** Automated scripts run without human action. The Stop hook fires on every completion attempt. Pre-commit fires on every git commit.

**What it prevents:** Broken code being declared "done." The AI cannot skip verification — it's enforced by the tool infrastructure.

### Layer 4: Independent Verification (QA Agent)

**What happens:** A separate QA agent, with fresh context and no knowledge of the code's history, tests it against the written criteria.

**What it prevents:** Self-certified quality. The builder grades its own work with blind spots. The QA agent sees the system as a user would.

### Layer 5: Human Review (Owner as Final Gate)

**What happens:** Some decisions require human judgment: approving test changes, evaluating UX, deciding if a quality drop is acceptable.

**What it prevents:** The AI making irreversible decisions without oversight.

### Why All 5 Layers Are Needed

No single layer is sufficient:
- CLAUDE.md can be misinterpreted → Kickoff prompt catches it
- Kickoff prompt can be skipped → Stop hook still fires
- Stop hook doesn't catch UI bugs → QA agent does
- QA agent can't judge UX quality → Human review does
- Human review doesn't scale → Automated gates handle the routine checks

Together, they form a chain where every gap in one layer is covered by another.

---

## Part 8: Deviation Detection — The Owner's Watchlist

Even with 5 layers of enforcement, the AI can drift. The owner's job is not to read every line of code — it is to watch for **specific, observable signals** that indicate the process has a leak.

### The 10 Deviation Signals

**Signal 1: PLAN.md not updated.**
The AI declared a slice done but the "Current state" block is stale. First symptom of context rot.

**Signal 2: QA report missing or shallow.**
No new file in `qa/reports/` after a slice. Or the report has no screenshots, no findings table. Quality is self-certified.

**Signal 3: Test count decreased.**
Previous slice: 50 tests. This slice: 48. Two tests were removed. The AI weakened the safety net.

**Signal 4: Large diffs.**
A single commit touches 15+ files or 500+ lines. The AI abandoned slice discipline. Large changes are hard to review and easy to break.

**Signal 5: Invented information.**
The AI references an endpoint, schema, or library function that doesn't exist in the docs. Hallucination.

**Signal 6: Guardrail files modified.**
`.claude/settings.json`, `scripts/verify.sh`, or `.pre-commit-config.yaml` were changed. The AI is disabling its own guardrails.

**Signal 7: Prompt changes without quality check.**
Files that affect AI behavior were modified without evaluating the impact.

**Signal 8: Claims without evidence.**
The AI says "I tested this and it works" but the transcript shows no test output or screenshot.

**Signal 9: Documents contradicting each other.**
ARCHITECTURE.md says one thing, the code does another. Context rot in action.

**Signal 10: AI skipping the kickoff protocol.**
The AI immediately starts coding without reading docs. Layer 2 was bypassed.

### 5-Minute Post-Slice Checklist

After every slice, before approving:

| # | Check | How | Pass If |
|---|-------|-----|---------|
| 1 | verify.sh green | Read the transcript | "verify: PASS" visible |
| 2 | Test count stable | Note pytest count | Same or higher than last slice |
| 3 | QA report exists | `ls qa/reports/` | New file with evidence |
| 4 | PLAN.md updated | Open it | "Current state" matches work done |
| 5 | Diff is small | `git diff --stat` | ≤10 files, ≤300 lines |
| 6 | No guardrail edits | Check diff on hook/script files | Empty diff |

### Response Ladder

**Level 1 — Remind** (Signals 1, 8, 10): The AI forgot a step. "Update PLAN.md before I merge."

**Level 2 — Reject and Redo** (Signals 2, 4, 5, 7): The AI cut corners. "QA report is missing — run QA before I review."

**Level 3 — Revert and Investigate** (Signals 3, 6, 9): The AI compromised a guardrail. `git revert HEAD`. Then investigate why.

---

## Part 9: Determinism — Making Development Reproducible

**Determinism** means: given the same inputs, you always get the same outputs. In software development, this means two different AI sessions, working on the same project, should produce compatible results.

### How We Achieve It

| Level | How |
|-------|-----|
| **Dependencies** | Lock files (`uv.lock`, `package-lock.json`) pin exact versions. Two sessions get identical environments. |
| **Tests** | Mock external services. No test depends on network, time, or external state. |
| **Linting** | Config in project files — same rules everywhere. No "it passed on my machine." |
| **Verification** | `verify.sh` is the single entry point. Same command, same checks, same result. |
| **Documents** | The AI reads the same CLAUDE.md, PRD.md, PLAN.md every session. Same context = same decisions. |

### Why Determinism Matters for AI

When an AI assistant works on your codebase:
- It starts fresh each session (no memory of past sessions)
- It may interpret ambiguous requirements differently each time
- It may "fix" something that was working

Determinism counteracts all of these:
- **Documents** provide the same context every session
- **Tests** catch regressions regardless of who introduced them
- **Lock files** prevent "it worked yesterday" dependency issues

---

## Part 10: Using the Scaffold Tool

### Quick Start

```bash
# Clone the scaffold repo
git clone <repo-url> ai-dev-scaffold
cd ai-dev-scaffold

# Run the CLI
python -m scaffold.cli
```

The CLI will ask you:
1. **Project name** — what you're building
2. **Description** — one-line summary
3. **Your name** — for document headers
4. **Tech stack** — Python, Python+React, Node+React, or Node
5. **AI tool** — Claude Code, Cursor, Windsurf, or all
6. **Output directory** — where to generate the project

### What Gets Generated

```
your-project/
├── CLAUDE.md                    # AI operating manual (auto-read each session)
├── README.md                    # Project entry point
├── .gitignore                   # Standard ignores for your stack
├── .pre-commit-config.yaml      # Gitleaks secrets scanning
├── scripts/
│   └── verify.sh                # Single verification entry point (adapted to your stack)
├── docs/
│   ├── PRD.md                   # Requirements (fill in)
│   ├── ARCHITECTURE.md          # Technical design (fill in)
│   ├── PLAN.md                  # Build plan with Phase 0 pre-filled
│   ├── VERIFICATION.md          # Testing regime (pre-filled)
│   ├── EVALS.md                 # Accuracy measurement (fill in)
│   ├── OWNER_TODO.md            # Your prerequisites checklist
│   └── KICKOFF_PROMPT.md        # First message for AI sessions
├── qa/
│   └── reports/                 # QA evidence lands here
└── .claude/                     # (or .cursorrules / .windsurfrules)
    ├── settings.json            # Stop hook configuration
    └── agents/
        └── qa.md                # QA agent instructions
```

### After Generation

1. **Complete `docs/OWNER_TODO.md`** — install prerequisites, create `.env`, set up Git remote
2. **Fill in `docs/PRD.md`** — your requirements, priorities, non-goals, success criteria
3. **Fill in `docs/ARCHITECTURE.md`** — components, schemas, API contracts
4. **Fill in `docs/PLAN.md`** — your phased build plan (Phase 0 is pre-filled)
5. **Start your first AI session** — paste `docs/KICKOFF_PROMPT.md` as the first message

### The First Session (Phase 0)

Your first AI session should establish the guardrails:
1. AI reads all docs, restates understanding, asks questions
2. AI sets up the project skeleton (package manager, basic structure)
3. AI hardens `verify.sh` and proves the Stop hook works (deliberately failing test must block)
4. AI sets up pre-commit hooks (linter + gitleaks)
5. After Phase 0, every future change is automatically verified

**This is the single most important session.** Once the guardrails are in place, every future session benefits from them. Skipping Phase 0 is like driving without a seatbelt — you might be fine for a while, but when something goes wrong, it goes very wrong.
