# Build Plan — {{PROJECT_NAME}}

> Update rules (AI agent): work one slice at a time, one branch per slice.
> After each session, update checkboxes AND the Current state block. Never
> start a phase whose blocker is unmet — say so instead.

## Current state
- Done: <!-- List completed phases/slices -->
- Phase: 0 (guardrails) — in progress
- Next: slice 0.1
- Blockers for later phases: <!-- List any blocking items -->

---

## Phase 0 — Repo & guardrails
Goal: Verification pipeline works. Stop hook blocks on failure. Pre-commit catches lint and secrets.
- [ ] 0.1 — Project scaffolding: package manager setup, dev server, basic structure
- [ ] 0.2 — verify.sh hardened + Stop hook PROVEN (deliberately failing test must block)
- [ ] 0.3 — Pre-commit hooks: linter + secrets scanner (gitleaks)
- **Acceptance:** verify.sh runs all checks; Stop hook blocks AI on failure (proven with deliberate fail); pre-commit blocks dirty commits.

## Phase 1 — Walking skeleton
Goal: The thinnest possible end-to-end path that proves the architecture works.
- [ ] 1.1 — <!-- First slice: smallest thing that crosses all layers -->
- [ ] 1.2 — <!-- Second slice -->
- **Acceptance:** <!-- What does "done" look like? Be specific. -->

## Phase 2 — Core features
Goal: <!-- The main functionality that makes the project useful -->
- [ ] 2.1 — <!-- Slice -->
- **Acceptance:** <!-- Criteria -->

<!-- Add more phases as needed. Each phase should have:
     1. A clear goal
     2. Slices (thin vertical cuts, ~30 min each)
     3. Written acceptance criteria BEFORE coding starts
     4. Any blockers listed -->
