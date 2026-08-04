---
title: Video 공개범위 visibility (구현 기준 — PUBLIC·PRIVATE·FRIENDS)
type: spec
product: fillmap
class: log
status: active
source: "BE/docs/MSG-285.md"
created: 2026-08-03
updated: 2026-08-03
keywords: [visibility, 공개범위, 공개 범위, FRIENDS, 친구만 보기, 친구 공개, PUBLIC, PRIVATE, 재생 판정, playback, 403, VIDEO_FORBIDDEN, 3403, 3420, V20, CHECK, switch, isFriend, existsAcceptedPair]
aliases: [FRIENDS 공개범위, 친구 공개, 영상 공개범위]
related: ["[[Video API]]", "[[Video 재생 조회 API 예정]]", "[[Friend API]]", "[[FillMap API 스펙 통합]]"]
---

# Video 공개범위 visibility (구현 기준 — PUBLIC·PRIVATE·FRIENDS)

> [!tldr]
> 공개범위 3값 확정 상태: 업로드 시 지정(MSG-204, 미지정=PUBLIC)·더보기 전환(MSG-162)·**FRIENDS 3값째(MSG-285, 2026-08-03)**. FRIENDS는 소유자 + ACCEPTED 친구(방향 무관)만 재생, 비친구는 **PRIVATE 비소유자와 바이트 동일한 403 "비공개 영상입니다"**(신규 에러코드 없음 — 당초 404 은닉안은 PRIVATE 실동작 403(MSG-206) 확인으로 폐기).
> 재생 판정은 enum-exhaustive **switch 식**(문은 javac 21이 누락 안 잡음 실측) — 4값째 추가 시 컴파일 에러 강제. 친구 쿼리는 FRIENDS && 비소유자만 1회.
> V20 마이그레이션 = CHECK DROP+ADD(데이터·인덱스 무변경, **롤백 불가**). 전역 노출 `= 'PUBLIC'` 9곳 무변경 — FRIENDS 자동 제외, 친구 대상 목록 노출은 MSG-187 몫(계약 선행 패턴).

## 이 노트로 답할 수 있는 질문
- FRIENDS 영상은 누가 재생할 수 있고, 비친구에겐 뭐가 보이나?
- 비친구 응답이 404가 아니라 403인 이유는?
- 재생 판정이 switch 식(expression)인 이유는?
- V20 마이그레이션이 뒤로 못 돌아가는 이유는?
- FRIENDS 영상이 격자 대표 영상·탐색에 안 보이는 근거는?
- 점령·스트릭·핫스코어에 공개범위가 영향을 주나? (안 준다 — FR-9)

## 판정 규칙 (GET /api/videos/{videoId})
① 존재/삭제 404 → ② BLINDED 타인 404 → ③ visibility switch 식(PUBLIC 통과 / FRIENDS `isFriend` 실시간 / PRIVATE 거부 — 거부는 단일 throw 3403) → ④ READY presign → ⑤ 조회수(타인 +1, 친구도 동일).

## 실패 응답
| 상황 | code/HTTP | 메시지 |
| --- | --- | --- |
| 비친구 FRIENDS·비소유자 PRIVATE 재생 | 3403 / 403 | "비공개 영상입니다" (동일) |
| 허용 외 값 | 3420 / 400 | "visibility 는 PUBLIC, PRIVATE, FRIENDS 중 하나여야 합니다" |

## 출처
raw: `BE/docs/MSG-285.md` (스펙 정본 + 작업 로그·런타임 동작) · glossary "친구 공개 (FRIENDS)" (`BE/.claude/rules/glossary.md`)
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/30179329 (cf-30179329, 2026-08-03 발행 — 다음 sync 때 raw 스냅샷 연결)
