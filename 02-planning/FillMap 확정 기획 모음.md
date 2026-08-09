---
title: FillMap 확정 기획 모음 (허브)
type: hub
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-25 FillMap 확정 기획 모음 (허브) (cf-24739846).md, raw/confluence/2026-07-25 FillMap 확정 기획 모음 (허브) (cf-24739846) (1).md"
created: 2026-07-25
updated: 2026-08-09
keywords: [확정 기획, 기획 모음, 허브, hub, 결정 목록, decisions index, 기획확정, 설계결정, ADR 목록, 지도 홈 개편, MVP 범위, 확정 사항]
aliases: [확정 기획 허브, 기획 결정 모음, 확정 기획서]
related: ["[[기획확정 지도 홈 개편 상단 셀]]", "[[ADR viewport polling SLO]]", "[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[ADR 격자 행정동 라벨 grids.region_code]]", "[[ADR AI 처리 실행 환경 FastAPI]]", "[[설계검토 미션·이벤트 기능 추가]]", "[[ADR 격자 표시명 zone]]", "[[ADR 지도 SDK 네이버 전환]]", "[[MSG-234 상권 작도 결정 공공데이터 검수]]"]
---

# FillMap 확정 기획 모음 (허브)

> [!tldr]
> 확정된 기획·설계 결정을 확정일 역순 한 표로 모은 허브 — 상세 정본은 각 링크 노트/Confluence 페이지.
> 운영 규칙: 새 기획 확정 시 이 표(그리고 Confluence 원본 허브)에 한 줄 추가.
> 최신: 2026-07-25 지도 홈 개편 (전체 모드 폐지 · 상단 셀 4종 단일 토글).

## 이 노트로 답할 수 있는 질문
- 지금까지 확정된 기획·설계 결정이 뭐뭐인가?
- 특정 결정의 확정일과 상세 문서는?
- 가장 최근에 확정된 기획은?
- 전체 모드/핫구역/미션의 현재 확정 상태는?

## 확정 목록

| 확정일 | 결정 | 요약 | 상세 |
|---|---|---|---|
| 2026-07-25 | 지도 홈 개편 | 전체 모드 완전 폐지 · 디폴트 개인 모드 · 상단 셀 4종(핫구역·축제·팝업·코스) 단일 선택 토글 | [[기획확정 지도 홈 개편 상단 셀]] |
| 2026-07-24 | MVP 범위 확대 | 핫구역 MVP 포함, 전송은 polling 유지(Redis ZSET 집계) | [[ADR viewport polling SLO]] §6 |
| 2026-07-23 | MSG-167 후속 | 라벨 저장 위치·탐험률 축(동 단위)·격자 표시명 확정 | [[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]] |
| 2026-07-22 | 개인 도감 화면 | 수집률/탐험률 확정 UX·API 설계 (MSG-153) | [[개인 도감 화면 확정 UX·API 설계]] |
| 2026-07-22 | 격자 행정동 라벨 | grids.region_code 저장 (MSG-167) | [[ADR 격자 행정동 라벨 grids.region_code]] |
| 2026-07-21 | AI 처리 실행 환경 | 상시 FastAPI 서버 (MSG-143) | [[ADR AI 처리 실행 환경 FastAPI]] |
| 2026-07-20 | 미션·이벤트 추가 | 지자체 축제·둘레길 코스·팝업을 격자 위에 | [[설계검토 미션·이벤트 기능 추가]] · [[미션 후속 결정 코스 포토스팟 방식]] |
| 2026-07-18 | 격자 표시명 | 수동 지정 구역(zone) + 격자 좌표 산술 (MSG-234 개발 보류·행정동 폴백) | [[ADR 격자 표시명 zone]] |
| 2026-07-17 | 지도 SDK | 카카오 → 네이버 전환 (FE 전용) | [[ADR 지도 SDK 네이버 전환]] |
| 2026-07-17 | viewport 전송방식 | polling 채택 + 부하 SLO·임계점 (MSG-134) | [[ADR viewport polling SLO]] |
| 2026-07-16 | 영상 삭제 정책 | 삭제·교체 시간 제한 없음, 삭제 시 즉시 점령 롤백 | BE 레포 `.claude/rules/glossary.md` |
| 2026-07-05 | MVP 도감 범위 | 개인 도감만 · 미점령 격자 미표시 (2026-07-24 확대로 일부 갱신) | BE 레포 `.claude/rules/glossary.md` |

## 출처
raw: `raw/confluence/2026-07-25 FillMap 확정 기획 모음 (허브) (cf-24739846).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/24739846
