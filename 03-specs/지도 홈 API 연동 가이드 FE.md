---
title: 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-08-07 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07) (cf-32636957).md"
created: 2026-08-07
updated: 2026-08-09
keywords: [지도 홈, 홈 화면, FE 연동, 프론트 가이드, 피그마 14176-6312, GET /api/zones, GET /api/grids, bbox, swLat, neLng, 0.5도, 4402, VIEWPORT_TOO_LARGE, nextCursor, 커서, 클러스터, 500m, floor, hotzones, missions/active, BOX, PATH, REGION, CELLS, reverse-geocode, regions grids, POPULAR, LATEST, gridCount, videoCount, coverThumbnailUrl, coverDurationSec, presigned URL, stats/by-grid, 탐험률, search places, trending, 디바운스, 300ms, 영상 검색 제외, zone-naming.json, 강남역 검증 벡터, MSG-340, MSG-234, MSG-259]
aliases: [지도 홈 FE 가이드, 홈 화면 API 매핑, 지도 홈 연동, FE 전달용 가이드]
related: ["[[ADR 격자 계산 EPSG5179 전환]]", "[[기획확정 지도 홈 개편 상단 셀]]", "[[zone 표시명 FE 계약]]", "[[FE 격자 계약 프론트-백 합의]]", "[[FillMap API 스펙 통합]]", "[[ADR 장소 검색 카카오 로컬 프록시]]", "[[지도·공간 데이터 설계 멘토 설명용]]", "[[PRD FillMap MVP 화면별 기능·API]]"]
---

# 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07)

> [!warning] 격자 산술은 이후 교체됨 (2026-08-08, MSG-347)
> 본문의 `floor(lat/0.0009)`·`floor(lng/0.00115)`는 **EPSG:5179 `floor(x/100)`으로 전환**됐다 →
> [[ADR 격자 계산 EPSG5179 전환]]. 셀이 위경도 축과 평행하지 않게 되어 FE 렌더는 Rectangle→**Polygon**,
> 뷰포트 범위는 2점→**4점**이다. **엔드포인트·응답 필드·호출 수·bbox 상한·표시명 규칙은 전부 유효**하고,
> 바뀐 것은 좌표→칸 번호 변환식과 격자선 도형뿐이다.

> [!tldr]
> 지도 홈 디자인(피그마 노드 14176-6312)의 **화면 요소마다 어떤 API를 어떻게 부르는지** 1:1로 매핑한 FE 전달 문서. 엔드포인트와 응답 필드는 2026-08-07 develop 코드에서 전수 확인했다.
> 핵심은 **서버 호출이 0인 항목이 꽤 많다는 것** — 점선 격자망, 격자 이름("서면 A-14"), 500m 줌아웃 클러스터, 격자 검색은 전부 FE 로컬 산술이다. 앱 기동 시 `GET /api/zones` 48건을 한 번 캐시하면 이름 관련 서버 호출은 이후 없다.
> 주의 지점 셋: **bbox는 위·경도 각 변에 따로 0.5도 상한**이라 부산 전역(경도 0.514°)은 동서 2분할이 필요하고, `sort`는 **대문자 전용**, 콘텐츠 없는 동네는 404가 아니라 **200 + 카운트 0 + 빈 배열**이다. 영상 검색은 2026-08-07 제외 확정 — 검색바 플레이스홀더에서 "영상" 제거 요청 필요.

## 이 노트로 답할 수 있는 질문
- 지도 홈 화면의 각 요소는 어떤 API에서 오나? 호출 수는 몇 개인가?
- FE가 서버 없이 직접 계산하는 것은 무엇인가?
- bbox 상한을 넘기면 어떻게 되나? 부산 전역은 왜 한 번에 못 부르나?
- 좌측 패널 카드 제목("서면 A-14")은 어디서 오나?
- 콘텐츠 없는 지역·바다 좌표는 어떤 응답이 오나?
- FE 격자 이름 구현이 BE와 일치하는지 어떻게 검증하나?

## 0. 앱 기동 1회
`GET /api/zones` → 구역 사각형 48건 메모리 캐시. 카드 제목·격자 이름의 재료이며 이후 이름 관련 서버 호출 없음. 응답 `regionCode`는 현재 전건 null이고 계산에 안 쓰니 무시.

## 1. 지도 영역

| 화면 요소 | 어디서 오나 |
| --- | --- |
| 점선 격자망 | **호출 0** — `floor(lat/0.0009)`, `floor(lng/0.00115)` (절사 아니라 `Math.floor`) |
| 색칠된 칸(내 도감) | `GET /api/grids?swLat&swLng&neLat&neLng` — 지도 이동이 멈출 때마다 |

- 응답 `gridY`·`gridX` 정수에 스텝을 곱하면 사각형 꼭짓점. 문자열 파싱 불필요.
- **bbox 상한: 위도·경도 각 변에 따로 0.5도.** 정확히 0.5도는 허용, 초과하면 잘림 없이 400(developCode 4402). 부산 전역은 경도 폭 0.514°라 **동서 2분할** 필요. (명세 보강 티켓 MSG-340)
- 다음 페이지는 응답 `nextCursor`를 `cursor` 파라미터로.
- **줌아웃 500m 클러스터: 추가 호출 없음** — 같은 데이터를 `floor(gridY/5)`, `floor(gridX/5)`로 묶으면 격자선과 정확히 정렬된다.

## 2. 상단 칩 4종 (한 번에 하나만 활성)

| 칩 | API |
| --- | --- |
| 핫구역 | `GET /api/hotzones` + 현재 bbox (최근 48시간 상위 격자) |
| 지역축제·팝업스토어·경로추천 | 셋 다 `GET /api/missions/active` 하나 (bbox 없는 전역 목록) |

missions/active는 서버가 1시간 캐시. 진입 시 한 번 받아 두고 **칩 전환은 재호출 없이** 응답의 렌더 shape(축제=BOX, 경로=PATH, 구역=REGION, 테마=CELLS)로 FE가 걸러 그린다.

## 3. 좌측 패널 — "이 지역 격자 N개 · 영상 M개"

```
지도 중심 좌표
→ GET /api/regions/reverse-geocode?lat&lng            → regionCode
→ GET /api/regions/{regionCode}/grids?sort=POPULAR&limit=3
```

| 디자인 요소 | 응답 필드 |
| --- | --- |
| "격자 5개 · 영상 355개" | `gridCount`, `videoCount` — **limit과 무관하게 전체 기준**이라 "전체 보기"와 숫자가 일치 |
| 카드 썸네일 | `grids[].coverThumbnailUrl` (presigned URL) |
| "1:24" 재생시간 배지 | `grids[].coverDurationSec` |
| "138개 영상" | `grids[].videoCount` |
| 카드 제목 "서면 A-14" | **응답에 없음** — `gridId`를 zones 캐시와 대조해 FE 로컬 산술. 구역 밖이면 `regionName` 폴백(번호 없이 이름만) |
| "전체 보기" | 같은 API를 `limit` 생략으로 재호출 |

- 콘텐츠 없는 동네는 **404가 아니라 200 + 카운트 0 + 빈 배열** — 에러 분기 없이 빈 상태 UI만.
- `sort`는 **대문자 전용**(`POPULAR` 조회수순 / `LATEST` 최신순). 소문자는 400.

## 4. 격자 클릭 → 요약 패널

| 내용 | 어디서 오나 |
| --- | --- |
| 격자 이름("서면 I-6" 또는 "부전제1동") | **호출 0** — 클릭 좌표를 `Math.floor`로 칸 번호화 후 zones 캐시와 정수 비교 |
| 행정동 이름 + 탐험률 | `GET /api/regions/stats/by-grid?gridId={y}_{x}` 1콜 |
| 내 점령 여부·영상 수 | 필요 시 `GET /api/grids/{gridId}` — 미점령도 404 아닌 `occupied=false` |

by-grid에 gridId를 그대로 넘기면 중심점 판정을 서버가 하므로 FE 좌표 변환 불필요. 바다처럼 무귀속이면 **200 + data null**.

## 5. 검색바

| 기능 | API | 상태 |
| --- | --- | --- |
| 인기 검색어 | `GET /api/search/trending` | 구현됨 |
| 장소 검색 | `GET /api/search/places?q=` (카카오 프록시, 300ms 디바운스) | 구현됨 — 결과에 gridId가 실려 와 선택 즉시 지도 이동 + 하이라이트 |
| 격자 검색("서면 A-14" 역파싱) | 서버 API 없음 — zones 캐시 48건 로컬 필터 | **FE 몫** (MSG-234 §D6) |
| 영상 검색 | — | **제외 확정 (2026-08-07, 정민·BE)** — 플레이스홀더에서 "영상" 제거 요청 필요 |

## 호출 수 요약

| 시점 | 호출 |
| --- | --- |
| 앱 기동 | zones 1 (+ missions 1) |
| 지도 팬·줌 1회 | grids 1 (+ 핫구역 칩 활성 시 hotzones 1) |
| 패널 갱신(중심 이동) | reverse-geocode 1 + region grids 1 |
| 격자 클릭 1회 | stats/by-grid 1 |
| 격자 이름·격자망·클러스터 | **0** (전부 FE 산술) |

## 구현 검증
격자 이름 산술의 실행형 정본은 BE 레포의 언어 중립 픽스처 `src/test/resources/fixtures/zone-naming.json` (7 시나리오 — 북단·서단 A-1, 겹침 타이브레이크, 행정동 폴백, null). **FE 테스트가 이 파일을 파싱해 자체 구현을 검증하면 계약 일치가 보장된다.** 좌표→칸 검증 벡터: 강남역 (37.4979, 127.0276) → `"41664_110458"`.

## 출처
raw: `raw/confluence/2026-08-07 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07) (cf-32636957).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/32636957
화면 근거: 피그마 노드 14176-6312 · 레포 보존 캡처 `blog-images/msg236-map-home.png`
