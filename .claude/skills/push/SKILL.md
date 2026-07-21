---
name: push
description: 변경을 AngularJS 커밋 컨벤션(한글)으로 커밋 → main push → Slack 알림. "push해줘" 요청 시 사용.
---

# push — 커밋 + push (main)

## 절차
1. **동기화:** `git pull --rebase origin main`
2. **lint 사전점검:** `node .claude/skills/wiki-lint/lint.js .` — 실패 시 멈추고 수정
3. **stage:** `git add -A && git status --short`
4. **commit** — AngularJS 컨벤션:
   - 헤더: `<type>(<scope>): <한글 요약>` (마침표 없이)
   - body: 추가/수정 파일 나열
   - type: `docs`(노트), `feat`(새 스킬/훅), `fix`(오류 수정), `refactor`(이동), `chore`(설정)
5. **push:** `git push origin main`
6. **Slack 알림:** `.env`에 `SLACK_WEBHOOK_URL` 있으면 `bash 00-meta/notify-slack.sh "<요약>"` 실행, 없으면 생략

## 커밋 메시지 예시
```
docs(05-meetings): 킥오프 회의록 ingest

추가: 05-meetings/2026-07-01 킥오프.md
수정: index.md, hot.md, log.md
```
