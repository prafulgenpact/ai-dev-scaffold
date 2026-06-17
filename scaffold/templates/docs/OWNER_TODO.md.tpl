# Owner TODO — what only you can do

Ordered. Complete items 1–4 before the first AI coding session.

## Before the first session
1. **Install prerequisites:** git, {{PACKAGE_MANAGER}}, {{LINTER}}. For AI: install your chosen AI coding tool.
2. **Create `.env`** from `.env.example` and fill in any API keys, model IDs, or configuration. Never commit it.
3. **Create a private GitHub repo** and add it as remote — your backup and revert point.
4. **Fill in `docs/PRD.md`** — requirements, priorities, non-goals, success criteria. This is the foundation.

## Blocking inputs (the build stalls without these)
5. **Fill in `docs/ARCHITECTURE.md`** — components, schemas, API contracts, key decisions. ⛔ Blocks Phase 1.
6. **Write acceptance criteria** for each slice in `docs/PLAN.md` BEFORE the slice begins. ⛔ Blocks every slice.
7. **Fill the rubric blanks** in `docs/EVALS.md` — what "accurate" means for each output type. ⛔ Blocks eval phase.

## Ongoing role (you are the final gate, not the test harness)
- Per merged slice: skim the QA report in `qa/reports/` (verdict + evidence), then do a 10-minute hands-on pass.
- Approve or reject any request to weaken/skip a test — that rule only works if you actually enforce it.
- When quality scores drop, demand the explanation before allowing the merge.

## Kickoff
When 1–4 are done: open your AI coding tool in the repo and paste the prompt from `docs/KICKOFF_PROMPT.md`.
