---
title: ERD 정렬 — 디자인 기준 데이터모델 결정 (현재 스키마 + 변경 집약)
type: research
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-19 ERD 정렬 디자인 기준 데이터모델 결정 — 현재 스키마 + 변경 집약 (cf-18874490).md"
created: 2026-07-19
updated: 2026-07-21
keywords: [ERD, 데이터모델, 스키마 변경, V1__init.sql, 14개 테이블, 소프트 삭제, Apple, zones, 시딩, 경계 귀속, 중심점, 스트릭, 뱃지, Redis, 팀 합의]
aliases: [ERD 정렬, 스키마 변경 집약]
related: ["[[FillMap DB Schema v5 MVP]]", "[[갭 분석 디자인 문서 코드 싱크]]", "[[PRD FillMap MVP 화면별 기능·API]]", "[[ADR 격자 표시명 zone]]", "[[FillMap API 설계 v2 draft]]", "[[2026-07-18 김태완 멘토 DB 피드백]]"]
---

# ERD 정렬 — 디자인 기준 데이터모델 결정 (현재 스키마 + 변경 집약)

> [!tldr]
> 현재 스키마(V1__init.sql 14개 테이블, users가 허브·reports만 CASCADE 예외)와 디자인 실현에 필요한 스키마 변경을 한곳에 집약한 팀 합의용 문서 — 결정을 대신하지 않음.
> MVP를 막는 스키마 변경: Apple provider(A-2)·계정 소프트 삭제(A-1)·닉네임 길이(A-3)·zones(C-1)·regions 시딩(C-2)·**격자↔행정동 경계 귀속 = 격자 중심점 규칙(C-5, 핵심)**·카운트 정본(C-3)·뱃지 마스터(D-2)·스트릭 갱신(D-1).
> 스키마 그대로 가능: 공개범위(B-1)·신고(F-3, enum 이미 있음)·grid_color 매핑. 인프라 선행: Redis(F-1·F-2). 확정되면 V2 마이그레이션 하나로 묶는다.

## 이 노트로 답할 수 있는 질문
- 현재 14개 테이블 구조와 관계는?
- MVP를 막는 스키마 변경 항목은 뭐고 어떤 순서로 정해야 하나?
- 격자와 행정동 경계가 걸칠 때 어떻게 귀속하기로 제안됐나?
- 신고 기능에 스키마 변경이 필요한가? (답: 불필요 — enum·status 이미 존재)
- regions.total_grid_count와 region_stats.total_count 중 정본은?
- Phase 2로 미뤄도 되는 항목은?

## 발견 (변경 집약)
- **A. users**: A-1 계정 삭제 막힘(reports FK) → soft delete 권장 · A-2 Apple CHECK 추가 · A-3 닉네임 20 vs 50 · A-4 닉네임 UNIQUE(P2) · A-5 grid_color 엔티티 매핑 누락.
- **B. videos**: B-1 공개범위 API 부재(전 영상 비공개 상태, MVP) · B-2 태그 컬럼 전무(P2?) · B-3 like_count 비정규화(P2) · B-4 AI 결과 저장 스키마 미설계.
- **C. 지역/표시명**: C-1 zones 신설 · C-2 GeoJSON 시딩(전국/서울 결정) · **C-5 경계 귀속 — 격자 대표 동 = ST_Contains(boundary, center_geom), 오차 ≤ ~50m, videos.region_code는 "실제 찍은 동" 기록으로 역할 분리, 저장은 grids.region_code 시딩 1회 vs 조회 시 계산 택1** · C-3 카운트 정본(C-5 선행) · C-4 집계 레벨(행정동 vs 시/도).
- **D. 게임화**: D-1 스트릭 갱신 주체(KST 주의) · D-2 뱃지 시딩+JSONB 포맷 · D-3 지급 주체(P2).
- **E. Social/알림**: 전부 P2 (초대코드·친구 도감·알림 설정·이력).
- **F. Auth/Moderation**: F-1 Redis+Refresh · F-2 블랙리스트 영속화 · F-3 신고는 API만.

## 시사점
팀 회의에서 🔧 항목부터 "간다/안 간다" 확정 → V2__*.sql 하나로 묶기 → 이 문서를 "확정 ERD"로 승격.

## 출처
raw: `raw/confluence/2026-07-19 ERD 정렬 디자인 기준 데이터모델 결정 — 현재 스키마 + 변경 집약 (cf-18874490).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18874490
