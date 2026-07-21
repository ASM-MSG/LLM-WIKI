---
title: ADR — 지도 SDK를 카카오에서 네이버로 전환
type: decision
product: fillmap
class: decision
status: active
source: "raw/confluence/2026-07-17 설계결정 지도 SDK를 카카오에서 네이버로 전환 (cf-18546692).md"
created: 2026-07-17
updated: 2026-07-21
keywords: [ADR, 지도 SDK, 카카오맵, 네이버 지도, naver maps, kakao, 구글 지도, Style Editor, StyleMap, POI, React Native, RN, 무료 한도, 600만, ncpKeyId, oapi]
aliases: [지도 SDK ADR, 네이버 전환]
related: ["[[ADR 격자 표시명 zone]]", "[[갭 분석 디자인 문서 코드 싱크]]", "[[Region API 예정]]"]
---

# ADR — 지도 SDK를 카카오에서 네이버로 전환

> [!tldr]
> 웹 지도 SDK를 카카오→네이버로 전환 (상태: 제안됨 — 규호·멘토 확인 필요). 영향은 FE 전용, 백엔드 변경 0 (격자 양자화는 SDK 무관).
> 이유: ① 카카오는 베이스맵 POI를 끌 수 없어 "노이즈 최소화" UI 정책과 충돌, 네이버 Style Editor는 symbol visibility OFF 가능 ② 카카오 RN 공식 SDK 부재(래퍼 1년 방치) — 앱 로드맵과 충돌 ③ 네이버 무료 월 600만 건(구글의 600배), 한도 설정으로 과금 차단 가능.
> 주의: 신규 Maps 상품은 호스트 oapi.map.naver.com + ncpKeyId (레거시 예제 그대로 쓰면 인증 실패). 네이버엔 키워드 검색이 없지만 행정동 검색은 우리 DB로 완결. 카카오 OAuth 로그인은 유지.

## 이 노트로 답할 수 있는 질문
- 지도 SDK를 왜 네이버로 바꾸나?
- 백엔드는 뭘 바꿔야 하나? (답: 없음)
- 네이버 신규 Maps 상품에서 주의할 점은 (레거시와 차이)?
- 무료 한도와 과금 방지책은?
- 네이버에 키워드 검색이 없는데 괜찮은 이유는?
- 구글 지도를 기각한 이유는?
- FE 연동에 필요한 값과 함정은?

## 맥락
카카오맵 웹 SDK 사용 중. 문제: ① POI/라벨 끄기·다크모드 불가 — glossary의 "시각적 노이즈 최소화" 정책과 도구 충돌 ② RN 공식 SDK 없음(웹 출시 후 RN 앱 계획과 충돌). 네이버는 2025년 Maps 독립 상품으로 개편 — 신규 가입은 자동으로 신규 Maps(레거시 신청 차단).

## 선택지
① 카카오 유지 ② 네이버 ③ 구글.

## 결정
**② 네이버.** Style Editor(10개 카테고리 visibility, symbol 전체 OFF 가능, Style ID를 웹·앱 공유) + 한국 지도 품질 유지 + 월 600만 무료(카운팅도 로딩 시 1건). 구글은 무료 1만 maploads(100명×3회/일이면 소진, 성장 시나리오 월 $980)·한국 품질 미검증·웹/RN 스타일 이원화로 기각.

## 근거
카카오 탈출은 앱 로드맵상 어차피 필요 · 네이버는 카카오 장점(품질·무료) 유지 · 검색은 SDK 무관(행정동은 regions+PostGIS로 완결, [[ADR 격자 표시명 zone]]의 자체 zones가 랜드마크 검색도 해결).

## 영향
- FE 연동: Client ID만 전달(Secret 금지), `oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=`, Dynamic Map만 등록, Web 서비스 URL에 로컬 origin 필수.
- 후속: 한도 설정(600만) · 운영 계정 결정(무료는 계정 단위, 대표 계정 자동 지정) · Style ID 제작 · 웹 PoC · RN 2.4.x PoC.
- 재검토 트리거: 랜드마크를 외부 API 의존으로 결정하면 카카오 Local API 재평가(현재 zone 자체 보유로 무관) · RN 라이브러리(1인 메인테이너) 막히면 재검토 · 구글 한국 품질 개선 시.

## 출처
raw: `raw/confluence/2026-07-17 설계결정 지도 SDK를 카카오에서 네이버로 전환 (cf-18546692).md`
Confluence: https://soma17-msg.atlassian.net/wiki/spaces/M/pages/18546692
