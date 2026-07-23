# 🗺️ index — 전체 지도 / 질의 진입점

> 모든 compiled 노트의 진입점. ingest 때마다 갱신한다. "이 제품만" 필터는 폴더가 아니라 frontmatter `product:`.

## 01-product (canon · 단일 진실)
_아직 없음_

## 02-planning (기획)
- [[IA v2 초안 (화면·기능 트리)]] — EDGE 수준 drill-down IA + 유스케이스 목표 단위 분해 (draft)
- [[설계검토 미션·이벤트 기능 추가]] — 축제·둘레길을 격자 위에, 피봇 아님 판정과 데이터 실측
- [[2026-07-13 격자 방문 체크 표시 아이디어]] — 방문 격자 체크 표시 UX 제안 (최규호)

## 03-specs (SPEC / PRD)
- [[FillMap API 스펙 통합]] — 전체 API 한 페이지 현황판 (구현 17 + AI 3 + 예정·제안, 열린 결정 10)
- [[PRD FillMap MVP 화면별 기능·API]] — 피그마 7화면 ↔ API 매핑, MVP 미확정 7항목
- [[개인 도감 화면 확정 UX·API 설계]] — PO 확정(7/22): 격자 중심 도감, 탐험률=격자 중심점 축, 신규는 MSG-153뿐
- [[FillMap API 명세 v1]] — 구현 기준 단일 진실 (허브) · 하위: [[Auth API]] · [[Grid API]] · [[Video API]]
- [[FillMap API 설계 v2 draft]] — 예정 API 허브 · 하위: [[Auth 확장 API 예정 Refresh Token]] · [[User 프로필 API 예정]] · [[Video 재생 조회 API 예정]] · [[Collection API 예정]] · [[Region API 예정]] · [[Grid 확장 API 예정]] · [[Social API 예정]] · [[Notification API 예정]]
- [[FillMap DB Schema v5 MVP]] — MVP 테이블 기준 (KangJeong)
- [[FillMap 지도·격자 DB 설계 MVP]] — 지도 도메인 DB 상세·쿼리·인덱스
- [[FillMap DB 자료형·ENUM·GeoJSON 기준]] — 타입·ENUM 10종·PostGIS·GeoJSON
- [[다이어그램 모음]] — 제출용 다이어그램 6종 포인터

## 04-decisions (ADR)
- [[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]] — 영상 직접 연결 기각, 탐험률=동 단위 확정, FE 격자 로컬 산술 계약
- [[ADR 격자 행정동 라벨 grids.region_code]] — 행정동 라벨은 grids에 격자당 1회 저장, 동 단위 영상 조회 신설 (MSG-167)
- [[ADR AI 처리 실행 환경 FastAPI]] — 상시 FastAPI 확정, Lambda·GPU 기각 (MSG-143)
- [[ADR 격자 표시명 zone]] — "홍대 A-14" = 수동 zone + 좌표 산술
- [[ADR 지도 SDK 네이버 전환]] — 카카오→네이버, POI OFF·RN·무료 600만
- [[ADR viewport polling SLO]] — polling 확정, p95<300ms SLO (MSG-134)

## 05-meetings (회의록)
- [[2026-07-23 기획회의 미션·이벤트 표시 방식]] — 점·선·면 수렴: 축제=면, 코스=직선 폴리라인, 팝업=마커 (녹음 전사 기반)
- [[2026-07-18 강성재 멘토 정규 멘토링]] — 백엔드 2주 보고 (인프라·격자·업로드·운영)
- [[2026-07-18 김태완 멘토 DB 피드백]] — grid·region 분리, PostGIS vs 레이블링
- [[2026-07-17 프론트-백 합의]] — bbox 폴링, 격자 영상 목록 형태
- [[2026-07-16 박원형 멘토 멘토링]] — 기획·인프라·CI/CD 보고와 피드백

## 06-research (리서치)
- [[AI 블러 파이프라인 실측 현황]] — E2E ~4분·추론 80%·NFR-003 판정, 지연 개선은 GPU뿐 (개선점 논의용)
- [[PostgreSQL 실무 가이드 모음]] — junhkang 레포 덤프(52편): 인덱스 6종 원리·실행계획·튜닝 참고 서가
- [[2026-07-21 AI Highlight-Blur 개발 기록]] — AI 서버 dev 배포 완료, AGPL 레포 분리·conf 0.05·jobs API 계약
- [[갭 분석 디자인 문서 코드 싱크]] — 시안 ↔ 코드 전수 대조, 보안 이슈 발견
- [[ERD 정렬 디자인 기준 데이터모델]] — 스키마 변경 집약 (팀 합의용)
- [[트러블슈팅 파일 없이 격자 점령 MSG-132]] — s3Key 검증 3종 도입기
- [[그라운드 플립 아티클 모음]] — 선배 팀(M3 PRO) velog 4편 허브 · 하위: [[그라운드 플립 부하 테스트 사례]] · [[그라운드 플립 뱃지 시스템 사례]] · [[그라운드 플립 마커 클러스터링 사례]] · [[분산락 적용 주의점]]
- [[그라운드 플립 발표자료·기획서]] — M3 PRO 최종 발표·소마 기획서 (성과: 사용자 2,640명)
- [[전국문화축제표준데이터 데이터셋]] — 축제 1,300건 좌표 데이터 (미션·이벤트 검증용)
- [[모행 발표자료]] — 타 팀 중간·최종 발표 구성 참고
- [[EDGE 아키텍처 문서 모음]] — 타 팀 아키텍처 다이어그램 벤치마크

## 90-archive
- [[구현된 API 스펙 v1 폐기 스텁]] — v1 명세로 통합되어 폐기

---

## 지원 파일
- `hot.md` — 최근 작업
- `log.md` — 이력
- `00-meta/SCHEMA.md` — 운영 규칙(권위)
- `00-meta/glossary.md` — 용어사전
