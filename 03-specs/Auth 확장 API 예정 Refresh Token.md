---
title: Auth 확장 API (예정) — Refresh Token
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Auth 확장 API (예정) — Refresh Token (cf-17891459).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Refresh Token, 리프레시 토큰, 재발급, 회전, rotation, 재사용 감지, reuse detection, Redis, 블랙리스트, httpOnly 쿠키, TTL, JWT, Owner B, 예정 API]
aliases: [리프레시 토큰 API, auth refresh]
related: ["[[Auth API]]", "[[FillMap API 설계 v2 draft]]", "[[FillMap API 명세 v1]]"]
---

# Auth 확장 API (예정) — Refresh Token

> [!tldr]
> SA는 "JWT 발급·Refresh Token 회전"을 요구하지만 코드에 refresh 문자열 0건 — status.md의 "✅ 완성"은 SA 대비 완성이 아님. 현재는 access 1시간 만료 시 재로그인뿐.
> 설계: POST /auth/refresh(인증 불필요·퍼블릭 경로 추가), 회전 시 기존 토큰 폐기+신규 발급, 저장은 Redis. 도입 시 login/oauth/logout 응답·동작이 바뀜(logout은 refresh도 폐기).
> ⚠️ Redis 의존성 자체가 build.gradle에 없음 — 의존성+인스턴스 준비가 선행. 로그아웃 블랙리스트 영속화(InMemory→Redis 구현체 교체)도 이때 같이 푸는 게 맞음.

## 이 노트로 답할 수 있는 질문
- refresh token이 왜 지금 필요한가 (TTL 딜레마)?
- POST /auth/refresh는 왜 인증 불필요인가?
- 도입 시 기존 API 3개는 어떻게 바뀌나?
- 회전·재사용 감지란 뭔가?
- Redis 선행 과제는 구체적으로 뭔가?
- 로그아웃 블랙리스트의 현재 한계는?
- access/refresh 만료 에러 코드를 왜 나누나?

## 설계 요지
- `POST /auth/refresh` — body: refreshToken → accessToken·refreshToken(회전 신규)·expiresInSec.
- 영향: LoginResponseDto에 refreshToken 추가(login·oauth 공유), logout은 refresh 폐기 추가.
- 회전: 1회용 전제. 재사용 감지는 복잡도 대비 MVP 포함 여부 결정 필요.
- 저장: Redis — 키 구조·TTL·값·장애 시 폴백 전부 미설계.
- 현 블랙리스트는 InMemoryInvalidatedTokenStore: 재시작 시 부활·다중 인스턴스 무공유. 인터페이스 분리돼 있어 Redis 구현체 추가로 해결.

## 열린 질문
전달 방식 body vs httpOnly 쿠키(웹 첫 타깃 — 중요) · refresh TTL(2주/30일) · access TTL 단축(15분?) · 재사용 감지 · 기기별 다중 세션 · JWT vs 불투명 랜덤 문자열(후자가 폐기 확실) · status.md 정정.

## 에러 코드 (제안)
2431 INVALID_REFRESH_TOKEN · 2432 EXPIRED_REFRESH_TOKEN(재로그인 유도 — access 만료와 구분해야 무한 루프 방지) · 2433 REFRESH_TOKEN_REUSED(도입 시).

## 출처
raw: `raw/confluence/2026-07-17 Auth 확장 API (예정) — Refresh Token (cf-17891459).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891459
