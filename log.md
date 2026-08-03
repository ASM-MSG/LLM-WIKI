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
- 2026-07-23 — 기획회의 녹음(25분 m4a) whisper-cpp(large-v3-turbo+VAD) 전사 → raw 회의록·srt 생성, [[2026-07-23 기획회의 미션·이벤트 표시 방식]] ingest (05-meetings). 화자 분리는 내용 기반 추정.
- 2026-07-23 — Confluence sync 3건 (스크럼 2건 제외, 기수집 2건 skip): API 스펙 통합 발행본(cf-21430294) 스냅샷 백필, AI 블러 실측(cf-22773767)·MSG-167 후속 결정(cf-23035906) → [[AI 블러 파이프라인 실측 현황]]·[[ADR MSG-167 후속 결정 탐험률 축·격자 표시명·격자 계약]] ingest. 역링크 6건, index/hot 갱신. lastSync 05:29Z.
- 2026-07-24 — Confluence sync 3건(코스 포토스팟 결정·FE 격자 계약·MSG-167 v2) → decisions 1·specs 1 신규 ingest, MSG-167 ADR·zone ADR(MSG-234 보류) 갱신, 역링크 3건.
- 2026-07-24 — 다이어그램 v2 세트 전면 정비(gen 스크립트 8개): EDGE 문법 정렬 — CA(ALB 통로 배치·SaaS 우회·WAF 복원·ECR 아이콘 수정), SA(화면 색 축·상태 태그 제거·무손실 압축·AI 환경 재배치), SysA(관통선 수정·워커 트리거 분리), IA(무채색·리프 96 드릴다운·라벨 다이어트), UseCase(30초 정정), User Journey v2 신설(6행 매트릭스), AI Pipeline(실측 각주·read 선 우회). 전 장 용어 정합(서면 A-14·탐험률 동 단위·코스 포토스팟)·티켓번호·이모지 제거. 제출 PPTX 7장 재조립.

- 2026-07-24 — [[FillMap API 스펙 통합]] 현황판 코드 실사 갱신 (BE main 04f1ae0 + Figma 화면 실사): 구현 17→23개 승격(재생 MSG-206·visibility MSG-162·탐험률 by-point/by-grid·도감 grids·동 단위 videos), 6xxx 대역·3420 확정, 구현 예정을 Mission 도메인으로 교체, Figma 파생 갭 3건(신고·공유·통합 검색)·도감 뱃지/스트릭 갭 신설, 열린 결정 4건 해소 반영.
- 2026-07-24 — IA v2 Figma 코멘트 리뷰 반영 (kangjeongmin·최규호, node 13775-6269 핀 12건): 게스트 모드 신설(비로그인 지도·핫구역 열람, 업로드·도감 로그인 유도), 세션 유지·내 색 팔레트·구역/행정동 경계 레이어·내 동네 채우기·거리별 버튼·요약 카드 삭제, 미션 진행도 표기는 개인 도감 스탬프북으로 이동, 격자 표시명 '서면 A-14' 제거(행정동 이름 기본 — MSG-234 보류 정합). gen-ia 재생성(리프 96→86)·PPTX s1 교체.
- 2026-07-24 — IA 사용자 직접 수정분(16:15) 백포트 + 파급 반영: IA에서 (미정) 7건 해소(핫구역 순위 산정=조회수 확정, AI 하이라이트·블러, 계정 삭제, 친구 찾기, 사유 선택, 실패·블라인드, 조회수), 미션 칩 '팝업' 추가, 핫구역 지수→순위 용어 통일, 교체·삭제에 '공유' 추가 → gen-ia 백포트·재생성(리프 87). 파급: UseCase(공유·비로그인 열람 추가, 미방문 추천·내 동네·진행도 제거, 55개), SA(요약 카드 행 삭제·지도홈→Collection 연결 제거, 게스트 열람 행, 조회수 산정, 표시명 행정동, visibility·reissue·videos?regionCode 라벨 현행화, boundary 행 제거). UserJourney·SysA·CA·AI Pipeline은 무영향 확인. PPTX s0(유스케이스 복구)·s1(IA)·s3(SA) 교체.
- 2026-07-25 — Confluence sync 4건(스크럼 1건 제외): 기획확정 지도 홈 개편(cf-24805388)·확정 기획 허브(cf-24739846) 신규, MSG-134 polling v4(§6 핫구역)·PRD v4(지도 홈 개편) 갱신분 → [[기획확정 지도 홈 개편 상단 셀]](04-decisions)·[[FillMap 확정 기획 모음]](02-planning) 신규 ingest, [[ADR viewport polling SLO]]·[[PRD FillMap MVP 화면별 기능·API]] 갱신, 역링크·index/hot 반영. lastSync 05:20Z.
- 2026-07-26 — 멘토 아키텍처 V2final 리뷰(7/25 docx) ingest → [[아키텍처 V2final 멘토 리뷰]] (06-research). raw는 `raw/Architecture Map/2026-07-25 FillMap 아키텍처 V2final 멘토 리뷰.docx`.
- 2026-07-26 — 멘토 리뷰 Quick Fix 반영: gen-apparch(A-2 API 경로 33개 /api/v1 통일 + A-1 서비스 매핑 캡션), gen-sysa(A-1 매핑 캡션 + A-3 "API Gateway = ALB+WAF" 각주) 수정 후 SA·SysA v2 draft xml 재생성. CQRS 라벨은 팀 확인 보류. 이후 다이어그램 동결(멘토 권고).
- 2026-07-26 — Confluence 발행본(cf-21430294) v4 갱신: 7/24 코드 실사분을 발행본에 반영 — 구현 17→23 승격(MSG-206·162·153·167·by-point/by-grid), 6xxx·3420 확정, Mission 🔜·Figma 갭 3건·열린 결정 9건 갱신, AI E2E 개통(MSG-168) 표기. 오늘 16시 박원형 멘토링 "API 스펙 점검" 대비.
- 2026-07-26 — [[ADR region_stats recompute equi-join 치환]](04-decisions) 신규 작성: MSG-236 구현분(BE feature/MSG-236-recompute-equi, b23e148) 반영 — refreshRegionStats ST_Covers→equi 치환·등가성 논거·테스트 23개·벤치 설계(미실행). index/hot 갱신.
- 2026-07-28 — [[ADR 장소 검색 카카오 로컬 프록시]](04-decisions) 신규: MSG-251 공급자 결정 ingest — 카카오 로컬 채택 근거·약관 조건(캐시 금지)·스모크 실측, 지도 SDK ADR 재검토 트리거 발동 기록. index/hot 갱신.
- 2026-07-30 — Confluence sync 9건 조회(스크럼 6·회고 1 제외 — 지도 홈 개편·확정 허브·viewport §6·PRD v4는 7/25 세션 기수집이라 skip) → 신규 3: [[MSG-234 상권 작도 결정 공공데이터 검수]](04-decisions, cf-26181633+cf-26116098), [[2026-07-26 이광헌 멘토 멘토링]]·[[2026-07-26 박원형 멘토 멘토링]](05-meetings). 갱신: [[ADR 격자 표시명 zone]](MSG-234 보류 해제·재개), [[FillMap API 스펙 통합]](source→7/26 발행 스냅샷). 역링크 6건. lastSync 00:24Z.
- 2026-07-30 — 재-sync 점검(01:50Z): Confluence 변경 3건 전부 skip(스크럼 1·멘토링 2건은 내용 동일 재검출 — 타임존 경계), Drive 신규 raw 없음. lastSync만 01:50Z로 갱신.

- 2026-07-30 — [[zone 표시명 데이터 파이프라인 해설]](06-research) 신규: BE 세션 산출 — 오프라인 1회(공공데이터→검수→시딩) vs 런타임 매번(FE 뺄셈 2번) 2단 구조, 격자별 이름 미저장 근거(42배), 검증 3층, 드라이런 17건 PASS. [[ADR 격자 표시명 zone]] tldr 상태 갱신(보류→MSG-234 종결·MSG-259 진행, 쟁점 3건 해소, 검색 251 이관). index/hot 갱신.

- 2026-07-30 — [[zone 표시명 FE 계약]](03-specs) 신규: FE가 구현할 것(fetch 1회 + 함수 20줄)과 검증 표를 계약으로 명문화 — 원문 cf-23199747 §7·§7-1 보존분 대체. [[FE 격자 계약 프론트-백 합의]] tldr·§5의 낡은 "zone 보류" 정정, related·updated 갱신. index/hot 반영.

- 2026-07-31 — Confluence sync 8건(cf-21430294 v7/26·26116098·26181633·27525122·27754514·27852802·27983873·28639233) 스냅샷 저장 + ingest: 신규 노트 1건([[zone 상권 공공데이터 근거]] — 결정·멘토링 3건은 07-30 원격 세션분과 중복이라 기존 노트 채택, 제안 cf-26116098 스냅샷은 결정 노트 source에 병기), 기존 노트 3건 갱신([[FillMap API 스펙 통합]] 07-26 코드 실사 반영, [[zone 표시명 FE 계약]]·[[zone 표시명 데이터 파이프라인 해설]] 발행 스냅샷 연결·현황 갱신 — cf-27983873은 파이프라인 해설과 중복이라 신설 없이 갱신 처리). 역링크: zone ADR·FE 계약·해설. lastSync 01:40Z.
- 2026-08-01 — 재-sync(08:55Z): 변경 8건 조회(스크럼 3 제외·멘토링 2건 동일 재검출 skip) — MSG-259 3건(cf-27852802·27983873·28639233)은 7/30~31 세션이 기 ingest라 신설 없음. raw 스냅샷 파일명 3건을 노트 source 참조와 정합(따옴표·날짜 표기), [[MSG-234 상권 작도 결정 공공데이터 검수]]에 MSG-259 후속 상태·역링크, [[ADR 장소 검색 카카오 로컬 프록시]]·index 정비. lastSync 08:55Z.
- 2026-08-03 — Confluence sync 2건 ingest (조회 6건 중 데일리 스크럼 2·스프린트 회고 2 제외): [[2026-08-01 신기용 멘토 멘토링]](05-meetings, cf-28999721) — 취업 관점 이력서 리뷰, "지도(PostGIS)·영상·AI는 서비스 백엔드 지원에선 변별력 없음 / Redis 하나를 깊게(페일오버 다운타임 실측 + WAS 대처 비즈니스 서술)", 신규 추천 = 대규모 알림·관측성, Redis+Lua 동시성 비추천, 공공 API는 배치 수집→정제 테이블→정제본 응답. [[백엔드 학습 로드맵 Redis HA·알림·관측성]](06-research, cf-29032474) — 후속 학습 계획 3트랙(Redis HA / 알림 파이프라인 = FillMap 미보유 신규 도메인 / 관측성 LGTM·Thanos), FillMap Redis 3사용처(핫스코어 MSG-183·핫구역 조회 MSG-184·refresh 토큰 MSG-135) 장애 시 동작 대비표. 역링크 5건(멘토링 2·zone 공공데이터·viewport ADR·분산락). lastSync 07:29Z.
