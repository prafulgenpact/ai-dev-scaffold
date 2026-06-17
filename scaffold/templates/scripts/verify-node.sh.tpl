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

# Node: lint, typecheck, tests
if [[ -f package.json ]]; then
  if ! command -v npm >/dev/null 2>&1; then
    note "verify: FATAL — package.json exists but npm is not installed"
    [[ $HOOK -eq 1 ]] && exit 2; exit 1
  fi
  run "eslint"  npx --no-install eslint .
  run "tsc"     npx --no-install tsc --noEmit
  [[ -d tests || -d __tests__ || -d src/__tests__ ]] && run "vitest" npx --no-install vitest run
fi

# Playwright E2E: full-run only — needs live servers
if [[ $HOOK -eq 0 ]] && compgen -G "playwright.config.*" >/dev/null; then
  run "playwright" npx --no-install playwright test
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
