---
title: FillMap 지도·격자 DB 설계 상세 — MVP
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-18 FillMap 지도·격자 DB 설계 상세 - MVP (cf-13992079).md"
created: 2026-07-18
updated: 2026-07-21
keywords: [지도, 격자, DB 설계, grids, user_grids, 뷰포트, viewport, ST_Intersects, bbox_geom, GIST, upsert, 커버 영상, 대표 영상, 지오코딩 배치, 인덱스]
aliases: [지도 격자 DB 설계, 지도 DB 상세]
related: ["[[FillMap DB Schema v5 MVP]]", "[[FillMap DB 자료형·ENUM·GeoJSON 기준]]", "[[Grid API]]", "[[2026-07-18 김태완 멘토 DB 피드백]]"]
---

# FillMap 지도·격자 DB 설계 상세 — MVP

> [!tldr]
> 지도 화면을 DB 4책임으로 분해: 격자 grids · 영상 videos · 개인 도감 user_grids · 행정구역 regions. 좌표는 GridEncoder로 grid_id 문자열("{y}_{x}") 변환, geohash라는 이름은 안 씀.
> 업로드 트랜잭션 안: grids 생성·videos 생성·user_grids UPSERT(ON CONFLICT, 커버는 최초 수집 영상 유지 추천). 트랜잭션 밖 비동기: region_code 지오코딩 배치·수집률 캐시·핫존 ZSET.
> 뷰포트 조회는 bbox_geom GIST + ST_Intersects(::geometry 캐스팅), 대표 영상은 READY+ACTIVE+PUBLIC에서 view_count→최신순. 개념 쿼리·응답 모델·추천 인덱스 5종 포함.

## 이 노트로 답할 수 있는 질문
- 지도 기능에서 각 테이블의 책임 분담은?
- 업로드 시 어떤 것을 트랜잭션 안/밖에서 처리하나?
- user_grids UPSERT와 커버 영상 정책은?
- 뷰포트 조회 쿼리와 인덱스는 어떻게 생겼나?
- 대표 영상 선정 기준은?
- grids.region_code는 누가 언제 채우나?
- 지역 필터(시도/시군구/행정동)는 어떻게 구현하나?

## 요지
- 흐름: lat/lng → GridEncoder → grid_id → grids 없으면 생성 → videos.grid_id 연결 → user_grids 채움.
- 뷰포트: `ST_Intersects(g.bbox_geom::geometry, ST_MakeEnvelope(...))` + user_grids left join으로 collectedByMe 포함 응답.
- 개인 도감 지도는 user_grids가 주인공(videos는 커버 썸네일 보조).
- 인덱스: idx_grids_bbox_geom(GIST) · idx_grids_region_code · uq_user_grids_user_grid · idx_user_grids_user_recent · idx_videos_grid_popular(partial).
- 지오코딩: region_code NULL인 격자를 배치가 모아 Python 서버에 벌크 요청 — 업로드 응답이 지오코딩에 안 묶이고, 서버가 죽어도 업로드는 성공.
- 지역 필터는 regions.parent_code 계층 또는 코드 prefix. MVP는 행정동만 먼저.
- MVP에서 미룸: 친구 격자·랭킹·핫구역 클러스터링·스폰서·video_views.

## 출처
raw: `raw/confluence/2026-07-18 FillMap 지도·격자 DB 설계 상세 - MVP (cf-13992079).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/13992079
