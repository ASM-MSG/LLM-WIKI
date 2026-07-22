---
title: 개인 도감 화면 — 확정 UX·API 설계 (수집률/탐험률)
type: spec
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-22 개인 도감 화면 — 확정 UX·API 설계 (수집률·탐험률) (cf-21528615).md"
created: 2026-07-22
updated: 2026-07-22
keywords: [개인 도감, 도감, collection, 도감 화면, 수집률, 탐험률, exploration rate, progressRate, 격자 중심, grid-centric, 최근 수집 격자, RECENT, 30개 제한, 페이지네이션 없음, 역지오코딩, reverse geocode, region_stats, regions stats, 행정동, 격자 중심점, visitedRegionCount, MSG-153, MSG-152, MSG-155, MSG-156, PO 확정, 디자인 ver4, Owner A, Owner B, 6404, no-match, 빈 상태]
aliases: [도감 확정 설계, 개인 도감 UX, 탐험률 설계, 수집률 설계, MSG-153 설계]
related: ["[[Collection API 예정]]", "[[Region API 예정]]", "[[PRD FillMap MVP 화면별 기능·API]]", "[[IA v2 초안 (화면·기능 트리)]]", "[[갭 분석 디자인 문서 코드 싱크]]", "[[FillMap DB Schema v5 MVP]]"]
---

# 개인 도감 화면 — 확정 UX·API 설계 (수집률/탐험률)

> [!tldr]
> **PO 확정(2026-07-22)**: 개인 도감은 "격자 중심" UX — 진입 시 최근 수집 격자 목록(RECENT 고정·30개·페이지네이션 없음) + 현재 위치 기반 탐험률 패널("지금 여기, 역삼1동 25%"). 행정동/시군구 리스트 나열안은 기각, 디자인 ver4 시안의 "지역별 수집 현황(구 단위)"은 이 UX로 대체(시안 갱신 필요).
> 탐험률 축은 **격자 중심점의 행정동**(MSG-155 D2), 방문 지역 수는 **업로드 좌표**(MSG-152) — 두 축이 달라 라벨을 구분해야 한다.
> API는 기존 자산(summary·grids?bbox·reverse-geocode·region_stats·regions/stats 모두 merge) 재사용, 신규는 **MSG-153**(`GET /api/collections/grids` 목록+클릭 응답)뿐.

## 이 노트로 답할 수 있는 질문
- 개인 도감 첫 화면에는 뭐가 나오나? (격자 목록 vs 지역 리스트)
- 탐험률("역삼1동 25%")은 어떤 축으로 계산하나? 방문 지역 수와 왜 다르나?
- 도감 화면의 각 요소는 어떤 API를 쓰고, 뭐가 구현돼 있나?
- MSG-153에서 아직 확정해야 할 쟁점은?
- FE는 탐험률 빈 응답·에러 코드(6404)·progressRate를 어떻게 처리하나?
- 기각된 대안(시군구 상위 집계, bbox 응답 추가)은 왜 버렸나?

## 1. 확정 UX — "격자 중심"
- 도감 진입: **최근 수집 격자 목록** (RECENT 정렬 고정, 30개 제한, 페이지네이션 없음) + **탐험률 패널**(현재 위치 기반: FE가 lat/lon 전달 → 역지오코딩 → "지금 여기, 역삼1동 25%").
- 폴백: 위치 권한 거부·바다/해외(no-match) → 빈 상태.
- 격자 클릭: 그 격자의 정보(영상 수·수집 시각·커버 썸네일) + **소속 행정동의 탐험률을 함께 반환**.
- 기각된 대안(결정 이력): ① 행정동/시군구 리스트 첫 화면 나열 — 디자인 ver4의 "지역별 수집 현황(구)" 대체, **시안 갱신 필요(FE/디자인 공유)** ② 시군구 상위 집계 API — MVP 이후 (`regions.parent_code` 체인 재료는 준비됨) ③ 수집률 응답에 bbox/중심좌표 — 지도 이동은 격자 목록의 gridY/gridX가 담당.

## 2. 데이터 축 원칙
| 지표 | 축 | 근거 |
| --- | --- | --- |
| 탐험률(수집률) | **격자 중심점**이 속한 행정동 | 격자당 행정동 1개로 결정적, 경계 이중 카운트 없음 (MSG-155 D2) |
| 방문 지역 수(visitedRegionCount) | 영상 **업로드 좌표** | 방문 = 이벤트의 위치 (MSG-152) |

경계 지역에서 두 지표가 어긋나 보일 수 있음 → 한 화면에서 라벨 구분("방문 지역 N곳" vs "탐험률"). 노출 문구는 FE/기획 확정 필요.

## 3. API 매핑 — 기존 자산 재사용
| 화면 요소 | API | 상태 |
| --- | --- | --- |
| 상단 요약 카드 | `GET /api/collections/summary` | ✅ merge (MSG-152) |
| 지도 뷰 (내 격자 색칠) | `GET /api/grids?bbox` | ✅ merge (MSG-90) |
| 좌표 → 행정동 판정 | `GET /api/regions/reverse-geocode` / `resolveByPoint` | ✅ merge (MSG-93) |
| 행정동별 탐험률 데이터 | `region_stats` (업로드/삭제 시 동기 갱신) | ✅ merge (MSG-155) |
| 행정동별 탐험률 조회 | `GET /api/regions/stats` | ✅ merge (MSG-156) |
| 최근 수집 격자 30개 + 클릭 응답 | `GET /api/collections/grids` (+상세) | ⬜ **MSG-153 구현 예정** |

신규 로직이 거의 없음 — MSG-153은 목록 쿼리 + 기존 자산 조합.

## 4. MSG-153에서 확정할 쟁점
1. **탐험률 조회 형태**: FE 2-call(역지오코딩 → regions/stats에 regionCode 단건 파라미터) vs **BE 1-call(좌표→행정동+탐험률 통합, 유력)** — 진입 초기값과 격자 클릭 응답 모양 통일 가능.
2. **격자 목록의 행정동 표기 축**: `videos.region_code`(영상 축) join 계획이 탐험률(격자 중심 축)과 어긋날 수 있음 — 중심점 축 통일 여부.
3. **Owner 경계**: 도감(usergrid, Owner B)이 행정동 귀속·탐험률(Owner A 자산)을 소비 — 계약 신설 vs region 쪽에서 A 자기완결.

## 5. FE 처리 규칙
- 탐험률 빈 배열/null = **에러 아님** (수집 없음·no-match는 정상).
- `6404` = 실존하지 않는 행정 구역 코드 입력 오류일 때만.
- `progressRate`는 서버에서 100 상한 clamp 완료 — FE 추가 처리 불필요.
- 탐험률은 업로드/삭제와 같은 트랜잭션에서 즉시 갱신 — 업로드 직후 재조회 시 최신값.
- 시/도 합산("서울 34%")을 FE에서 임의 계산 금지 — 집계 정책 미확정.

## 출처
raw: `raw/confluence/2026-07-22 개인 도감 화면 — 확정 UX·API 설계 (수집률·탐험률) (cf-21528615).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21528615
