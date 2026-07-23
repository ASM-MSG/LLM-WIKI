---
title: ADR — 격자 표시명 체계 (수동 지정 구역 zone + 격자 좌표 산술)
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-18 설계결정 격자 표시명 — 수동 지정 구역(zone) + 격자 좌표 산술 (cf-18972673).md"
created: 2026-07-18
updated: 2026-07-21
keywords: [ADR, 격자 표시명, zone, 구역, 홍대, 가로수길, 표시명, display name, A-14, 행정동 폴백, 지하철역, 산술, zones 테이블, 검색]
aliases: [격자 표시명 ADR, zone ADR]
related: ["[[Region API 예정]]", "[[ADR 지도 SDK 네이버 전환]]", "[[갭 분석 디자인 문서 코드 싱크]]", "[[Grid 확장 API 예정]]", "[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]]"]
---

# ADR — 격자 표시명 체계 (수동 지정 구역 zone + 격자 좌표 산술)

> [!tldr]
> "홍대입구 A-14" 같은 사람용 격자 이름은 **수동 지정 구역(zones) + 격자 좌표 산술**로 결정 (상태: 제안됨 — 규호·디자이너 확인 필요).
> zones는 grid_y/x 정수 사각형(PostGIS 불필요), 이름 = zone명 + 행(A=북쪽)·열(서→동) 산술 — grids에 저장 안 해도 빈 격자도 즉시 계산. 유명 구역 아니면 행정동 폴백.
> 기각: 행정동만(홍대 안 나옴), 지하철역 반경 자동(가로수길류 미커버·경계 애매·역 개통 시 이름 변동). zones가 검색까지 풀어 네이버 SDK 결정도 강화. 한계: 남북 26행=2.6km.

## 이 노트로 답할 수 있는 질문
- "홍대 A-14" 같은 격자 이름은 어떻게 만들어지나?
- 왜 지하철역 반경 자동 판정을 기각했나?
- zones 테이블 구조와 이름 산술 규칙은?
- 유명 구역이 아닌 격자는 어떻게 표시되나?
- 구역 크기 한계는 얼마인가?
- 남은 쟁점 3개는 뭔가?

## 맥락
시안은 "홍대입구 A-14"를 요구하는데 grid_id는 `{grid_y}_{grid_x}` 기계 식별자뿐. "홍대"는 행정동이 아니고(서교동/동교동), 통칭은 행정동으로도 역명으로도 일반화 안 됨(가로수길·경리단길).

## 선택지
① 행정동만 ② 지하철역 반경 자동 판정 ③ 수동 지정 zone + 산술.

## 결정
**③ 채택.** zones(name·region_code·min/max_grid_y/x·priority) 정수 사각형. `row = max_grid_y - grid_y → A,B,C…(북쪽이 A)`, `col = grid_x - min_grid_x + 1`. 매칭 없으면 행정동 폴백. 검색도 zones→regions 2단 폴백으로 확장 — 네이버 SDK의 키워드 검색 부재가 무의미해져 [[ADR 지도 SDK 네이버 전환]]이 더 단단해짐.

## 근거
가로수길류 커버 · 커버리지 통제 · lazy insert여도 순수 산술이라 즉시 계산 · 외부 데이터 무의존(이름 안정).

## 영향
- 한계: 알파벳 26행 = 남북 2.6km — MVP 구역은 2.6km 이하로 제약.
- 쟁점: ① 행정동 폴백 번호 체계(추천: 번호 없이 "서교동"만) ② 구역 겹침(안 겹치게 그리는 운영 규칙 추천) ③ 서울 상권 30~50개를 누가 어떻게(드래그 내부 도구 제안).
- 후속: zones 마이그레이션 · 시딩 · 이름 계산 유틸(GridEncoder 옆) · GET /api/search · glossary에 용어 추가 · 디자이너 확인.

## 출처
raw: `raw/confluence/2026-07-18 설계결정 격자 표시명 — 수동 지정 구역(zone) + 격자 좌표 산술 (cf-18972673).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18972673
