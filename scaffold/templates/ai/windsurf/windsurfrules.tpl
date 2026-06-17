# {{PROJECT_NAME}} — Windsurf / Cascade Rules

## Context
{{DESCRIPTION}}

## Mandatory Reading (before ANY code changes)
Read these files in order before starting work:
1. CLAUDE.md (project context, priorities, invariants, rules)
2. docs/PRD.md (requirements and non-goals)
3. docs/ARCHITECTURE.md (technical design)
4. docs/PLAN.md (current phase, next slice, acceptance criteria)
5. docs/VERIFICATION.md (testing regime, definition of done)

## Hard Rules
- Thin vertical slices (~30 min). One git branch per slice.
- Never start coding without reading docs/PLAN.md first.
- Never claim "done" without running scripts/verify.sh and showing the output.
- Tests are append-only. Never weaken, skip, or delete a test without explicit owner approval.
- Evidence or it didn't happen. Show test output or screenshots as proof.
- Ask before destructive operations (schema migrations, deletions, force-push).
- Update docs/PLAN.md (checkboxes + Current state) after completing each slice.

## Definition of Done (every slice)
1. scripts/verify.sh green
2. Slice acceptance criteria from docs/PLAN.md demonstrably met
3. QA evidence in qa/reports/
4. PLAN.md updated

## Verification Command
```bash
scripts/verify.sh        # Full: lint + typecheck + tests
scripts/verify.sh --hook  # Fast mode: lint + typecheck + unit tests only
```
