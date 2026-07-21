#!/bin/bash
set -euo pipefail
source .env
if [ -z "${GDRIVE_RAW_LOCAL_PATH:-}" ]; then
  echo "❌ .env에 GDRIVE_RAW_LOCAL_PATH를 설정하세요"
  exit 1
fi
if [ -e raw ] && [ ! -L raw ]; then
  echo "❌ raw/가 이미 실제 폴더로 존재합니다 (심볼릭 링크가 아님)"
  exit 1
fi
ln -sfn "$GDRIVE_RAW_LOCAL_PATH" raw
echo "✅ raw → $GDRIVE_RAW_LOCAL_PATH 링크 완료"
