---
title: Notification API (예정)
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 Notification API (예정) (cf-17498239).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Notification, 알림, 푸시, push, FCM, 토큰, push_tokens, UPSERT, SSE, 알림 설정, 읽음 처리, 예정 API]
aliases: [알림 API, 푸시 API]
related: ["[[FillMap API 설계 v2 draft]]", "[[Auth API]]", "[[Social API 예정]]"]
---

# Notification API (예정)

> [!tldr]
> FCM 푸시 토큰 등록/삭제 2개만 정의 가능 — 스키마가 push_tokens 테이블 하나뿐이라서. 담당 미정.
> 등록은 반드시 UPSERT(fcm_token이 PK — INSERT로 짜면 재로그인 시 터짐), 삭제는 멱등 권장. 플랫폼은 WEB 우선.
> 알림 설정 on/off·목록·읽음·리텐션 등 IA/SA의 나머지는 전부 테이블이 없어 스키마 변경 선행. FCM vs SSE도 미확정.

## 이 노트로 답할 수 있는 질문
- 현재 스키마로 정의 가능한 알림 API는 뭐뿐인가?
- 토큰 등록을 왜 UPSERT로 해야 하나?
- 로그아웃과 토큰 삭제의 관계는?
- 알림 설정/목록/읽음 처리는 왜 스펙을 못 쓰나?
- FCM vs SSE는 결정됐나?
- 알림 에러 코드 대역은?

## 설계 요지
- `POST /api/notifications/tokens` — fcmToken(≤512)·platform(IOS/ANDROID/WEB)·appVersion. **UPSERT** (ON CONFLICT DO UPDATE).
- `DELETE /api/notifications/tokens?fcmToken=` — 로그아웃 시. 멱등 권장(8404 불필요). /auth/logout과의 통합 여부 미정.

## 스키마가 없어서 못 쓰는 것
알림 설정 토글 · 알림 이력/읽음 · 친구 활동(Social 선행) · 뱃지/랭킹(배치 선행) · 핫구역(실시간 위치 수집 — 프라이버시 검토) · 리텐션(발송 이력 필요).

## 열린 질문
담당 Owner · 알림 설정 스키마(기획 선행) · FCM vs SSE · 발송 파이프라인은 별도 문서 · 토큰 만료 정리 배치. 에러 대역 8xxx 제안(미확정).

## 출처
raw: `raw/confluence/2026-07-17 Notification API (예정) (cf-17498239).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17498239
