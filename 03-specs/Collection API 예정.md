---
title: Collection API (예정) — 개인 도감 3뷰
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Collection API (예정) (cf-17498218).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Collection, 도감, 컬렉션, 갤러리, 뱃지, badge, 스트릭, streak, 수집률, user_grids, 페이지네이션, pagination, Owner B, 예정 API]
aliases: [도감 API, 컬렉션 API]
related: ["[[Grid API]]", "[[Video 재생 조회 API 예정]]", "[[FillMap API 설계 v2 draft]]", "[[2026-07-13 격자 방문 체크 표시 아이디어]]", "[[그라운드 플립 뱃지 시스템 사례]]"]
---

# Collection API (예정) — 개인 도감 3뷰

> [!tldr]
> 개인 도감 3뷰(지도·갤러리·뱃지)·요약·스트릭 설계 초안 (Owner B). 데이터는 이미 쌓이는데 볼 API가 없는 상태.
> 지도 뷰는 기존 GET /api/grids 재사용 — 새로 만들지 않는다. 새로 필요한 건 summary·grids(갤러리)·grids/{gridId}/videos·badges 4개.
> 쟁점: 뱃지 마스터 데이터가 비어 있고 progress용 JSONB 포맷 미정, 스트릭 갱신 주체·타임존, 그리고 **프로젝트 첫 페이지네이션 API라 offset vs cursor 결정이 관례가 된다.**

## 이 노트로 답할 수 있는 질문
- 도감 3뷰 중 지도 뷰는 왜 새 API가 필요 없나?
- 도감 요약에는 어떤 숫자들이 나오나?
- 갤러리 뷰 응답 필드와 정렬 옵션은?
- 뱃지 목록 API의 쟁점(마스터 데이터·progress)은?
- 페이지네이션 방식은 왜 여기서 중요해지나?
- 수집률("강남구 25%")은 어느 API 소관인가?

## 설계 요지
- `GET /api/collections/summary` — totalGridCount·totalVideoCount·badgeCount·currentStreak·maxStreak·lastRecordedDate. streaks row 없는 사용자 처리 미정.
- `GET /api/collections/grids` — 갤러리. sort RECENT|FIRST, 페이지네이션 필요. 응답: gridId·gridY/X·firstCollectedAt·lastUploadedAt·videoCount·coverVideoId·coverThumbnailUrl·regionName.
- `GET /api/collections/grids/{gridId}/videos` — 격자별 내 영상 (idx_videos_user_created). 재생 URL 미포함.
- `GET /api/collections/badges?earnedOnly=` — code·name·description·iconUrl·conditionType·earned·earnedAt. condition_value(JSONB) 미노출, progress는 빼는 게 안전.

## 열린 질문
뱃지 progress JSONB 포맷 · 뱃지 시딩 없음(빈 배열) · 뱃지 지급 주체(배치 vs 동기, Notification 연계) · 스트릭 갱신 주체·KST 타임존 · offset vs cursor(첫 페이지네이션 — 관례 결정) · UserGridQueryService 계약 동시 생성 · 수집률은 [[Region API 예정]] 소관.

## 에러 코드 (제안, 5xxx 미확정)
5404 GRID_NOT_COLLECTED · 5400 INVALID_SORT. 격자 식별자 오류는 4400 재사용.

## 출처
raw: `raw/confluence/2026-07-17 Collection API (예정) (cf-17498218).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17498218
