# Kickoff prompt — paste this as the first message in your AI coding session

---

Read CLAUDE.md fully, then docs/PRD.md, docs/ARCHITECTURE.md, docs/PLAN.md, docs/VERIFICATION.md, and docs/EVALS.md.

Then, before writing any code:

1. Restate in at most 15 bullets what you are building, the ranked priorities, and the hard invariants.
2. List anything you find ambiguous, contradictory, or missing as questions. Do not start coding until I answer them.
3. Confirm the next slice from docs/PLAN.md, then execute ONLY that slice, following the definition of done in docs/VERIFICATION.md §5.

Standing reminders for every session:
- Thin slices, one branch per slice, evidence before claims.
- Use the QA agent (if available) before declaring any slice done.
- Update docs/PLAN.md (checkboxes + Current state) as the last act of the session.
- Ask before destructive operations (schema migrations, deletions, force-push).
- Verify the Stop hook actually fires during Phase 0 (deliberately failing test must block you).
