---
title: FillMap API 스펙 통합 (전체 한눈에)
type: hub
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-26 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-22 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md, raw/confluence/2026-07-17 FillMap API 설계 — 예정 (v2 draft) (cf-17793077).md, raw/confluence/2026-07-22 개인 도감 화면 — 확정 UX·API 설계 (수집률·탐험률) (cf-21528615).md, raw/confluence/2026-07-21 FillMap AI Highlight-Blur — 레포 생성부터 dev 배포까지 (cf-21102593).md"
created: 2026-07-22
updated: 2026-07-24
keywords: [API 스펙, API 명세, 통합, 전체, 한눈에, one page, 멘토링, 스펙 점검, 구현 현황, 예정 API, 에러 코드, developCode, jobs API, AI 서버, 열린 질문]
aliases: [API 통합 뷰, API 전체 스펙, API 스펙 한눈에]
related: ["[[FillMap API 명세 v1]]", "[[FillMap API 설계 v2 draft]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[2026-07-21 AI Highlight-Blur 개발 기록]]", "[[2026-07-16 박원형 멘토 멘토링]]"]
---

# FillMap API 스펙 통합 (전체 한눈에)

> [!tldr]
> 흩어진 API 노트 13개를 한 페이지로 모은 통합 뷰 — 멘토링 "API 스펙 점검"(0714 박원형 액션 아이템) 대비용.
> **2026-07-24 BE 코드 실사 반영**(main 04f1ae0): 구현 ✅ 23개(BE) + AI 서버 3개 — 재생(MSG-206)·공개 전환(MSG-162)·탐험률 by-point/by-grid·도감 격자(MSG-153)·동 단위 영상(MSG-167)이 구현으로 승격. 구현 예정 🔜 = Mission 도메인(7/23 결정), 제안 📝 약 15개 + Figma 파생 갭 3건(신고·공유·통합 검색).
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
- **에러 대역**: 1xxx user · 2xxx auth · 3xxx video(+3420 INVALID_VISIBILITY 신설) · 4xxx grid · **6xxx region(6400 좌표·6404 코드 — 코드로 확정)** / 5xxx collection · 7xxx social · 8xxx notification — **제안(미확정)**
- **페이지네이션 관례**: cursor 방식 (MSG-90 `GET /api/grids`가 첫 확정)

## 1. 구현된 API — BE (✅ 23개 — 2026-07-24 코드 실사, main 04f1ae0)

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

### Video — `/api/videos` (6개, 전부 인증) → [[Video API]]
| API | 핵심 |
| --- | --- |
| `POST /api/videos/presigned-url` | extension(mp4/mov)·contentType·contentLength → uploadUrl·s3Key·expiresInSec |
| `POST /api/videos` | s3Key·lat·lon·durationSec(1~30)·recordedAt → 메타 저장 + 격자 점령. s3Key 3중 검증(MSG-132) |
| `GET /api/videos/{videoId}` | **재생 조회 (MSG-206)** — 표시 메타 + presigned GET playbackUrl(READY 아니면 null). 삭제·블라인드(타인) 404 · 비공개(타인) 403 |
| `PUT /api/videos/{videoId}` | 본인만. 좌표 지정 시 같은 격자 검사(3422 GRID_MISMATCH). 교체 직후 UPLOADED |
| `PATCH /api/videos/{videoId}/visibility` | **공개 범위 전환 (MSG-162)** — PUBLIC↔PRIVATE, 같은 값 재전환 멱등 |
| `DELETE /api/videos/{videoId}` | 본인만. 격자 내 0개 되면 점령 롤백 |

`HEAD /api/videos/{videoId}`는 view_count 오염 방지용 내부 심(@Hidden, MSG-208) — API 표면 아님.
에러: 3400 INVALID_COORDINATE · 3401 INVALID_S3_KEY · 3402 UPLOAD_NOT_FOUND · 3403 VIDEO_FORBIDDEN · 3404 VIDEO_NOT_FOUND · 3413 FILE_TOO_LARGE · 3415 UNSUPPORTED_EXTENSION · 3420 INVALID_VISIBILITY · 3422 GRID_MISMATCH

### Region — `/api/regions` (4개, 전부 인증) → [[Region API 예정]]
| API | 핵심 | 티켓 |
| --- | --- | --- |
| `GET /api/regions/reverse-geocode` | 좌표 → 행정동 판정. 바다·국외는 404 아닌 **200 + body null**, 한국 범위 밖 400(6400) | MSG-93 |
| `GET /api/regions/stats` | 행정동별 탐험률 — collectedCount·totalCount·progressRate(100 clamp). parentCode 필터(실존 안 하면 6404)·collectedOnly(false면 롤백 0-row 포함). 수집 없으면 200 + 빈 배열 | MSG-156 |
| `GET /api/regions/stats/by-point` | 도감 갤러리 진입 초기값 — 현재 위치 행정동의 내 수집률. 수집 없어도 **0% 합성**, 무귀속은 200 + null | MSG-153 계열 |
| `GET /api/regions/stats/by-grid` | 격자 클릭 → 격자 **중심점** 귀속 행정동 수집률 (집계 축 MSG-155와 동일 → 라벨·탐험률 일치). 이상 입력도 200 + null | MSG-153 계열 |

### Collection — `/api/collections` (3개, 전부 인증) → [[개인 도감 화면 확정 UX·API 설계]]
| API | 핵심 | 티켓 |
| --- | --- | --- |
| `GET /api/collections/summary` | 도감 요약 — totalGridCount·totalVideoCount·visitedRegionCount. **뱃지·스트릭 필드 없음** (Figma 도감 화면과 갭 — §5) | MSG-152 |
| `GET /api/collections/grids` | 최근 수집 격자 first_collected_at DESC **최대 30·무커서**. cover 영상 ID·썸네일·regionName(nullable). 0건도 200 빈 배열 | MSG-153 |
| `GET /api/collections/videos?regionCode=` | **동 단위 내 영상 (MSG-167)** — created_at DESC 무커서. 내 도감이라 PRIVATE·인코딩 중 포함(ACTIVE만). 미존재 regionCode도 200 빈 배열 | MSG-167 |

상세 계약은 [[개인 도감 화면 확정 UX·API 설계]]·[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]] + Swagger가 정본. **[[FillMap API 명세 v1]]에 미승격 API 7개 — 갱신 필요.**

## 2. 구현 예정 (🔜 결정 확정 — Mission 도메인)
7/22판의 🔜 2건(도감 격자 MSG-153 · 공개 전환 MSG-162)은 구현 완료되어 §1로 승격. 남은 확정 결정분은 미션 도메인:

| API | 핵심 | 근거 |
| --- | --- | --- |
| `GET /api/missions/active` | 활성 미션 + 표시 지오메트리 — 면(축제)·마커(팝업)·폴리라인(코스)·격자 점(테마). 코스 PATH shape 소스는 mission_grids가 아닌 **missions.path** (MSG-222). TTL 1h 캐시 | [[2026-07-23 기획회의 미션·이벤트 표시 방식]] |
| 미션 판정·진행도 | 업로드 훅에서 mission_grids **포토스팟** 판정 `count(distinct grid_id) ≥ target_count` → user_missions 스탬프(비회수, UNIQUE). 코스 무기간·과거 영상 인정 | [[미션 후속 결정 코스 포토스팟 방식]] · MSG-223·225 |

## 3. 제안 단계 (📝 경로·메서드는 draft — 정본은 각 노트)

### User 프로필 (Owner B) → [[User 프로필 API 예정]]
`GET /api/users/me` · `PATCH /api/users/me`(nickname·gridColor 8색·profileImageUrl) · `DELETE /api/users/me`
⛔ 계정 삭제는 reports FK 때문에 하드 삭제 불가 — 소프트/NULL/익명화 결정 + 마이그레이션 선행. 쟁점: 닉네임 20 vs 50, 닉네임 UNIQUE 없음

### Video 재생 — 구현 완료 (MSG-206) → §1로 승격
쟁점 3건 전부 코드로 확정: 재생 소스 = **presigned GET**(Block Public Access 유지) · BLINDED(타인) = **404** · view_count는 GET에서 증가(HEAD 폴백 오염은 내부 심으로 차단)

### Collection 잔여 (Owner B) → [[Collection API 예정]]
`GET /api/collections/badges?earnedOnly=` — 격자별 영상 목록 제안(`/collections/grids/{gridId}/videos`)은 동 단위 영상(MSG-167, regionCode 축)으로 대체돼 철회
⛔ 뱃지 마스터 시딩 없음(빈 배열) + progress JSONB 포맷 미정. 스트릭 갱신 주체·KST 타임존 미정 — Figma 도감은 뱃지·스트릭이 핵심 요소인데 summary에도 두 값이 없음

### Region 잔여 (Owner A) → [[Region API 예정]]
`GET /api/regions/search?q=` (DB 3,558개로 완결, SDK 불필요) · `GET /api/regions/{code}` · `GET /api/regions/{code}/boundary`(GeoJSON, 무거워서 분리)
쟁점: 랜드마크 검색("홍대")은 [[ADR 격자 표시명 zone]]과 같은 뿌리, 시/도 상위 집계는 MVP 이후

### Grid 확장 (Owner A/B) → [[Grid 확장 API 예정]]
`GET /api/grids/{gridId}/videos`(전역 목록 — 남의 영상 포함) · `POST/DELETE /api/videos/{videoId}/likes`(멱등 UPSERT) · `GET /api/grids/hot`
MSG-162 구현으로 전역 목록 블로커 해소 — 착수 가능. 핫존은 Redis 스키마 설계 티켓부터

### Social (Owner 미정) → [[Social API 예정]]
`POST /api/friends/requests` · `PATCH /api/friends/requests/{requesterId}` · `GET /api/friends?status=` · `DELETE /api/friends/{userId}` · `POST /api/friends/{userId}/block`
⛔ **상대 userId를 알 방법이 없음**(검색·초대 코드 부재) — Social 전체 블로커

### Notification (Owner 미정) → [[Notification API 예정]]
`POST /api/notifications/tokens`(FCM, **반드시 UPSERT**) · `DELETE /api/notifications/tokens?fcmToken=`
그 외(설정·목록·읽음)는 테이블이 없어 스펙 불가. FCM vs SSE 미확정

### Figma 파생 갭 — 디자인엔 있는데 스펙 자체가 없음 (2026-07-24 디자인 실사)
- **영상 신고 플로우** — 격자 상세 더보기 메뉴에 신고(사유 선택→접수) UI 존재. reports 테이블은 있으나(계정 삭제 FK 쟁점의 근거 테이블) API 스펙 0건
- **공유 버튼** — 격자 상세 시트에 존재. 딥링크·공유 URL 정책 미정
- **통합 검색** — "장소, 격자, 영상 검색" 입력창. Region 검색 제안(위 §3)의 상위 집합 — 범위 재정의 필요

## 4. AI 서버 API — 별도 FastAPI (dev 배포 완료, BE 연동 대기)
| API | 핵심 |
| --- | --- |
| `POST /jobs` | 즉시 202 + job_id. 단일 워커 큐 순차 처리 |
| `GET /jobs/{id}` | 폴링. 상태 `QUEUED → PROCESSING → DONE\|FAILED` — PROCESSING = BE `processing_status=BLURRING` |
| `GET /jobs/{id}/video` | 결과 다운로드. 1080p 30초 E2E 실측 4.3분 |

AGPL 때문에 별도 레포·HTTP 통신 — [[2026-07-21 AI Highlight-Blur 개발 기록]] · [[ADR AI 처리 실행 환경 FastAPI]]

## 5. 열린 결정 (스펙 점검에서 짚일 후보 — 2026-07-24 갱신)
해소됨: MSG-162 공개 전환(구현) · view_count 시점(GET에서 증가, HEAD 심) · BLINDED 응답(타인 404) · 탐험률 조회 형태(FE 2-call — by-point/by-grid + videos로 구현)

1. **v1 명세 문서가 코드보다 뒤처짐** — 미승격 7개(재생·visibility·by-point/by-grid·도감 3종) 승격 필요
2. developCode 신규 대역 — 6xxx는 코드로 확정, 5·7·8xxx 미확정
3. 닉네임 길이 20 vs 50 불일치 · UNIQUE 없음
4. 계정 삭제 방식 (FK 제약)
5. Social·Notification Owner 미정 + 친구 찾기 수단 부재
6. AI jobs API의 BE 연동 계약(콜백 vs 폴링 주기·실패 재시도) 미정
7. **도감 뱃지·스트릭** — Figma 도감의 핵심 요소인데 summary 필드·badges API 모두 없음 (§3)
8. **신고·공유·통합 검색** — Figma에 있으나 스펙 0건 (§3 Figma 파생 갭)
9. Mission 도메인 티켓 분해 — active API 응답 계약(MSG-222)·판정 훅(MSG-223·225) 스펙 문서화 필요

## 출처
raw: `raw/confluence/2026-07-22 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md` (발행본 스냅샷) 외 v1 명세·v2 draft·도감 확정·AI 개발 기록 (frontmatter source 참조)
코드 실사: github.com/ASM-MSG/BE main `04f1ae0` (2026-07-24) — 컨트롤러 7종·DTO·ErrorCode 전수 대조 / 디자인 실사: Figma Fill-Map (node 13021-520) 화면 프레임 전수
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21430294
각 도메인 상세 정본: [[FillMap API 명세 v1]] · [[FillMap API 설계 v2 draft]] 하위 노트
Confluence 발행본: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21430294 (cf-21430294 — 이 노트에서 발행. sync 때 새 문서로 재ingest하지 말고 이 노트에 연결할 것)
발행본은 이 현황판을 넘어 **API별 요청/응답 필드·에러·쟁점까지 담은 도메인별 전체 명세판** — 일요일 멘토링 "API 스펙 점검"용. 원재료는 raw/confluence의 v1·v2 draft 스냅샷 + MSG-135/90 이후 변경분 보정.
**발행본 v4(2026-07-26)**: 7/24 코드 실사 반영 갱신 — 구현 17→23 승격(§5 재생·visibility ✅, §8 Collection 3종 ✅, §9 by-point/by-grid ✅), 6xxx·3420 확정, §12 Mission 🔜·§14 열린 결정 9건·Figma 갭 3건 신설, §13 AI E2E 개통(MSG-168) 표기. 다음 confluence-sync 때 새 스냅샷 수집 예정.
