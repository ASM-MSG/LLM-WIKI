---
title: ADR 격자 행정동 라벨 — grids.region_code 저장 (MSG-167)
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-22 격자 행정동 라벨 설계 결정 — grids.region_code (MSG-167) (cf-22216705).md"
created: 2026-07-22
updated: 2026-07-22
keywords: [격자, 행정동, 라벨, region_code, grids, 도감 갤러리, regionName, 동 단위 영상, by-grid, ST_Covers, geospatial 금지, equi-join, lazy insert, 백필, region_stats, 라이브 집계, MSG-167, MSG-153, MSG-155, MSG-164, 함수 종속, 비정규화]
aliases: [MSG-167 결정, 격자 행정동 라벨, grids region_code]
related: ["[[개인 도감 화면 확정 UX·API 설계]]", "[[Region API 예정]]", "[[Collection API 예정]]", "[[FillMap 지도·격자 DB 설계 MVP]]", "[[FillMap API 스펙 통합]]"]
---

# ADR 격자 행정동 라벨 — grids.region_code 저장 (MSG-167)

> [!tldr]
> 도감 갤러리 30개 셀에 행정동 이름("역삼1동")을 붙이기 위해 **격자의 행정동을 `grids.region_code` 컬럼(V4, nullable FK)에 저장**하기로 확정 (2026-07-22, KangJeong).
> 핵심 논리: ① 행정동은 격자 중심점만으로 정해지는 **격자 자체의 속성**(함수 종속 `grid_id → region_code`) — user_grids에 두면 점령자 수만큼 중복 ② MSG-155 때 폐기했던 안의 **정당한 부활**(당시엔 쓰기 경로뿐이라 저장 불필요 → 지금은 조회 경로 요구 발생, "조회 경로 geospatial 금지" ADR상 저장 필수) ③ 조회는 PK equi-join 2개 ≈0.4~0.5ms(MSG-164 실측) — 비정규화·조회 시 ST_Covers 안 기각.
> **같은 티켓에 동 단위 내 영상 조회 API 신설**(예: `GET /api/collections/videos?regionCode=`) — 귀속 축은 영상 GPS가 아니라 **격자 중심점**이라 탐험률과 어긋날 수 없음. region_stats 라이브 집계 전환은 백로그 보류.

## 이 노트로 답할 수 있는 질문
- 격자의 행정동 이름은 어디에 저장하고 언제 판정하나? (grids.region_code, lazy insert 시 1회)
- 왜 user_grids가 아니라 grids에 저장하나? (함수 종속·중복)
- MSG-155에서 폐기한 안을 왜 다시 채택해도 모순이 아닌가?
- 목록 라벨 조인 비용은 얼마고 어떤 대안을 기각했나? (MSG-164 실측 근거)
- 격자 클릭 → 동 단위 내 영상 모아보기는 어떤 축으로 귀속되나? (격자 중심점)
- region_stats를 라이브 집계로 바꾸지 않은 이유는? (검증된 코드 churn + 156 계약 의미 변화)

## 결정 요약
1. **저장 위치**: `grids.region_code VARCHAR(10) NULL REFERENCES regions(region_code)` (V4 마이그레이션) — 격자당 1회, lazy insert 시 ST_Covers 판정(격자 생애 1회), 기존 격자는 멱등 백필.
2. **판정 규칙 통일**: 격자 중심점 ST_Covers + `ORDER BY region_code LIMIT 1` — MSG-93/155/153과 동일해 목록 라벨·동 단위 영상·클릭 탐험률(by-grid) 귀속이 항상 일치. 무귀속(해안)은 NULL.
3. **조회 방식**: grids+regions PK equi-join 2개(≈0.4~0.5ms/요청, geospatial 0) 채택. region_name 비정규화(개편 시 이중 갱신 리스크), 조회 시 ST_Covers(ADR 위반) 기각.
4. **동 단위 내 영상 조회 신설**: `videos ⨝ grids`에 `g.region_code` 필터 — FE 동선: 격자 클릭 → by-grid(동+탐험률) → 동 단위 내 영상. 내 영상만·ACTIVE·최신순.
5. **보류**: region_stats → 라이브 집계 전환은 백로그 (착수 조건: 운영 부담 발생 or 156 계약 변경 시).

## 시사점
- [[FillMap API 스펙 통합]] 갱신 대상: `GET /api/regions/stats/by-grid`(격자 클릭 응답 — MSG-153 스펙에서 확정된 신규 경로)와 동 단위 내 영상 API(MSG-167 예정)가 현재 통합 명세판에 없음.
- MSG-153의 쟁점 ②(행정동 표기 축)가 이 결정으로 종결 — 격자 중심점 축으로 통일.
- 갤러리 목록 응답에 `regionName`(nullable) 필드 추가 예정.

## 출처
raw: `raw/confluence/2026-07-22 격자 행정동 라벨 설계 결정 — grids.region_code (MSG-167) (cf-22216705).md`
Confluence 원본: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/22216705
