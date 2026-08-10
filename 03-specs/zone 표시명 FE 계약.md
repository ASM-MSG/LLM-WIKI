---
title: zone 표시명 FE 계약 — "서면 A-14"를 화면이 만드는 규칙
type: spec
product: fillmap
class: log
status: active
source: 'raw/confluence/2026-07-30 격자 표시명 "서면 A-14" — 동작 원리 해설 + FE 구현 계약 (MSG-259) (cf-27852802).md, BE 레포 src/test/java/com/msg/fillmap/zone/ZoneNamingContractTest.java(실행형 정본) · docs/spec/MSG-234.md §D2~D5 · docs/prd/MSG-259-prd.md'
created: 2026-07-30
updated: 2026-08-10
keywords: [zone, 표시명, display name, 서면 A-14, FE 계약, 프론트, GET /api/zones, 명명 산술, 로컬 계산, 폴백, regionName, priority, zoneKey, 겹침, 픽스처, fixture, 드리프트, MSG-234, MSG-259, 캐시]
aliases: [zone FE 계약, 표시명 계약, 격자 이름 계약]
related: ["[[FE 격자 계약 프론트-백 합의]]", "[[ADR 격자 표시명 zone]]", "[[zone 표시명 데이터 파이프라인 해설]]", "[[MSG-234 상권 작도 결정 공공데이터 검수]]", "[[zone 상권 공공데이터 근거]]", "[[ADR 장소 검색 카카오 로컬 프록시]]", "[[지도 홈 API 연동 가이드 FE]]"]
---


> **⚠️ 결정 보완 (2026-08-10, MSG-349)**: 행정동 폴백 재료(`regionName`)도 이제 **모든 격자 응답에 실려 온다** — MSG-341이 "폴백 미제공"으로 남겼던 뷰포트(`GET /api/grids`, 친구 격자 공용)·단일 격자(`GET /api/grids/{gridId}`, 미점령 빈 칸 포함)·핫구역(`GET /api/hotzones`)까지. FE 조립은 응답 무관 한 줄이다: `label = zoneName ? zoneName+" "+zoneCell : regionName`. 이름 목적의 by-grid 병행 호출은 더 필요 없다. `regionName`은 구역 안 격자에도 항상 실린다(위치줄 "부산 부산진구 서면"의 시/구 재료 — 시 이름 축약과 조립은 FE 몫). 바다 위 등 무귀속 격자만 null이며 그때는 이름 없음이 정상. 정본: BE 레포 `docs/spec/MSG-349.md`.

> **⚠️ 결정 변경 (2026-08-07, MSG-341)**: 표시명 계산 주체가 **서버**로 바뀌었다. 격자를 담는 조회 응답 9종에 `zoneName`·`zoneCell` 필드가 실려 오고, FE는 조립(`zoneName + " " + zoneCell`)과 행정동 폴백 표시만 한다. 이 문서의 "화면이 만드는 규칙"(FE 로컬 산술) 서술은 이력이다. 명명 규칙 자체와 폴백 번호 없음, zones 캐시의 검색 이동 용도(§D6)는 불변. 정본: BE 레포 `docs/spec/MSG-341.md`.

# zone 표시명 FE 계약 — "서면 A-14"를 화면이 만드는 규칙

> [!tldr]
> 서버는 격자 이름을 **만들지 않는다**. FE가 `GET /api/zones`(구역 사각형 ~40건, 세션당 1회)를 받아두고,
> 격자 번호로 **뺄셈 두 번** 해서 "서면 A-14"를 만든다. 매칭되는 구역이 없으면 이미 받고 있는
> `regionName`("부전동")을 그대로 쓰면 된다(번호 안 붙임).
> 지금은 구역 데이터가 0건이라 **전부 폴백으로 표시되는 게 정상** — FE가 계산 로직을 미리 구현해두면,
> 백엔드가 데이터를 넣는 순간(MSG-259) FE 배포 없이 "서면 A-14"가 켜진다.

## 이 노트로 답할 수 있는 질문
- FE가 "서면 A-14"를 만들려면 뭘 구현해야 하나? (API 1개 + 함수 20줄)
- 격자가 어느 구역에도 안 들면 / 두 구역에 겹치면 어떻게 표시하나?
- 내 구현이 맞는지 어떻게 검증하나? (기대값 표)
- /api/zones는 언제 다시 불러야 하나?
- 지금 왜 아무 격자도 "A-14"가 안 나오나? (데이터 0건 — 정상)

## 0. 큰 그림 — 왜 FE가 계산하나

서버가 모든 응답에 이름을 얹으면 지도 폴링 응답이 화면당 +9~23KB씩 커져 응답속도 예산을
갉아먹는다. 대신 구역 데이터(8KB)를 세션당 1번만 받고 FE가 계산한다 — 실측 카드 30장에 7.1µs라
성능 걱정은 없다. 전체 구조(데이터가 어디서 오는지)는 [[zone 표시명 데이터 파이프라인 해설]] 참조.

```text
앱 진입 1회:  GET /api/zones  →  사각형 ~40건 캐시
화면마다:     쥐고 있는 격자 번호 + 캐시  →  뺄셈 2번  →  "서면 A-14"
매칭 없으면:  응답에 이미 있는 regionName  →  "부전동"   (번호 없음)
```

## 1. 데이터 — `GET /api/zones` (로그인 필요)

응답 항목 하나 = 구역 사각형 하나. 시딩 전엔 **빈 배열**(에러 아님 — 전부 폴백으로 동작해야 함).

```json
{ "zoneKey": "seomyeon",      // 안정 식별자 — 겹침 타이브레이크·캐시 키로 사용
  "name": "서면",              // 화면에 그대로 노출되는 이름
  "regionCode": "2623051000", // 소속 행정동 (nullable, 문맥용 — 계산엔 불필요)
  "minGridY": 39056, "maxGridY": 39072,   // 세로 범위 (양끝 포함)
  "minGridX": 112220, "maxGridX": 112229, // 가로 범위 (양끝 포함)
  "priority": 0 }             // 겹침 우선순위 (현재 전원 0)
```

- **호출 시점**: 앱 진입 시 1회, 세션 동안 재사용. 갱신 신호(버전/ETag)는 아직 없음 —
  데이터가 거의 안 바뀌어 재접속 시 재조회로 충분 (미해결로 관리 중, MSG-259 §8)
- 격자 번호(gridY/gridX)는 이미 쥐고 있다: 갤러리 응답(`/api/collections/grids`)엔 필드로 옴,
  그 외엔 `gridId`("39070_112223")를 `split('_')` 후 숫자 변환

## 2. 계산 — 참조 구현 (이대로 옮기면 됨)

```js
// 매칭: 사각형 안(양끝 포함) 판정 → 겹치면 priority 큰 것, 같으면 zoneKey 사전순 앞의 것
function matchZone(zones, gy, gx) {
	return zones
		.filter(z => gy >= z.minGridY && gy <= z.maxGridY && gx >= z.minGridX && gx <= z.maxGridX)
		.sort((a, b) => b.priority - a.priority || (a.zoneKey < b.zoneKey ? -1 : 1))[0] ?? null;
	// zoneKey 비교는 단순 < 사용 — ASCII slug 전제. localeCompare는 서버(Java compareTo)와 어긋날 수 있음
}

// 명명: 행 = 사각형 북쪽 끝에서 몇 칸 아래인지(A,B,C…) · 열 = 서쪽 끝에서 몇 번째인지(1부터)
function label(zone, gy, gx) {
	const row = String.fromCharCode(65 + zone.maxGridY - gy); // 65 = 'A'
	const col = gx - zone.minGridX + 1;
	return `${zone.name} ${row}-${col}`;
}

// 표시명: 매칭 있으면 계산, 없으면 regionName 그대로 (번호 붙이지 않음)
function displayName(zones, gy, gx, regionName) {
	const z = matchZone(zones, gy, gx);
	return z ? label(z, gy, gx) : regionName; // regionName도 null이면 표시명 없음 — gridId 등 FE 재량
}
```

## 3. 검증 — 기대값 표 (이 표와 다르면 구현이 틀린 것)

BE의 실행형 정본(`ZoneNamingContractTest`, 테스트 7건)과 같은 값. 테스트 구역:
`서면` = {minGridY 1000, maxGridY 1010, minGridX 2000, maxGridX 2020, priority 0}

| 입력 격자 (gy, gx) | 기대 표시명 | 확인하는 규칙 |
|---|---|---|
| (1010, 2000) | `서면 A-1` | 북쪽 끝 = A행, 서쪽 끝 = 1열 |
| (1010, 2013) | `서면 A-14` | 열 = 2013 − 2000 + 1 |
| (1009, 2000) | `서면 B-1` | 한 칸 남쪽 = B |
| (1000, 2000), 구역이 1000~1025 | `… Z-1` | 최대 높이 26칸의 남쪽 끝 = Z |
| (1011, 2000) / (1005, 2021) | 매칭 없음 → 폴백 | 사각형 밖 (경계는 양끝 포함) |
| (1005, 2010), 큰구역(pri 0)+핫스팟(pri 10) 겹침 | 핫스팟 이름 | priority 큰 쪽 |
| (9999, 9999), regionName "부전동" | `부전동` | 폴백은 이름만, 번호 없음 |

언어 중립 픽스처 파일(JSON)로 추출 예정(MSG-259) — 나오면 위 표 대신 그 파일이 정본.

## 4. 엣지 케이스 정리

| 상황 | 표시 |
|---|---|
| zones 응답이 빈 배열 (지금 상태) | 전 격자 regionName 폴백 — 에러 아님 |
| 매칭 구역 없음 | regionName 그대로 (번호 붙이지 않음 — "부전동 A-3" 금지) |
| regionName도 null (해안 등 무귀속) | 표시명 없음 — gridId 표기 등 FE 재량 |
| 두 구역에 겹침 | priority 큰 쪽 → 같으면 zoneKey 사전순. 데이터는 안 겹치게 관리되므로 보험 |
| 사각형 경계 칸 | 양끝 포함 (min ≤ g ≤ max) |

## 5. 일정 — FE가 지금 할 수 있는 것

- **지금**: 위 함수 + `/api/zones` 1회 fetch 구현. 데이터가 0건이라 화면 변화는 없음(전부 폴백)
- **MSG-259 시딩 후**: 구역 사각형 안 격자만 자동으로 "서면 A-14"로 바뀜 — **FE 재배포 불필요**
- 장소 검색("서면" 입력→지도 이동)은 별도: 카카오 프록시 `GET /api/search`
  ([[ADR 장소 검색 카카오 로컬 프록시]]) + zone 이름 매치는 zones 캐시 로컬 필터

## 출처
raw: `raw/confluence/2026-07-30 격자 표시명 "서면 A-14" — 동작 원리 해설 + FE 구현 계약 (MSG-259) (cf-27852802).md` (Confluence 발행본 — 이 노트에서 발행, 재ingest 시 이 노트 갱신)
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/27852802
BE 레포: `src/test/java/com/msg/fillmap/zone/ZoneNamingContractTest.java`(명명 규칙 실행형 정본) · `docs/spec/MSG-234.md` §D2(산술)·§D3(FE-local)·§D4(폴백)·§D5(겹침) · `ZoneResponseDto`(응답 형태) · 성능 실측치는 [[zone 표시명 데이터 파이프라인 해설]]
