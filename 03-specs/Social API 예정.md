---
title: Social API (예정) — 친구·차단
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Social API (예정) (cf-18448512).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Social, 소셜, 친구, friend, friendships, 친구 요청, 수락, 차단, block, 초대 코드, invite code, 방향성, PENDING, ACCEPTED, 예정 API]
aliases: [친구 API, 소셜 API]
related: ["[[FillMap API 설계 v2 draft]]", "[[Notification API 예정]]", "[[User 프로필 API 예정]]"]
---

# Social API (예정) — 친구·차단

> [!tldr]
> friendships 테이블 기반 친구 요청·수락/거절·목록·삭제·차단 설계 초안. 담당 미정 — Owner 배정이 선행.
> 스키마가 강제하는 것: 관계는 방향 있음(A→B ≠ B→A, 목록은 양방향 UNION), 자기 요청은 DB가 차단, 상태 4종(PENDING/ACCEPTED/REJECTED/BLOCKED).
> 최대 블로커: 상대 userId를 알 방법이 없음(닉네임 검색·이메일·초대 코드 전부 문제 있음) — **이게 없으면 Social 전체가 동작 불가.** 친구 도감은 Phase 2+ 기획 미확정이라 스펙 안 씀.

## 이 노트로 답할 수 있는 질문
- 친구 요청/수락/목록/차단 API의 잠정 설계는?
- friendships 스키마가 강제하는 규칙은 (방향·자기요청·상태)?
- 친구 목록 조회에 왜 양방향 UNION이 필요한가?
- 엇갈린 요청(서로 PENDING)은 어떻게 되나?
- 왜 초대 코드/사용자 검색이 최대 블로커인가?
- 친구 도감 조회 스펙은 왜 아직 안 쓰나?

## 설계 요지
- `POST /api/friends/requests` (addresseeId) → PENDING · `PATCH /api/friends/requests/{requesterId}` (ACCEPTED|REJECTED, responded_at 기록) · `GET /api/friends?status=` (기본 ACCEPTED, 양방향 UNION) · `DELETE /api/friends/{userId}` (row 삭제 vs REJECTED 보존 미정) · `POST /api/friends/{userId}/block` (UPSERT, 관계 없어도 차단 가능).
- 인덱스는 받은 요청 조회(addressee_id, status)에 최적.

## 열린 질문
Owner 미정(최우선) · 초대 코드/사용자 검색 부재(테이블 없음 — Social 전체 블로커) · 엇갈린 요청 처리 · 차단 방향성(양방향 판정, 노출 여부) · 친구 수 상한 · 친구 도감(Phase 2+, glossary "MVP는 개인 도감만"과 충돌 주의).

## 에러 코드 (제안, 7xxx 미확정)
7400 SELF_FRIEND_REQUEST · 7404 FRIENDSHIP_NOT_FOUND · 7409 FRIENDSHIP_ALREADY_EXISTS · 7403 FRIENDSHIP_BLOCKED. 대상 사용자 없음은 1404 재사용.

## 출처
raw: `raw/confluence/2026-07-17 Social API (예정) (cf-18448512).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18448512
