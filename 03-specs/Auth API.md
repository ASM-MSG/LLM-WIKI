---
title: Auth API (v1 구현 기준)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-17 Auth API (cf-18448445).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Auth, 인증, 로그인, login, 회원가입, signup, 로그아웃, logout, 소셜 로그인, OIDC, oauth, JWT, accessToken, 에러 코드]
aliases: [인증 API, 어스 API]
related: ["[[FillMap API 명세 v1]]", "[[Auth 확장 API 예정 Refresh Token]]"]
---

# Auth API (v1 구현 기준)

> [!tldr]
> 인증/회원 도메인, base `/api/auth`. 회원가입·로컬 로그인·로그아웃·소셜 로그인(OIDC)·토큰 재발급(reissue) 5개 + dev 전용 소셜 로그인 모의 1개 = 6개 구현.
> 로그인 응답은 accessToken(1시간) + refreshToken(2주, MSG-135) — 웹은 HttpOnly 쿠키, 앱은 body(X-Client-Type). Redis 저장·로테이션·재사용 감지·로그아웃 블랙리스트.
> 에러 코드는 Auth 2xxx, User 1xxx 체계.

## 이 노트로 답할 수 있는 질문
- 회원가입/로그인/로그아웃/소셜 로그인의 경로와 요청·응답 필드는?
- 비밀번호 검증 규칙은?
- 소셜 로그인은 어떤 방식(OIDC)이고 요청에 뭘 보내나?
- Auth 도메인 에러 코드(2xxx)는 뭐가 있나?
- refresh token은 구현돼 있나?

## 엔드포인트
| 메서드/경로 | 인증 | 핵심 |
| --- | --- | --- |
| `POST /api/auth/signup` | 불필요 | email·password(8~64, 영문+숫자)·nickname(2~20). 409 EMAIL_ALREADY_EXISTS |
| `POST /api/auth/login` | 불필요 | email·password → accessToken + refreshToken(웹=HttpOnly 쿠키/앱=body). X-Device-Id 헤더 없으면 서버 생성 후 응답 헤더로 반환 |
| `POST /api/auth/logout` | 필요 | Bearer 토큰 무효화(Redis 블랙리스트) + 해당 디바이스 refresh 세션 삭제. X-Device-Id 없으면 전 디바이스 삭제. 응답 null |
| `POST /api/auth/oauth/{provider}` | 불필요 | OIDC idToken → accessToken + refreshToken. 미지원 provider는 2422 |
| `POST /api/auth/reissue` | 불필요 | refresh(웹=쿠키/앱=body)로 새 access + 회전된 새 refresh 발급. 회전된 옛 토큰 재사용 시 세션 체인 폐기 (MSG-135) |
| `POST /api/auth/dev/social-login` | 불필요 | **local/dev 프로파일 전용(prod 미노출)**. ID Token 검증 없이 (provider, oid)로 find-or-create 후 토큰 발급. refresh는 body |

## 에러 코드
- Auth 2xxx: 2401 INVALID_TOKEN · 2402 EXPIRED_TOKEN · 2403 UNAUTHENTICATED · 2411 INVALID_CREDENTIALS · 2421 INVALID_ID_TOKEN · 2422 UNSUPPORTED_PROVIDER · 2431 INVALID_REFRESH_TOKEN · 2432 EXPIRED_REFRESH_TOKEN · 2433 REFRESH_TOKEN_REUSE_DETECTED
- User 1xxx: 1404 USER_NOT_FOUND · 1409 EMAIL_ALREADY_EXISTS

## 출처
raw: `raw/confluence/2026-07-17 Auth API (cf-18448445).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18448445
