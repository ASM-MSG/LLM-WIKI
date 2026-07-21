---
title: FillMap DB 자료형·ENUM·GeoJSON 처리 기준
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-18 FillMap DB 자료형·ENUM·GeoJSON 처리 기준 (cf-13959279).md"
created: 2026-07-18
updated: 2026-07-21
keywords: [자료형, 타입, ENUM, CHECK, GEOGRAPHY, GEOMETRY, PostGIS, SRID 4326, GeoJSON, HangJeongDong, adm_cd2, 좌표 순서, lng lat, 시딩, UTC]
aliases: [DB 자료형 기준, ENUM 기준, GeoJSON 처리]
related: ["[[FillMap DB Schema v5 MVP]]", "[[FillMap 지도·격자 DB 설계 MVP]]", "[[Region API 예정]]"]
---

# FillMap DB 자료형·ENUM·GeoJSON 처리 기준

> [!tldr]
> 스키마 공통 기준 모음: PK는 BIGINT, 코드류 VARCHAR·URL은 TEXT, TIMESTAMP는 UTC 저장(표시만 KST). ENUM은 PostgreSQL ENUM 대신 **VARCHAR + CHECK** (개발 중 값 변경이 쉬움) — 10종 정의(auth_provider·user_role·friendship_status·video_processing/visibility/status·report_reason/status·badge_condition_type·sponsor_ad_status).
> PostGIS: 저장은 GEOGRAPHY(SRID 4326) 우선, 뷰포트 교차는 ::geometry 캐스팅. **좌표 순서는 [lng, lat]** — Point(lat, lng)는 버그.
> GeoJSON은 HangJeongDong_ver20260701.geojson(adm_cd2 10자리): Python 지오코딩 서버는 메모리 로드로 판정(DB 없음), PostGIS는 같은 파일로 regions 시딩·검증·조회.

## 이 노트로 답할 수 있는 질문
- ENUM을 DB ENUM이 아닌 VARCHAR+CHECK로 두는 이유는?
- 서비스에 어떤 ENUM 10종이 있나?
- GEOGRAPHY vs GEOMETRY는 언제 뭘 쓰나?
- 좌표 순서에서 주의할 점은?
- 공간 컬럼(center/bbox/geom/boundary)의 추천 타입은?
- 행정동 GeoJSON 파일 구조와 시딩 방식은?
- TIMESTAMP는 어느 타임존으로 저장하나?

## 요지
- 자료형: BIGINT PK(누적 테이블 마이그레이션 비용 회피) · SMALLINT duration_sec · NUMERIC progress_rate · JSONB는 남발 금지.
- 공간: grids.center_geom GEOGRAPHY(POINT) · grids.bbox_geom POLYGON(교차 조회 잦으면 GEOMETRY 고려) · videos.geom POINT · regions.boundary_geom MULTIPOLYGON.
- ENUM 10종: auth_provider(LOCAL/KAKAO) · user_role · friendship_status · video_processing_status(UPLOADED/ENCODING/BLURRING/READY/FAILED) · video_visibility(PUBLIC/PRIVATE) · video_status(ACTIVE/BLINDED/DELETED) · report_reason(INAPPROPRIATE/PRIVACY/SPAM/COPYRIGHT/OTHER) · report_status · badge_condition_type · sponsor_ad_status.
- GeoJSON: 파일 하나를 Python(메모리 판정)과 PostGIS(regions 시딩)가 같이 씀. Python 서버는 adm_cd2만 반환, 전용 DB 불필요.

## 출처
raw: `raw/confluence/2026-07-18 FillMap DB 자료형·ENUM·GeoJSON 처리 기준 (cf-13959279).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/13959279
