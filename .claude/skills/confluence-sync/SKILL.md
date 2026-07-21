---
name: confluence-sync
description: 팀 Confluence(MSG 스페이스)에서 지난 sync 이후 추가·수정된 페이지를 raw/confluence/ 스냅샷으로 저장한다. 데일리 스크럼·스프린트 회고는 제외. "컨플 sync해줘", "confluence 가져와줘" 요청 시 또는 wiki-ingest-and-push의 Step 0로 사용.
---

# confluence-sync — Confluence → raw

Atlassian MCP(claude.ai 연동)로 팀 Confluence를 조회해 새/수정 문서를 raw 스냅샷으로 저장한다.

## 설정
- cloudId: `e33d1b40-dcdd-479f-9227-00c400ca5b6e` (soma17-msg.atlassian.net)
- 대상: `space = M` (MSG 팀 스페이스)만 — 개인 스페이스 제외
- 상태 파일: `00-meta/confluence-sync-state.json` → `{ "lastSync": "<ISO8601>" }`

## 제외 규칙 (제목 기준)
- `데일리 스크럼*`
- `스프린트 * 회고*`

## 절차
0. **raw 연결 확인** — `raw/` 디렉토리가 실제로 존재하는지 확인 (`ls raw/`). 없으면 멈추고 사용자에게 Drive 연결(`bash 00-meta/setup-raw-link.sh`)을 안내한다. `raw/confluence/`가 없으면 생성.
1. 상태 파일에서 `lastSync`를 읽는다.
2. `searchConfluenceUsingCql`:
   `space = M AND type = page AND lastmodified > "<lastSync를 yyyy-MM-dd HH:mm으로>" ORDER BY lastmodified ASC`
3. 제외 규칙에 걸리는 제목은 skip.
4. 각 페이지를 `getConfluencePage`로 읽어 스냅샷 저장:
   - 경로: `raw/confluence/YYYY-MM-DD 제목 (cf-<페이지ID>).md` — 날짜는 페이지 최종 수정일, 제목의 `[` `]` `/` `:`는 제거·치환
   - 파일 상단에 메타 블록: 원본 URL · 페이지 ID · 버전 · 작성자 · 수집 시각
   - 같은 페이지가 나중에 또 수정되면 기존 스냅샷은 그대로 두고 **새 날짜의 새 파일**로 저장 (raw 불변 — raw-guard가 덮어쓰기를 막는다)
5. `lastSync`를 현재 시각으로 갱신 (상태 파일은 raw가 아니므로 수정 가능).
6. 저장한 파일 목록을 보고하고, ingest까지 요청된 흐름이면 `wiki-ingest`로 넘긴다.

## 스냅샷 파일 형식
```markdown
> [!info] Confluence 스냅샷
> - 원본: <webUrl>
> - 페이지 ID: <id> · 버전: <version>
> - 작성자: <displayName> · 수집: <ISO8601>

(페이지 본문 markdown)
```

## 주의
- MCP 인증은 claude.ai 세션 기반 — 스케줄/헤드리스 자동 실행 불가, **수동 트리거 전용**.
- 페이지의 이미지·첨부파일은 스냅샷에 포함되지 않는다. 필요하면 원본 URL로 확인.
- Confluence 원본은 절대 수정하지 않는다 (읽기 전용 수집).
