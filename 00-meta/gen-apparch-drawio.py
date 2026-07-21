#!/usr/bin/env python3
"""FillMap Application Architecture (SA v2) → drawio. EDGE 밀도 + 도메인 색 체계.
티어: 클라이언트 → REST API → 서비스 계약 → Repository → 저장소 (+ AI 처리 환경).
도메인 색이 API 카드→서비스→Repository→연결선까지 일관되게 흐른다. 행 색 = 구현 상태.
실행: repo 루트에서 python3 00-meta/gen-apparch-drawio.py
근거: PRD(cf-18972709) · API v1/v2 문서 · infrastructure 계약 · 미션 설계검토(cf-19857410) · SysA 도메인 색"""
from xml.sax.saxutils import escape, quoteattr

# 상태 (행 fill)
ST = {"구현": ("#d5e8d4", "#82b366"), "부분": ("#fff2cc", "#d6b656"),
      "미구현": ("#ffffff", "#999999"), "신규": ("#FBF6E4", "#D6A34A"),
      "미생성": ("#ffffff", "#b85450"), "P2": ("#dae8fc", "#6c8ebf")}

# 도메인 (카드 테두리·헤더 tint·연결선)
DOM = {
    "AUTH":    ("#E7F4EE", "#3E9E6D"),
    "GRID":    ("#E8F0F8", "#4E7EA8"),
    "VIDEO":   ("#FDF1DE", "#E58E1C"),
    "COLL":    ("#FBEAF3", "#D96AA1"),
    "REGION":  ("#E0F2F1", "#4A9086"),
    "SOCIAL":  ("#F0EBF8", "#8A6ABF"),
    "MISSION": ("#FBF6E4", "#D6A34A"),
    "AI":      ("#E8EAF6", "#5C6BC0"),
    "ADMIN":   ("#FBEBE8", "#C15848"),
    "SPON":    ("#EFEBE9", "#8D6E63"),
    "UI":      ("#E8F0F8", "#4E7EA8"),
}

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

# (이름, 도메인, 상태, 엔드포인트 행)
APIS = [
    ("Auth API", "AUTH", "구현", [("POST /auth/signup · login", "구현"), ("POST /auth/logout", "구현"),
                                  ("POST /auth/oauth/{provider}", "구현"), ("POST /auth/refresh (예정)", "미구현")]),
    ("Grid API", "GRID", "구현", [("GET /api/grids (뷰포트)", "구현"), ("GET /api/grids/{gridId}", "부분")]),
    ("Grid 확장 API", "GRID", "미구현", [("GET /grids/{id}/videos", "미구현"), ("GET /api/grids/hot", "미구현"),
                                         ("POST·DEL /videos/{id}/likes", "미구현")]),
    ("Mission API", "MISSION", "신규", [("GET /api/missions/active", "신규"), ("(bbox 없음 · TTL 1h 캐시)", "신규")]),
    ("Video 재생 API", "VIDEO", "미구현", [("GET /api/videos/{videoId}", "미구현"), ("(presigned GET · 상태 분기)", "미구현")]),
    ("Social·Report API", "SOCIAL", "미구현", [("POST /api/reports", "미구현"), ("POST /friends/requests (P2)", "P2"),
                                               ("PATCH /friends/requests (P2)", "P2"), ("GET·DELETE /friends (P2)", "P2"),
                                               ("POST /friends/{id}/block (P2)", "P2")]),
    ("Video API", "VIDEO", "구현", [("POST /videos/presigned-url", "구현"), ("POST /api/videos (점령)", "구현"),
                                    ("PUT /api/videos/{videoId}", "구현"), ("DELETE /api/videos/{videoId}", "구현")]),
    ("Collection API", "COLL", "미구현", [("GET /collections/summary", "미구현"), ("GET /collections/grids", "미구현"),
                                          ("GET /collections/{id}/videos", "미구현"), ("GET /collections/badges", "미구현")]),
    ("Region API", "REGION", "미구현", [("GET /regions/search", "미구현"), ("GET /regions/stats", "미구현"),
                                        ("GET /regions/{code}", "미구현"), ("GET /regions/{code}/boundary", "미구현")]),
    ("User API", "AUTH", "미구현", [("GET /api/users/me", "미구현"), ("PATCH /api/users/me", "미구현"),
                                    ("DELETE /api/users/me", "미구현")]),
    ("Sponsor API", "SPON", "P2", [("(미설계 — P2 캠페인·리포트)", "P2")]),
]

SERVICES = [
    ("AuthService", "AUTH", "구현"), ("UserService", "AUTH", "미생성"),
    ("GridQueryService", "GRID", "구현"), ("HotZoneService", "GRID", "미생성"),
    ("MissionService", "MISSION", "신규"), ("VideoService + 인코딩 워커", "VIDEO", "구현"),
    ("UserGridQueryService", "COLL", "미생성"), ("RegionService", "REGION", "미생성"),
    ("Social·ModerationService", "SOCIAL", "미생성"),
]

# (Repository 클래스, 도메인, 상태, 테이블 행)
REPOS = [
    ("UserRepository", "AUTH", "구현", ["users"]),
    ("GridRepository", "GRID", "구현", ["grids", "user_grids"]),
    ("VideoRepository", "VIDEO", "구현", ["videos", "likes"]),
    ("MissionRepository", "MISSION", "신규", ["missions", "mission_grids", "user_missions"]),
    ("RegionRepository", "REGION", "미생성", ["regions", "region_stats"]),
    ("CollectionRepository", "COLL", "미생성", ["badges", "user_badges", "streaks"]),
    ("FriendshipRepository", "SOCIAL", "미생성", ["friendships", "reports"]),
]

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
API_SVC = [
    ("Auth API", "AuthService"), ("User API", "UserService"),
    ("Grid API", "GridQueryService"), ("Grid 확장 API", "HotZoneService"),
    ("Grid 확장 API", "VideoService + 인코딩 워커"), ("Mission API", "MissionService"),
    ("Video 재생 API", "VideoService + 인코딩 워커"), ("Video API", "VideoService + 인코딩 워커"),
    ("Social·Report API", "Social·ModerationService"), ("Collection API", "UserGridQueryService"),
    ("Region API", "RegionService"),
]
SVC_REPO = [
    ("AuthService", "UserRepository"), ("UserService", "UserRepository"),
    ("GridQueryService", "GridRepository"), ("MissionService", "MissionRepository"),
    ("VideoService + 인코딩 워커", "VideoRepository"), ("UserGridQueryService", "CollectionRepository"),
    ("UserGridQueryService", "GridRepository"), ("RegionService", "RegionRepository"),
    ("Social·ModerationService", "FriendshipRepository"),
]

RH, RGAP, HDRH, CGAP = 22, 5, 26, 24
X_UI, W_UI = 190, 255
X_API, W_API = 560, 255
X_SVC, W_SVC = 930, 220
X_REPO, W_REPO = 1265, 200
X_STORE = 1580
Y0 = 170

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def card(key, title, rows, x, y, w, dom):
    hf, hs = DOM[dom]
    h = HDRH + len(rows) * (RH + RGAP) + 8
    gid = nid("g")
    ids[key] = gid
    cells.append(f'<mxCell id="{gid}" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;'
                 f'fillColor=#FFFFFF;strokeColor={hs};strokeWidth=1.5;shadow=1;" vertex="1" parent="1">'
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

def edge(s, t, color, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;", dashed=False, label=""):
    eid = nid("e")
    v = f' value={quoteattr(escape(label))}' if label else ''
    d = "dashed=1;dashPattern=6 4;" if dashed else ""
    edges.append(f'<mxCell id="{eid}"{v} style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                 f'strokeColor={color};strokeWidth=1.2;endArrow=open;endSize=6;{d}fontSize=9;fontColor={color};'
                 f'labelBackgroundColor=#FFFFFF;{extra}" edge="1" parent="1" '
                 f'source="{ids[s]}" target="{ids[t]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

api_dom = {a[0]: a[1] for a in APIS}
svc_dom = {s[0]: s[1] for s in SERVICES}
repo_dom = {r[0]: r[1] for r in REPOS}

# ── ① 클라이언트 ──
y = Y0
for name, rows in SCREENS:
    y += card(name, name, rows, X_UI, y, W_UI, "UI") + CGAP
h_ui = y
y_admin = h_ui + 40
card("운영자 콘솔", "운영자 콘솔 (Admin · Web)", [("신고 처리 → 블라인드", "미구현"),
     ("사용자 차단·Trust Score", "미구현"), ("통계 모니터링", "미구현"), ("미션 수동 등록", "신규")],
     X_UI, y_admin, W_UI, "ADMIN")
y_spon = y_admin + 190
card("스폰서 포털", "스폰서 포털 (광고주 · Web · P2)", [("캠페인 관리", "P2"),
     ("스폰서 격자 지정", "P2"), ("성과 리포트 조회", "P2")], X_UI, y_spon, W_UI, "SPON")

# ── ② REST API ──
y = Y0
for name, dom, st, eps in APIS:
    y += card(name, f"{name}  [{st}]", eps, X_API, y, W_API, dom) + CGAP
h_api = y

# ── ③ 서비스 계약 ──
y = Y0 + 30
for name, dom, st in SERVICES:
    hf, hs = DOM[dom]
    f_, s_ = ST[st]
    gid = nid("s")
    ids[name] = gid
    suffix = "  ⚠미생성" if st == "미생성" else (f"  [{st}]" if st != "구현" else "")
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(name + suffix))} '
                 f'style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor={f_ if st != "구현" else hf};'
                 f'strokeColor={hs};strokeWidth=1.5;fontSize=10;fontStyle=1;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_SVC}" y="{y}" width="{W_SVC}" height="36" as="geometry"/></mxCell>')
    y += 36 + 52
h_svc = y

# ── ④ Repository ──
y = Y0 + 30
for name, dom, st, tables in REPOS:
    y += card(name, f"{name}  [{st}]", [(t, st) for t in tables], X_REPO, y, W_REPO, dom) + 28
h_repo = y

# ── ⑤ 저장소 ──
stores = [("PostgreSQL + PostGIS", "#dae8fc", "#6c8ebf"), ("Redis (Hot ZSET·캐시)", "#FBEBE8", "#C15848"),
          ("S3 (원본·인코딩본)", "#d5e8d4", "#82b366")]
y = Y0 + 200
for name, f_, s_ in stores:
    gid = nid("st")
    ids[name] = gid
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(name))} style="shape=cylinder3;whiteSpace=wrap;html=1;'
                 f'fillColor={f_};strokeColor={s_};strokeWidth=1.5;fontSize=10.5;fontStyle=1;shadow=1;" vertex="1" parent="1">'
                 f'<mxGeometry x="{X_STORE}" y="{y}" width="195" height="64" as="geometry"/></mxCell>')
    y += 150

# ── AI 처리 환경 (하단 대형 박스, 2단 구조) ──
AIF, AIS = DOM["AI"]
y_ai = max(h_ui, h_api, h_svc, h_repo, y_spon + 160) + 70
ai_w = X_REPO + W_REPO - X_API
cells.append(f'<mxCell id="aienv" value="AI 처리 환경 — 상시 Python FastAPI 서버 · EC2 (ADR MSG-143: Lambda·GPU 기각, 1080p 다운스케일 필수 전제)" '
             f'style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor={AIF};strokeColor={AIS};strokeWidth=2;'
             f'verticalAlign=top;fontStyle=1;fontSize=12;fontColor={AIS};" vertex="1" parent="1">'
             f'<mxGeometry x="{X_API}" y="{y_ai}" width="{ai_w}" height="210" as="geometry"/></mxCell>')
ids["AI환경"] = "aienv"
row1 = ["Kafka video.uploaded 컨슈머", "1080p·30fps 다운스케일", "FFmpeg 인코딩·썸네일"]
row2 = ["PySceneDetect 장면 분할", "CLIP 하이라이트 스코어링", "YOLO 얼굴·차번호 블러", "pHash 중복 검사"]
aw1 = (ai_w - 20 - 16 * len(row1)) / len(row1)
aw2 = (ai_w - 20 - 16 * len(row2)) / len(row2)
prev = None
for r, (row, aw) in enumerate([(row1, aw1), (row2, aw2)]):
    for i, label in enumerate(row):
        gid = nid("ai")
        cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(label))} style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;'
                     f'fillColor=#FFFFFF;strokeColor={AIS};strokeWidth=1.3;fontSize=10;shadow=1;" vertex="1" parent="1">'
                     f'<mxGeometry x="{X_API+12+i*(aw+16):.0f}" y="{y_ai+40+r*66}" width="{aw:.0f}" height="44" as="geometry"/></mxCell>')
        if prev:
            eid = nid("e")
            ex = "exitX=1;exitY=0.5;entryX=0;entryY=0.5;" if i > 0 else "exitX=0;exitY=1;entryX=0;entryY=0;"
            edges.append(f'<mxCell id="{eid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={AIS};'
                         f'strokeWidth=1.2;endArrow=block;endSize=5;{ex}" edge="1" parent="1" '
                         f'source="{prev}" target="{gid}"><mxGeometry relative="1" as="geometry"/></mxCell>')
        prev = gid
ids["AI말단"] = prev
cells.append(f'<mxCell id="aiout" value="산출: 인코딩본·썸네일 → S3  ·  videos.processing_status = READY  ·  하이라이트 구간 메타" '
             f'style="text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontStyle=2;fontColor={AIS};" vertex="1" parent="1">'
             f'<mxGeometry x="{X_API+12}" y="{y_ai+178}" width="{ai_w-24}" height="18" as="geometry"/></mxCell>')

# ── 배경·환경 박스·티어 pill (뒤에 깔기) ──
env = []
total_w = X_STORE + 350
total_h = y_ai + 320
env.append(f'<mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F2F4;strokeColor=none;" vertex="1" parent="1">'
           f'<mxGeometry x="-30" y="-50" width="{total_w+120}" height="{total_h+140}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_ui" value="" style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
           f'strokeColor=#4E7EA8;strokeWidth=1.5;dashed=1;dashPattern=10 5;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_UI-28}" y="{Y0-58}" width="{W_UI+56}" height="{y_spon+180-Y0+70}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_be" value="" style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
           f'strokeColor=#3E9E6D;strokeWidth=1.5;dashed=1;dashPattern=10 5;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_API-28}" y="{Y0-58}" width="{X_REPO+W_REPO-X_API+56}" height="{max(h_api,h_svc,h_repo)-Y0+90}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="env_dt" value="" style="rounded=1;arcSize=2;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
           f'strokeColor=#6c8ebf;strokeWidth=1.5;dashed=1;dashPattern=10 5;" vertex="1" parent="1">'
           f'<mxGeometry x="{X_STORE-25}" y="{Y0-58}" width="250" height="{max(h_api,h_repo)-Y0+90}" as="geometry"/></mxCell>')

def pill(idv, text, x, w, color):
    env.append(f'<mxCell id="{idv}" value={quoteattr(escape(text))} style="rounded=1;arcSize=40;whiteSpace=wrap;html=1;'
               f'fillColor={color};strokeColor=none;fontSize=12;fontStyle=1;fontColor=#FFFFFF;" vertex="1" parent="1">'
               f'<mxGeometry x="{x}" y="{Y0-92}" width="{w}" height="26" as="geometry"/></mxCell>')

pill("p1", "① 클라이언트", X_UI - 28, 200, "#4E7EA8")
pill("p2", "② REST API", X_API - 28, 180, "#3E9E6D")
pill("p3", "③ 서비스 계약", X_SVC - 10, 180, "#E58E1C")
pill("p4", "④ Repository · 테이블", X_REPO - 10, 210, "#8A6ABF")
pill("p5", "⑤ 저장소 (Data Tier)", X_STORE - 25, 210, "#6c8ebf")
env.append('<mxCell id="ttl" value="FillMap · Application Architecture (SA v2 · 2026.07)" '
           'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=17;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
           '<mxGeometry x="30" y="-36" width="760" height="26" as="geometry"/></mxCell>')
env.append('<mxCell id="sub" value="선·카드 색 = 도메인 (Auth 초록 · Grid 파랑 · Video 주황 · Collection 분홍 · Region 청록 · Social 보라 · Mission 금색 · AI 남색) — 행 색 = 구현 상태 (초록 구현 · 노랑 부분 · 흰 미구현 · 금색 신규 · 파랑 P2 · 빨강 테두리 미생성)" '
           'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#6B7075;" vertex="1" parent="1">'
           '<mxGeometry x="30" y="-8" width="1300" height="18" as="geometry"/></mxCell>')

# 액터 3
for label, emoji, (f_, s_), ay in [("사용자", "🧑‍🎓", ("#EAF3E2", "#8FBF7B"), Y0 + 300),
                                    ("운영자", "🧑‍💼", ("#F6E4DC", "#C0684A"), y_admin + 30),
                                    ("스폰서 (광고주)", "🧑‍💼", ("#FBF6E4", "#D6A34A"), y_spon + 10)]:
    aid = nid("a")
    ids[f"actor_{label}"] = aid
    env.append(f'<mxCell id="{aid}" value={quoteattr(emoji)} style="ellipse;whiteSpace=wrap;html=1;fillColor={f_};'
               f'strokeColor={s_};strokeWidth=1.5;fontSize=34;shadow=1;" vertex="1" parent="1">'
               f'<mxGeometry x="46" y="{ay}" width="64" height="64" as="geometry"/></mxCell>')
    env.append(f'<mxCell id="{nid()}" value={quoteattr(escape(label))} style="text;html=1;strokeColor=none;fillColor=none;'
               f'align=center;fontSize=11;fontStyle=1;" vertex="1" parent="1">'
               f'<mxGeometry x="8" y="{ay+66}" width="140" height="18" as="geometry"/></mxCell>')

cells = env + cells
edges.append(f'<mxCell id="{nid("e")}" style="html=1;strokeColor=#B4B9BE;endArrow=none;" edge="1" parent="1" '
             f'source="{ids["actor_사용자"]}" target="env_ui"><mxGeometry relative="1" as="geometry"/></mxCell>')
edges.append(f'<mxCell id="{nid("e")}" style="html=1;strokeColor=#B4B9BE;endArrow=none;" edge="1" parent="1" '
             f'source="{ids["actor_운영자"]}" target="{ids["운영자 콘솔"]}"><mxGeometry relative="1" as="geometry"/></mxCell>')
edges.append(f'<mxCell id="{nid("e")}" style="html=1;strokeColor=#B4B9BE;endArrow=none;" edge="1" parent="1" '
             f'source="{ids["actor_스폰서 (광고주)"]}" target="{ids["스폰서 포털"]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# 연결 (도메인 색)
for s, t in LINKS:
    edge(s, t, DOM[api_dom[t]][1])
edge("운영자 콘솔", "Social·Report API", DOM["ADMIN"][1])
edge("운영자 콘솔", "Mission API", DOM["ADMIN"][1])
edge("스폰서 포털", "Sponsor API", DOM["SPON"][1], dashed=True, label="미설계")
for s, t in API_SVC:
    edge(s, t, DOM[svc_dom[t]][1])
for s, t in SVC_REPO:
    edge(s, t, DOM[repo_dom[t]][1])
for r, dom, _, _ in REPOS:
    edge(r, "PostgreSQL + PostGIS", DOM[dom][1])
edge("HotZoneService", "Redis (Hot ZSET·캐시)", DOM["GRID"][1])
edge("Video API", "S3 (원본·인코딩본)", DOM["VIDEO"][1], "exitX=1;exitY=0.2;entryX=0;entryY=1;")
edge("Video 재생 API", "S3 (원본·인코딩본)", DOM["VIDEO"][1], "exitX=1;exitY=0.2;entryX=0;entryY=0.5;")
edge("VideoService + 인코딩 워커", "AI환경", DOM["AI"][1], "exitX=0.5;exitY=1;entryX=0.3;entryY=0;", dashed=True, label="Kafka video.uploaded")
edge("AI환경", "S3 (원본·인코딩본)", DOM["AI"][1], "exitX=1;exitY=0.3;entryX=0.5;entryY=1;", dashed=True, label="인코딩본·썸네일")
edge("AI환경", "PostgreSQL + PostGIS", DOM["AI"][1], "exitX=1;exitY=0.15;entryX=0.3;entryY=1;", dashed=True, label="READY 갱신")

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
print(f"OK: screens={len(SCREENS)}+콘솔2 apis={len(APIS)} svc={len(SERVICES)} repos={len(REPOS)} 연결={len(edges)}")
