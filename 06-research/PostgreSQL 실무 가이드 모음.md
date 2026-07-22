---
title: PostgreSQL 실무 가이드 모음 (junhkang 레포)
type: hub
product: fillmap
class: log
status: active
source: "raw/2026-07-22 postgresql-main"
created: 2026-07-22
updated: 2026-07-22
keywords: [PostgreSQL, 포스트그레스, DB, 인덱스, index, B-tree, GIN, GiST, SP-GiST, BRIN, Hash, MVCC, Vacuum, WAL, TOAST, 트랜잭션, transaction, Lock, 실행계획, Explain, 커버링 인덱스, covering index, Full Text Search, pg_stat_statements, 페이징, OFFSET, LIMIT, 성능향상, 튜닝]
aliases: [postgresql-main, PostgreSQL 노하우, junhkang postgresql]
related: ["[[FillMap 지도·격자 DB 설계 MVP]]", "[[FillMap DB Schema v5 MVP]]", "[[2026-07-18 김태완 멘토 DB 피드백]]", "[[그라운드 플립 부하 테스트 사례]]"]
---

# PostgreSQL 실무 가이드 모음 (junhkang 레포)

> [!tldr]
> GitHub `junhkang/postgresql` 레포 전체 덤프(md 52편 + 이미지) — "산업의 역군"에서 수천만 건 데이터를 PostgreSQL로 운영하며 얻은 노하우, 공식 문서 기반. 개념 20편 · 인덱스 7편 · 성능향상 8편 · 사용법 13편 + 용어사전.
> FillMap 직결 포인트: **GiST 인덱스 원리**(PostGIS 격자·공간 쿼리의 기반), **인덱스 설계·Index-Only/커버링 스캔**(뷰포트 조회 튜닝), **OFFSET/LIMIT 페이징 주의점**(우리가 cursor를 택한 이유 뒷받침), **pg_stat_statements**(RDS 전환 후 쿼리 모니터링).
> 원문 상세는 junhkang.tistory.com. 필요할 때 개별 문서를 열어 보는 참고 서가 — 개별 노트로 쪼개지 않는다.

## 이 노트로 답할 수 있는 질문
- raw의 `2026-07-22 postgresql-main` 폴더는 뭐고 어디서 왔나?
- PostgreSQL 인덱스 종류별(B-tree/GIN/GiST/SP-GiST/BRIN/Hash) 원리 자료는 어디 있나?
- 실행계획(Explain) 읽는 법·쿼리 튜닝 자료는 어디 있나?
- FillMap 격자/뷰포트 쿼리 설계에 어떤 문서가 유용한가?
- MVCC·Vacuum·WAL 같은 내부 구조 학습 자료는 어디 있나?

## 구성 (폴더별)
- **개념/ (20편)** — MVCC · Vacuum · WAL·아카이브 백업 · TOAST · Lock(Dead lock) · 트랜잭션 개념/작동원리 · 2PC · Planner/Optimizer · Visibility Map · 물리적 한계치 · 상속 · 뷰 · 시퀀스 · 함수 · Trigger/Procedure · 제약조건 · 외래키 · 윈도우 함수 · ROLE/권한
- **개념/인덱스/ (7편)** — 인덱스 개념·설계 방법 + B-tree · GIN · **GiST** · SP-GiST · BRIN · Hash 원리
- **성능향상/ (8편)** — 실행계획 보는 법(Explain 지표) · Index-Only 스캔·커버링 인덱스 · 미사용 인덱스 찾기 · 명시적 JOIN으로 플래너 제어 · 대량 INSERT 개선 · Full Text Search · ORDER BY 인덱스 정렬 · RDS pg_stat_statements
- **사용/ (13편)** — **OFFSET/LIMIT 페이징 주의점** · GROUPING SETS/CUBE/ROLLUP · UNION/INTERSECT/EXCEPT · ROW_NUMBER/RANK · 문자열·날짜 처리 · DISK 모니터링 등
- `용어사전.md` — frozen 튜플·Page·Oid 등 내부 용어

## FillMap 관점 메모
- 격자·뷰포트 공간 쿼리는 PostGIS = GiST 기반 — [[FillMap 지도·격자 DB 설계 MVP]]의 인덱스 선택 근거 보강용
- "페이징 OFFSET/LIMIT 주의점"은 우리 cursor 페이지네이션 관례(MSG-90)의 이유를 설명할 때 인용 가능
- RDS 전환(출시 시점) 후 모니터링은 pg_stat_statements 문서 참고 — [[2026-07-18 김태완 멘토 DB 피드백]]과 연결

## 출처
raw: `raw/2026-07-22 postgresql-main/` (폴더 전체)
원본: https://github.com/junhkang/postgresql · 상세 글: junhkang.tistory.com
