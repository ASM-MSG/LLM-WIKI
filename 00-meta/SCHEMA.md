---
title: SCHEMA — 운영 규칙
type: hub
product: fillmap
class: canon
status: active
source: "LLM-WIKI-SETUP.md"
created: 2026-07-21
updated: 2026-07-21
keywords: [스키마, schema, 규칙, 봉투, envelope, frontmatter, canon, 네이밍, confluence, 컨플루언스]
aliases: [운영규칙, 저장소규약]
related: []
---

# SCHEMA — 운영 규칙 (권위 · Layer 3)

> [!tldr]
> 이 문서가 저장소의 권위(단일 진실). 봉투 계약·type/class/product 어휘·네이밍 규칙·Confluence 수집 규칙을 못박는다.

## 이 노트로 답할 수 있는 질문
- 새 노트를 만들 때 어떤 frontmatter를 넣어야 하나?
- type·class·product 값으로 뭘 쓸 수 있나?
- 파일명은 어떻게 짓나?
- 어떤 문서가 canon이고 어떻게 변경하나?
- Confluence 문서는 어떻게 raw로 들어오나?

## 1. 봉투(envelope) 계약 — 모든 노트 공통
1. frontmatter (§2)
2. `# 제목`
3. `> [!tldr]` 3줄 요약
4. `## 이 노트로 답할 수 있는 질문` (4~6개)
5. `## 출처` — `raw: \`...\``

## 2. Frontmatter 계약
```yaml
title:                 # 필수
type:      meeting     # meeting|research|decision|spec|planning|product|hub|note
product:   fillmap     # 제품 태그
class:     log         # canon|log|decision|raw
status:    draft       # draft|active|archived
source:    "raw/..."   # 원본 경로 (필수)
created:   YYYY-MM-DD
updated:   YYYY-MM-DD
keywords:  []          # ★ 한/영 동의어 풍부히 (검색 핵심)
aliases:   []
related:   []          # [[wikilink]]
```

## 3. type 어휘
`meeting · research · decision · spec · planning · product · hub · note`

| type | 폴더 |
| --- | --- |
| product | `01-product/` |
| planning | `02-planning/` |
| spec | `03-specs/` |
| decision | `04-decisions/` |
| meeting | `05-meetings/` |
| research | `06-research/` |
| note | `07-individual/<사람>/` |
| hub | 종류에 맞는 폴더 |

## 4. class 어휘
| class | 변경 규칙 |
| --- | --- |
| 🟦 canon | 한 곳에서만 정의. 변경은 사람 승인 (`canon-guard`) |
| 🟩 log | append-only. 새 파일로만 추가 |
| 🟨 decision | 스냅샷. 뒤집으면 `superseded` + 새 ADR |
| 🟥 raw | 불변. 수정·삭제 금지 (`raw-guard`) |

## 5. 네이밍
- 날짜형: `YYYY-MM-DD 제목.md` (회의록·리서치·개인노트)
- 개념형: slug (`GOAL.md`, `demand-forecast-spec.md`)
- 파일명에 `[` `]` 금지
- 교차참조: `[[파일명]]` (경로 아닌 파일명 — 폴더 이동에 안 깨짐)
- 과업: `- [ ] @담당 ~납기`

## 6. Confluence 수집 (raw 소스)
- 팀 Confluence(MSG 스페이스, space = M)의 페이지는 `confluence-sync` 스킬이 `raw/confluence/`에 스냅샷으로 저장한다.
- **제외:** 제목이 `데일리 스크럼*` 또는 `스프린트 * 회고*`인 페이지.
- 스냅샷 파일명: `YYYY-MM-DD 제목 (cf-<페이지ID>).md` — 제목의 `[` `]` `/`는 제거·치환.
- 페이지가 수정되면 기존 스냅샷을 덮어쓰지 않고 새 날짜의 새 스냅샷을 만든다 (raw 불변).
- sync 상태는 `00-meta/confluence-sync-state.json`(lastSync)에 기록한다.

## 7. unfold (제품 1개 → 2개+)
git mv로 `products/<제품>/` 하위로 이동. wikilink·source 안 깨짐.

## 출처
raw: `LLM-WIKI-SETUP.md`
