---
title: FillMap API 명세 v1 (구현 기준)
type: hub
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [API 명세, API spec, v1, 구현 기준, ApiResponseDto, 응답 래퍼, developCode, JWT, Bearer, 인증, 에러코드 대역, 미구현, 예정]
aliases: [API 명세, v1 명세, FillMap API]
related: ["[[Auth API]]", "[[Grid API]]", "[[Video API]]", "[[FillMap API 설계 v2 draft]]"]
---

# FillMap API 명세 v1 (구현 기준)

> [!tldr]
> 실제 구현된 REST API의 단일 진실(2026-07-17 코드 기준, 추측 없음): 컨트롤러 3개(Auth·Grid·Video), 엔드포인트 10개.
> 공통 규약: 모든 응답은 ApiResponseDto(developCode·httpStatus·message·body), JWT Bearer(1시간, refresh 없음), 퍼블릭은 /auth/signup·login·oauth뿐.
> developCode 대역: 1xxx user · 2xxx auth · 3xxx video · 4xxx grid. 미구현 목록(§4)과 v2 draft 관계도 정의 — 구현 기준은 언제나 이 문서.

## 이 노트로 답할 수 있는 질문
- 현재 구현된 API는 몇 개고 어디에 정리돼 있나?
- 공통 응답 래퍼 구조는?
- 인증 방식과 토큰 만료는? refresh token은 있나?
- developCode 대역 규칙은?
- 미구현·예정 API는 뭐가 있고 담당은 누구인가?
- v1 문서와 v2 draft의 관계는?

## 개요
- 구현: [[Auth API]](4) · [[Grid API]](2) · [[Video API]](4) — 총 10개.
- 응답 래퍼: `developCode`(성공 200)·`httpStatus`·`message`·`body`.
- 인증: JWT Bearer, TTL 1시간(PT1H), **refresh 없음** → 만료 시 재로그인. 퍼블릭: signup·login·oauth.
- 에러 대역: 1xxx user / 2xxx auth / 3xxx video / 4xxx grid / 4xx·5xx 공통.

## 미구현·예정 (§4 요약)
- 구현 도메인 내 누락: Refresh Token([[Auth 확장 API 예정 Refresh Token]]) · 재생 조회([[Video 재생 조회 API 예정]]) · 개인 도감([[Collection API 예정]]) — 전부 Owner B.
- 패키지 없음: [[User 프로필 API 예정]] · [[Region API 예정]] · [[Grid 확장 API 예정]] · [[Social API 예정]] · [[Notification API 예정]] · Moderation · 광고.
- ⚠️ status.md의 "✅ 완성"은 패키지 기준 — SA 기능 목록과 코드를 직접 대조할 것.
- AI Highlight-Blur는 별도 Python FastAPI 서버 소관.

## 하위 노트 목록
[[Auth API]] · [[Grid API]] · [[Video API]]

## 출처
raw: `raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891367
