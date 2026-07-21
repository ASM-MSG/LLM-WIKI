---
title: AI Highlight-Blur 개발 기록 — 레포 생성부터 dev 배포까지
type: research
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-21 FillMap AI Highlight-Blur — 레포 생성부터 dev 배포까지 (cf-21102593).md"
created: 2026-07-21
updated: 2026-07-21
keywords: [AI, 블러, blur, 하이라이트, highlight, YOLO, YOLOv11, PySceneDetect, ultralytics, AGPL, 라이선스, FastAPI, dev 배포, Graviton, 실측, conf, 얼굴 탐지, 번호판, torch, torchvision, x86, MSG-142, MSG-143, MSG-144, MSG-158, MSG-159, MSG-161]
aliases: [AI 서버 개발 기록, Highlight-Blur 배포]
related: ["[[ADR AI 처리 실행 환경 FastAPI]]", "[[다이어그램 모음]]", "[[PRD FillMap MVP 화면별 기능·API]]"]
---

# AI Highlight-Blur 개발 기록 — 레포 생성부터 dev 배포까지 (2026-07-20~21)

> [!tldr]
> 얼굴·번호판 자동 블러 + 하이라이트 추천 서버(ASM-MSG/AI)를 이틀 만에 측정→결정→구현→**dev 배포 완료**. 1080p 30초 실영상 E2E 4.3분, 하이라이트 3구간.
> 핵심 결정: ① Ultralytics AGPL 때문에 **AI 서버만 별도 레포·별도 프로세스로 분리**(BE는 MIT 유지) ② Lambda 기각·상시 FastAPI (MSG-143 ADR) ③ 얼굴 미탐지는 모델 키우기가 아니라 **conf 0.25→0.05 하향**으로 해결 (recall 0.72→0.98, 시간 불변).
> API 계약: `POST /jobs` → 폴링 → `GET /jobs/{id}/video`, 상태 QUEUED→PROCESSING→DONE|FAILED. 남은 것: BE 연동·부하 테스트·S3 연동.

## 이 노트로 답할 수 있는 질문
- AI 블러·하이라이트 서버는 지금 어떤 상태인가? (답: dev 배포 완료, BE 연동 대기)
- 왜 AI 서버가 별도 레포인가? (AGPL)
- 얼굴 미탐지는 어떻게 해결했나? (conf 하향, 실험표)
- BE는 AI 서버와 어떻게 통신하나? (jobs API 계약·상태 매핑)
- 처리 시간은 얼마나 걸리나? (1080p 30초 ≈ 3~4분, 실측)
- x86 Docker 배포에서 뭘 조심해야 하나? (torch·torchvision CPU 인덱스)

## 요약
- **모델**: 얼굴 YOLOv11n-face + 번호판 YOLOv11n-plate + PySceneDetect — 런타임 ultralytics 1벌 (MSG-144)
- **라이선스 분리**: Ultralytics AGPL-3.0 → AI만 별도 레포(AGPL)·HTTP 통신, BE MIT 유지
- **실측 (MSG-142)**: Graviton3 기준 1080p 30초 3.1~3.8분 / 4K 9.7분, vCPU 증설 무효 → 다운스케일이 정답
- **얼굴 미탐지 (MSG-158)**: conf 0.05 채택 — recall 0.980, 시간 1.01×. 모델 확대·imgsz 상향은 기각
- **하이라이트 폴백 (MSG-159)**: 장면 전환 없으면 균등 3분할
- **서버 (MSG-161)**: FastAPI 단일 워커 큐, `POST /jobs`→폴링→비디오 다운로드, PROCESSING = BE의 `BLURRING`
- **배포**: dev EC2(x86) Docker, E2E 통과. torch·torchvision은 CPU 전용 인덱스로 함께 설치할 것

## 시사점
- MSG-143 ADR의 전제(1080p 다운스케일 → 3~4분)가 E2E 실측(4.3분)으로 검증됨
- PRD의 "AI 하이라이트·블러 [미구현]" 항목이 **서버 측 완료 → BE 연동 대기**로 진전 — SA v2 다이어그램의 AI 파이프라인 행 상태 갱신 대상

## 출처
raw: `raw/confluence/2026-07-21 FillMap AI Highlight-Blur — 레포 생성부터 dev 배포까지 (cf-21102593).md`
Confluence 원본: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/21102593
