---
name: wiki-ingest
description: raw 원본을 읽어 봉투(envelope)+frontmatter를 갖춘 compiled 노트로 변환하고 index/hot/log를 갱신한다. "ingest해줘", "이 raw 정리해줘" 요청 시 사용.
---

# wiki-ingest — raw → compiled

raw/의 원본을 **수정하지 않고** 텍스트만 추출해 종류별 폴더의 compiled 노트로 만든다.

## 포맷 추출
| 포맷 | 방법 |
| --- | --- |
| `.txt` `.md` `.csv` | Claude Read 도구 |
| `.pdf` | Claude Read (`pages` 파라미터) |
| `.xlsx` `.docx` `.pptx` | `python .claude/skills/wiki-ingest/extract.py "<파일>"` |
| `.png` `.jpg` 등 이미지 | Claude Read (시각 분석) — 텍스트·구조·데이터·맥락 추출 |
| 웹 URL | WebFetch → `raw/reference/YYYY-MM-DD <제목> (출처).md` 스냅샷 저장 후 ingest |

## 절차
0. **sync 확인** — 대상 raw가 로컬에 실제로 존재하는지 확인. Drive 동기화가 안 끝났으면 대기.
1. 대상 raw 텍스트 추출 (**원본 수정 금지** — raw-guard가 강제).
2. **분류** — type 판별 → 해당 폴더로 배치.
3. **분해** — 길면 허브 1 + atomic n, 짧으면 단일. 파일명에 `[` `]` 금지.
4. **노트 작성** (`00-meta/templates/_base.md` 봉투 사용):
   - frontmatter 전부 채우기
   - `keywords`·`aliases`: 한/영 동의어 풍부히 (검색 정확도의 핵심)
   - `related`: 기존 노트와 `[[wikilink]]` 연결
   - `> [!tldr]`: 3줄 요약
   - `## 이 노트로 답할 수 있는 질문`: 4~6개
   - 본문: type에 맞는 템플릿 구조 사용
   - `## 출처`: raw 경로
5. 기존 노트의 `related`에 역링크 추가.
6. `index.md`·`hot.md`·`log.md` 갱신.
7. lint로 검증.

## 개인 노트 (raw/individual → 07-individual)
- `type: note` · `class: log` · `author: <사람>` 필수
- 봉투는 유지하되 본문은 짧게. tldr에 "개인 의견(팀 합의 아님)" 명시
- index/hot/log 갱신 안 함 (팀 인덱스를 가볍게 유지)

## Confluence 스냅샷 (raw/confluence → 종류별 폴더)
- `confluence-sync`가 저장한 스냅샷도 일반 raw와 동일하게 ingest한다.
- 같은 페이지의 새 스냅샷(cf-ID 동일)이 오면 **기존 compiled 노트를 갱신**하고 `source`를 최신 스냅샷 경로로 바꾼다.
- 노트의 `## 출처`에 raw 경로와 함께 Confluence 원본 URL도 남긴다.

## 주의
- raw를 절대 수정하지 않는다.
- 같은 raw를 다시 ingest하면 기존 노트를 갱신(덮어쓰기)한다.
- canon 수정은 canon-guard가 막는다 → 사람 승인 먼저.
