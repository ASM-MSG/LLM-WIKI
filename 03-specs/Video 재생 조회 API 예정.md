---
title: Video 재생 조회 API (예정)
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Video 재생 조회 API (예정) (cf-18448491).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Video, 재생, playback, 재생 URL, presigned GET, encoded_url, visibility, PRIVATE, BLINDED, view_count, 조회수, 대표 영상, Owner B, 예정 API]
aliases: [영상 재생 API, playback API]
related: ["[[Video API]]", "[[FillMap API 설계 v2 draft]]", "[[Grid 확장 API 예정]]"]
---

# Video 재생 조회 API (예정)

> [!tldr]
> `GET /api/videos/{videoId}` 재생 URL 발급 설계 — video 패키지의 유일한 미구현 항목 (Owner B).
> 접근 제어는 status(DELETED→404, BLINDED→미정)·visibility(PRIVATE+타인→403)·processing_status(READY 아니면 playbackUrl=null)가 결정. visibility 기본 PRIVATE라 공개 전환 API 부재가 큰 구멍.
> 최대 쟁점: presigned GET vs encoded_url 직접 노출(버킷 공개 전제), view_count 증가 시점(격자 대표 영상 품질 좌우).

## 이 노트로 답할 수 있는 질문
- 영상 재생 URL은 어떤 API로 받게 되나?
- 삭제/블라인드/비공개/인코딩 중 영상의 응답은 각각 어떻게 되나?
- playbackUrl 발급 방식 쟁점(presign vs encoded_url)은 뭔가?
- view_count는 언제 올리기로 했나?
- 왜 공개 범위 변경 API가 필요한가?
- 내 영상 목록 조회는 어디서 다루나?

## 설계 요지
응답: videoId·playbackUrl·thumbnailUrl·gridId·durationSec·processingStatus·visibility·viewCount·recordedAt·expiresInSec.

| 조건 | 응답 |
| --- | --- |
| DELETED | 3404 (존재 미노출) |
| BLINDED | 미정 (403+사유 vs 404) |
| PRIVATE + 타인 | 3403 |
| READY 아님 | playbackUrl=null + 상태 |

## 열린 질문
presign vs encoded_url · view_count 증가 시점과 중복 방지 · BLINDED/FAILED 응답 · **공개 범위 변경 API 부재**(업로드에도 필드 없음 — IA 미구현) · 내 영상 목록은 Collection에서 · 3403 메시지 일반화 필요.

## 출처
raw: `raw/confluence/2026-07-17 Video 재생 조회 API (예정) (cf-18448491).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18448491
