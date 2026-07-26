---
title: ADR region_stats recompute equi-join 치환 (MSG-236)
type: decision
product: fillmap
class: decision
status: active
source: "BE 레포 docs/MSG-236.md (feature/MSG-236-recompute-equi, b23e148)"
created: 2026-07-26
updated: 2026-07-26
keywords: [region_stats, recompute, refreshRegionStats, equi-join, equi, ST_Covers, geospatial, 수집률, 재계산, 점령, 롤백, grids.region_code, 행정동 라벨, 무라벨, no-op 가드, RegionRepository, 벤치, bench, EXPLAIN, MSG-236, MSG-167, MSG-155, MSG-165, seedLabeledGrid, GridFixtures]
aliases: [MSG-236 결정, recompute 단순화, 수집률 재계산 단순화, recompute equi 치환]
related: ["[[ADR 격자 행정동 라벨 grids.region_code]]", "[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]]", "[[Region API 예정]]", "[[FillMap 지도·격자 DB 설계 MVP]]"]
---

# ADR region_stats recompute equi-join 치환 (MSG-236)

> [!tldr]
> 수집률 재계산 쿼리(`RegionRepository.refreshRegionStats`)의 격자→행정동 귀속을 **ST_Covers LATERAL 2회 → `grids.region_code` equi-join**으로 치환 (MSG-167 §D6이 예약한 후속의 실행, 2026-07-26 구현 완료).
> 점령/롤백 쓰기 경로에서 공간 연산이 완전히 사라짐 — 라벨 저장 규칙이 구 쿼리와 동일(중심점 ST_Covers + `ORDER BY region_code LIMIT 1`)이라 결과 등가이고, 등가성은 167의 3중 일치 테스트로 고정돼 있음. 무라벨(해안) 격자는 `IS NOT NULL` 가드로 기존과 같은 no-op.
> **PR 전 잔여: 구/신 벤치 실측**(scripts/bench-msg236.sql, 미실행) — 성능 변경은 실측 비교가 채택 근거라는 팀 원칙. API·응답·스키마 무변경.

## 이 노트로 답할 수 있는 질문
- refreshRegionStats에서 ST_Covers가 왜/어떻게 사라졌나?
- 구 쿼리와 결과가 같다는 근거는 무엇인가? (등가성 논거·게이트)
- 무라벨(해안·무귀속) 격자는 치환 후 어떻게 처리되나? (no-op 가드)
- 이 변경의 영향 범위는? (쓰기 경로만 — 조회 API 무변경, main 코드 1파일)
- 채택 확정까지 남은 것은? (벤치 실측 → PR)
- 테스트 픽스처는 왜 seedLabeledGrid로 갈라졌나? (백필 테스트의 무라벨 계약 보존)

## 결정 요약
1. **치환 형태**: 구 쿼리의 LATERAL 2개(대상 격자 귀속 판정 + 분자 카운트의 점령 격자 전수 판정)를 각각 `JOIN regions tr ON tr.region_code = g.region_code` / `g2.region_code = tr.region_code` 로 대체. recompute UPSERT 틀(INSERT … SELECT … ON CONFLICT)은 무변경.
2. **등가성 논거**: `grids.region_code`는 격자 lazy insert 시 구 쿼리와 동일 규칙(중심점 ST_Covers + 동일 타이브레이크)으로 1회 판정해 저장한 값. 저장값 = 라이브 판정값은 MSG-167의 3중 일치 테스트(저장 라벨 · by-grid · recompute 귀속)로 고정.
3. **무라벨 no-op 가드**: `WHERE … AND g.region_code IS NOT NULL` — 구 쿼리의 "LATERAL empty → 무변경 no-op"과 등가 (equi JOIN도 NULL을 탈락시키지만 의도를 명시).
4. **게이트 통과**: RegionStatsRecomputeTest 11 · CommandService 2 · Concurrency(MSG-165 회귀) 1 · PointGridQueryService 9 = 23개 테스트 equi 전환 후 전건 통과. 픽스처는 `seedLabeledGrid` 신설(기존 `seedGrid`는 백필 테스트의 무라벨 계약 보존을 위해 유지).
5. **채택 게이트(잔여)**: `scripts/bench-msg236.sql` — 구/신 팔을 K=10/100/1,000(점령 격자 수) 스윕, EXPLAIN(ANALYZE,BUFFERS) + p50/p95/p99 (iters 300), SELECT부만 측정, 단일 트랜잭션 ROLLBACK 원복. **부하테스트 아님(쿼리 단건 측정)**. 실측 후 PR.

## 영향 범위
- main 코드 변경은 `region/repository/RegionRepository.java` 1파일 (+13/−22). 조회 API·응답 계약·DB 스키마 무변경 — 점령/롤백 트랜잭션 내부의 쓰기 경로만.
- 호출 체인: VideoService(점령/롤백) → RegionStatsCommandServiceImpl.refresh → advisory lock(MSG-165) → **refreshRegionStats(치환 지점)**.
- 시스템 전체 geospatial 사용처는 이제 쓰기 시 1회 라벨 판정(lazy insert·백필)과 역지오코딩 단건(resolveByPoint)만 남음.

## 브랜치 상태 (2026-07-26)
- `feature/MSG-236-recompute-equi` origin 푸시됨, HEAD b23e148. 커밋 6개(docs 4 · feat 1 · test 1), develop 대비 8파일 +612/−31.
- 잔여: 벤치 실행 → 결과를 docs/MSG-236.md에 기록·채택 판정 → PR(develop). 리캡 대시보드: https://claude.ai/code/artifact/df3f2f68-fa1d-4b79-b1ca-49465933f29f

## 출처
raw: `BE 레포 docs/MSG-236.md · scripts/bench-msg236.sql · git diff develop...feature/MSG-236-recompute-equi (b23e148)`
