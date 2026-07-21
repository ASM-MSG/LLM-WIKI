---
title: User 프로필 API (예정)
type: spec
product: fillmap
class: log
status: draft
source: "raw/confluence/2026-07-17 User 프로필 API (예정) (cf-17891397).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [User, 프로필, profile, 계정 삭제, 닉네임, nickname, gridColor, 도감 색상, PATCH, 소프트 삭제, soft delete, Owner B, 예정 API]
aliases: [유저 API, 프로필 API]
related: ["[[FillMap API 설계 v2 draft]]", "[[Auth API]]", "[[FillMap DB Schema v5 MVP]]"]
---

# User 프로필 API (예정)

> [!tldr]
> 프로필 조회(GET /api/users/me)·수정(PATCH)·계정 삭제(DELETE) 설계 초안 — 전부 미구현(service·controller·dto 없음), 담당 Owner B.
> 최대 쟁점: 닉네임 길이 20 vs 50 불일치, 계정 삭제가 reports FK 때문에 하드 삭제 불가(소프트/NULL/익명화 중 결정 + 마이그레이션 선행).
> 닉네임 중복 허용 여부·프로필 이미지 업로드 방식·email 변경도 열린 질문.

## 이 노트로 답할 수 있는 질문
- 프로필 조회/수정/삭제 API의 잠정 설계는?
- 프로필 응답에 role을 왜 안 넣나?
- 닉네임 길이 검증이 왜 문제인가 (20 vs 50)?
- 계정 삭제가 왜 스키마에 막혀 있고 선택지는 뭔가?
- 닉네임 중복은 현재 허용인가?
- gridColor 허용 값은?

## 설계 요지
- `GET /api/users/me` — id·email·nickname·profileImageUrl·gridColor·provider·emailVerified·createdAt. role은 미노출.
- `PATCH /api/users/me` — 부분 수정: nickname·gridColor(BLUE~TEAL 8색, chk 제약)·profileImageUrl.
- `DELETE /api/users/me` — ⚠️ `reports.reporter_id`/`reviewed_by`가 CASCADE 아님 → 하드 삭제 FK 위반. (a) 소프트 삭제 (b) NULL 밀기 (c) 익명화 — 모두 스키마 변경 선행. S3 정리는 MSG-133 경로 재사용.

## 열린 질문
닉네임 20 vs 50 · 삭제 방식 · 닉네임 UNIQUE 없음(중복 허용 상태) · 프로필 이미지 presign vs 외부 URL · email 변경 API · User 엔티티에 grid_color 매핑 누락.

## 에러 코드
기존 1404·1409. 신설 제안: 1400 INVALID_GRID_COLOR, 1410 NICKNAME_ALREADY_EXISTS(중복 금지 시).

## 출처
raw: `raw/confluence/2026-07-17 User 프로필 API (예정) (cf-17891397).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17891397
