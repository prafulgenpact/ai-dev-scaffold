#!/usr/bin/env bash
# Single verification entry point. Tolerant: skips suites that don't exist yet,
# fails loudly on any that exist and fail.
# Usage: scripts/verify.sh [--hook]
#   --hook : AI Stop-hook mode — fast suites only, ALL output to stderr, exit 2 on failure.
set -uo pipefail
cd "$(dirname "$0")/.."

HOOK=0; [[ "${1:-}" == "--hook" ]] && HOOK=1
[[ $HOOK -eq 1 ]] && exec 1>&2

fail=0; ran=0

note() { printf '%s\n' "$*"; }
run()  { local name="$1"; shift; ran=1; note "── ${name}"
         if "$@"; then note "   PASS"; else note "   FAIL"; fail=1; fi; }

# Python: lint, typecheck, tests
if [[ -f pyproject.toml ]]; then
  if command -v uv >/dev/null 2>&1; then
    run "ruff"   uv run ruff check .
    run "mypy"   uv run mypy .
    [[ -d tests ]] && run "pytest" uv run pytest -q -m "not live"
  elif command -v python3 >/dev/null 2>&1; then
    run "ruff"   python3 -m ruff check .
    run "mypy"   python3 -m mypy .
    [[ -d tests ]] && run "pytest" python3 -m pytest -q -m "not live"
  else
    note "verify: FATAL — pyproject.toml exists but neither uv nor python3 found"
    [[ $HOOK -eq 1 ]] && exit 2; exit 1
  fi
fi

if [[ $ran -eq 0 ]]; then
  note "verify: nothing to run yet (no suites found) — OK"
  exit 0
fi
if [[ $fail -eq 1 ]]; then
  note "verify: FAIL"
  [[ $HOOK -eq 1 ]] && exit 2
  exit 1
fi
note "verify: PASS"
exit 0
