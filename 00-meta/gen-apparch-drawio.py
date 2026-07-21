#!/usr/bin/env python3
"""FillMap Application Architecture (SA v2) → drawio. EDGE 2번 장 스타일: UI 화면 → API → 저장소.
실행: repo 루트에서 python3 00-meta/gen-apparch-drawio.py
근거: PRD 화면별 기능·API(cf-18972709) · API 명세 v1/v2 문서들 · IA v2 초안 · 미션 설계검토(cf-19857410)"""
from xml.sax.saxutils import escape, quoteattr

# 상태색 (IA와 동일 어휘)
ST = {"구현": ("#d5e8d4", "#82b366"), "부분": ("#fff2cc", "#d6b656"),
      "미구현": ("#ffffff", "#666666"), "신규": ("#FBF6E4", "#D6A34A"), "P2": ("#dae8fc", "#6c8ebf")}

# UI 화면 카드: (이름, [(행, 상태)])
SCREENS = [
    ("로그인·온보딩", [("카카오 로그인", "구현"), ("Apple·로컬 (미정)", "미구현"), ("위치·카메라 권한", "미구현")]),
    ("① 지도 홈", [("내 격자 색칠 (뷰포트)", "구현"), ("미션 칩·바텀시트", "신규"),
                   ("요약 카드 (핫·추천·수집)", "미구현"), ("행정동 검색", "미구현")]),
    ("② 격자 썸네일", [("격자 요약", "부분"), ("영상 썸네일 그리드", "미구현")]),
    ("③ 핫구역", [("순위 리스트·갱신", "미구현")]),
    ("④ 격자 상세", [("표시명·활동 지표", "미구현"), ("영상 목록·재생", "미구현"),
                     ("좋아요", "미구현"), ("신고 진입", "미구현")]),
    ("⑤ 신고 모달", [("사유 선택·제출", "미구현")]),
    ("⑥ 촬영·업로드", [("촬영·갤러리 선택", "구현"), ("업로드·진행 표시", "구현"),
                       ("AI 하이라이트·블러 확인", "미구현"), ("교체·삭제", "구현")]),
    ("⑦ 개인 도감", [("요약·3뷰 (지도·갤러리·뱃지)", "미구현"), ("뱃지·스트릭", "미구현"),
                     ("지역별 수집률", "미구현"), ("스탬프북", "신규"), ("공개범위 설정", "미구현")]),
    ("설정·프로필", [("프로필 수정", "미구현"), ("로그아웃·계정 삭제", "부분")]),
]

# API 카드: (이름, 상태, [엔드포인트 행])
APIS = [
    ("Auth API", "구현", ["POST /auth/oauth/kakao", "POST /auth/login·logout", "Refresh Token (예정)"]),
    ("Grid API", "구현", ["GET /api/grids (뷰포트)", "GET /api/grids/{id}"]),
    ("Grid 확장 API", "미구현", ["GET /grids/{id}/videos", "GET /grids/hot (핫구역)", "POST·DEL /videos/{id}/likes"]),
    ("Mission API", "신규", ["GET /api/missions/active", "(전역 캐시 · bbox 없음)"]),
    ("Video 재생 API", "미구현", ["GET /api/videos/{id}", "(presigned GET · 상태 분기)"]),
    ("Social·Report API", "미구현", ["POST /api/reports", "friends CRUD (P2)"]),
    ("Video API", "구현", ["POST /videos/presigned-url", "POST /api/videos (점령)", "PUT·DELETE /videos/{id}"]),
    ("Collection API", "미구현", ["GET /collections/summary", "GET /collections/grids", "GET /collections/badges"]),
    ("Region API", "미구현", ["GET /regions/search", "GET /regions/stats", "GET /regions/{code}"]),
    ("User API", "미구현", ["GET·PATCH /users/me", "DELETE /users/me"]),
]

# 화면 → API 연결 (PRD §2 매핑 그대로)
LINKS = [
    ("로그인·온보딩", "Auth API"),
    ("① 지도 홈", "Grid API"), ("① 지도 홈", "Grid 확장 API"), ("① 지도 홈", "Mission API"),
    ("① 지도 홈", "Collection API"), ("① 지도 홈", "Region API"),
    ("② 격자 썸네일", "Grid API"), ("② 격자 썸네일", "Grid 확장 API"), ("② 격자 썸네일", "Video 재생 API"),
    ("③ 핫구역", "Grid 확장 API"),
    ("④ 격자 상세", "Grid API"), ("④ 격자 상세", "Grid 확장 API"), ("④ 격자 상세", "Video 재생 API"),
    ("④ 격자 상세", "Region API"), ("④ 격자 상세", "Social·Report API"),
    ("⑤ 신고 모달", "Social·Report API"),
    ("⑥ 촬영·업로드", "Video API"),
    ("⑦ 개인 도감", "Collection API"), ("⑦ 개인 도감", "Region API"), ("⑦ 개인 도감", "User API"),
    ("설정·프로필", "User API"), ("설정·프로필", "Auth API"),
]

# API → 저장소 연결
STORES = [
    ("PostgreSQL + PostGIS", "#dae8fc", "#6c8ebf"),
    ("Redis (Hot ZSET · 캐시)", "#FBEBE8", "#C15848"),
    ("S3 (원본·인코딩본)", "#d5e8d4", "#82b366"),
    ("Kafka → FastAPI AI 서버", "#F0EBF8", "#8A6ABF"),
]
SLINKS = [
    ("Auth API", "PostgreSQL + PostGIS"), ("Grid API", "PostgreSQL + PostGIS"),
    ("Grid 확장 API", "Redis (Hot ZSET · 캐시)"), ("Grid 확장 API", "PostgreSQL + PostGIS"),
    ("Mission API", "PostgreSQL + PostGIS"),
    ("Video 재생 API", "S3 (원본·인코딩본)"),
    ("Social·Report API", "PostgreSQL + PostGIS"),
    ("Video API", "S3 (원본·인코딩본)"), ("Video API", "Kafka → FastAPI AI 서버"), ("Video API", "PostgreSQL + PostGIS"),
    ("Collection API", "PostgreSQL + PostGIS"), ("Region API", "PostgreSQL + PostGIS"),
    ("User API", "PostgreSQL + PostGIS"),
]

CW_UI, CW_API, RH, RGAP, HDRH, CGAP = 220, 230, 22, 5, 26, 24
X_UI, X_API, X_ST = 170, 640, 1150
Y0 = 120

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def card(name, rows, x, y, w, hdr_fill, hdr_stroke, row_status=True):
    """헤더 + 행 목록 카드. 반환: (카드 id, 높이)"""
    h = HDRH + len(rows) * (RH + RGAP) + 8
    gid = nid("g")
    ids[name] = gid
    cells.append(f'<mxCell id="{gid}" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;'
                 f'fillColor=#FFFFFF;strokeColor={hdr_stroke};strokeWidth=1.3;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value={quoteattr(escape(name))} style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;'
                 f'fillColor={hdr_fill};strokeColor=none;fontSize=11;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x+4}" y="{y+3}" width="{w-8}" height="{HDRH-6}" as="geometry"/></mxCell>')
    for i, r in enumerate(rows):
        if row_status:
            label, st = r
            f_, s_ = ST[st]
        else:
            label, (f_, s_) = r, ("#FFFFFF", "#B4B9BE")
        cells.append(f'<mxCell id="{nid()}" value={quoteattr(escape(label))} style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;'
                     f'fillColor={f_};strokeColor={s_};fontSize=9.5;fontColor=#2B2B2B;" vertex="1" parent="1">'
                     f'<mxGeometry x="{x+8}" y="{y+HDRH+i*(RH+RGAP)}" width="{w-16}" height="{RH}" as="geometry"/></mxCell>')
    return gid, h

def edge(sname, tname, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;"):
    eid = nid("e")
    edges.append(f'<mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                 f'strokeColor=#B4B9BE;strokeWidth=1;endArrow=open;endSize=6;{extra}" edge="1" parent="1" '
                 f'source="{ids[sname]}" target="{ids[tname]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# UI 화면 컬럼
y = Y0
for name, rows in SCREENS:
    _, h = card(name, rows, X_UI, y, CW_UI, "#E8F0F8", "#4E7EA8")
    y += h + CGAP
h_ui = y

# API 컬럼
y = Y0
for name, st, eps in APIS:
    f_, s_ = ST[st]
    _, h = card(f"{name}  [{st}]", [(e, st) for e in eps], X_API, y, CW_API, f_, s_)
    ids[name] = ids[f"{name}  [{st}]"]
    y += h + CGAP
h_api = y

# 저장소 컬럼 (실린더)
y = Y0 + 120
for name, f_, s_ in STORES:
    gid = nid("s")
    ids[name] = gid
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(name))} style="shape=cylinder3;whiteSpace=wrap;html=1;'
                 f'fillColor={f_};strokeColor={s_};strokeWidth=1.5;fontSize=10.5;fontStyle=1;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_ST}" y="{y}" width="200" height="60" as="geometry"/></mxCell>')
    y += 60 + 60

# 액터
aid = nid("a")
cells.append(f'<mxCell id="{aid}" value="🧑‍🎓" style="ellipse;whiteSpace=wrap;html=1;fillColor=#EAF3E2;strokeColor=#8FBF7B;'
             f'strokeWidth=1.5;fontSize=34;shadow=1;" vertex="1" parent="1">'
             f'<mxGeometry x="40" y="{Y0 + h_ui/2 - 100}" width="64" height="64" as="geometry"/></mxCell>')
cells.append(f'<mxCell id="{nid()}" value="사용자" style="text;html=1;strokeColor=none;fillColor=none;align=center;'
             f'fontSize=11;fontStyle=1;" vertex="1" parent="1">'
             f'<mxGeometry x="22" y="{Y0 + h_ui/2 - 32}" width="100" height="18" as="geometry"/></mxCell>')
ids["__actor__"] = aid
for name, _ in SCREENS[:3]:
    edge("__actor__", name, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=none;")

# 화면→API, API→저장소
for s, t in LINKS:
    edge(s, t)
for s, t in SLINKS:
    edge(s, t)

# 헤더·범례
total_w = X_ST + 260
total_h = max(h_ui, h_api) + 60
cells.insert(0, f'<mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F2F4;strokeColor=none;" vertex="1" parent="1">'
                f'<mxGeometry x="-30" y="-30" width="{total_w+120}" height="{total_h+160}" as="geometry"/></mxCell>')
cells.insert(1, '<mxCell id="ttl" value="FillMap · Application Architecture (SA v2 · 2026.07) — 화면(IA) → API → 저장소" '
                'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=15;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
                '<mxGeometry x="40" y="0" width="900" height="24" as="geometry"/></mxCell>')
cells.insert(2, '<mxCell id="sub" value="행 색 = 구현 상태 (초록 구현 · 노랑 부분 · 흰 미구현 · 금색 신규 미션) — 매핑 근거: PRD 화면별 기능·API'
                ' · API 설계 v1/v2" '
                'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#6B7075;" vertex="1" parent="1">'
                '<mxGeometry x="40" y="26" width="900" height="18" as="geometry"/></mxCell>')
cells.insert(3, f'<mxCell id="c_ui" value="UI 화면 (IA 기준)" style="text;html=1;strokeColor=none;fillColor=#F1F2F4;fontSize=12;fontStyle=1;'
                f'fontColor=#4E7EA8;" vertex="1" parent="1"><mxGeometry x="{X_UI}" y="{Y0-34}" width="180" height="20" as="geometry"/></mxCell>')
cells.insert(4, f'<mxCell id="c_api" value="REST API (도메인)" style="text;html=1;strokeColor=none;fillColor=#F1F2F4;fontSize=12;fontStyle=1;'
                f'fontColor=#3E9E6D;" vertex="1" parent="1"><mxGeometry x="{X_API}" y="{Y0-34}" width="180" height="20" as="geometry"/></mxCell>')
cells.insert(5, f'<mxCell id="c_st" value="저장소·비동기" style="text;html=1;strokeColor=none;fillColor=#F1F2F4;fontSize=12;fontStyle=1;'
                f'fontColor=#8A6ABF;" vertex="1" parent="1"><mxGeometry x="{X_ST}" y="{Y0-34}" width="180" height="20" as="geometry"/></mxCell>')

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="SA v2 — Application Architecture" id="sa-v2-apparch">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{total_w+100}" pageHeight="{total_h+200}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 3_FillMap_SA_v2_AppArch_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · screens={len(SCREENS)} apis={len(APIS)} links={len(LINKS)+len(SLINKS)}")
