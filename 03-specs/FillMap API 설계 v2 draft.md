---
title: FillMap API 설계 v2 draft (예정 API 허브)
type: hub
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 FillMap API 설계 — 예정 (v2 draft) (cf-17793077).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [API 설계, v2, draft, 예정, 근거 등급, developCode 대역, 선행 과제, Redis, 페이지네이션, Owner, 초안]
aliases: [v2 draft, 예정 API]
related: ["[[FillMap API 명세 v1]]", "[[Auth 확장 API 예정 Refresh Token]]", "[[User 프로필 API 예정]]", "[[Video 재생 조회 API 예정]]", "[[Collection API 예정]]", "[[Region API 예정]]", "[[Grid 확장 API 예정]]", "[[Social API 예정]]", "[[Notification API 예정]]"]
---

# FillMap API 설계 v2 draft (예정 API 허브)

> [!tldr]
> 앞으로 만들 API를 필드 수준까지 뽑아둔 초안 트리의 허브 — 경로·메서드는 전부 제안(🔴), 구현 기준은 언제나 v1. 구현되면 v1으로 승격 후 폐기.
> 근거 체계: 기능 목록은 SA/IA, 필드·타입은 V1__init.sql(테이블 14개 이미 존재), 경로·메서드는 어디에도 없음. 근거 등급 🟢스키마/🟡컨벤션/🔴제안.
> 최대 선행 과제는 **Redis 미도입**(Refresh Token·핫존·로그아웃 블랙리스트 3개가 걸림). 신규 대역 제안: 5xxx collection · 6xxx region · 7xxx social · 8xxx notification.

## 이 노트로 답할 수 있는 질문
- 예정 API 초안은 어떤 근거로 작성됐나 (SA/스키마/제안 구분)?
- v1과 v2 문서의 관계와 승격 규칙은?
- 도메인별 담당 Owner와 상태는?
- API보다 먼저 풀어야 할 선행 과제는 뭐가 있나?
- 왜 Redis가 가장 넓게 막고 있는 선행 과제인가?
- 신규 developCode 대역 제안은?

## 개요
- 범위: MVP 연장선 + Social·Notification (Moderation·광고 제외).
- ⚠️ "패키지 없음 = 미구현"이 아님 — auth가 "✅ 완성"인데 Refresh Token 누락. SA 기능 목록과 코드를 직접 대조할 것.

## 하위 노트 목록
| 노트 | 근거 테이블 | 담당 |
| --- | --- | --- |
| [[Auth 확장 API 예정 Refresh Token]] | 없음(Redis) | Owner B |
| [[User 프로필 API 예정]] | users | Owner B |
| [[Video 재생 조회 API 예정]] | videos | Owner B |
| [[Collection API 예정]] | user_grids·streaks·badges | Owner B |
| [[Region API 예정]] | regions·region_stats | Owner A |
| [[Grid 확장 API 예정]] | likes·videos | Owner A/B |
| [[Social API 예정]] | friendships | 미정 |
| [[Notification API 예정]] | push_tokens | 미정 |

## 선행 과제 (스키마가 없어서 못 쓴 것)
**Redis 미도입**(최상단 — Refresh·핫존·블랙리스트) · 영상 공개 범위 설정 API(없으면 격자 영상 목록 항상 빈 배열) · 친구 찾기 수단(Social 전체 블로커) · 알림 설정 테이블 · 뱃지 시딩+JSONB 포맷 · regions 시딩·region_stats 배치 · 계정 삭제 마이그레이션 · 핫존 Redis 스키마 · 태그 컬럼.

## 열린 질문
Social·Notification Owner · 신규 대역 확정 · Refresh 전달 방식(body vs httpOnly 쿠키) · 페이지네이션 offset vs cursor(첫 관례) · 닉네임 20 vs 50 · 친구 도감(Phase 2+ 보류) · status.md 정정.

## 출처
raw: `raw/confluence/2026-07-17 FillMap API 설계 — 예정 (v2 draft) (cf-17793077).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17793077
