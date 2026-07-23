---
title: FillMap API 스펙 통합 (전체 한눈에)
type: hub
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-22 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md, raw/confluence/2026-07-17 FillMap API 설계 — 예정 (v2 draft) (cf-17793077).md, raw/confluence/2026-07-22 개인 도감 화면 — 확정 UX·API 설계 (수집률·탐험률) (cf-21528615).md, raw/confluence/2026-07-21 FillMap AI Highlight-Blur — 레포 생성부터 dev 배포까지 (cf-21102593).md"
created: 2026-07-22
updated: 2026-07-23
keywords: [API 스펙, API 명세, 통합, 전체, 한눈에, one page, 멘토링, 스펙 점검, 구현 현황, 예정 API, 에러 코드, developCode, jobs API, AI 서버, 열린 질문]
aliases: [API 통합 뷰, API 전체 스펙, API 스펙 한눈에]
related: ["[[FillMap API 명세 v1]]", "[[FillMap API 설계 v2 draft]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[2026-07-21 AI Highlight-Blur 개발 기록]]", "[[2026-07-16 박원형 멘토 멘토링]]"]
---

# FillMap API 스펙 통합 (전체 한눈에)

> [!tldr]
> 흩어진 API 노트 13개를 한 페이지로 모은 통합 뷰 — 멘토링 "API 스펙 점검"(0714 박원형 액션 아이템) 대비용.
> 구현 ✅ 17개(BE) + AI 서버 3개, 구현 예정 🔜 1개(MSG-153), 제안 📝 약 20개.
> 상세 필드·쟁점은 각 도메인 노트가 정본 — 이 페이지는 목차이자 현황판. 상태가 바뀌면 여기도 갱신한다.

## 이 노트로 답할 수 있는 질문
- 지금까지 정의된 API 전체가 몇 개고 각각 상태는?
- 구현/예정/제안 구분과 담당 Owner는?
- 공통 규약(응답 래퍼·인증·에러 대역)은?
- 멘토링 스펙 점검에서 짚일 만한 열린 결정은 뭐가 있나?

**범례**: ✅ 구현(merge) · 🔜 구현 예정(티켓 확정) · 📝 draft(경로·메서드는 제안) · ⛔ 블로커 있음

## 0. 공통 규약
- **응답 래퍼**: 모든 응답 `ApiResponseDto` — `developCode`(성공 200)·`httpStatus`·`message`·`body`
- **인증**: JWT Bearer — access 1시간(PT1H) + refresh 2주(P14D, MSG-135). Redis 저장·디바이스별 세션(X-Device-Id)·로테이션+재사용 감지·로그아웃 블랙리스트. 재발급 `POST /api/auth/reissue`(웹=HttpOnly 쿠키 / 앱=body, X-Client-Type)
- **퍼블릭 경로**: signup·login·oauth·reissue (+ dev/social-login은 local/dev 프로파일 전용)
- **에러 대역**: 1xxx user · 2xxx auth · 3xxx video · 4xxx grid — 확정 / 5xxx collection · 6xxx region · 7xxx social · 8xxx notification — **제안(미확정)**
- **페이지네이션 관례**: cursor 방식 (MSG-90 `GET /api/grids`가 첫 확정)

## 1. 구현된 API — BE (✅ 17개)

### Auth — `/api/auth` (6개) → [[Auth API]]
| API | 인증 | 핵심 |
| --- | --- | --- |
| `POST /api/auth/signup` | — | email·password(8~64, 영문+숫자)·nickname(2~20). 1409 중복 |
| `POST /api/auth/login` | — | → access + refresh(웹 쿠키/앱 body). X-Device-Id 없으면 서버 생성 |
| `POST /api/auth/logout` | 필요 | access 블랙리스트 + 해당 디바이스 refresh 세션 삭제 |
| `POST /api/auth/oauth/{provider}` | — | OIDC idToken → 토큰 발급. 미지원 provider 2422 |
| `POST /api/auth/reissue` | — | refresh로 재발급 + 회전. 재사용 감지 시 세션 체인 폐기 (MSG-135) |
| `POST /api/auth/dev/social-login` | — | **local/dev 전용, prod 미노출**. 검증 없이 find-or-create |

에러: 2401 INVALID_TOKEN · 2402 EXPIRED_TOKEN · 2403 UNAUTHENTICATED · 2411 INVALID_CREDENTIALS · 2421 INVALID_ID_TOKEN · 2422 UNSUPPORTED_PROVIDER · 2431~2433 refresh 3종 / 1404 USER_NOT_FOUND · 1409 EMAIL_ALREADY_EXISTS

### Grid — `/api/grids` (2개, 전부 인증) → [[Grid API]]
| API | 핵심 |
| --- | --- |
| `GET /api/grids/{gridId}` | 단일 격자 셀. gridId `{grid_y}_{grid_x}`. 미점령이어도 200 (occupied=false) |
| `GET /api/grids` | 뷰포트 색칠 격자 (MSG-90). swLat·swLng·neLat·neLng + cursor·size(기본 1000, 최대 5000). bbox 한 변 최대 0.5도 |

에러: 4400 INVALID_GRID_ID · 4401 INVALID_VIEWPORT · 4402 VIEWPORT_TOO_LARGE · 4403 INVALID_CURSOR · 4404 INVALID_PAGE_SIZE

### GridVideo — `/api/grids/{gridId}/…` (2개, video 패키지 Owner B)
| API | 핵심 |
| --- | --- |
| `GET /api/grids/{gridId}/my-videos` | 그 격자의 내 영상 리스트, createdAt DESC (MSG-127). 미점령/타인 격자는 빈 배열 |
| `GET /api/grids/{gridId}/cover` | 격자 전역 대표 영상 1건 — PUBLIC·READY 중 조회수→최신 (MSG-87). 작성자 미포함 |

### Video — `/api/videos` (4개, 전부 인증) → [[Video API]]
| API | 핵심 |
| --- | --- |
| `POST /api/videos/presigned-url` | extension(mp4/mov)·contentType·contentLength → uploadUrl·s3Key |
| `POST /api/videos` | s3Key·lat·lon·durationSec(1~30)·recordedAt → 메타 저장 + 격자 점령. s3Key 3중 검증(MSG-132) |
| `PUT /api/videos/{videoId}` | 본인만. 좌표 지정 시 같은 격자 검사(3422 GRID_MISMATCH) |
| `DELETE /api/videos/{videoId}` | 본인만. 격자 내 0개 되면 점령 롤백 |

에러: 3400 INVALID_COORDINATE · 3401 INVALID_S3_KEY · 3402 UPLOAD_NOT_FOUND · 3403 VIDEO_FORBIDDEN · 3404 VIDEO_NOT_FOUND · 3413 FILE_TOO_LARGE · 3415 UNSUPPORTED_EXTENSION · 3422 GRID_MISMATCH

### Collection·Region — v1 명세 이후 merge (3개) ⚠️ v1 문서 미반영
| API | 핵심 | 티켓 |
| --- | --- | --- |
| `GET /api/collections/summary` | 도감 요약 — totalGridCount·totalVideoCount·badgeCount·streak 등 | MSG-152 |
| `GET /api/regions/reverse-geocode` | 좌표 → 행정동 판정 (resolveByPoint) | MSG-93 |
| `GET /api/regions/stats` | 행정동별 탐험률 — collectedCount·totalCount·progressRate(100 clamp) | MSG-156 |

상세 계약은 [[개인 도감 화면 확정 UX·API 설계]] + Swagger가 정본. **[[FillMap API 명세 v1]]에 아직 승격 안 됨 — 갱신 필요.**

## 2. 구현 예정 (🔜 티켓 확정)
| API | 핵심 | 근거 |
| --- | --- | --- |
| `GET /api/collections/grids` (+격자 클릭 상세) | 최근 수집 격자 **RECENT 고정·30개·페이지네이션 없음** + 클릭 시 소속 행정동 탐험률 동봉. PO 확정 UX | MSG-153 · [[개인 도감 화면 확정 UX·API 설계]] |
| 영상 공개 범위 변경 | visibility 기본 PRIVATE → 공개 전환. **없으면 전역 목록·cover가 항상 빈 결과** ⛔ | MSG-162 |

## 3. 제안 단계 (📝 경로·메서드는 draft — 정본은 각 노트)

### User 프로필 (Owner B) → [[User 프로필 API 예정]]
`GET /api/users/me` · `PATCH /api/users/me`(nickname·gridColor 8색·profileImageUrl) · `DELETE /api/users/me`
⛔ 계정 삭제는 reports FK 때문에 하드 삭제 불가 — 소프트/NULL/익명화 결정 + 마이그레이션 선행. 쟁점: 닉네임 20 vs 50, 닉네임 UNIQUE 없음

### Video 재생 (Owner B) → [[Video 재생 조회 API 예정]]
`GET /api/videos/{videoId}` — playbackUrl 발급. DELETED→3404 · PRIVATE+타인→3403 · READY 아니면 playbackUrl=null
쟁점: presigned GET vs encoded_url, view_count 증가 시점, BLINDED 응답 미정

### Collection 잔여 (Owner B) → [[Collection API 예정]]
`GET /api/collections/grids/{gridId}/videos` · `GET /api/collections/badges?earnedOnly=`
⛔ 뱃지 마스터 시딩 없음(빈 배열) + progress JSONB 포맷 미정. 스트릭 갱신 주체·KST 타임존 미정

### Region 잔여 (Owner A) → [[Region API 예정]]
`GET /api/regions/search?q=` (DB 3,558개로 완결, SDK 불필요) · `GET /api/regions/{code}` · `GET /api/regions/{code}/boundary`(GeoJSON, 무거워서 분리)
쟁점: 랜드마크 검색("홍대")은 [[ADR 격자 표시명 zone]]과 같은 뿌리, 시/도 상위 집계는 MVP 이후

### Grid 확장 (Owner A/B) → [[Grid 확장 API 예정]]
`GET /api/grids/{gridId}/videos`(전역 목록 — 남의 영상 포함) · `POST/DELETE /api/videos/{videoId}/likes`(멱등 UPSERT) · `GET /api/grids/hot`
⛔ 전역 목록은 MSG-162(공개 전환) 선행. 핫존은 Redis 스키마 설계 티켓부터

### Social (Owner 미정) → [[Social API 예정]]
`POST /api/friends/requests` · `PATCH /api/friends/requests/{requesterId}` · `GET /api/friends?status=` · `DELETE /api/friends/{userId}` · `POST /api/friends/{userId}/block`
⛔ **상대 userId를 알 방법이 없음**(검색·초대 코드 부재) — Social 전체 블로커

### Notification (Owner 미정) → [[Notification API 예정]]
`POST /api/notifications/tokens`(FCM, **반드시 UPSERT**) · `DELETE /api/notifications/tokens?fcmToken=`
그 외(설정·목록·읽음)는 테이블이 없어 스펙 불가. FCM vs SSE 미확정

## 4. AI 서버 API — 별도 FastAPI (dev 배포 완료, BE 연동 대기)
| API | 핵심 |
| --- | --- |
| `POST /jobs` | 즉시 202 + job_id. 단일 워커 큐 순차 처리 |
| `GET /jobs/{id}` | 폴링. 상태 `QUEUED → PROCESSING → DONE\|FAILED` — PROCESSING = BE `processing_status=BLURRING` |
| `GET /jobs/{id}/video` | 결과 다운로드. 1080p 30초 E2E 실측 4.3분 |

AGPL 때문에 별도 레포·HTTP 통신 — [[2026-07-21 AI Highlight-Blur 개발 기록]] · [[ADR AI 처리 실행 환경 FastAPI]]

## 5. 열린 결정 (스펙 점검에서 짚일 후보)
1. **v1 명세 문서가 코드보다 뒤처짐** — merge된 3개(§1 마지막 표) 승격 필요
2. **MSG-162 공개 범위 전환 API** — 전역 노출 기능 전체의 전제 ⛔
3. developCode 신규 대역(5~8xxx) 미확정
4. 닉네임 길이 20 vs 50 불일치 · UNIQUE 없음
5. 계정 삭제 방식 (FK 제약)
6. view_count 증가 시점·중복 방지 (격자 대표 영상 품질 좌우)
7. BLINDED 영상 응답 (403+사유 vs 404)
8. Social·Notification Owner 미정 + 친구 찾기 수단 부재
9. 탐험률 조회 형태 — FE 2-call vs BE 1-call 통합 (MSG-153 쟁점)
10. AI jobs API의 BE 연동 계약(콜백 vs 폴링 주기·실패 재시도) 미정

## 출처
raw: `raw/confluence/2026-07-22 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md` (발행본 스냅샷) 외 v1 명세·v2 draft·도감 확정·AI 개발 기록 (frontmatter source 참조)
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21430294
각 도메인 상세 정본: [[FillMap API 명세 v1]] · [[FillMap API 설계 v2 draft]] 하위 노트
Confluence 발행본: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21430294 (cf-21430294 — 이 노트에서 발행. sync 때 새 문서로 재ingest하지 말고 이 노트에 연결할 것)
발행본 v2(2026-07-22)는 이 현황판을 넘어 **API별 요청/응답 필드·에러·쟁점까지 담은 도메인별 전체 명세판** — 일요일 멘토링 "API 스펙 점검"용. 원재료는 raw/confluence의 v1·v2 draft 스냅샷 + MSG-135/90 이후 변경분 보정.
