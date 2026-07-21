---
title: Grid API (v1 구현 기준)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-17 Grid API (cf-17498151).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Grid, 격자, API, 도감, 뷰포트, viewport, bbox, gridId, occupied, 점령, GridController, 색칠]
aliases: [격자 API, 그리드 API]
related: ["[[FillMap API 명세 v1]]", "[[Grid 확장 API 예정]]", "[[2026-07-17 프론트-백 합의]]"]
---

# Grid API (v1 구현 기준)

> [!tldr]
> 격자(도감) 도메인, base `/api/grids`, 전 엔드포인트 인증 필요. 사용자 식별은 @AuthenticationPrincipal.
> 구현 2개: 단일 격자 셀 조회(GET /{gridId})와 뷰포트 내 색칠 격자 목록(GET /api/grids, sw/ne 좌표 4개).
> 격자는 논리 개념 — 미점령이어도 404 아님(occupied=false).

## 이 노트로 답할 수 있는 질문
- 격자 조회 API의 경로와 파라미터는?
- gridId 포맷은 어떻게 생겼나?
- 뷰포트 조회에 어떤 파라미터가 필요하고 누락되면 어떤 에러가 나나?
- 미점령 격자를 조회하면 404가 나나?
- Grid 도메인 에러 코드(4xxx)는 뭐가 있나?

## 엔드포인트
| 메서드/경로 | 설명 |
| --- | --- |
| `GET /api/grids/{gridId}` | 단일 격자 셀 조회. gridId 포맷 `{grid_y}_{grid_x}`. 응답: gridId·occupied·videoCount. 미점령이어도 200 |
| `GET /api/grids` | 뷰포트 내 색칠 격자 목록. swLat·swLng·neLat·neLng(하나라도 누락 시 4401) + strategy(기본 A). 응답: gridId·gridY·gridX 목록 |

## 에러 코드 (4xxx)
4400 INVALID_GRID_ID · 4401 INVALID_VIEWPORT · 4402 VIEWPORT_TOO_LARGE

## 출처
raw: `raw/confluence/2026-07-17 Grid API (cf-17498151).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17498151
