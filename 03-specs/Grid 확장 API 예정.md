---
title: Grid 확장 API (예정) — 격자 상세·좋아요·핫존
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Grid 확장 API (예정) (cf-17891437).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Grid 확장, 격자 상세, 대표 영상, 좋아요, like, likes, 핫존, hot zone, Redis ZSET, idx_videos_grid_popular, Owner 경계, 예정 API]
aliases: [격자 확장 API, 핫존 API, 좋아요 API]
related: ["[[Grid API]]", "[[Video 재생 조회 API 예정]]", "[[FillMap API 설계 v2 draft]]", "[[2026-07-17 프론트-백 합의]]"]
---

# Grid 확장 API (예정) — 격자 상세·좋아요·핫존

> [!tldr]
> 격자 영상 목록(GET /api/grids/{gridId}/videos)·좋아요(POST/DELETE /api/videos/{videoId}/likes)·핫존(GET /api/grids/hot) 설계 초안.
> 정렬은 스키마가 결정: idx_videos_grid_popular = 조회수→최신, ACTIVE+PUBLIC+READY만. ⚠️ visibility 기본이 PRIVATE라 공개 전환 API 없이는 이 API가 항상 빈 배열.
> 좋아요는 멱등 UPSERT(복합 PK). 핫존은 Redis 스키마 근거가 전무 — 별도 설계 티켓 권장. Owner A/B 경계 문제 미결.

## 이 노트로 답할 수 있는 질문
- 격자를 탭했을 때 영상 목록은 어떤 정렬·필터로 나오나?
- 왜 지금 데이터로는 격자 영상 목록이 빈 배열인가?
- 좋아요 API는 왜 멱등이고 body가 없나?
- 핫존 API는 왜 아직 정의할 수 없나?
- 격자 상세의 Owner는 누구인가(A/B 경계)?
- likeCount는 어떻게 세나 (N+1 문제)?

## 설계 요지
- `GET /api/grids/{gridId}/videos` — 남의 격자도 조회 가능. 응답: videoId·thumbnailUrl·durationSec·viewCount·likeCount·liked·authorNickname·authorGridColor·recordedAt. 재생 URL은 별도([[Video 재생 조회 API 예정]]).
- `POST/DELETE /api/videos/{videoId}/likes` — likes PK (user_id, video_id), ON CONFLICT DO NOTHING. 응답: videoId·likeCount·liked. 좋아요는 Owner B(영상에 붙음).
- `GET /api/grids/hot` — 전부 제안. Redis ZSET 키 구조·스코어 산식·TTL 설계 선행 필요.

## 열린 질문
Owner 배정(a: video에 두고 경로만 grids, b: VideoQueryService 계약) · 핫존 Redis 스키마(범위 제외 권장) · likeCount COUNT vs 비정규화(컬럼 없음) · PRIVATE 영상 좋아요 · 태그/분위기 필터(컬럼 없음, 범위 밖) · 신고 진입(Moderation).

## 출처
raw: `raw/confluence/2026-07-17 Grid 확장 API (예정) (cf-17891437).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891437
