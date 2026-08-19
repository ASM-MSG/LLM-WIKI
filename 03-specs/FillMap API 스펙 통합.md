---
title: FillMap API 스펙 통합 (전체 한눈에)
type: hub
product: fillmap
class: log
status: active
source: "raw/confluence/2026-08-19 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-26 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-26 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294) (1).md, raw/confluence/2026-07-22 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md, raw/confluence/2026-07-17 FillMap API 명세 (v1 — 구현 기준) (cf-17891367).md, raw/confluence/2026-07-17 FillMap API 설계 — 예정 (v2 draft) (cf-17793077).md"
created: 2026-07-22
updated: 2026-08-19
keywords: [API 스펙, API 명세, 통합, 전체, 한눈에, one page, 현황판, 구현 현황, 엔드포인트, 71개, 컨트롤러, developCode, 에러 코드, 대역, ApiResponseDto, data, body, httpStatus, MSG-311, MSG-265, 인증, JWT, refresh, auth, user, video, grid, collection, region, zone, hotzone, search, mission, badge, friend, notification, moderation, admin, AI 서버, jobs, 미구현, likes, sponsor_ads]
aliases: [API 통합 뷰, API 전체 스펙, API 스펙 한눈에, API 현황판]
related: ["[[FillMap API 명세 v1]]", "[[FillMap API 설계 v2 draft]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[지도 홈 API 연동 가이드 FE]]", "[[ADR 격자 계산 EPSG5179 전환]]", "[[ADR 줌아웃 클러스터링 행정 단위 집계 H3 기각]]", "[[Friend API]]", "[[Video 공개범위 visibility]]", "[[zone 표시명 FE 계약]]", "[[FillMap DB Schema v5 MVP]]"]
---

# FillMap API 스펙 통합 (전체 한눈에)

> [!tldr]
> 도메인별 REST API가 지금 어디까지 있는지 보는 현황판. **2026-08-19 develop 전수 실사로 다시 썼다** — 직전 갱신(2026-07-26) 이후 도메인 여섯 개가 새로 생기면서 엔드포인트가 **23개에서 71개**가 됐다.
> 옛 판의 "제안"·"블로커" 표기는 대부분 해소됐다. Owner 미정이던 Social·Notification은 둘 다 Owner B로 구현을 마쳤고, 친구 찾기 수단 부재·Redis 미도입·공개 범위 전환 부재 같은 선행 과제도 전부 풀렸다.
> **응답 래퍼가 두 번 바뀌었다**: 실데이터 키 `body` → `data`(MSG-311), `httpStatus` 필드 삭제(MSG-265). 옛 문서를 그대로 읽으면 틀린다.

## 이 노트로 답할 수 있는 질문
- 지금 서버에 API가 몇 개고 도메인별로 무엇이 있나?
- 공통 응답 래퍼·인증·시각 표기·developCode 대역은?
- 어떤 도메인이 어느 Owner 소관인가?
- 아직 서버에 없는 것은 무엇이고 왜 없나?
- 옛 API 문서(v1 명세·v2 draft)를 어디까지 믿어도 되나?

> [!warning] 상세 계약의 정본은 코드와 Swagger
> 이 노트와 컨플루언스 현황판은 "무엇이 있고 무엇이 없나"를 담는다. 요청·응답 필드 수준은 코드가 이긴다.
> 도메인별 초안 페이지([[FillMap API 설계 v2 draft]] 트리)는 **착수 전 제안**이라 지금 코드와 맞지 않는다.

## 0. 도메인 현황판 — 합계 71개, 컨트롤러 15개

| 도메인 | Owner | 개수 | 비고 |
| --- | --- | --- | --- |
| Auth `/api/auth` | B | 8 | 이메일·카카오 로그인, 리프레시 회전과 재사용 감지(MSG-135), dev 전용 모의 로그인 1개 |
| User `/api/users` | B | 7 | 프로필, 닉네임, 프로필 이미지 3종, 위치 동의, 계정 삭제 |
| Video `/api/videos` | B | 7 | 업로드 3종, 재생, 교체, 삭제, 공개 범위 전환 |
| Grid `/api/grids` | A | 3 | 단일, 뷰포트(커서), 줌아웃 집계 |
| 격자 영상 `/api/grids/{gridId}/…` | B | 4 | 경로는 격자, 구현체는 video 패키지 |
| Collection `/api/collections` | B | 4 | 도감 요약, 갤러리 격자, 동 단위 영상, 날짜별 업로드 기록 |
| Region `/api/regions` | A·B | 6 | 역지오코딩·수집률 3종(A) + 지역 탐색 2종(video 패키지, B) |
| Zone `/api/zones` | A | 1 | 구역 목록 |
| HotZone `/api/hotzones` | A | 1 | 뷰포트 핫구역 |
| Search `/api/search` | A | 2 | 장소 검색(카카오 프록시), 인기 검색어 |
| Mission `/api/missions` | B | 4 | 활성 목록, 진행도, 상세, 미션 영상 목록 |
| Badge `/api/badges` | B | 2 | 목록, 대표 뱃지 교체 |
| Friend `/api/friends` | B | 12 | 친구 코드, 요청과 수락, 목록, 프로필, 친구 도감 3종 |
| Notification `/api/notifications` | B | 4 | FCM 토큰 2종, 알림 설정 2종 |
| Moderation | B | 6 | 신고 접수 1종, 관리자 5종(`/api/admin`) |
| AI 서버 | AI | 3 | 별도 FastAPI 레포 |

그 밖에 조회수 오염을 막는 내부용 심 `HEAD /api/videos/{videoId}`(Swagger 비노출)가 하나 있다.

## 1. 공통 규약

**응답 래퍼 `ApiResponseDto<T>`는 필드 셋이다**: `developCode`(성공 200) · `message` · `data`.
`body` → `data` rename은 MSG-311(FE 동시 배포 전제), `httpStatus` 삭제는 MSG-265다(status line과 중복이고 springdoc이 틀린 예시를 만들었다).

**인증은 JWT Bearer.** 액세스 1시간, 리프레시 2주(Redis, `X-Device-Id` 디바이스별 세션, 회전 + 재사용 감지, 로그아웃 블랙리스트). 퍼블릭은 회원가입·로그인·소셜 로그인 3종·재발급이고 dev 모의 로그인은 local·dev 전용이다.

**시각은 전부 UTC `Z` 표기**로 오간다(전역 코덱, MSG-376). KST 날짜 라벨이 필요한 자리만 `LocalDate`(업로드 기록의 `uploadDate`). 저장도 실행 환경 시간대와 무관하다(MSG-379).

**격자 식별자 포맷 `"{grid_y}_{grid_x}"`는 그대로지만 값이 전부 바뀌었다** — 2026-08-08 EPSG:5179 전환([[ADR 격자 계산 EPSG5179 전환]]). 격자를 담는 응답에는 표시명 재료 `zoneName`·`zoneCell`·`regionName`이 함께 실린다(MSG-341·349).

**developCode 대역** (정본은 레포 `.claude/rules/response-pattern.md`, 새 도메인은 표에 행을 먼저 넣는다):

| 대역 | 도메인 | 예 |
| --- | --- | --- |
| 4xx·5xx | 공통 | 400, 401, 403, 404, 500 |
| 1xxx | user | 1404 USER_NOT_FOUND, 1413 IMAGE_TOO_LARGE |
| 2xxx | auth | 2431~2433 리프레시 3종, 2502 OAUTH_PROVIDER_ERROR |
| 3xxx | video | 3420 INVALID_VISIBILITY, 3425~3429 하이라이트 |
| 4xxx | grid | 4401 INVALID_VIEWPORT, 4405 INVALID_AGGREGATION_UNIT |
| 5xxx | search | 5502 SEARCH_UPSTREAM_ERROR |
| 6xxx | region | 6400, 6404 |
| 7xxx | badge | 7400, 7403 |
| 8xxx | hotzone | 8400 |
| 9xxx | friend | 9400, 9404, 9409, 9410, 9414, 9420, 9424 |
| 10xxx | notification | 10400, 10420 |
| 11xxx | moderation | 11400~11421 |
| 12xxx | mission | 12400~12404 |

옛 판의 "5xxx collection · 7xxx social · 8xxx notification" 제안은 **전부 다르게 확정**됐다. 페이지네이션은 커서가 기본이고 관리자 신고 목록만 page·size를 받는다.

## 2. 엔드포인트 전량

**Auth** `signup` · `login` · `oauth/{provider}` · `oauth/kakao/authorize`(인가 진입점) · `oauth/kakao/code` · `reissue` · `logout` · `dev/social-login`

**User** `GET me` · `PUT me/nickname` · `PUT me/location-consent` · `POST me/profile-image/presigned-url` · `PUT me/profile-image` · `DELETE me/profile-image` · `DELETE me`

**Video** `POST presigned-url` · `POST /api/videos`(업로드 확정, s3Key 3중 검증) · `POST highlight-preview`(하이라이트 선분석) · `GET {videoId}`(재생, READY 아니면 URL null) · `PUT {videoId}`(교체, 같은 격자만) · `PATCH {videoId}/visibility` · `DELETE {videoId}`(0개면 점령 롤백)

**Grid** `GET {gridId}` · `GET /api/grids`(뷰포트, 커서) · `GET /api/grids/aggregation`(줌아웃 집계 — [[ADR 줌아웃 클러스터링 행정 단위 집계 H3 기각]])

**격자 영상** `my-videos` · `cover` · `videos`(전역 목록) · `hourly-uploads`(시간대 분포)

**Collection** `summary` · `grids`(갤러리) · `videos?regionCode=` · `upload-history`

**Region** `reverse-geocode` · `stats` · `stats/by-point` · `stats/by-grid` · `{regionCode}/grids`(격자 카드 + 헤더 카운트) · `explore`(전체 지역 리스트)

**Zone** `GET /api/zones` — **HotZone** `GET /api/hotzones` — **Search** `places` · `trending`

**Mission** `active`(뷰포트) · `progress` · `{missionId}` · `{missionId}/videos`

**Badge** `GET /api/badges` · `PUT /api/badges/featured`

**Friend** `code` · `preview` · `POST requests` · `requests/received` · `requests/{id}/accept` · `requests/{id}/reject` · `GET /api/friends` · `DELETE {userId}` · `{userId}/profile` · `{userId}/grids` · `{userId}/grids/aggregation` · `{userId}/grids/{gridId}/videos`

**Notification** `POST tokens` · `DELETE tokens` · `GET preferences` · `PATCH preferences/{category}`

**Moderation** `POST /api/videos/{videoId}/reports` · `GET /api/admin/reports` · `approve` · `reject` · `videos/{videoId}/unblind` · `GET /api/admin/videos/{videoId}`

**AI 서버(별도 레포)** `POST /jobs` · `GET /jobs/{id}` · `GET /jobs/{id}/video`

## 3. 도메인별 짚을 점
- **Video 공개 범위**는 PUBLIC·PRIVATE·FRIENDS 3값(MSG-285). 비친구 거부는 PRIVATE 비소유자와 **같은 403**이고 별도 코드가 없다. 판정은 요청 시점 실시간이라 친구를 끊으면 다음 요청부터 막힌다 → [[Video 공개범위 visibility]]
- **친구 도감 레이어**는 항상 친구 한 명 단위, 단일색, PRIVATE 제외. 비친구 조회는 관계·계정 존재를 숨기는 단일 실패 응답(9424) → [[Friend API]]
- **알림 설정 카테고리는 일곱 가지**(BADGE·HOTZONE·REMIND·VIDEO·WEEKLY·FRIEND·MISSION_NEARBY). MODERATION은 운영 조치라 끌 수 없어 설정 표면에서 빠졌고(MSG-417), MISSION_NEARBY는 알림을 **기기가 만들어** 서버 발송 경로가 없는 최초의 카테고리다. 서버는 on/off 상태만 들고 근접 판정은 기기가 하며 위치를 받지도 저장하지도 않는다(MSG-418)
- **미션 뱃지**는 2026-08-10에 종류별로 갈라 종류마다 1·3·10개 임계로 지급하도록 재편했고 기존 합산 뱃지 3종은 은퇴시켰다(MSG-363)
- **핫구역**은 48시간 윈도우·상위 50·최소 임계 3, Redis 정렬 집합 6시간 버킷이고 DB 테이블이 없다
- **장소 검색**은 카카오 로컬 BE 프록시이고 약관 때문에 결과를 캐시하지 않는다 → [[ADR 장소 검색 카카오 로컬 프록시]]

## 4. 아직 서버에 없는 것 (요구사항 ID는 레포 `docs/srs.md`)

| 없는 것 | 상태 | 근거 |
| --- | --- | --- |
| 알림 이력·읽음 조회 API, 푸시 딥링크 | 미착수 | 발송 기록은 남아 조회 계층만 얹으면 된다 (FR-NOTI-12) |
| 좋아요 API | 테이블만 있음 | `likes`는 V1부터 있는데 코드 참조가 0건 |
| 스폰서 격자 | 테이블만 있음 | `sponsor_ads`도 같은 상태, Phase 2 |
| 특수(SPECIAL) 축 뱃지 | 시딩 없음 | 지급 규칙을 뱃지별로 정해야 한다 (FR-BADGE-11) |
| 시·도 상위 집계("서울 34%") | MVP 밖 | 집계 정책 미확정, FE 임의 계산도 금지 (FR-REGION-13) |
| 영상 검색 | MVP 밖 | 검색바 안내 문구에서도 "영상"을 뺐다 (FR-SEARCH-13) |
| 표시명 역파싱 검색 | 서버 API 없음 | 구역 캐시 48건을 FE가 로컬 필터로 처리 (FR-SEARCH-14) |
| 친구 차단, 전체 친구 합산 레이어, 코드 재발급, 목록 페이지네이션 | 미도입 확정 | FR-FRIEND-13 |
| 신고자 결과 통지, 신고 남용 상한 | 미도입 확정 | FR-MOD-14 |
| 애플 로그인 | iOS 단계 | 앱스토어 심사 요구 (FR-AUTH-12) |

**서버는 됐고 화면이 남은 것**: 미션 목록·상세·진행도의 서버 재료는 MSG-383·398로 끝났고 지도 표현과 카드 UI가 FE 몫이다(FR-MISSION-13~18). 프로필 이미지 표시는 코드가 끝났고 스토리지 공개 읽기 정책이 걸려 있다(FR-USER-13). 외부 이미지 미러링은 형식 통일까지 정하고 진행 중이다(NFR-DATA-07).

## 출처
raw: `raw/confluence/2026-08-19 FillMap API 스펙 통합 (전체 한눈에) (cf-21430294).md`
원본: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21430294
