---
title: ADR — viewport 전송방식 polling · 부하 SLO·임계점 (MSG-134)
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-16 설계결정 viewport 실시간 전송방식(polling) · 부하 SLO·임계점 (MSG-134) (cf-18219010).md"
created: 2026-07-16
updated: 2026-07-21
keywords: [ADR, viewport, 뷰포트, polling, 폴링, websocket, 웹소켓, SLO, p95, RPS, 임계점, freshness, 캐시, Redis, k6, fetch-on-pan, 줌 레벨, MSG-134]
aliases: [viewport ADR, 폴링 결정]
related: ["[[Grid API]]", "[[2026-07-16 박원형 멘토 멘토링]]", "[[2026-07-17 프론트-백 합의]]", "[[그라운드 플립 부하 테스트 사례]]"]
---

# ADR — viewport 전송방식 polling · 부하 SLO·임계점 (MSG-134)

> [!tldr]
> 지도 뷰포트 조회(메인 화면 최고 트래픽)는 polling(fetch-on-pan)으로 확정, websocket은 Phase 2 유예.
> SLO: p95 < 300ms · p99 < 800ms · 5xx < 1% · freshness stale ≤ 30s. 임계점은 연결 수가 아니라 이 SLO를 깨는 RPS로 정의, t3.small에서 k6 열린 모델로 실측.
> 줌 레벨 파라미터는 MVP에 안 둠(bbox가 줌을 담고 span 상한 0.5°가 폭주 방어). 내 업로드 즉시 반영은 FE 낙관적 색칠로.

## 이 노트로 답할 수 있는 질문
- 지도 뷰포트 갱신은 폴링인가 웹소켓인가, 왜?
- viewport 조회의 SLO 수치와 근거는?
- 부하 임계점은 어떻게 정의하고 측정하나?
- 줌 레벨(level) 파라미터가 MVP에 없는 이유는?
- 내가 방금 올린 격자가 즉시 칠해지는 건 어떻게 처리하나?
- 임계점이 부족할 때 쓸 레버는?

## 맥락
`GET /api/grids?bbox&strategy`는 지도 팬마다 호출되는 최고 트래픽 엔드포인트. MSG-90(viewport 응답)·MSG-89(Redis 캐시) 구현 전에 전송방식과 임계점을 확정.

## 선택지
polling(fetch-on-pan) vs websocket.

## 결정
- **polling 채택.** 개인 도감 색칠은 내 업로드로만 바뀜 → 서버 push 이유 없음. 무상태·수평확장·캐시 친화. websocket은 연결당 메모리/FD 상시 점유 + 다중 인스턴스 pub/sub 필요 — t3.small에서 수천 연결이 한계, Phase 2(친구/핫존 라이브)로 유예.
- **SLO**: p95<300ms(팬 후 디바운스 기준, 150ms는 결제급 과함) · p99<800ms · 5xx<1%(읽기·자가치유) · stale≤30s(=캐시 TTL, 공격적 캐싱 허용).
- **임계점** = p95>300ms 또는 5xx>1%가 되는 RPS. 수요 모델 peak RPS ≈ U×A/60. k6 s4(100→1000 RPS)로 knee 실측. 로컬 벤치(~286 RPS)는 닫힌 모델이라 임계점 아님.
- **level 파라미터 없음**: bbox가 줌을 담음 + MAX_VIEWPORT_SPAN_DEG 0.5° 상한. Phase 2 클러스터링 때 도입.

## 근거
상태 변경 주체 분석(내 업로드뿐) · 서비스 성격(읽기·개인·저위험) · 스키마/기존 구현(MSG-73 span 상한, 전략 A p95 ~2.6× 우위).

## 영향
Redis 캐시(MSG-89)·좌표 스냅·클라 디바운스가 임계점 레버. FE는 업로드 응답으로 낙관적 색칠. cursor 페이지네이션은 MSG-90.

## 출처
raw: `raw/confluence/2026-07-16 설계결정 viewport 실시간 전송방식(polling) · 부하 SLO·임계점 (MSG-134) (cf-18219010).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18219010
