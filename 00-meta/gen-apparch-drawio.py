#!/usr/bin/env python3
"""FillMap Application Architecture (SA v2) → drawio. EDGE 2번 장 스타일 풀 버전.
UI(IA 리프 전체) → REST API(엔드포인트 전체) → 서비스 계약 → Repository/테이블 → 저장소, 환경 박스 포함.
실행: repo 루트에서 python3 00-meta/gen-apparch-drawio.py
근거: PRD(cf-18972709) · API v1(cf-17891367)·v2 설계 문서들 · infrastructure 계약(GridQueryService 등) · 미션 설계검토(cf-19857410)"""
from xml.sax.saxutils import escape, quoteattr

ST = {"구현": ("#d5e8d4", "#82b366"), "부분": ("#fff2cc", "#d6b656"),
      "미구현": ("#ffffff", "#666666"), "신규": ("#FBF6E4", "#D6A34A"),
      "미생성": ("#ffffff", "#b85450"), "P2": ("#dae8fc", "#6c8ebf")}

SCREENS = [
    ("로그인·온보딩", [("카카오 로그인 (OIDC)", "구현"), ("Apple·로컬 로그인 (미정)", "미구현"),
                      ("위치·카메라 권한 요청", "미구현"), ("세션 유지 (Refresh)", "미구현")]),
    ("① 지도 홈", [("내 격자 색칠 (뷰포트 폴링)", "구현"), ("미점령 격자 미표시 정책", "구현"),
                   ("미션 레이어 (면·선·점·경계)", "신규"), ("미션 칩 + 숫자 배지", "신규"),
                   ("미션 바텀시트 (3단)", "신규"), ("행정동 검색·자동완성", "미구현"),
                   ("요약: 핫구역 TOP 5", "미구현"), ("요약: 추천·수집·지역률", "미구현")]),
    ("② 격자 썸네일", [("격자 요약 (점령·영상 수)", "부분"), ("최근 업로드·누적 조회수", "미구현"),
                       ("썸네일 그리드 (정렬 고정)", "미구현"), ("좋아요 ♥ / 취소", "미구현")]),
    ("③ 핫구역", [("순위 리스트 (10분 업로드)", "미구현"), ("갱신 시각·카운트다운", "미구현"),
                  ("항목 탭 → 격자 상세", "미구현")]),
    ("④ 격자 상세", [("격자 표시명 '홍대입구 A-14'", "미구현"), ("행정 지역명·활동 지표", "미구현"),
                     ("격자 내 영상 목록", "미구현"), ("영상 재생 (상태 분기)", "미구현"),
                     ("인근 미방문 격자 추천", "미구현"), ("영상 신고 진입", "미구현")]),
    ("⑤ 신고 모달", [("신고 사유 선택", "미구현"), ("제출 → 접수 안내", "미구현")]),
    ("⑥ 촬영·업로드", [("촬영 (격자 내 GPS 검증)", "구현"), ("갤러리 선택 (1~30초)", "구현"),
                       ("업로드·인코딩 진행 표시", "구현"), ("AI 하이라이트 구간 조정", "미구현"),
                       ("AI 블러 확인·토글", "미구현"), ("공개 범위 선택", "미구현"),
                       ("스탬프 획득 연출 🎆", "신규"), ("영상 교체·삭제", "구현")]),
    ("⑦ 개인 도감", [("요약 (격자·영상·뱃지·스트릭)", "미구현"), ("지도 뷰 (기존 API 재사용)", "구현"),
                     ("갤러리 뷰·정렬", "미구현"), ("뱃지 뷰·필터", "미구현"),
                     ("지역별 수집률", "미구현"), ("스탬프북", "신규"), ("공개범위 설정", "미구현")]),
    ("설정·프로필", [("프로필 조회", "미구현"), ("닉네임·색상·이미지 수정", "미구현"),
                     ("로그아웃", "구현"), ("계정 삭제", "미구현")]),
]

APIS = [
    ("Auth API", "구현", [("POST /auth/signup · login", "구현"), ("POST /auth/logout", "구현"),
                          ("POST /auth/oauth/{provider}", "구현"), ("POST /auth/refresh (예정)", "미구현")]),
    ("Grid API", "구현", [("GET /api/grids (뷰포트)", "구현"), ("GET /api/grids/{gridId}", "부분")]),
    ("Grid 확장 API", "미구현", [("GET /grids/{id}/videos", "미구현"), ("GET /api/grids/hot", "미구현"),
                                 ("POST /videos/{id}/likes", "미구현"), ("DELETE /videos/{id}/likes", "미구현")]),
    ("Mission API", "신규", [("GET /api/missions/active", "신규"), ("(bbox 없음 · TTL 1h 전역 캐시)", "신규")]),
    ("Video 재생 API", "미구현", [("GET /api/videos/{videoId}", "미구현"), ("(presigned GET · 상태 분기)", "미구현")]),
    ("Social·Report API", "미구현", [("POST /api/reports", "미구현"), ("POST /friends/requests (P2)", "P2"),
                                     ("PATCH /friends/requests/{id} (P2)", "P2"), ("GET·DELETE /friends (P2)", "P2"),
                                     ("POST /friends/{id}/block (P2)", "P2")]),
    ("Video API", "구현", [("POST /videos/presigned-url", "구현"), ("POST /api/videos (점령)", "구현"),
                           ("PUT /api/videos/{videoId}", "구현"), ("DELETE /api/videos/{videoId}", "구현")]),
    ("Collection API", "미구현", [("GET /collections/summary", "미구현"), ("GET /collections/grids", "미구현"),
                                  ("GET /collections/grids/{id}/videos", "미구현"), ("GET /collections/badges", "미구현")]),
    ("Region API", "미구현", [("GET /regions/search", "미구현"), ("GET /regions/stats", "미구현"),
                              ("GET /regions/{code}", "미구현"), ("GET /regions/{code}/boundary", "미구현")]),
    ("User API", "미구현", [("GET /api/users/me", "미구현"), ("PATCH /api/users/me", "미구현"),
                            ("DELETE /api/users/me", "미구현")]),
]

SERVICES = [
    ("AuthService", "구현"), ("GridQueryService", "구현"), ("HotZoneService", "미생성"),
    ("MissionService", "신규"), ("VideoService + 인코딩 워커", "구현"), ("UserGridQueryService", "미생성"),
    ("RegionService", "미생성"), ("UserService", "미생성"), ("Social·ModerationService", "미생성"),
]

REPOS = [
    ("user", ["users"]),
    ("grid", ["grids", "user_grids"]),
    ("video", ["videos", "likes"]),
    ("region", ["regions", "region_stats"]),
    ("collection", ["badges", "user_badges", "streaks"]),
    ("social", ["friendships", "reports"]),
    ("mission (신규)", ["missions", "mission_grids", "user_missions"]),
]

LINKS = [  # 화면 → API (PRD §2)
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
API_SVC = [
    ("Auth API", "AuthService"), ("Grid API", "GridQueryService"),
    ("Grid 확장 API", "HotZoneService"), ("Grid 확장 API", "VideoService + 인코딩 워커"),
    ("Mission API", "MissionService"), ("Video 재생 API", "VideoService + 인코딩 워커"),
    ("Social·Report API", "Social·ModerationService"), ("Video API", "VideoService + 인코딩 워커"),
    ("Collection API", "UserGridQueryService"), ("Region API", "RegionService"), ("User API", "UserService"),
]
SVC_REPO = [
    ("AuthService", "user"), ("GridQueryService", "grid"), ("MissionService", "mission (신규)"),
    ("VideoService + 인코딩 워커", "video"), ("UserGridQueryService", "collection"),
    ("UserGridQueryService", "grid"), ("RegionService", "region"), ("UserService", "user"),
    ("Social·ModerationService", "social"),
]

RH, RGAP, HDRH, CGAP = 22, 5, 26, 22
X_UI, W_UI = 170, 255
X_API, W_API = 520, 255
X_SVC, W_SVC = 870, 215
X_REPO, W_REPO = 1170, 195
X_STORE = 1450
Y0 = 150

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def card(key, title, rows, x, y, w, hf, hs):
    h = HDRH + len(rows) * (RH + RGAP) + 8
    gid = nid("g")
    ids[key] = gid
    cells.append(f'<mxCell id="{gid}" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;'
                 f'fillColor=#FFFFFF;strokeColor={hs};strokeWidth=1.3;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="{nid()}" value={quoteattr(escape(title))} style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;'
                 f'fillColor={hf};strokeColor=none;fontSize=10.5;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x+4}" y="{y+3}" width="{w-8}" height="{HDRH-6}" as="geometry"/></mxCell>')
    for i, (label, st) in enumerate(rows):
        f_, s_ = ST[st]
        cells.append(f'<mxCell id="{nid()}" value={quoteattr(escape(label))} style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;'
                     f'fillColor={f_};strokeColor={s_};fontSize=9;fontColor=#2B2B2B;align=left;spacingLeft=6;" vertex="1" parent="1">'
                     f'<mxGeometry x="{x+8}" y="{y+HDRH+i*(RH+RGAP)}" width="{w-16}" height="{RH}" as="geometry"/></mxCell>')
    return h

def edge(s, t, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;", arrow="open"):
    eid = nid("e")
    edges.append(f'<mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                 f'strokeColor=#B4B9BE;strokeWidth=1;endArrow={arrow};endSize=6;{extra}" edge="1" parent="1" '
                 f'source="{ids[s]}" target="{ids[t]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# ── UI 컬럼 ──
y = Y0
for name, rows in SCREENS:
    y += card(name, name, rows, X_UI, y, W_UI, "#E8F0F8", "#4E7EA8") + CGAP
h_ui = y

# 운영자 콘솔 (UI 밴드 하단)
y_admin = h_ui + 30
card("운영자 콘솔", "운영자 콘솔 (Admin · Web)", [("신고 처리 → 블라인드", "미구현"),
     ("사용자 차단·Trust Score", "미구현"), ("통계 모니터링", "미구현"), ("미션 수동 등록", "신규")],
     X_UI, y_admin, W_UI, "#FBEBE8", "#C15848")

# ── API 컬럼 ──
y = Y0
for name, st, eps in APIS:
    f_, s_ = ST[st]
    y += card(name, f"{name}  [{st}]", eps, X_API, y, W_API, f_, s_) + CGAP
h_api = y

# ── 서비스 계약 컬럼 ──
y = Y0 + 40
for name, st in SERVICES:
    f_, s_ = ST[st]
    gid = nid("s")
    ids[name] = gid
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(name + ("  ⚠미생성" if st == "미생성" else "")))} '
                 f'style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor={f_};strokeColor={s_};strokeWidth=1.3;'
                 f'fontSize=10;fontStyle=1;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_SVC}" y="{y}" width="{W_SVC}" height="34" as="geometry"/></mxCell>')
    y += 34 + 46
h_svc = y

# ── Repository/테이블 컬럼 ──
y = Y0 + 40
for name, tables in REPOS:
    st = "신규" if "신규" in name else "미구현"
    f_, s_ = ("#FBF6E4", "#D6A34A") if st == "신규" else ("#F1F2F4", "#8A8F94")
    y += card(name, f"{name} 도메인", [(t, st if st == "신규" else "미구현") for t in tables],
              X_REPO, y, W_REPO, f_, s_) + 30
h_repo = y

# ── 저장소 실린더 ──
stores = [("PostgreSQL + PostGIS", "#dae8fc", "#6c8ebf"), ("Redis (Hot ZSET·캐시)", "#FBEBE8", "#C15848"),
          ("S3 (원본·인코딩본)", "#d5e8d4", "#82b366")]
y = Y0 + 160
for name, f_, s_ in stores:
    gid = nid("st")
    ids[name] = gid
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(name))} style="shape=cylinder3;whiteSpace=wrap;html=1;'
                 f'fillColor={f_};strokeColor={s_};strokeWidth=1.5;fontSize=10.5;fontStyle=1;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_STORE}" y="{y}" width="190" height="60" as="geometry"/></mxCell>')
    y += 130

# ── AI 처리 환경 (하단 가로 밴드) ──
y_ai = max(h_ui, h_api, h_svc, h_repo) + 90
ai_boxes = ["Kafka video.uploaded 컨슈머", "1080p·30fps 다운스케일 + FFmpeg", "PySceneDetect·CLIP 하이라이트",
            "YOLO 얼굴·차번호 블러", "pHash 중복 검사 → READY 갱신"]
aw = 230
cells.append(f'<mxCell id="aienv" value="AI 처리 환경 — 상시 Python FastAPI 서버 (ADR MSG-143 · Lambda/GPU 기각)" '
             f'style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=#F0EBF8;strokeColor=#8A6ABF;strokeWidth=1.3;'
             f'dashed=1;dashPattern=8 4;verticalAlign=top;fontStyle=1;fontSize=11;fontColor=#8A6ABF;" vertex="1" parent="1">'
             f'<mxGeometry x="{X_API}" y="{y_ai}" width="{len(ai_boxes)*(aw+16)+16}" height="96" as="geometry"/></mxCell>')
ids["AI환경"] = "aienv"
prev = None
for i, label in enumerate(ai_boxes):
    gid = nid("ai")
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(label))} style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;'
                 f'fillColor=#FFFFFF;strokeColor=#8A6ABF;fontSize=9.5;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_API+16+i*(aw+16)}" y="{y_ai+34}" width="{aw}" height="40" as="geometry"/></mxCell>')
    if prev:
        eid = nid("e")
        edges.append(f'<mxCell id="{eid}" style="html=1;strokeColor=#8A6ABF;strokeWidth=1;endArrow=block;endSize=5;" '
                     f'edge="1" parent="1" source="{prev}" target="{gid}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    prev = gid

# ── 환경 박스 (뒤에 깔기 위해 앞쪽 삽입) ──
env = []
env.append(f'<mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F2F4;strokeColor=none;" vertex="1" parent="1">'
           f'<mxGeometry x="-30" y="-40" width="{X_STORE+340}" height="{y_ai+260}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_ui" value="모바일 앱 — React Native (사용자) / Web (운영자)" '
           f'style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#4E7EA8;strokeWidth=1.3;'
           f'dashed=1;dashPattern=8 4;verticalAlign=top;fontStyle=1;fontSize=11;fontColor=#4E7EA8;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_UI-25}" y="{Y0-45}" width="{W_UI+50}" height="{y_admin - Y0 + 220}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_be" value="Spring Boot API 서버 — EC2 ×2 · Multi-AZ (SysA 8서비스)" '
           f'style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#3E9E6D;strokeWidth=1.3;'
           f'dashed=1;dashPattern=8 4;verticalAlign=top;fontStyle=1;fontSize=11;fontColor=#3E9E6D;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_API-25}" y="{Y0-45}" width="{X_REPO+W_REPO-X_API+50}" height="{max(h_api,h_svc,h_repo)-Y0+70}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_dt" value="Data Tier" '
           f'style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#6c8ebf;strokeWidth=1.3;'
           f'dashed=1;dashPattern=8 4;verticalAlign=top;fontStyle=1;fontSize=11;fontColor=#6c8ebf;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_STORE-20}" y="{Y0-45}" width="240" height="{max(h_api,h_repo)-Y0+70}" as="geometry"/></mxCell>')
env.append('<mxCell id="ttl" value="FillMap · Application Architecture (SA v2 · 2026.07)" '
           'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=16;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
           '<mxGeometry x="40" y="-10" width="700" height="26" as="geometry"/></mxCell>')
env.append('<mxCell id="sub" value="UI(IA 리프) → REST API → 서비스 계약 → Repository/테이블 → 저장소 · 행 색 = 구현 상태 (초록 구현 · 노랑 부분 · 흰 미구현 · 금색 신규 미션 · 빨강 테두리 계약 미생성)" '
           'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#6B7075;" vertex="1" parent="1">'
           '<mxGeometry x="40" y="18" width="1100" height="18" as="geometry"/></mxCell>')

# 액터
aid = nid("a")
env.append(f'<mxCell id="{aid}" value="🧑‍🎓" style="ellipse;whiteSpace=wrap;html=1;fillColor=#EAF3E2;strokeColor=#8FBF7B;'
           f'strokeWidth=1.5;fontSize=34;shadow=1;" vertex="1" parent="1">'
           f'<mxGeometry x="40" y="{Y0+250}" width="64" height="64" as="geometry"/></mxCell>')
env.append(f'<mxCell id="{nid()}" value="사용자" style="text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=11;fontStyle=1;" '
           f'vertex="1" parent="1"><mxGeometry x="22" y="{Y0+316}" width="100" height="18" as="geometry"/></mxCell>')
aid2 = nid("a")
env.append(f'<mxCell id="{aid2}" value="🧑‍💼" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F6E4DC;strokeColor=#C0684A;'
           f'strokeWidth=1.5;fontSize=34;shadow=1;" vertex="1" parent="1">'
           f'<mxGeometry x="40" y="{y_admin+20}" width="64" height="64" as="geometry"/></mxCell>')
env.append(f'<mxCell id="{nid()}" value="운영자" style="text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=11;fontStyle=1;" '
           f'vertex="1" parent="1"><mxGeometry x="22" y="{y_admin+86}" width="100" height="18" as="geometry"/></mxCell>')
edges.append(f'<mxCell id="{nid("e")}" style="html=1;strokeColor=#B4B9BE;endArrow=none;" edge="1" parent="1" '
             f'source="{aid}" target="env_ui"><mxGeometry relative="1" as="geometry"/></mxCell>')
edges.append(f'<mxCell id="{nid("e")}" style="html=1;strokeColor=#B4B9BE;endArrow=none;" edge="1" parent="1" '
             f'source="{aid2}" target="{ids["운영자 콘솔"]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

cells = env + cells

# ── 연결 ──
for s, t in LINKS:
    edge(s, t)
edge("운영자 콘솔", "Social·Report API")
edge("운영자 콘솔", "Mission API")
for s, t in API_SVC:
    edge(s, t)
for s, t in SVC_REPO:
    edge(s, t)
for r, _ in REPOS:
    edge(r, "PostgreSQL + PostGIS")
edge("HotZoneService", "Redis (Hot ZSET·캐시)", "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("Video API", "S3 (원본·인코딩본)", "exitX=1;exitY=0.2;entryX=0;entryY=1;")
edge("Video 재생 API", "S3 (원본·인코딩본)", "exitX=1;exitY=0.2;entryX=0;entryY=0.5;")
edges.append(f'<mxCell id="{nid("e")}" value="video.uploaded" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
             f'strokeColor=#8A6ABF;strokeWidth=1.2;dashed=1;endArrow=open;fontSize=9;fontColor=#8A6ABF;'
             f'exitX=0.5;exitY=1;entryX=0;entryY=0.5;" edge="1" parent="1" '
             f'source="{ids["VideoService + 인코딩 워커"]}" target="aienv"><mxGeometry relative="1" as="geometry"/></mxCell>')
edges.append(f'<mxCell id="{nid("e")}" value="인코딩본·READY" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
             f'strokeColor=#8A6ABF;strokeWidth=1.2;dashed=1;endArrow=open;fontSize=9;fontColor=#8A6ABF;'
             f'exitX=1;exitY=0.5;entryX=0.5;entryY=1;" edge="1" parent="1" '
             f'source="aienv" target="{ids["S3 (원본·인코딩본)"]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

total_w = X_STORE + 320
total_h = y_ai + 240
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="SA v2 — Application Architecture" id="sa-v2-apparch">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{total_w}" pageHeight="{total_h}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 3_FillMap_SA_v2_AppArch_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
rows = sum(len(r) for _, r in SCREENS) + sum(len(e) for _, _, e in APIS)
print(f"OK: screens={len(SCREENS)} apis={len(APIS)} svc={len(SERVICES)} repos={len(REPOS)} 행={rows} 연결={len(edges)}")
