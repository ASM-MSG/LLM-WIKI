---
title: FE 격자 계약 — 프론트-백 합의 (격자 사전 생성 정정)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-23 프론트-백 합의 사항 — 격자 계약 (격자 사전 생성 정정) (cf-23199747).md"
created: 2026-07-23
updated: 2026-07-24
keywords: [격자 계약, grid contract, FE, 프론트, 사전 생성, 전역 고정 눈금, GRID_LAT_STEP, GRID_LNG_STEP, 0.0009, 0.00115, Math.floor, GridEncoder, gridId, bbox, 네이버 지도, v3, WGS84, TM128, naver.maps, getBounds, Rectangle, regionName, nullable, thumbnailUrl, zones, zone 보류, MSG-234, displayName, 서면 A-14, 장소 검색, api/search, by-point, by-grid, regionCode]
aliases: [격자 계약, FE 격자 계약, 격자 사전 생성 정정, 네이버 v3 격자 연동]
related: ["[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]]", "[[ADR 격자 표시명 zone]]", "[[ADR 지도 SDK 네이버 전환]]", "[[Grid API]]", "[[FillMap API 스펙 통합]]", "[[개인 도감 화면 확정 UX·API 설계]]"]
---

# FE 격자 계약 — 프론트-백 합의 (격자 사전 생성 정정)

> [!tldr]
> "격자 사전 생성" 합의 정정 — 격자는 서버 리소스가 아니라 **전역 고정 눈금**(0.0009°×0.00115°, Math.floor 반열림). FE가 로컬 산술로 칸을 그리고, DB엔 영상 올라온 칸만 기록.
> 네이버 지도 **v3(WGS84)** 좌표가 계산식 입력 그 자체라 변환 0 — 단 레거시 v2(TM128)·좌표 반올림은 금지.
> **zone(표시명 "서면 A-14"·장소 검색)은 MSG-234로 개발 보류** — FE는 행정동 폴백(regionName)만으로 진행. 계약 보존본은 원문 §7 참조.

## 이 노트로 답할 수 있는 질문
- 격자 사전 생성 논의는 어떻게 정리됐나? (없던 걸로 — 전역 고정 눈금)
- FE는 격자 ID·칸 경계를 어떻게 계산하나? (Math.floor 산술 — 코드 포함)
- 격자 관련 API 계약은? (색칠·칸 클릭·갤러리·탐험률·동 단위 영상 5종)
- 네이버 지도 v3에서 이 계약이 그대로 통하나? (WGS84라 직결 — v2·반올림만 금지)
- "서면 A-14" 표시명은 언제 어떻게? (MSG-234 보류 — regionName 폴백으로 진행)
- regionName·thumbnailUrl이 null이면? (정상 케이스 2종)

## 계약 요약
1. **격자 = 전역 고정 눈금**: `gridY = Math.floor(lat/0.0009)`, `gridX = Math.floor(lng/0.00115)`, `gridId = "{y}_{x}"` — `| 0`·parseInt 금지(음수 좌표). bbox·center 전부 산술. BE GridEncoder와 동일해야 함(서버 재계산이 정본, FE는 표시용).
2. **API 5종**: 색칠 `GET /api/grids`(bbox 0.5도·size≤5000·cursor) · 칸 클릭 `GET /api/grids/{gridId}`(미존재도 200 occupied=false) · 갤러리 `GET /api/collections/grids`(regionName nullable) · 탐험률 by-point/by-grid(동 단위) · 동 단위 영상 `GET /api/collections/videos?regionCode=`(gridId 포함, 빈 배열 200, 페이지네이션 없음).
3. **네이버 v3 직결**: `e.coord.lat()`·`getBounds()`가 WGS84라 계산식 입력 그 자체. 셀은 Rectangle에 bbox 산술값 그대로. ⚠ 레거시 v2(TM128)·좌표 반올림(toFixed) 금지.
4. **nullable 2종 = 정상**: regionName(무귀속 해안 칸) · thumbnailUrl(READY 전).
5. **zone 보류 (MSG-234, 2026-07-23)**: 상권 작도 리소스 미확정 — 표시명 "서면 A-14"·`GET /api/zones`·장소 검색은 개발 보류, FE는 **행정동 폴백(regionName)만 구현**. 재개 시 계약(zones 규칙표 1회 다운로드 + FE 로컬 명명)은 원문 §7·§7-1에 보존.

## 출처
raw: `raw/confluence/2026-07-23 프론트-백 합의 사항 — 격자 계약 (격자 사전 생성 정정) (cf-23199747).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/23199747
