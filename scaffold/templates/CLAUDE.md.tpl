# {{PROJECT_NAME}} — AI Agent Context

{{DESCRIPTION}}

* Remember to speak to me in direct, simple and concise language. No jargons, no complicated answers.

## Priorities (ranked — when in conflict, higher wins)
1. Accuracy of outputs (enforced by evals + review, not just tests)
2. User experience
3. Verification at every slice (docs/VERIFICATION.md)
4. No doom loops (thin slices, QA agent, mechanical gates)
5. Traceability / auditability

## Stack (decided — do not relitigate without updating docs/PRD.md)
<!-- OWNER: Fill in your actual technology choices below -->
- Language: {{LANGUAGE}}
- Package manager: {{PACKAGE_MANAGER}}
- Linter: {{LINTER}}
- Type checker: {{TYPE_CHECKER}}
- Test runner: {{TEST_RUNNER}}
- Formatter: {{FORMATTER}}

## Hard invariants (violating any of these is a bug, even if all tests pass)
1. Every design decision is documented before implementation begins.
2. Tests are append-only. Never weaken, skip, or delete a test without explicit owner approval.
3. Every slice has written acceptance criteria BEFORE coding starts.
4. Secrets never enter the repo. The .env file is gitignored; gitleaks blocks leaks in pre-commit.
5. Evidence or it didn't happen. Never claim something works without test output or a screenshot.

## Working rules
- Thin vertical slices (~30 min of work each). One git branch per slice. Merge only on green `scripts/verify.sh` + QA sign-off.
- Definition of done for any slice: verify.sh green + slice acceptance criteria (docs/PLAN.md) met + QA agent pass with evidence + PLAN.md checkboxes and "Current state" updated.
- Test files are append-only. Never weaken, skip, or delete an assertion without explicit owner approval in the session transcript.
- Never claim something works without having run it. Evidence (test output, screenshot) or it didn't happen.
- Ask before destructive operations (schema migrations, deletions, force-push).

## Commands
- `scripts/verify.sh` — single verification entry point: lint, typecheck, tests. `--hook` flag = Stop-hook mode (exit 2 on failure).
<!-- OWNER: Add your dev server commands, database commands, etc. below -->

## Map
- docs/PRD.md — what & why, requirements, non-goals, success criteria
- docs/ARCHITECTURE.md — components, schemas, contracts, execution semantics
- docs/PLAN.md — phased build plan with acceptance criteria + current state (update every session)
- docs/VERIFICATION.md — testing regime, QA protocol, doom-loop countermeasures
- docs/EVALS.md — accuracy measurement: golden tasks, rubrics, trigger policy
- docs/OWNER_TODO.md — what the owner must supply, and what blocks on it
