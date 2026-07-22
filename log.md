# 📜 log — 이력

> 저장소에 일어난 변경 이력(append-only). 시간순 추가.

- 2026-07-21 — 저장소 초기화. Confluence 연동(confluence-sync) 포함.
- 2026-07-21 — Confluence 기존 문서 32건 백필(raw/confluence/) 및 일괄 ingest (compiled 노트 32개 생성, index/hot 갱신).
- 2026-07-21 — Drive 신규 raw 10건 ingest: velog 아티클 4편 스냅샷(raw/article/), 그라운드 플립·모행·EDGE·축제 데이터셋 research 노트 9개 생성, 다이어그램 모음 노트에 PDF 원본 연결, raw 파일명 정리.
- 2026-07-21 — raw 폴더 재구성 반영: Architecture Map/(다이어그램 원본 png·drawio 12개 추가), 기획레퍼런스/ 이동에 따른 노트 source 경로 갱신.
- 2026-07-21 — 03-specs 6건을 코드 레포 현행화(컨트롤러 5개·엔드포인트 14개): API 명세 v1·Auth API·Grid API에 reissue/dev·GridVideo(my-videos·cover)·커서 페이지네이션 반영, Refresh Token 예정 문서를 MSG-135 구현 완료로 승격, Grid 확장·v2 draft의 Redis/선행 과제 갱신.
- 2026-07-21 — IA v2 초안 노트 작성 (02-planning) — 미션·이벤트 반영, 유스케이스 세분화안 포함.
- 2026-07-21 — AI 파이프라인 다이어그램 draft 생성 (EDGE 5번 장 스타일, 유스케이스 v2 draft와 함께 Architecture Map/).
- 2026-07-21 — 멘토 피드백(에픽≠유스케이스) 반영: 유스케이스를 IA 리프 1:1(57개)로 재생성, 기준을 IA v2 노트 §2에 명문화.
- 2026-07-21 — SA v2 (Application Architecture) draft 생성: IA 화면 → API 10개 도메인 → 저장소 매핑, PRD 기준 연결 35개.
- 2026-07-21 — SysA v2(논리 뷰) draft 생성 — 기술명 제거·역할 그룹만, EDGE식 개편 5종 세트 완성 (IA·유스케이스·SA v2·AI 파이프라인·SysA v2).
- 2026-07-21 — Confluence 신규 1건 ingest (AI Highlight-Blur 개발 기록, cf-21102593). lastSync 갱신.
- 2026-07-22 — 재-ingest 점검: 신규 raw 없음. IA v2 drawio 수동 레이아웃 조정분 확인(내용·상태 동일, 배치만 변경) — IA v2 노트에 재생성 시 덮어쓰기 주의 명기.
- 2026-07-22 — Confluence 신규 1건 sync+ingest (개인 도감 화면 확정 UX·API 설계, cf-21528615) → 03-specs 노트 생성, 관련 노트 6건 역링크·대체 포인터 반영. lastSync 갱신.
- 2026-07-22 — [[FillMap API 스펙 통합]] 신설: 멘토링 스펙 점검 대비 전체 API 통합 뷰(hub). index 등록.
- 2026-07-22 — Drive 신규 raw ingest: postgresql-main 레포 덤프(154파일) → [[PostgreSQL 실무 가이드 모음]] 허브 노트. 폴더 "2026-07-22 postgresql-main"으로 리네임, lint.js raw-naming이 폴더 날짜 접두사도 인정하도록 수정. Confluence sync: 신규 없음(데일리 스크럼 제외, API 스펙 통합 발행본은 재ingest 안 함), lastSync 06:41Z.
- 2026-07-22 — Confluence 신규 1건 ingest: MSG-167 격자 행정동 라벨 설계 결정(cf-22216705) → [[ADR 격자 행정동 라벨 grids.region_code]]. lastSync 08:20Z.
