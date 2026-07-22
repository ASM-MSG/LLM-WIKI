---
title: Region API (예정) — 행정동 검색·수집률·경계
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Region API (예정) (cf-17891417).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Region, 행정동, 지역, 검색, search, 수집률, region_stats, regions, GeoJSON, 시딩, seeding, 경계, boundary, ST_Envelope, fitBounds, Owner A, 예정 API]
aliases: [지역 API, 행정동 API]
related: ["[[FillMap API 설계 v2 draft]]", "[[Grid API]]", "[[ADR 격자 표시명 zone]]", "[[Collection API 예정]]", "[[개인 도감 화면 확정 UX·API 설계]]"]
---

# Region API (예정) — 행정동 검색·수집률·경계

> [!tldr]
> 행정동 검색(/search)·내 수집률(/stats)·정보(/{code})·경계 폴리곤(/boundary) 설계 초안 (Owner A, 패키지 미생성).
> 행정동 검색은 우리 DB(3,558개)로 완결 — 지도 SDK 검색 API 불필요. FE는 검색 → fitBounds → 기존 GET /api/grids 흐름, 새로 만들 건 검색 API 하나뿐.
> ⚠️ 최대 선행 과제는 데이터: regions GeoJSON 시딩과 region_stats 갱신 배치가 없으면 API 전체 무효. "홍대" 같은 랜드마크 검색은 격자 표시명 설계와 같은 뿌리.

## 이 노트로 답할 수 있는 질문
- 행정동 검색에 지도 SDK 검색 API가 왜 필요 없나?
- 검색 → 지도 이동 → 격자 표시의 FE 흐름은?
- "강남구 25%" 수집률은 어떤 테이블·API에서 오나?
- 경계 폴리곤을 왜 별도 엔드포인트로 분리했나?
- 이 API의 선행 과제(시딩·배치)는?
- "홍대"로 검색이 안 되는 이유는?

## 설계 요지
- `GET /api/regions/search?q=&limit=` — regionCode·regionName·parentCode·bounds(ST_Envelope). 동명이인 행정동은 parentCode로 구분.
- `GET /api/regions/stats?parentCode=&collectedOnly=` — region_stats(PK user_id+region_code) 단순 SELECT: collectedCount·totalCount·progressRate·updatedAt. ⚠️ 시안은 시/도 단위("서울 34%")인데 테이블은 행정동 단위 — 집계 레벨 확정 필요.
- `GET /api/regions/{regionCode}` — 기본 정보 (boundary_geom 미포함).
- `GET /api/regions/{regionCode}/boundary` — GeoJSON MultiPolygon (수백 KB~MB라 분리, ST_Simplify·캐싱 미정, 프론트 필요성부터 확인).

## 열린 질문
LIKE vs 전문검색(3,558개면 LIKE 충분) · 동명이인 표시(상위 지역명 join) · 랜드마크 검색(격자 표시명과 함께) · region_stats 갱신 주체(동기/배치/lazy — 롤백 반영이 관건) · regions 시딩(전국 vs 서울) · total_grid_count 계산 · regions.total_grid_count vs region_stats.total_count 중복 · 공개 API 여부(SecurityConfig 변경 수반) · UserGridQueryService 계약.

## 에러 코드 (제안, 6xxx 미확정)
6404 REGION_NOT_FOUND · 6400 INVALID_REGION_CODE. 검색 결과 없음은 빈 배열.

## 출처
raw: `raw/confluence/2026-07-17 Region API (예정) (cf-17891417).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891417
