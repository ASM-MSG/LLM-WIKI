#!/bin/bash
set -euo pipefail
source .env 2>/dev/null || true
if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then exit 0; fi
MSG="${1:-위키 갱신}"
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-type: application/json' \
  -d "{\"text\": \"${MSG}\"}" > /dev/null 2>&1 || true
