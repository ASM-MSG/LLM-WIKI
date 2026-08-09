---
title: FE 격자 계약 — 프론트-백 합의 (격자 사전 생성 정정)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-23 프론트-백 합의 사항 — 격자 계약 (격자 사전 생성 정정) (cf-23199747).md"
created: 2026-07-23
updated: 2026-08-09
keywords: [격자 계약, grid contract, FE, 프론트, 사전 생성, 전역 고정 눈금, GRID_LAT_STEP, GRID_LNG_STEP, 0.0009, 0.00115, Math.floor, GridEncoder, gridId, bbox, 네이버 지도, v3, WGS84, TM128, naver.maps, getBounds, Rectangle, regionName, nullable, thumbnailUrl, zones, zone 보류, MSG-234, displayName, 서면 A-14, 장소 검색, api/search, by-point, by-grid, regionCode]
aliases: [격자 계약, FE 격자 계약, 격자 사전 생성 정정, 네이버 v3 격자 연동]
related: ["[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]]", "[[ADR 격자 표시명 zone]]", "[[ADR 지도 SDK 네이버 전환]]", "[[Grid API]]", "[[FillMap API 스펙 통합]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[MSG-234 상권 작도 결정 공공데이터 검수]]", "[[zone 표시명 FE 계약]]", "[[지도 홈 API 연동 가이드 FE]]", "[[지도·공간 데이터 설계 멘토 설명용]]", "[[2026-08-08 김민수 멘토 멘토링]]"]
---


> **⚠️ 결정 변경 (2026-08-08, MSG-347)**: 격자 계산 규칙 자체가 **EPSG:5179 미터 좌표 기반**으로 바뀌었다. 아래 "전역 고정 눈금 0.0009°×0.00115°, `Math.floor`" 산술은 **이력**이다. 새 규칙은 위경도를 5179로 투영한 뒤 `floor(x/100)`·`floor(y/100)`이고, FE는 proj4js로 BE와 **같은 proj4 정의 문자열**을 쓴다. 셀이 위경도 축과 평행하지 않아 렌더는 `Rectangle` → **`Polygon`(꼭짓점 4점)**, 뷰포트 격자 범위도 SW·NE 2점 → **꼭짓점 4점 min/max**로 바뀐다. gridId 포맷·API 계약·nullable 2종·zone 캐시 용도는 불변이고 **값만** 바뀐다(서울 `41642_110458` → `19422_9582` 대역). 검증은 BE 픽스처 `grid-epsg5179-samples.json` 200건 전수 대조. 정본: [[ADR 격자 계산 EPSG5179 전환]] · BE 레포 `docs/MSG-347.md`.
>
> **⚠️ 결정 변경 (2026-08-07, MSG-341)**: 표시명 계산 주체가 **서버**로 바뀌었다. 격자를 담는 조회 응답 9종에 `zoneName`·`zoneCell` 필드가 실려 오고, FE는 조립(`zoneName + " " + zoneCell`)과 행정동 폴백 표시만 한다. 이 문서의 "화면이 만드는 규칙"(FE 로컬 산술) 서술은 이력이다. 명명 규칙 자체와 폴백 번호 없음, zones 캐시의 검색 이동 용도(§D6)는 불변. 정본: BE 레포 `docs/MSG-341.md`.

# FE 격자 계약 — 프론트-백 합의 (격자 사전 생성 정정)

> [!tldr]
> "격자 사전 생성" 합의 정정 — 격자는 서버 리소스가 아니라 **전역 고정 눈금**(0.0009°×0.00115°, Math.floor 반열림). FE가 로컬 산술로 칸을 그리고, DB엔 영상 올라온 칸만 기록.
> 네이버 지도 **v3(WGS84)** 좌표가 계산식 입력 그 자체라 변환 0 — 단 레거시 v2(TM128)·좌표 반올림은 금지.
> **zone 재개(2026-07-30)**: 표시명 "서면 A-14" 기계장치는 MSG-234로 구현 완료·데이터 시딩만 잔여(MSG-259) — FE 구현 계약은 [[zone 표시명 FE 계약]] 참조. 장소 검색은 카카오 프록시(MSG-251)로 분리 완료.

## 이 노트로 답할 수 있는 질문
- 격자 사전 생성 논의는 어떻게 정리됐나? (없던 걸로 — 전역 고정 눈금)
- FE는 격자 ID·칸 경계를 어떻게 계산하나? (Math.floor 산술 — 코드 포함)
- 격자 관련 API 계약은? (색칠·칸 클릭·갤러리·탐험률·동 단위 영상 5종)
- 네이버 지도 v3에서 이 계약이 그대로 통하나? (WGS84라 직결 — v2·반올림만 금지)
- "서면 A-14" 표시명은 언제 어떻게? (구현 완료·시딩 잔여 — 계약은 [[zone 표시명 FE 계약]])
- regionName·thumbnailUrl이 null이면? (정상 케이스 2종)

## 계약 요약
1. **격자 = 전역 고정 눈금**: `gridY = Math.floor(lat/0.0009)`, `gridX = Math.floor(lng/0.00115)`, `gridId = "{y}_{x}"` — `| 0`·parseInt 금지(음수 좌표). bbox·center 전부 산술. BE GridEncoder와 동일해야 함(서버 재계산이 정본, FE는 표시용).
2. **API 5종**: 색칠 `GET /api/grids`(bbox 0.5도·size≤5000·cursor) · 칸 클릭 `GET /api/grids/{gridId}`(미존재도 200 occupied=false) · 갤러리 `GET /api/collections/grids`(regionName nullable) · 탐험률 by-point/by-grid(동 단위) · 동 단위 영상 `GET /api/collections/videos?regionCode=`(gridId 포함, 빈 배열 200, 페이지네이션 없음).
3. **네이버 v3 직결**: `e.coord.lat()`·`getBounds()`가 WGS84라 계산식 입력 그 자체. 셀은 Rectangle에 bbox 산술값 그대로. ⚠ 레거시 v2(TM128)·좌표 반올림(toFixed) 금지.
4. **nullable 2종 = 정상**: regionName(무귀속 해안 칸) · thumbnailUrl(READY 전).
5. ~~zone 보류~~ → **zone 재개·구현 완료 (2026-07-30 갱신)**: `GET /api/zones`는 develop 반영 완료(MSG-234), 데이터 시딩만 남음(MSG-259). FE 구현 계약(응답 형태·명명 산술 참조 구현·검증 기대값 표·엣지 케이스)은 **[[zone 표시명 FE 계약]]이 정본** — 원문 §7·§7-1을 대체. 시딩 전엔 빈 배열 → 기존 행정동 폴백(regionName) 그대로, 시딩 후 FE 재배포 없이 "서면 A-14" 활성. 장소 검색은 [[ADR 장소 검색 카카오 로컬 프록시]]로 분리(MSG-251, 구현 완료).

## 출처
raw: `raw/confluence/2026-07-23 프론트-백 합의 사항 — 격자 계약 (격자 사전 생성 정정) (cf-23199747).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/23199747
