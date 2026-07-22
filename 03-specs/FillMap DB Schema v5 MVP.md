---
title: FillMap DB Schema v5 — MVP 개인 도감
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-18 FillMap DB Schema v5 - MVP 개인 도감 (cf-14090329).md"
created: 2026-07-18
updated: 2026-07-21
keywords: [DB, 스키마, schema, v5, ERD, users, grids, regions, videos, user_grids, view_count, 지오코딩, geocoding, GeoJSON, MVP 테이블, 도감]
aliases: [DB Schema v5, MomentMap DB Schema]
related: ["[[FillMap 지도·격자 DB 설계 MVP]]", "[[FillMap DB 자료형·ENUM·GeoJSON 기준]]", "[[ERD 정렬 디자인 기준 데이터모델]]", "[[2026-07-18 김태완 멘토 DB 피드백]]", "[[개인 도감 화면 확정 UX·API 설계]]"]
---

# FillMap DB Schema v5 — MVP 개인 도감

> [!tldr]
> MVP DB의 팀 공통 기준 (작성 KangJeong): mvp_* 별도 테이블 없이 같은 테이블을 작게 시작. 중심 5개 = users·regions·grids·videos·user_grids.
> videos.view_count는 MVP 필수(대표 영상이 조회수 정렬을 요구) — video_views 이력 테이블은 분석 필요해질 때. 부분 인덱스 idx_videos_grid_popular 포함.
> Python 지오코딩 서버는 DB 없음 — GeoJSON을 메모리에 올려 판정, 결과 adm_cd2만 grids.region_code에 저장(NULL이면 배치가 벌크 판정). 후순위: friendships·streaks·badges·likes·sponsor_ads 등.

## 이 노트로 답할 수 있는 질문
- MVP에 포함되는 테이블과 제외되는 테이블은?
- view_count를 MVP에 두는 이유와 video_views를 안 만드는 이유는?
- 지오코딩 서버와 DB의 책임 경계는?
- grids.region_code는 언제 어떻게 채워지나?
- user_grids의 제약과 업로드 시 처리 흐름은?
- 대표 영상 정렬 인덱스는 어떻게 생겼나?

## 요지
- **MVP 포함**: users(UNIQUE(provider,oid), 카카오 중심) · regions(adm_cd2 마스터) · grids(양자화 grid_id, region_code는 배치로 지연 채움) · videos(S3 참조+상태, duration 제한, PUBLIC/PRIVATE, ACTIVE/BLINDED/DELETED) · user_grids(UNIQUE(user_id,grid_id), cover_video_id).
- **선택**: region_stats(수집률 캐시). **후순위/제외**: push_tokens·friendships·streaks·badges·user_badges·likes·reports·sponsor_ads.
- **view_count**: 재생 판정 시점에 원자적 +1. 중복 방지·유니크 시청자·체류 분석이 필요해지면 그때 video_views 추가(그 전엔 운영 부담).
- **인덱스**: `idx_videos_grid_popular (grid_id, view_count DESC, created_at DESC) WHERE ACTIVE AND PUBLIC`.
- **지오코딩 경계**: Python 서버는 GeoJSON 메모리 판정만, R-tree·전용 테이블·로그는 DB에 안 둠.

주의: 이 문서의 "5초 제한"·일부 컬럼 구성은 v5 시점 기준 — 현행 정본은 V1__init.sql과 [[ERD 정렬 디자인 기준 데이터모델]] 참고 (예: 영상 30초 제한, push_tokens PK는 fcm_token).

## 출처
raw: `raw/confluence/2026-07-18 FillMap DB Schema v5 - MVP 개인 도감 (cf-14090329).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/14090329 (구조도 이미지는 원본에만)
