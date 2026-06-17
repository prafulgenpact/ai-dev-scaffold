# Verification Regime — anti-doom-loop

The doom loop: agent claims done → owner opens app → broken → owner describes bug → agent guesses → partial fix → regression. Root causes and their countermeasures, each mechanical rather than aspirational:

| Root cause | Countermeasure |
|---|---|
| Agent never used the app like a user | End-user impersonation (scripted + exploratory) with screenshots |
| Verification self-reported by the builder | Separate QA agent with fresh context judges against written criteria |
| No regression net | Full test pyramid in `scripts/verify.sh`, enforced by Stop hook |
| Owner acts as the test harness | Owner reviews evidence reports, not raw breakage |

## 1. The testing pyramid (each layer has a distinct job)
- **Unit ({{TEST_RUNNER}})** — fault *localization*. E2E says "broken"; unit says "here".
- **Integration** — cross-component behavior. Uses mocks/fixtures for determinism.
- **E2E scripted** — permanent user-journey regression net.
- **E2E exploratory (QA agent)** — unscripted impersonation: act like the owner, try to break it, screenshot everything.

## 2. Builder/judge separation
The session that wrote the code has the same blind spots that wrote the bug. After every slice, the **QA agent** runs with fresh context, only the written acceptance criteria, and browser/CLI tools. It files an evidence-backed report to `qa/reports/`. Builder fixes → QA re-verifies → loop until PASS. QA never edits code or tests.

## 3. Mechanical gates
- `scripts/verify.sh` — the single entry point (lint, typecheck, tests). Tolerant: skips suites that don't exist yet; fails loudly on any that exist and fail.
- **Stop hook** runs `verify.sh --hook` whenever the AI agent tries to finish; exit code 2 blocks completion. Hook scope: fast layers only (lint, typecheck, unit tests).
- **Test files are append-only.** Weakening, skipping, or deleting an assertion requires explicit owner approval.
- One branch per slice; merge only on green + QA pass.

## 4. Slice discipline — the strongest single lever
Doom loops correlate with big-bang changes. Slices are thin vertical cuts (~30 min). A 30-minute slice cannot waste hours. If a slice balloons, stop and split it.

## 5. Definition of done (for every slice)
1. `scripts/verify.sh` green
2. Slice acceptance criteria (PLAN.md) demonstrably met
3. QA agent PASS with evidence in `qa/reports/`
4. PLAN.md checkboxes + Current state updated
5. No claim without evidence: test output or screenshot, in the transcript
