---
title: ADR 영속 계층 JPA 유지 — MyBatis 전환 반려
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-08-03 설계결정 영속 계층 JPA 유지 — MyBatis 전환 반려 (2026-08-03) (cf-29917209).md"
created: 2026-08-03
updated: 2026-08-03
keywords: [JPA, MyBatis, 마이바티스, ORM, 영속 계층, persistence, 쿼리 전략, query strategy, 네이티브 쿼리, nativeQuery, native query, ON CONFLICT, upsert, PostGIS, Hibernate, Hibernate Spatial, Spring Data JPA, QueryDSL, OpenFeign querydsl, JdbcClient, jOOQ, SqlResultSetMapping, 하이브리드, hybrid, 전환 반려, Reject, 채택 판정]
aliases: [JPA vs MyBatis, MyBatis 전환 검토, 영속 계층 결정, 쿼리 전략 ADR, ORM 교체 반려]
related: ["[[ADR region_stats recompute equi-join 치환]]", "[[ADR 격자 행정동 라벨 grids.region_code]]"]
---

# ADR 영속 계층 JPA 유지 — MyBatis 전환 반려

> [!tldr]
> 네이티브 쿼리 비중 증가("이럴 거면 MyBatis?")를 계기로 영속 계층을 정식 판정 — **Spring Data JPA + 전략적 네이티브 유지, MyBatis 전면 전환 반려** (2026-08-03, 판정 등급 Reject).
> 근거: 네이티브 ~50곳(커스텀 쿼리의 ~70%)은 전부 PostgreSQL 전용 기능(ON CONFLICT upsert·PostGIS·advisory lock·원자 카운터) 때문 — MyBatis로 가도 같은 SQL을 XML 매퍼에 손으로 쓰므로 한 줄도 안 줄고, 파생 파인더 14곳·엔티티 13개 매핑·Hibernate Spatial만 잃는다. pain 신호 0건, JPA→MyBatis 전면 전환 사례 보고는 한·영 모두 부재.
> 번복 트리거: 동적 조건 조립 쿼리 증식 또는 DTO 매핑 보일러플레이트 반복 지적 — 그때도 1순위는 전면 교체가 아니라 JPA 옆에 QueryDSL(OpenFeign 포크)·JdbcClient·jOOQ 추가.

## 이 노트로 답할 수 있는 질문
- 네이티브 쿼리가 많은데 JPA를 유지하는 근거는? (실측 수치 포함)
- MyBatis로 전환하면 무엇이 좋아지고 무엇을 잃나? (트레이드오프)
- 우리 네이티브 쿼리 ~50곳은 왜 존재하나? (PostgreSQL 전용 기능 목록)
- 이 결정을 뒤집는 조건과 그때의 대안은? (QueryDSL 포크·JdbcClient·jOOQ)
- QueryDSL을 쓰게 되면 어떤 좌표를 써야 하나? (원본 방치·OpenFeign 포크)
- 이 판정의 방법·근거 출처는? (실측 grep·선례 조사·외부 소스)

## 결정 요약
1. **유지**: Spring Data JPA(Hibernate + Hibernate Spatial) + 전략적 native `@Query` 하이브리드 — `project-conventions.md`의 "Repository는 JpaRepository 상속 + native UPSERT는 `@Modifying @Query nativeQuery = true`" 컨벤션 그대로.
2. **반려**: MyBatis 전면 전환. 전환해도 네이티브 SQL은 위치만 이동(애너테이션→XML)하고, 파생 파인더·엔티티 매핑·Hibernate Spatial을 수작업으로 재작성해야 함. MyBatis용 PostGIS TypeHandler 생태계는 방치 상태(마지막 커밋 2018).
3. **실측 (2026-08-03 grep)**: 네이티브 ~50곳(11/13 리포지토리 — Video 15·UserBadge 9·Region 7·Grid 5) · JPQL `@Query` 6곳 · 파생 파인더 14곳 · 엔티티 13개. 네이티브 사유는 전부 PostgreSQL 전용: ON CONFLICT upsert 6종, ST_Covers/ST_Area/ST_GeomFromGeoJSON, pg_advisory_xact_lock, KST CASE(스트릭), GREATEST 원자 카운터.
4. **선례·pain**: 팀 차원 MyBatis 검토 이력 0건(레포·위키·PR·Jira). 교체 요구 이슈·TODO 0건. "순수 aggregate만 native" 패턴이 MSG-154·155·166·222 등 스펙 8건+에 일관 적용 — 네이티브 비중은 설계의 결과.
5. **외부 근거**: "JPA CRUD + QueryDSL/native 복잡 쿼리"가 한국 실무 표준(우아한형제들 정산시스템 실명 사례). JPA→MyBatis 전면 전환 후기 부재. mybatis-spring-boot-starter 자체는 건재 — 반려 사유는 "MyBatis가 나빠서"가 아니라 "전환으로 얻는 게 없어서".

## 번복 트리거와 대안 경로
- 동적 조건 조립 쿼리(관리자 검색류)가 문자열 조립식 네이티브로 증식하거나, `@SqlResultSetMapping`류 DTO 매핑 보일러플레이트가 리뷰마다 반복되면 재검토.
- 그때의 1순위 = **JPA 옆에 추가**: QueryDSL은 반드시 OpenFeign 포크 좌표(`io.github.openfeign.querydsl` — 원본 `com.querydsl`은 2021년 이후 방치, Spring Data도 포크로 이관 중) · Spring `JdbcClient`(Framework 6.1+) · jOOQ(PostgreSQL 대상 Apache 2.0 무료).
- 참고: 현행 Hibernate(6.5+)는 `ON CONFLICT`를 HQL로 지원 — 네이티브 upsert 일부 축소 가능하나 현행 컨벤션이 안정적이라 필수 아님.

## 출처
raw: `raw/confluence/2026-08-03 설계결정 영속 계층 JPA 유지 — MyBatis 전환 반려 (2026-08-03) (cf-29917209).md` · BE 레포 grep 실측(src/main, develop c38c02e) · 외부: techblog.woowahan.com/2662 · github.com/mybatis/spring-boot-starter releases · github.com/OpenFeign/querydsl releases · spring-data-jpa#3335 · jooq.org/legal/licensing · github.com/eyougo/mybatis-typehandlers-postgis
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/29917209
