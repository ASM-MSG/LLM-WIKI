---
title: 백엔드 학습 로드맵 — Redis HA · 대규모 알림 · 관측성 (멘토링 08-01 후속)
type: research
product: fillmap
class: log
status: active
source: "raw/confluence/2026-08-01 백엔드 학습 로드맵 (cf-29032474).md"
created: 2026-08-01
updated: 2026-08-03
keywords: [학습 로드맵, 공부 계획, Redis, 고가용성, HA, 센티널, Sentinel, 클러스터, Cluster, 레플리카, replication, 페일오버, failover, SDOWN, ODOWN, quorum, 해시 슬롯, hash slot, MOVED, ASK, hash tag, Lettuce, 토폴로지 갱신, Valkey, 알림, 푸시, notification, FCM, 배치 발송, Spring Batch, ShedLock, 스로틀링, throttling, rate limit, 멱등, 중복 방지, outbox, DLQ, 관측성, observability, 옵저버빌리티, LGTM, Loki, Grafana, Tempo, Mimir, Prometheus, Thanos, 타노스, ELK, Grafana Alloy, OpenTelemetry, OTel, 부하 테스트, k6, p95, pg_stat_statements, auto_explain, slow query, 트레이싱, 메트릭]
aliases: [백엔드 학습 로드맵, Redis HA 로드맵, 관측성 학습 계획, 08-01 후속 로드맵]
related: ["[[2026-08-01 신기용 멘토 멘토링]]", "[[ADR viewport polling SLO]]", "[[PostgreSQL 실무 가이드 모음]]", "[[분산락 적용 주의점]]", "[[그라운드 플립 부하 테스트 사례]]"]
---

# 백엔드 학습 로드맵 — Redis HA · 대규모 알림 · 관측성 (멘토링 08-01 후속)

> [!tldr]
> [[2026-08-01 신기용 멘토 멘토링]] 피드백을 트랙 3개로 분해한 개인 공부 계획. 원칙은 하나 — **직접 실습 없이 이력서에 쓰지 않는다.** 이력서 불릿 공식: 공부 → 실습 → 장애 주입 → 검증 → 우리 서비스 관점 서술.
> 트랙 1 **Redis HA**(센티널 vs 클러스터, 마스터 kill → 페일오버 다운타임 실측 → WAS 관점 실험)가 최우선. FillMap의 Redis 사용처 3곳(핫스코어 MSG-183 / 핫구역 조회 MSG-184 / refresh 토큰 MSG-135)이 장애 시 대처가 서로 달라 **비즈니스 관점 서사가 이미 준비돼 있다**.
> 트랙 2 **대규모 알림**(FillMap 미보유 도메인 — outbox·배치·스로틀링·멱등), 트랙 3 **관측성**(부하테스트 사이클 + Prometheus/Grafana → slow query 추적 → LGTM·Thanos). 우선순위: 1 → 3-1 → 3-2 → 2.

## 이 노트로 답할 수 있는 질문
- Redis 센티널과 클러스터는 무엇이 다르고 언제 무엇을 쓰나?
- 페일오버 실습을 어떤 순서로 하고 무엇을 실측해야 하나?
- FillMap의 Redis가 죽으면 각 기능은 어떻게 동작하나?
- 대규모 알림 서비스는 어떤 요소로 구성되나? (배치·스로틀링·중복 방지·outbox)
- LGTM 스택과 ELK의 본질적 차이는? Thanos와 Mimir는 어떻게 다른가?
- FillMap에서 부하 테스트·slow query 추적 대상은 어디인가?

## 요약
멘토 판정을 그대로 옮기면: **버림** = 기술 스택 나열 불릿·의미 불명 항목. **살림 + 깊이** = Redis. **신규 추천** = 대규모 알림 서비스, 관측성. 이 판정을 트랙 3개 + 우선순위로 정리한 문서다.

## 발견

### 트랙 1. Redis 고가용성 — 센티널 vs 클러스터

**선행 개념 (실습 전에 답할 수 있어야 하는 것)**
- **복제**: 마스터→레플리카 **비동기** 복제. 왜 비동기이고, 페일오버 때 무엇을 잃는가(마스터 승인 후 미복제분 유실 — 알고 쓰는 트레이드오프).
- **Sentinel**: 별도 프로세스가 마스터 감시. SDOWN(주관적) vs ODOWN(객관적), **quorum**(센티널이 홀수 3대 이상인 이유), 리더 선출 → 레플리카 승격 → 클라이언트 통지. **샤딩 없음** — 데이터가 한 마스터에 다 들어갈 때의 HA.
- **Cluster**: **16384 해시 슬롯** 샤딩 + 마스터별 레플리카로 HA까지. gossip으로 노드끼리 감시(별도 센티널 없음), `MOVED`/`ASK` 리다이렉션, **멀티키·Lua는 같은 슬롯이어야** 함(hash tag `{}`). 회사 기본 스택인 이유는 스케일아웃 + HA를 한 구조로 해결하기 때문.
- 선택 기준 한 줄: 한 인스턴스에 들어가면 Sentinel, 샤딩이 필요하면 Cluster.
- **클라이언트(Lettuce) 관점**: 페일오버 순간 연결 끊김 → 예외 → 토폴로지 갱신 → 새 마스터 재연결. Spring Data Redis의 `RedisStaticMasterReplicaConfiguration` vs `RedisSentinelConfiguration` vs `RedisClusterConfiguration` 차이.
- 참고: 라이선스 분쟁으로 갈라진 **Valkey**(오픈소스 포크) 존재 정도는 알아두기.

**실습 로드맵 (멘토 지정 흐름)**
1. **Sentinel 구성** — docker-compose로 마스터 1 + 레플리카 2 + 센티널 3, quorum 2. `redis-cli -p 26379 sentinel master`로 상태 확인.
2. **마스터 죽이기** — `docker stop` → 센티널 로그 `+sdown` → `+odown` → `+switch-master` 확인. `down-after-milliseconds`·`failover-timeout`을 바꿔가며 **다운타임 실측**(이 숫자가 이력서 불릿 재료).
3. **Cluster 구성** — 마스터 3 + 레플리카 3, `redis-cli --cluster create`. `CLUSTER KEYSLOT`으로 슬롯 분배 확인, 마스터 kill → 승격 관측.
4. **WAS 관점 실험(핵심)** — Spring Boot(Lettuce)를 Sentinel에 붙이고 페일오버 도중 요청을 계속 쏘며(k6) **어떤 예외가 몇 초간 나는지** 실측 → 재시도/예외 삼킴/폴백을 케이스별로 코드화.

**FillMap 접점 — 비즈니스 관점 서술 재료 (이미 있는 것)**

| 사용처 | 장애 시 동작 (현재 설계) | 서술 포인트 |
| --- | --- | --- |
| 핫스코어 집계 (MSG-183) | 전용 스레드에서 실패 삼킴 + warn. 업로드는 무조건 성공 | "부가 신호는 유실 허용, 핵심 경로 비전파" — 페일오버 다운타임에도 업로드 API 무영향 |
| 핫구역 조회 (MSG-184) | 예외 전파 → 500. SLO 5xx<1% 관리 대상 | 조회는 실패가 보여야 하는 경로 — 다운타임 동안 500률로 관측 |
| refresh 토큰 (MSG-135) | Redis 죽으면 재발급 실패 → 재로그인 유도 | 세션 계층이 Redis 종속 — Sentinel이 필요한 실제 이유. "액세스 토큰은 stateless라 만료 전까지 이용은 지속"까지 붙이면 완성 |

실습 4단계를 FillMap dev 구성(EC2 docker-compose)에 축소 적용해 "페일오버 N초 동안 로그인 연장만 실패하고 업로드·조회는 이렇게 버틴다"를 숫자로 말할 수 있으면 멘토가 말한 "비즈니스 관점 포함 서술"이 완성된다. (핫구역 Redis ZSET 집계 맥락은 [[ADR viewport polling SLO]] §6)

**면접 예상 질문 (막히면 안 되는 것)**
- 센티널 quorum이 2인데 센티널이 2대면? (스플릿 브레인·과반 선출 불가)
- 페일오버 중 쓰기 유실이 왜 생기나? `min-replicas-to-write`는 뭘 완화하나?
- Cluster에서 `MGET a b c`가 실패하는 이유와 hash tag 해법
- Lettuce는 페일오버를 어떻게 알아채나? (Sentinel pub/sub 구독 vs Cluster 토폴로지 갱신)

### 트랙 2. 대규모 알림 서비스
FillMap에 알림 도메인이 **아직 없다** — 이벤트 소스(뱃지 획득·미션 스탬프·스트릭 임박·핫구역 진입)는 이미 쌓여 있어 붙이기 좋은 신규 기능. **"핫구역 뜸 → 근처 사용자 대량 발송"** 시나리오가 트래픽 쏠림 제어까지 한 세트로 맞는다.

- **실시간 개별 vs 대량 발송**: 개별은 이벤트 훅에서 바로, 대량은 저장 후 배치.
- **예약 발송 배치**: PENDING→SENT 상태 테이블 + 주기 배치(회사 실무 방식). Spring Batch(Job·Step·chunk) 또는 `@Scheduled` + 상태 테이블부터. 다중 인스턴스 중복 실행 방지(ShedLock·DB 락 — [[분산락 적용 주의점]]과 연결).
- **스로틀링/분산 발송**: 나눠 보내는 이유는 발송 부하가 아니라 **유입 트래픽 평탄화**. 배치 N등분 시차 발송 또는 큐 + 소비 속도 제한.
- **중복 방지**: 멱등 키(사용자×알림종류×기준시각), DB 유니크 제약이 최후 방어선 (FillMap `insertIgnoreConflict` 패턴 재사용 가능).
- **outbox 패턴**: 비즈니스 트랜잭션과 발송 요청 저장을 한 트랜잭션으로, 발송은 별도 폴러가 — "커밋됐는데 유실"/"롤백됐는데 발송" 양쪽 차단. FillMap afterCommit 훅과 비교 설명하면 좋은 어필.
- 채널(FCM·웹푸시)보다 **파이프라인 설계**가 어필 포인트. 이력 보존·파티셔닝, 재시도 정책(지수 백오프·DLQ)까지.

**실습 아이디어(FillMap 티켓화 후보)**: ① notifications 테이블 + 이벤트 훅 PENDING 적재(outbox) ② 배치 발송기(폴링·배치 크기 제한·동시 실행 락) ③ 핫구역 진입 알림 N분할 시차 발송 + k6로 몰림 vs 분산 유입 비교 ④ 유니크 제약 + 재시도 테스트.

### 트랙 3. 모니터링 · 관측성

**3-1. 기본 사이클이 뼈대** — 부하 테스트 → 병목 확인 → 개선 → 재테스트. 도구는 수단.
- **부하 테스트**: k6 기본(시나리오·VU·p95/p99). FillMap 대상 후보 — `GET /api/hotzones`(캐시 만료 순간 동시 재계산), `GET /api/grids` viewport, 업로드 확정.
- **메트릭 파이프라인**: Spring Actuator + Micrometer → Prometheus(pull·scrape) → Grafana. HTTP p95·에러율·커넥션 풀·JVM 힙 기본 패널.
- **slow query 추적**: 멘토 지적 "Grafana가 시각화만 하면 한계". PostgreSQL `pg_stat_statements`(누적 통계)·`auto_explain`(느린 쿼리 실행계획 자동 로깅). FillMap 대상: viewport keyset 쿼리·region_stats recompute·미션 판정 native 쿼리. ([[PostgreSQL 실무 가이드 모음]])
- 메트릭 vs 로그 vs 트레이스 — 세 신호의 역할 구분을 자기 말로.

**3-2. LGTM 스택**

| 구성 | 역할 | 핵심 한 줄 |
| --- | --- | --- |
| **L**oki | 로그 | **라벨만 인덱싱**, 본문은 압축 청크로 오브젝트 스토리지에 — ELK 대비 저장 비용이 구조적으로 싼 이유 |
| **G**rafana | 시각화 | 벤더 중립 단일 화면 — Prometheus·Loki·Tempo·ES 전부 데이터소스 |
| **T**empo | 트레이스 | traceID 기반 저장·조회. 로그↔트레이스↔메트릭 점프(correlation)가 셀링 포인트 |
| **M**imir | 메트릭 장기 저장 | Prometheus의 수평 확장·장기 보관판 (Cortex 계보) |

- 수집 에이전트는 **Grafana Alloy**(구 Agent, OTel 호환)가 현재 표준 — OpenTelemetry 계측 → Alloy가 밀어넣는 구성이 2026 기본형.
- **LGTM vs ELK**: 인덱싱 전략이 본질 — ES는 전 필드 역인덱스(검색 강력·비용 큼), Loki는 라벨만(grep식·비용 작음). 전문 검색이면 ELK, 대량 로그 경제성이면 Loki. 반론: LGTM은 상태ful 시스템 3~4개를 굴리는 운영 세금이 있다.
- **Thanos**(멘토 키워드 "타노스 아키텍처"): Prometheus 단일 인스턴스의 한계 3개 — ① 로컬 디스크라 장기 보관 불가 ② HA 없음(죽으면 구멍) ③ 여러 Prometheus 글로벌 뷰 없음 — 을 기존 Prometheus를 안 건드리고 옆에서 푼다.
  - 구성: **Sidecar**(블록 S3 업로드 + 실시간 프록시) · **Store Gateway**(S3 과거 조회) · **Querier**(팬아웃 합산 = 글로벌 뷰) · **Compactor**(다운샘플링·압축).
  - HA 방식: Prometheus 2대가 **중복 수집**하고 Querier가 조회 시 **dedup** — 한 대 죽어도 구멍이 안 난다.
  - **vs Mimir**: 같은 문제의식, 반대 접근 — Thanos는 기존 Prometheus 옆에 붙는 연합형, Mimir는 remote write 중앙 집중형(Cortex 계보). "이미 Prometheus가 여기저기면 Thanos, 처음부터 중앙화면 Mimir".
  - 실습은 로컬 docker-compose로 Prometheus 2대 + Sidecar + Querier → 한 대 kill 후 dedup으로 그래프에 구멍이 안 나는 것 확인 정도면 충분.
- 트레이싱 실습: OTel Java agent를 붙여 업로드 확정 훅 체인(badge→streak→mission→hotzone)이 트레이스로 어떻게 보이는지 — 이미 있는 코드가 좋은 데모.

**3-3. 실습 순서 (t3.small 2GB 제약 주의)**
1. 로컬 docker-compose: Prometheus + Grafana + FillMap → 기본 대시보드
2. k6로 핫구역 조회 부하 → 병목 하나 개선 → 전후 p95 비교 (불릿 1개 완성)
3. `pg_stat_statements`로 slow query 상위 추출 → 인덱스/쿼리 개선 실측
4. Loki + Alloy 추가 → 로그·메트릭 한 화면
5. Tempo + OTel agent → 훅 체인 트레이스 (dev EC2는 메모리 부족 — 로컬/별도 인스턴스)

## 시사점
- **우선순위**: ① 트랙 1(Redis) — 멘토가 "살릴 것"으로 지목한 유일한 기존 자산, 실습 4단계가 1~2주고 FillMap 접점 서사가 준비돼 있어 투자 대비 가장 빠름. ② 트랙 3-1 — Redis WAS 실험과 도구(k6)가 겹쳐 이어서 하면 싸다. ③ 트랙 3-2 LGTM/Thanos — 심화, "면접관이 모르는 최신 개념" 카드. ④ 트랙 2(알림) — 유일하게 신규 개발이 필요, PRD부터 태워 FillMap 티켓으로.
- 트랙 2는 **FillMap 신규 기능 제안**이기도 하다 — 진행하려면 팀 합의·티켓화가 선행되어야 한다(현재는 개인 학습 계획 단계).
- 트랙 3의 dev EC2(t3.small 2GB) 제약 때문에 관측성 스택 실습은 로컬 또는 별도 인스턴스가 전제.

## 원본 링크
- [ELK vs. Grafana Stack: A Practical Comparison for Observability](https://medium.com/@krunalpatel1530/elk-vs-grafana-stack-a-practical-comparison-for-observability-5b6b90fc980a)
- [Arbitrating Your Observability Architecture (ELK vs LGTM)](https://medium.com/@elammarisoufiane/one-stack-to-rule-them-all-arbitrating-your-observability-architecture-elk-vs-lgtm-one-choice-per-1af7410152fc)
- [How to Build a Complete LGTM Stack with OpenTelemetry](https://oneuptime.com/blog/post/2026-02-06-lgtm-stack-opentelemetry/view)
- [How to Set Up Redis Sentinel with Docker Compose](https://oneuptime.com/blog/post/2026-03-31-redis-sentinel-docker-compose/view)
- [Emulate a Redis Failover with Docker](https://intelligentbee.com/blog/emulating-redis-failover-docker/)
- [Redis cluster with Docker Compose](https://github.com/AliyunContainerService/redis-cluster)

## 출처
raw: `raw/confluence/2026-08-01 백엔드 학습 로드맵 (cf-29032474).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/29032474
