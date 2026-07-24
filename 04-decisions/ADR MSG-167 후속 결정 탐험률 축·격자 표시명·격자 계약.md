---
title: ADR MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 · FE 격자 계약
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-23 MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 (cf-23035906) v2.md, raw/confluence/2026-07-23 MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 (cf-23035906).md"
created: 2026-07-23
updated: 2026-07-24
keywords: [MSG-167, 후속 결정, region_code, grids, 라벨, 탐험률, 동 단위, 행정동, 격자 표시명, zone, 서면 A-14, FE 계약, grid contract, 격자 사전 생성, 전역 고정 눈금, GridEncoder, Math.floor, GRID_LAT_STEP, GRID_LNG_STEP, 0.0009, 0.00115, regionName, nullable, PR 52, 멘토 피드백, 영상 직접 연결 기각]
aliases: [MSG-167 후속, 격자 계약, FE 격자 계약, 탐험률 축 확정]
related: ["[[ADR 격자 행정동 라벨 grids.region_code]]", "[[ADR 격자 표시명 zone]]", "[[개인 도감 화면 확정 UX·API 설계]]", "[[Grid API]]", "[[FillMap API 스펙 통합]]", "[[2026-07-23 기획회의 미션·이벤트 표시 방식]]", "[[FE 격자 계약 프론트-백 합의]]"]
---

# ADR MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 · FE 격자 계약

> [!tldr]
> PR #52 머지 시점 결정 기록(2026-07-23, KangJeong). ① 멘토의 "영상→리전 직접 연결" 제안 **기각** — 저장하는 건 N:M 포함관계가 아니라 격자 중심점 대표 귀속(함수값 1개)이라 grids.region_code 유지, videos 복제는 드리프트 ② **탐험률 축 = 동(행정동) 단위 확정**(BE 기구현, 변경 0건) ③ 격자 표시명 "서면 A-14" = zone ADR 재확인, 그 전까지 regionName 폴백.
> **FE 격자 계약**: "격자 사전 생성" 합의 정정 — 격자는 서버 리소스가 아니라 **전역 고정 눈금**(0.0009°×0.00115°, Math.floor 반열림). FE가 로컬 계산으로 칸을 그리고, DB엔 영상 올라온 칸만 기록.
> nullable 2개는 정상 케이스: regionName(무귀속 해안 칸) · thumbnailUrl(READY 전).

## 이 노트로 답할 수 있는 질문
- 멘토의 "영상→리전 직접 연결" 제안은 왜 기각됐나?
- 탐험률은 구 단위인가 동 단위인가? (동 확정)
- "서면 A-14" 표시명은 언제 어떻게 제공되나? 그 전엔?
- FE는 격자 칸을 어떻게 그리나? (로컬 산술 — 코드 포함)
- "격자 사전 생성" 얘기는 어떻게 정리됐나?
- regionName·thumbnailUrl이 null이면 에러인가? (아니오)

## 결정 요약
1. **라벨 저장 = grids.region_code 유지** — 목적은 조회 경로 geospatial 금지(ADR)+귀속 축 통일. 조인 비용 PK 건당 0.006ms(MSG-164). videos.region_code는 영상 좌표 축 예약 컬럼(MSG-66 유예)이라 대체 저장소 아님.
2. **탐험률 축 = 동 단위** — 그 동 수집 격자/총 격자. region_stats 기구현 그대로, 구 단위 집계 API 불필요. 디자인 목업 "부산진구 탐험률"은 실데이터상 동 이름으로 표시.
3. **격자 표시명 = zone ADR(cf-18972673) 재확인** — zones 테이블+좌표 산술, 미매칭은 행정동 이름 폴백. BE 별도 티켓 필요. ver 5 디자인이 전 화면 채택.
4. **동 단위 영상 조회 — 구현 완료 (PR #55, 2026-07-23 저녁)**: `GET /api/collections/videos?regionCode=` — 테스트 16건 신규·빌드 green·리뷰 클린. MSG-167 전체 스코프(라벨 기입·갤러리 regionName·동 단위 영상) 종결. 구현 중 확정: 전역 400 매핑 2건(파라미터 누락·타입 불일치가 500이던 결함 정정), 정렬 타이브레이크 created_at DESC + id DESC, 페이지네이션 미도입 유지(Open Q: 무한스크롤 필요 여부 PO/FE 확인). 알려진 한계: 행정동 경계 개편 시 기존 라벨 재판정 없음(운영 마이그레이션 소관).
5. **FE 전달 사항 분리**: 격자 계약 상세는 [[FE 격자 계약 프론트-백 합의]] 페이지로 분리됨 (cf-23199747).

## FE 격자 계약 (2026-07-23)
- **격자 = 전역 고정 눈금**: `gridY = Math.floor(lat/0.0009)`, `gridX = Math.floor(lng/0.00115)`, `gridId = "{y}_{x}"` — `| 0`·parseInt 금지(음수 좌표). bbox·center 전부 산술. 상세 코드는 raw 참조.
- API 계약: 색칠 `GET /api/grids`(bbox 0.5도, size≤5000, cursor) · 칸 클릭 `GET /api/grids/{gridId}`(미존재도 200 occupied=false) · 갤러리 `GET /api/collections/grids`(regionName nullable) · 탐험률 by-point/by-grid(동 단위) · 동 단위 영상(신규, 빈 배열 200).

## 출처
raw: `raw/confluence/2026-07-23 MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 (cf-23035906) v2.md` (최신 — PR #55 종결 기록), `raw/confluence/2026-07-23 MSG-167 후속 결정 — 라벨 저장 위치 Q&A · 탐험률 축 · 격자 표시명 (cf-23035906).md` (초판)
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/23035906
