---
title: 아키텍처 V2final 멘토 리뷰
type: research
product: fillmap
class: log
status: active
source: "raw/Architecture Map/2026-07-25 FillMap 아키텍처 V2final 멘토 리뷰.docx"
created: 2026-07-26
updated: 2026-07-26
keywords: [아키텍처 리뷰, architecture review, 멘토 피드백, mentor feedback, V2 final, SA, SysA, 서비스 매핑, service mapping, API 버전, /api/v1, ALB, WAF, API Gateway, CQRS, 이중 인코딩, double encoding, 지연 예산, latency budget, p95, 다이어그램 동결, diagram freeze]
aliases: [멘토 아키텍처 리뷰, V2final 리뷰, 아키텍처 피드백 7-25]
related: ["[[다이어그램 모음]]", "[[AI 블러 파이프라인 실측 현황]]", "[[ADR viewport polling SLO]]", "[[FillMap API 스펙 통합]]"]
---

# 아키텍처 V2final 멘토 리뷰

> [!tldr]
> 멘토 총평(7/25): "면접에 그대로 들고 갈 수준" — 유스케이스 1:1·SA 5-티어·SysA 논리 뷰·AI Pipeline 신설 모두 인정.
> Quick Fix 3건(A-1 서비스 매핑, A-2 /api/v1 통일, A-3 ALB·WAF 각주)은 **7/26 gen 스크립트에 반영 완료** — 이후 다이어그램은 동결 권고.
> 남은 차별화는 코드·측정 두 가지: ① AI 파이프라인 4.3분 → X초 (이중 인코딩 제거), ② 격자 쿼리 p95 실측.

## 이 노트로 답할 수 있는 질문
- 멘토가 아키텍처 V2 final에서 지적한 것과 인정한 것은?
- A-1/A-2/A-3 Quick Fix는 무엇이고 어떻게/어디에 반영됐나?
- SA↔SysA 서비스 매핑은 어떻게 정해졌나?
- CQRS(GridQueryService 분리) 라벨은 왜 보류됐나?
- 다이어그램은 왜/언제부터 동결인가?
- 남은 B 항목(코드·측정)은 무엇이고 누가 담당인가?

## 좋다고 인정된 것 (유지)
- 유스케이스: IA 리프 1:1(56개) + include/extend 6개 — '에픽 ≠ 유스케이스' 반영 확인
- SA: 화면 11 → REST API → 서비스 → Repository(실제 테이블) → 데이터 5-티어, Repository↔테이블 매핑이 강점
- SysA: 순수 논리 뷰 + 워커 트리거 경로별(Event/Batch) 분리 + Mission 도메인
- AI Pipeline 장 신설: 5단계 + 상태머신 + 저장계층 + 실측치

## Quick Fix (A) — 반영 완료 (2026-07-26)
| 항목 | 지적 | 반영 |
|---|---|---|
| A-1 서비스 정합 | SA 9개 vs SysA 9개인데 쪼갠 방식이 다름 (Grid 3↔1, Social·Moderation 1↔2, Collection·Notification 대응 불명) | **매핑 명시 방식** 채택 — 두 다이어그램 캡션에 매핑 한 줄 추가: Auth=AuthService·UserService / Grid=GridQueryService·HotZoneService / Collection=UserGridQueryService / Video=VideoService+인코딩 워커 / Social+Moderation=Social·ModerationService / Notification=SA 미표기(P2) |
| A-2 API 경로 | /api 접두사가 붙다 말다 | 33개 엔드포인트 전부 **`/api/v1/*`** 로 통일 (`gen-apparch-drawio.py` APIS 블록) |
| A-3 논리↔물리 | SysA API Gateway의 물리 대응 불명 | SysA 캡션 각주: "API Gateway(논리) = CA에선 ALB + WAF" |

- 수정 파일: `00-meta/gen-apparch-drawio.py` · `00-meta/gen-sysa-drawio.py` → SA·SysA v2 draft xml 재생성
- ⚠️ **A-2는 다이어그램 표기 통일** — 실제 서버 라우팅·[[FillMap API 스펙 통합]] 문서는 아직 `/api/v1` 아님. 코드 반영 여부는 별도 결정 필요.
- ⏸️ **CQRS 보류**: GridQueryService/UserGridQueryService 분리가 의도된 읽기/쓰기 분리인지 팀 확인 필요 (멘토: 의도면 라벨 달아 살리고, 우연이면 병합). 확인 전까지 라벨 미부착.

## 남은 것 (B) — 코드·측정 (이 위키 밖 작업)
| 항목 | 내용 | 담당(제안) | 완료 기준 |
|---|---|---|---|
| B-1 ★최우선 | AI 파이프라인 4.3분/30초 병목: 이중 인코딩(ENCODING→BLURRING) 제거 — 검출은 저해상도 프록시, 블러 좌표만 최종 인코딩 1패스에. 단계별 지연 예산 실측 | 조성민·AI | "4.3분 → X초" 수치 |
| B-2 | 단일-AZ SPOF(FastAPI·Kafka) 설명 준비 + 자체 Kafka vs MSK 트레이드오프 정리, 재생 경로 CloudFront 경유 검토 | 조성민 | 말로 설명 가능 + 결정 기록 |
| 측정 | 지도 격자 쿼리 p95 실측 (k6 등) — [[ADR viewport polling SLO]]의 p95<300ms SLO 검증 | 강정민 | p95 수치 |

> 참고: 멘토의 "YOLO 프레임 샘플링 후 보간" 제안은 [[AI 블러 파이프라인 실측 현황]]에서 **프레임 스킵 기각(도로 번호판 커버 46-62%)** 이력이 있음 — 단순 스킵이 아닌 저해상도 프록시 검출+보간 조합인지 구분해서 검토할 것.

## 결정: 다이어그램 동결
A 반영 후 다이어그램 추가 수정 중단(멘토 권고, 전원). 이후 시간은 동작하는 코드 + 측정 숫자에만.

## 출처
raw: `raw/Architecture Map/2026-07-25 FillMap 아키텍처 V2final 멘토 리뷰.docx` (원본: FillMap_아키텍처_V2final_리뷰_연수생_전달용.docx, 2026-07-25 멘토 → MSG팀)
