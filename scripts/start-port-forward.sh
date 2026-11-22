#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-30080}"
PID_FILE="${TMPDIR:-/tmp}/mts-demo-port-forward.pid"
LOG_FILE="${TMPDIR:-/tmp}/mts-demo-port-forward.log"
if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(cat "$PID_FILE" || true)"
  if [[ -n "${OLD_PID:-}" ]] && kill -0 "$OLD_PID" 2>/dev/null; then kill "$OLD_PID" || true; fi
  rm -f "$PID_FILE"
fi
nohup kubectl port-forward service/mts-demo "${PORT}:8080" --address 0.0.0.0 >"$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
for attempt in $(seq 1 30); do
  if curl --silent --fail "http://127.0.0.1:${PORT}/health" >/dev/null; then
    echo "MTS demo available at http://localhost:${PORT}"
    exit 0
  fi
  sleep 2
done
cat "$LOG_FILE"
exit 1
