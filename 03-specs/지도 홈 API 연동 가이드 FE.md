---
title: 지도 홈 API 연동 가이드 (FE 전달용)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-08-15 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07) (cf-32636957).md, raw/confluence/2026-08-07 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07) (cf-32636957).md"
created: 2026-08-07
updated: 2026-08-19
keywords: [지도 홈, 홈 화면, FE 연동, 프론트 가이드, 피그마 14176-6312, GET /api/zones, GET /api/grids, aggregation, 집계, 줌아웃, currentRegion, items, bbox, swLat, neLng, 0.5도, 1.0도, 4.0도, 10.0도, 4401, 4402, 4405, VIEWPORT_TOO_LARGE, INVALID_AGGREGATION_UNIT, nextCursor, 커서, DONG, SIGUNGU, SIDO, EPSG:5179, proj4, 폴리곤, 4점, hotzones, missions/active, BOX, PATH, REGION, CELLS, collections grids, UPLOADED, COLLECTED, LATEST, POPULAR, 장소 불러오기, 이 지역 재검색, 헤더 카운트 폐기, coverThumbnailUrl, coverDurationSec, zoneName, zoneCell, regionName, presigned URL, stats/by-grid, 탐험률, search places, trending, 디바운스, 영상 검색 제외, zone-naming.json, 강남역 검증 벡터, MSG-347, MSG-356, MSG-374, MSG-387, MSG-388]
aliases: [지도 홈 FE 가이드, 홈 화면 API 매핑, 지도 홈 연동, FE 전달용 가이드]
related: ["[[ADR 격자 계산 EPSG5179 전환]]", "[[ADR 줌아웃 클러스터링 행정 단위 집계 H3 기각]]", "[[기획확정 지도 홈 개편 상단 셀]]", "[[zone 표시명 FE 계약]]", "[[FE 격자 계약 프론트-백 합의]]", "[[FillMap API 스펙 통합]]", "[[ADR 장소 검색 카카오 로컬 프록시]]", "[[지도·공간 데이터 설계 멘토 설명용]]", "[[PRD FillMap MVP 화면별 기능·API]]"]
---

# 지도 홈 API 연동 가이드 (FE 전달용)

> [!tldr]
> 지도 홈 디자인(피그마 노드 14176-6312)의 **화면 요소마다 어떤 API를 어떻게 부르는지** 1:1로 매핑한 FE 전달 문서. 원본은 2026-08-07 작성이고 그 뒤 네 번 갱신됐다(8/8 격자 산술, 8/10 줌아웃 집계, 8/13 응답 겉면·카드 규칙, 8/15 패널 전면).
> **가장 크게 바뀐 것 둘**: ① 줌아웃 클러스터가 FE 로컬 산술에서 **서버 집계**로 넘어갔다(MSG-356). ② 좌측 패널이 전역 조회에서 **내 격자 카드 조회**로 바뀌고 헤더의 "격자 N개 · 영상 M개" 줄은 **폐기**됐다(MSG-388, 2026-08-15).
> 여전히 서버 호출이 0인 것: 점선 격자망, 격자 이름 조립, 격자 검색. 주의 지점 셋은 **bbox 상한(개별 0.5도, 집계는 단위별 차등)**, **`sort`는 대문자 전용이고 값 이름이 바뀌었다(`LATEST` 아님, `UPLOADED`)**, **빈 동네는 404가 아니라 200 + 빈 배열**이다.

## 이 노트로 답할 수 있는 질문
- 지도 홈 화면의 각 요소는 어떤 API에서 오나? 호출 수는?
- 줌아웃하면 무엇이 내려오나? 단위(동·구·시)는 누가 정하나?
- 좌측 패널의 지역명과 카드는 각각 어디서 오나?
- FE가 서버 없이 직접 계산하는 것은 무엇인가?
- bbox 상한을 넘기면 어떻게 되나?
- FE 격자 이름 구현이 BE와 일치하는지 어떻게 검증하나?

## 0. 앱 기동 1회
`GET /api/zones` → 구역 사각형 48건 메모리 캐시. 격자 검색(역파싱)의 재료다. 응답 `regionCode`는 현재 전건 null이라 무시한다.

표시명 계산 자체는 2026-08-07에 서버로 옮겨졌다(MSG-341) — 격자를 담는 응답이 `zoneName`·`zoneCell`·`regionName`을 직접 내려주므로 카드 제목은 zones 캐시 대조 없이 조립만 하면 된다.

## 1. 지도 영역 (점선 격자망 + 색칠 칸)

| 화면 요소 | 어디서 오나 |
| --- | --- |
| 점선 격자망 | **호출 0** — 좌표를 EPSG:5179로 변환(proj4js)한 뒤 `floor(x/100)`, `floor(y/100)` |
| 색칠된 칸(내 도감) | `GET /api/grids?swLat&swLng&neLat&neLng` — 지도 이동이 멈출 때마다 |

- `gridY`·`gridX`에 100을 곱한 5179 좌표를 역변환하면 셀 꼭짓점이 나온다. 문자열 파싱 불필요.
- **셀은 위경도 축과 평행하지 않다**(자오선 수렴 최대 약 1.6도). 2점 직사각형이 아니라 **꼭짓점 4점 폴리곤**으로 그리고, 화면 격자 범위도 4점의 min/max로 구한다.
- proj4 정의 문자열은 서버와 **글자 단위로 같아야** 한다: `+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs`
- **bbox 상한: 위도·경도 각 변에 따로 0.5도.** 정확히 0.5도는 허용, 초과하면 400(4402). 부산 전역은 경도 폭 0.514°라 **동서 2분할** 필요(명세 보강 티켓 MSG-340).
- 다음 페이지는 응답 `nextCursor`를 `cursor` 파라미터로.
- 옛 판의 "줌아웃 500m 클러스터는 FE 로컬 산술"은 **폐기**됐다(2026-08-10) → 아래 1.5절.

## 1.5 줌아웃 클러스터링 — 서버 집계 (MSG-356, 겉면 MSG-374)

```
내 도감:    GET /api/grids/aggregation?swLat&swLng&neLat&neLng&unit=DONG|SIGUNGU|SIDO
친구 도감:  GET /api/friends/{userId}/grids/aggregation
```

unit은 대소문자 무관. 전환 축척은 **FE가 정한다**(서버는 축척을 모른다). 2026-08-10 합의 시작값은 개별 칸 ~100m대, 동 250m~500m, 구 1km~8km, 시 16km~전체다.

**응답은 `{currentRegion, items}` 객체다** (내 도감만. 친구 집계는 예전처럼 배열 — 친구 화면에 좌측 패널이 없어 MSG-374가 닿지 않았다).

- `currentRegion` — 뷰포트 **중심점**이 속한 행정동. unit·축척과 무관하게 항상 온다. `name`은 동 이름 한 토큰("부전2동"). `gridCount`·`videoCount`는 그 동 전체에서 내 것을 세지만 **헤더 카운트 줄이 8/15 폐기되어 화면은 더는 쓰지 않는다**(필드는 서버 계약으로 유지). 중심이 바다·국외면 `null`(에러 아님).
- `items[]` — `regionCode`(마커 식별 키, 동 이름은 전국 중복 가능) · `name` · `lat`·`lng` · `count`. 행정동 없는 격자는 이름 null 항목으로 묶여 온다(합이 개별 칸 총수와 맞아야 하므로). 0개인 동은 항목 자체가 안 온다. 정렬은 regionCode 오름차순, null 마지막.
- 마커 겹침 병합은 네이버 지도 SDK 클러스터링이 하고, 병합 숫자는 count를 그냥 더하면 된다.
- **상한은 단위별 차등**: 동 1.0도, 구 4.0도, 시 10.0도(전국 시야 약 5도라 한 번에 가능). 초과 4402, 뷰포트 불량 4401, unit 불량 **4405**.

## 2. 상단 칩 4종 (한 번에 하나만 활성)

| 칩 | API |
| --- | --- |
| 핫구역 | `GET /api/hotzones` + 현재 bbox (최근 48시간 상위 격자) |
| 지역축제·팝업스토어·경로추천 | 셋 다 `GET /api/missions/active` 하나 (bbox 없는 전역 목록) |

missions/active는 서버가 1시간 캐시. 진입 시 한 번 받아 두고 **칩 전환은 재호출 없이** 응답의 렌더 shape(축제=BOX, 경로=PATH, 구역=REGION, 테마=CELLS)로 FE가 걸러 그린다.

## 3. 좌측 패널 — 헤더는 동 이름만, 카드는 내 격자 (2026-08-15 전면 갱신)

**지역명**은 집계 응답의 `currentRegion` 하나로 끝난다. reverse-geocode 호출은 이 화면에서 더는 필요 없다.

| 디자인 요소 | 응답 필드 |
| --- | --- |
| 지역명 | `currentRegion.name` (동 이름 한 토큰. 디자인의 "부산진구 부전동"처럼 구 병기가 필요하면 서버 확장 논의 필요) |
| "부전동 장소 불러오기" 버튼 라벨 | `currentRegion.name` 재사용 |
| 버튼 노출 여부 | **FE 규칙** — 뷰포트 가로·세로 모두 1km 이하일 때만 |

확대 구간(개별 칸을 그리는 시야)에는 개별 격자 조회에 `currentRegion`이 없으므로 집계 조회를 `unit=DONG`으로 **같이** 부른다. 이 시야의 bbox는 동 단위 상한(1.0도) 안이라 4402 걱정이 없다.

**카드 = 내 격자, 최신 업로드순 최대 20장.** "장소 불러오기"를 눌렀을 때만 갱신한다(지도 이동만으로는 안 바뀐다 — 네이버 지도 "이 지역 재검색"과 같은 패턴).

```
GET /api/collections/grids?regionCode={currentRegion.regionCode}&sort=UPLOADED&limit=20
```

**임시로 쓰던 전역 조회에서 갈아탈 때 두 가지가 다르다**: ① 경로가 `/api/regions/{regionCode}/grids`(전역, 타인 영상 포함)에서 내 도감 조회 확장으로 바뀐다 — 인증 토큰 필수, 응답은 내 격자만. ② `sort` 값 이름이 다르다 — `UPLOADED`(내 영상 최신 업로드순) · `COLLECTED`(수집순, 기본값). 기존 `LATEST`·`POPULAR`를 그대로 보내면 **400**이다. 전역 조회는 상단 칩 화면과 격자 썸네일 뷰 용도로만 남는다.

| 디자인 요소 | 응답 필드 |
| --- | --- |
| 카드 썸네일 | `[].coverThumbnailUrl` (presigned URL). **인코딩 전이면 null인데 카드는 그려야 한다** — 플레이스홀더 |
| "1:24" 재생시간 배지 | `[].coverDurationSec` — 인코딩 중에도 온다. null은 커버 영상 자체가 없는 격자뿐 |
| "138개 영상" | `[].videoCount` — 내 영상 수(비공개·인코딩 중·블라인드 포함, 삭제만 차감) |
| 카드 제목 "서면 A-14" | `[].zoneName + " " + [].zoneCell`, 구역 밖이면 `[].regionName` 폴백(번호 없이) — **응답에 다 있다** |
| "전체 보기" | 같은 API를 `limit` 생략으로 재호출 |
| 카드 탭 | `[].gridId`로 격자 진입 |

- 응답은 **배열**이다. 전역 조회의 `{gridCount, videoCount, grids}` 래퍼가 없다.
- 내 격자 없는 동네·없는 regionCode는 **404가 아니라 200 + 빈 배열**.
- `sort`는 **대문자 전용**. 소문자·무효 값은 400.
- 옛 판의 "헤더는 내 것, 카드는 전역"이라는 기준 섞임 경고는 해소됐다 — 패널 전체가 내 격자 기준이다(SRS FR-MAP-07).

## 4. 격자 클릭 → 요약 패널

| 내용 | 어디서 오나 |
| --- | --- |
| 격자 이름("서면 I-6" 또는 "부전제1동") | **호출 0** — 클릭 좌표를 5179로 변환해 `Math.floor`로 칸 번호화 후 zones 캐시와 정수 비교 |
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
| 지도 팬·줌 1회 | grids 1 (+ 핫구역 칩 활성 시 hotzones 1). 축소 구간은 grids 대신 집계 1. 확대 구간에서 패널까지 갱신하면 집계(unit=DONG) 1 추가 |
| 패널 지역명 | **0** — 집계 응답의 currentRegion에 동봉 |
| 카드 갱신("장소 불러오기" 클릭) | collections grids 1 |
| 격자 클릭 1회 | stats/by-grid 1 |
| 격자 이름·격자망 | **0** (FE 산술. 줌아웃 클러스터는 2026-08-10부터 서버 집계라 제외) |

## 구현 검증
격자 이름 산술의 실행형 정본은 BE 레포의 언어 중립 픽스처 `src/test/resources/fixtures/zone-naming.json` (7 시나리오 — 북단·서단 A-1, 겹침 타이브레이크, 행정동 폴백, null). **FE 테스트가 이 파일을 파싱해 자체 구현을 검증하면 계약 일치가 보장된다.**

좌표→칸 검증 벡터: 강남역 (37.4979, 127.0276) → **`"19443_9582"`** (MSG-347 이후 값. 구 체계의 `"41664_110458"`은 폐기). 전국 200건 대조 픽스처는 `src/test/resources/fixtures/grid-epsg5179-samples.json`.

## 출처
raw: `raw/confluence/2026-08-15 지도 홈 API 연동 가이드 (FE 전달용, 2026-08-07) (cf-32636957).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/32636957
화면 근거: 피그마 노드 14176-6312 · 레포 보존 캡처 `blog-images/msg236-map-home.png`
