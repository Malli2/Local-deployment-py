#!/usr/bin/env bash
set -euo pipefail
PID_FILE="${TMPDIR:-/tmp}/mts-demo-port-forward.pid"
if [[ -f "$PID_FILE" ]]; then
  PID="$(cat "$PID_FILE" || true)"
  if [[ -n "${PID:-}" ]] && kill -0 "$PID" 2>/dev/null; then kill "$PID"; fi
  rm -f "$PID_FILE"
else
  echo "No port-forward PID file found"
fi
