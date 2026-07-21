---
title: ADR — AI 처리 실행 환경, 상시 FastAPI 서버 (MSG-143)
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-21 설계결정 AI 처리 실행 환경 — 상시 FastAPI 서버 (MSG-143) (cf-20643841).md"
created: 2026-07-21
updated: 2026-07-21
keywords: [ADR, AI, FastAPI, Lambda, GPU, 실행 환경, Graviton3, YOLOv11n, 블러, blur, 하이라이트, PySceneDetect, 다운스케일, 1080p, 실측, 벤치마크, MSG-143, MSG-142]
aliases: [AI 실행 환경 ADR, FastAPI ADR]
related: ["[[2026-07-16 박원형 멘토 멘토링]]", "[[다이어그램 모음]]", "[[Video API]]"]
---

# ADR — AI 처리 실행 환경, 상시 FastAPI 서버 (MSG-143)

> [!tldr]
> AI Highlight-Blur는 **상시 Python(FastAPI) 서버**로 확정 (Lambda·GPU 기각). 필수 전제: 입력을 1080p 30fps로 다운스케일.
> 근거는 Graviton3(c7g.large) 실측: 1080p 30초 3~4분, 4K 9.7분(Lambda 15분의 65%), vCPU 늘려도 안 빨라짐(추론 비병렬), 프레임당 227~230ms로 해상도 무관(imgsz=640). 노트북(M5) 수치는 4배 낙관적이라 무효.
> 비용 손익분기 월 ~6,650건, 그 이상이면 상시 서버가 오히려 쌈. 처리 요청은 비동기(BLURRING 상태). 미해결: 얼굴 미탐지 심각·단일 씬 하이라이트 0개(MVP 블로커).

## 이 노트로 답할 수 있는 질문
- AI 블러/하이라이트 처리는 어디서 실행되나?
- Lambda를 기각한 세 가지 이유는?
- 왜 노트북 벤치마크를 믿으면 안 됐나?
- 1080p 다운스케일이 왜 필수 전제인가?
- 비용 손익분기와 재검토 조건은?
- 동시 처리 상한과 그 한계는?
- 아직 안 풀린 AI 품질 문제는?

## 맥락
ToBe 다이어그램에 Lambda(옵션A) vs FastAPI(옵션B)가 "택1 보류"로 남아 있었음. MSG-142에서 실측 후 결정.

## 선택지
① Lambda ② 상시 FastAPI ③ GPU 인스턴스.

## 결정
**② 상시 FastAPI** — dev EC2에 Docker 컨테이너로, c7g.medium 이상, ASM-MSG/AI 레포(AGPL-3.0, 모델은 MSG-144: YOLOv11n 얼굴+번호판 + PySceneDetect). 처리 3~4분이므로 **비동기**(Spring이 넘기고 processing_status=BLURRING). 파이프라인 첫 단계에 1080p 30fps 다운스케일(선택 아님).

## 근거 (실측)
- 워크로드가 분 단위(4K는 Lambda 한도의 65%, S3 I/O·이미지 pull 더하면 11~13분) — 서버형.
- vCPU 확장 무의미(+1~10%) → Lambda의 "메모리로 시간 산다" 카드 무효.
- 프레임당 추론 시간 해상도 무관 → 다운스케일로 프레임 수만 줄이면 9.7분→3~4분, 정확도 손실 없음.
- 비용: 1,000건/월 Lambda $4.5 vs FastAPI $29.8, 10,000건이면 역전. 팀이 이미 EC2+Docker 운영 중이라 신규 파이프라인(ECR) 비용 없음. GPU $384는 과함.

## 영향
- 받아들임: 유휴 비용 월 ~$30, 1 vCPU 시간당 ~17건 상한(동시 부하 미측정).
- 문서 수정: architecture.md(FastAPI 확정·다운스케일 추가), ToBe drawio(Lambda 제거), YOLO/CLIP 표기 갱신(CLIP·pHash Phase 2).
- 재검토: 간헐적 스파이크 트래픽 → Lambda / 처리 10분 초과 → GPU.
- ⚠️ MVP 블로커 2건(범위 밖): 정면 얼굴도 다수 미탐지(conf 0.25에서도, MSG-140 미충족) · 단일 씬 영상 하이라이트 0개(MSG-141 미충족).

## 출처
raw: `raw/confluence/2026-07-21 설계결정 AI 처리 실행 환경 — 상시 FastAPI 서버 (MSG-143) (cf-20643841).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/20643841
