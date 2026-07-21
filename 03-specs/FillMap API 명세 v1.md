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
> 실제 구현된 REST API의 단일 진실(2026-07-21 코드 기준, 추측 없음): 컨트롤러 5개(Auth·DevAuth·Grid·GridVideo·Video), 엔드포인트 14개.
> 공통 규약: 모든 응답은 ApiResponseDto(developCode·httpStatus·message·body), JWT Bearer(access 1시간 + refresh 2주 — MSG-135: Redis 저장·로테이션·재사용 감지·블랙리스트, POST /api/auth/reissue로 재발급).
> 퍼블릭: /auth/signup·login·oauth·reissue + /auth/dev/social-login(local/dev 프로파일 전용). developCode 대역: 1xxx user · 2xxx auth · 3xxx video · 4xxx grid.

## 이 노트로 답할 수 있는 질문
- 현재 구현된 API는 몇 개고 어디에 정리돼 있나?
- 공통 응답 래퍼 구조는?
- 인증 방식과 토큰 만료는? refresh token은 있나?
- developCode 대역 규칙은?
- 미구현·예정 API는 뭐가 있고 담당은 누구인가?
- v1 문서와 v2 draft의 관계는?

## 개요
- 구현: [[Auth API]](5 + dev 전용 1) · [[Grid API]](2) · GridVideo(2) · [[Video API]](4) — 총 14개, 컨트롤러 5개.
- 응답 래퍼: `developCode`(성공 200)·`httpStatus`·`message`·`body`.
- 인증: JWT Bearer — access TTL 1시간(PT1H) + **refresh 2주(P14D, MSG-135 구현)**. Redis 저장, 디바이스별 세션, 로테이션+재사용 감지, 로그아웃 시 access 블랙리스트(Redis). 재발급은 `POST /api/auth/reissue`(웹=HttpOnly 쿠키, 앱=body).
- 퍼블릭: signup·login·oauth·reissue + dev/social-login(local/dev 프로파일 전용, prod 미노출).
- 에러 대역: 1xxx user / 2xxx auth / 3xxx video / 4xxx grid / 4xx·5xx 공통.

### GridVideo (격자 상세 — video 패키지, Owner B)
- `GET /api/grids/{gridId}/my-videos` (MSG-127) — 그 격자에 내가 올린 영상 리스트, createdAt DESC. 항목: videoId·thumbnailUrl(presigned GET, READY 전 null)·processingStatus·durationSec·createdAt. 미점령/타인 격자/없는 gridId는 빈 배열. 상세: 레포 `docs/MSG-127.md`.
- `GET /api/grids/{gridId}/cover` (MSG-87) — 격자 전역 대표 영상 1건. PUBLIC·READY 중 조회수→최신 순, 본인·타인 모두 후보. 응답: videoId·thumbnailUrl·durationSec·viewCount·recordedAt, 후보 없으면 body null. 작성자 정보 미포함(프라이버시). 상세: 레포 `docs/MSG-87.md`.

## 미구현·예정 (§4 요약)
- 구현 도메인 내 누락: 재생 조회([[Video 재생 조회 API 예정]]) · 개인 도감([[Collection API 예정]]) — 전부 Owner B. (Refresh Token은 MSG-135로 구현 완료 → [[Auth API]])
- 패키지 없음: [[User 프로필 API 예정]] · [[Region API 예정]] · [[Grid 확장 API 예정]] · [[Social API 예정]] · [[Notification API 예정]] · Moderation · 광고.
- ⚠️ status.md의 "✅ 완성"은 패키지 기준 — SA 기능 목록과 코드를 직접 대조할 것.
- AI Highlight-Blur는 별도 Python FastAPI 서버 소관.

## 하위 노트 목록
[[Auth API]] · [[Grid API]] · [[Video API]]

## 출처
raw: `raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891367
