---
title: Video API (v1 구현 기준)
type: spec
product: fillmap
class: log
status: active
source: "raw/confluence/2026-07-17 Video API (cf-17498193).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [Video, 영상, API, 업로드, upload, presigned URL, S3, 삭제, 교체, replace, 점령, 롤백, 인코딩, 격자]
aliases: [영상 API, 비디오 API]
related: ["[[FillMap API 명세 v1]]", "[[Video 재생 조회 API 예정]]", "[[트러블슈팅 파일 없이 격자 점령 MSG-132]]"]
---

# Video API (v1 구현 기준)

> [!tldr]
> 영상(방문·점령) 도메인, base `/api/videos`, 전 엔드포인트 인증 필요.
> 업로드 흐름: presigned URL 발급 → 클라이언트 S3 직접 업로드 → 메타 저장(POST /api/videos, 이때 격자 점령).
> 교체는 같은 격자 안에서만(3422 GRID_MISMATCH), 내 영상이 0개 되면 점령 롤백.

## 이 노트로 답할 수 있는 질문
- 영상 업로드는 어떤 흐름으로 이루어지나?
- 업로드 메타 저장에 어떤 필드를 보내고 응답에 뭐가 오나?
- 영상 교체 시 좌표를 생략하면/보내면 어떻게 동작하나?
- 영상을 모두 삭제하면 격자 점령은 어떻게 되나?
- 영상 길이·확장자 제한은?
- Video 도메인 에러 코드(3xxx)는 뭐가 있나?

## 엔드포인트
| 메서드/경로 | 핵심 |
| --- | --- |
| `POST /api/videos/presigned-url` | extension(mp4/mov)·contentType·contentLength → uploadUrl·s3Key·expiresInSec |
| `POST /api/videos` | s3Key·lat·lon·durationSec(1~30)·recordedAt → videoId·gridId·processingStatus·occupied(첫 점령 여부) |
| `PUT /api/videos/{videoId}` | 본인만. 좌표 생략=파일만 교체, 좌표 지정=같은 격자 검사(다르면 3422). 교체 후 상태 UPLOADED(재인코딩) |
| `DELETE /api/videos/{videoId}` | 본인만. 격자 내 영상 0개 되면 점령 롤백. 시간 제한 없음 |

## 에러 코드 (3xxx)
3400 INVALID_COORDINATE · 3401 INVALID_S3_KEY · 3402 UPLOAD_NOT_FOUND · 3403 VIDEO_FORBIDDEN · 3404 VIDEO_NOT_FOUND · 3413 FILE_TOO_LARGE · 3415 UNSUPPORTED_EXTENSION · 3422 GRID_MISMATCH

## 출처
raw: `raw/confluence/2026-07-17 Video API (cf-17498193).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/17498193
