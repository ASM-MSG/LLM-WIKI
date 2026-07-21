---
title: PRD — FillMap MVP 화면별 기능·API 명세
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-18 PRD FillMap MVP — 화면별 기능·API 명세 (cf-18972709).md"
created: 2026-07-18
updated: 2026-07-21
keywords: [PRD, 화면, 피그마, Figma, 와이어프레임, 7개 화면, 지도 홈, 격자 상세, 핫구역, 업로드, 개인 도감, 신고, API 매핑, MVP 범위]
aliases: [화면별 PRD, PRD]
related: ["[[FillMap API 명세 v1]]", "[[FillMap API 설계 v2 draft]]", "[[갭 분석 디자인 문서 코드 싱크]]", "[[ADR 격자 표시명 zone]]", "[[Collection API 예정]]", "[[Region API 예정]]"]
---

# PRD — FillMap MVP 화면별 기능·API 명세

> [!tldr]
> 피그마 웹 와이어프레임 7개 화면 ↔ 필요 API를 [구현]/[부분]/[미구현]으로 매핑한 단일 문서. 구현 10개(Auth 4·Grid 2·Video 4), 나머지는 도메인별 v2 설계 문서로 연결.
> 화면 요약: ①지도 홈(색칠만 구현) ②격자 썸네일(부분) ③핫구역(미구현) ④격자 상세(부분) ⑤신고(미구현) ⑥업로드(파이프라인 구현, AI 미구현) ⑦개인 도감(미구현).
> §4가 핵심: 피그마에 그려졌어도 MVP 미확정인 7항목(핫구역·AI·미방문 추천·격자 표시명·신고 처리·도감 공개범위·Apple 로그인) — 결정이 선행돼야 화면이 산다.

## 이 노트로 답할 수 있는 질문
- 어떤 화면에 어떤 API가 필요하고 각각 구현 상태는?
- 현재 호출 가능한 API 10개는 뭔가?
- 화면에 그려졌지만 MVP 범위가 미확정인 항목은?
- 격자 썸네일 뷰에서 지금 안 나오는 정보는?
- 개인 도감 화면은 왜 전부 미구현인가?
- 신고 기능의 현재 상태는?

## 목표·비목표
- 목표: 화면 기준으로 필요 API를 한 곳에 — 개발 착수 시 이 문서 하나로 파악.
- 비목표: 필드 상세(각 v2 문서에 위임), Phase 2 상세.

## 제품 범위 (화면 지도)
| 화면 | 상태 |
| --- | --- |
| ① 지도 홈 | 격자 색칠 [구현] · 핫구역/수집현황/추천 [미구현] |
| ② 격자 썸네일 뷰 | 단건 조회 [부분] · 영상목록 [미구현] |
| ③ 핫구역 뷰 | [미구현] |
| ④ 격자 상세 | 단건 [부분] · 표시명/영상목록/지표/신고 [미구현] |
| ⑤ 영상 신고 모달 | [미구현] (reports 테이블만) |
| ⑥ 영상 업로드 | 파이프라인 [구현] · AI [미구현] |
| ⑦ 개인 도감 | [미구현] (스키마만) |

구현 10개: auth 4종([[Auth API]]) · `GET /api/grids`(±{gridId})([[Grid API]]) · videos 4종([[Video API]]).

## MVP 결정 필요 (§4)
핫구역 MVP 포함 여부 · AI 하이라이트/블러 필수 여부 · 미방문 격자 추천 로직 · 격자 표시명 쟁점([[ADR 격자 표시명 zone]]) · 신고 사유 enum/플로우 · 도감 공개 범위(친구는 Phase 2 → 공개/비공개 2단?) · Apple/로컬 로그인 화면.

## 출처
raw: `raw/confluence/2026-07-18 PRD FillMap MVP — 화면별 기능·API 명세 (cf-18972709).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18972709
