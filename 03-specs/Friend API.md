---
title: Friend API (구현 기준 — MSG-185·186)
type: spec
product: fillmap
class: log
status: active
source: "BE/docs/MSG-186.md"
created: 2026-08-03
updated: 2026-08-03
keywords: [Friend, 친구, friendships, 친구 목록, friend list, 친구 프로필, friend profile, 도감 요약, 친구 코드, friend code, 수락, ACCEPTED, PENDING, 9xxx, 9420, 9424, existsAcceptedPair, 은닉, LATERAL, 썸네일, sort, respondedAt]
aliases: [친구 API, 소셜 API 구현, Friend 목록 API, 친구 프로필 API]
related: ["[[Social API 예정]]", "[[Video 공개범위 visibility]]", "[[Video API]]", "[[FillMap API 스펙 통합]]"]
---

# Friend API (구현 기준 — MSG-185·186)

> [!tldr]
> `/api/friends` 9종 구현 완료 (Owner B, friend 패키지): 관계 수명주기 7종(MSG-185 — 코드·preview·요청/수락/거절/받은목록·삭제) + **목록·프로필 2종(MSG-186, 2026-08-03)**. 프라이버시 확정 — 친구면 도감 요약 전부 공개, 설정 없음(Phase 2+).
> 프로필 실패는 비친구·본인·PENDING·미존재 **전건 9424 단일 응답**(존재 은닉). 친구 판정은 무잠금 `existsAcceptedPair`(양방향 OR, `findPair`는 PESSIMISTIC_WRITE라 조회 재사용 금지) — MSG-285와 동일 시그니처 병렬 합의.
> 친구용 썸네일은 재생 허용 공개 영상만(LATERAL, cover 우선→최신 폴백, 없으면 null) — 본인용 갤러리 재사용 금지(PRIVATE 누출)·coverVideoId 미노출.

## 이 노트로 답할 수 있는 질문
- 친구 목록/프로필 API의 응답 형태와 정렬 옵션은?
- 비친구가 프로필을 조회하면 어떻게 되나 (왜 404 하나뿐인가)?
- 친구에게 보이는 도감 요약·격자 썸네일의 범위는?
- "친구인가" 판정 쿼리는 무엇이고 왜 findPair를 안 쓰나?
- friend 도메인 에러 대역(9xxx)에서 이번에 추가된 코드는?
- MSG-285(FRIENDS 공개범위)와의 병렬 머지 충돌 지점은?

## 구현 표면 (전 9종, 인증 필수)

| API | 티켓 | 내용 |
| --- | --- | --- |
| GET /api/friends/code · /preview, POST /requests, GET /requests/received, POST /requests/{id}/accept·reject, DELETE /{userId} | MSG-185 | 고정 친구 코드 기반 관계 수명주기 — [[Social API 예정]] 배너 참조 |
| **GET /api/friends?sort=** | MSG-186 | ACCEPTED 전체(방향 무관), `recent`(기본, respondedAt DESC NULLS LAST) · `nickname`, 무페이지네이션, 그 외 sort → 9420 |
| **GET /api/friends/{userId}/profile** | MSG-186 | 프로필 + 도감 요약(본인 요약 MSG-152/246 동일 산식 재사용) + 최근 수집 격자 30(공개 썸네일 LATERAL) — 단일 응답 |

## 설계 요지 (MSG-186 D-결정 압축)
- 목록 = UNION 아닌 OR 2분기 세타 조인 JPQL 생성자 프로젝션, 정렬 2본 정적 분리. sort enum 미신설.
- 은닉: 실패 전건 기존 9424 `FRIENDSHIP_NOT_FOUND`(404) — `USER_NOT_FOUND` 혼입 금지(계정 존재 누설). 실시간 판정(캐시 없음, 삭제 즉시 차단).
- `existsAcceptedPair` — 무잠금 양방향 exists. PostgreSQL은 read-only 트랜잭션에서 FOR UPDATE 계열 거부 → `findPair`(PESSIMISTIC_WRITE) 재사용 불가. **MSG-285 브랜치와 바이트 동일 합의** — 늦게 머지되는 쪽이 중복 선언 1개 제거.
- 썸네일 4조건(ACTIVE·PUBLIC·READY·NOT NULL) + cover 우선 `(v.id = ug.cover_video_id) DESC` → 최신 폴백. PUBLIC 필터 한 곳이 MSG-285 FRIENDS 확장 지점(`IN ('PUBLIC','FRIENDS')`).
- 경계면: friend → usergrid 단방향 소비(`getCollectionGridsForFriend` 비파괴 추가), usergrid는 friend 미참조.

## 출처
raw: `BE/docs/MSG-186.md` (스펙 정본 + 작업 로그·런타임 동작) · `BE/docs/MSG-185.md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/30113794 (cf-30113794, 2026-08-03 발행 — 다음 sync 때 raw 스냅샷 연결)
