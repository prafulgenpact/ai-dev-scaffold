# {{PROJECT_NAME}}

{{DESCRIPTION}}

- Humans: start with `docs/PRD.md`, then `docs/OWNER_TODO.md`.
- AI agents: start with `CLAUDE.md`, kickoff prompt in `docs/KICKOFF_PROMPT.md`.

Built with disciplined AI-assisted development. Docs are the contract; code follows them.

## Quick Start

1. Complete `docs/OWNER_TODO.md` prerequisites
2. Fill in `docs/PRD.md` with your requirements
3. Fill in `docs/PLAN.md` with your phased build plan
4. Start your AI coding session with the prompt from `docs/KICKOFF_PROMPT.md`

## Verification

```bash
scripts/verify.sh        # Full verification: lint + typecheck + tests
scripts/verify.sh --hook  # Fast mode (used by AI Stop hook)
```

## Documentation

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | AI agent operating manual — stack, invariants, rules |
| `docs/PRD.md` | Product requirements — what & why |
| `docs/ARCHITECTURE.md` | Technical design — how |
| `docs/PLAN.md` | Build plan — when (updated every session) |
| `docs/VERIFICATION.md` | Testing regime — proof |
| `docs/EVALS.md` | Accuracy measurement — quality |
| `docs/OWNER_TODO.md` | Human inputs — blockers |
| `docs/KICKOFF_PROMPT.md` | First message for AI sessions |
