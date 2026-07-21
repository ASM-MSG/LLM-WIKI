---
title: Auth 확장 API (예정) — Refresh Token
type: spec
product: fillmap
class: log
status: archived
source: "raw/confluence/2026-07-17 Auth 확장 API (예정) — Refresh Token (cf-17891459).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Refresh Token, 리프레시 토큰, 재발급, 회전, rotation, 재사용 감지, reuse detection, Redis, 블랙리스트, httpOnly 쿠키, TTL, JWT, Owner B, 예정 API]
aliases: [리프레시 토큰 API, auth refresh]
related: ["[[Auth API]]", "[[FillMap API 설계 v2 draft]]", "[[FillMap API 명세 v1]]"]
---

# Auth 확장 API (예정) — Refresh Token

> [!info] 2026-07-21 MSG-135로 구현 완료 — 구현 기준은 [[Auth API]] 참조. 이 문서는 설계 초안 기록으로만 남긴다.

> [!tldr]
> **구현 완료(MSG-135)**: 경로는 설계안 /auth/refresh 대신 `POST /api/auth/reissue`(퍼블릭)로 확정. RefreshTokenService + RefreshTokenProvider/RefreshTokenStore(Redis 구현체 RedisRefreshTokenStore), refresh TTL 2주(P14D, 슬라이딩).
> 로테이션(재발급마다 회전+직전 토큰 즉시 무효화) + 재사용 감지(회전된 토큰 재사용 시 디바이스 세션 체인 폐기) 구현. 전달은 하이브리드 — 웹 HttpOnly 쿠키 / 앱 body(X-Client-Type 헤더).
> Redis 의존성(spring-boot-starter-data-redis) 도입 완료, 로그아웃 블랙리스트도 RedisInvalidatedTokenStore로 영속화됨. login/oauth 응답에 refreshToken 추가, logout은 디바이스 refresh 세션 삭제 포함.

## 이 노트로 답할 수 있는 질문
- refresh token이 왜 지금 필요한가 (TTL 딜레마)?
- POST /auth/refresh는 왜 인증 불필요인가?
- 도입 시 기존 API 3개는 어떻게 바뀌나?
- 회전·재사용 감지란 뭔가?
- Redis 선행 과제는 구체적으로 뭔가?
- 로그아웃 블랙리스트의 현재 한계는?
- access/refresh 만료 에러 코드를 왜 나누나?

## 설계 요지 → 구현 결과 (MSG-135)
- 설계안 `POST /auth/refresh` → 실제 `POST /api/auth/reissue`. 요청: 웹=쿠키 / 앱=body(refreshToken) → accessToken + 회전 신규 refreshToken.
- LoginResponseDto에 refreshToken 추가(login·oauth 공유), logout은 디바이스 refresh 세션 삭제 포함 — 설계대로 반영.
- 회전 1회용 + 재사용 감지(REFRESH_TOKEN_REUSE_DETECTED 시 세션 체인 폐기)까지 MVP에 포함됨.
- 저장: Redis(RedisRefreshTokenStore) — 디바이스별 세션(X-Device-Id), TTL P14D 슬라이딩.
- 블랙리스트: InMemoryInvalidatedTokenStore → RedisInvalidatedTokenStore로 이관 완료(인터페이스 유지).

## 열린 질문 (당시) → 결론
전달 방식: 하이브리드(웹 HttpOnly 쿠키 / 앱 body, X-Client-Type) · refresh TTL: 2주 · access TTL: 1시간 유지 · 재사용 감지: 포함 · 기기별 다중 세션: X-Device-Id로 지원 · 토큰 형식: JWT(JwtRefreshTokenProvider).

## 에러 코드 (구현 확정)
2431 INVALID_REFRESH_TOKEN · 2432 EXPIRED_REFRESH_TOKEN · 2433 REFRESH_TOKEN_REUSE_DETECTED — `AuthErrorCode`에 존재.

## 출처
raw: `raw/confluence/2026-07-17 Auth 확장 API (예정) — Refresh Token (cf-17891459).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891459
