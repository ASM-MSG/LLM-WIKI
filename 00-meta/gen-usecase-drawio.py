#!/usr/bin/env python3
"""유스케이스 다이어그램 v2 (IA 리프 1:1 · 56개) → drawio. 원본 0_FillMap_UseCase 스타일.
실행: repo 루트에서 python3 00-meta/gen-usecase-drawio.py
근거: 02-planning/IA v2 초안 §2 (멘토 피드백: 에픽 ≠ 유스케이스)"""
from xml.sax.saxutils import escape, quoteattr

# 원본 팔레트: (연한 fill, stroke)
BLUE   = ("#E8F0F8", "#4E7EA8")
ORANGE = ("#FDF1DE", "#E58E1C")
GREEN  = ("#E7F4EE", "#3E9E6D")
GOLD   = ("#FBF6E4", "#D6A34A")
PINK   = ("#FBEAF3", "#D96AA1")
RED    = ("#FBEBE8", "#C15848")
PURPLE = ("#F0EBF8", "#8A6ABF")
GRAY   = ("#F5F5F5", "#6B7075")

# (그룹명, 색, [유스케이스…]) — IA 리프(액션형)와 1:1. 표시 전용·시스템 규칙 리프 제외
GROUPS = [
    ("계정·권한", BLUE, [
        "카카오 로그인", "Apple·로컬 로그인", "위치·카메라 권한 동의",
        "프로필 조회", "프로필 수정 (닉네임·색상·이미지)", "로그아웃", "계정 삭제"]),
    ("5초 촬영·업로드", ORANGE, [
        "현재 위치 영상 촬영", "갤러리 영상 선택", "업로드 진행 확인",
        "AI 하이라이트 구간 조정", "AI 블러 확인·토글", "공개 범위 선택",
        "영상 교체", "영상 삭제"]),
    ("지도 탐색·시청", GREEN, [
        "지도 이동으로 내 격자 확인", "행정동 검색", "검색 위치로 지도 이동",
        "격자 요약 확인", "격자 영상 목록 열람", "격자 상세 조회",
        "영상 재생", "영상 좋아요·취소", "미방문 격자 추천 확인", "핫구역 순위 조회"]),
    ("미션·이벤트 (신규)", GOLD, [
        "지도에서 미션 영역 확인", "축제 칩으로 필터", "코스 칩으로 필터",
        "내 동네 채우기 보기", "미션 리스트 훑기", "미션 상세 확인",
        "미션 진행도 확인", "미션 격자 촬영·스탬프 획득", "스탬프북 조회"]),
    ("개인 도감·게임화", PINK, [
        "수집 요약 조회", "도감 지도 뷰 확인", "갤러리 열람·정렬 변경",
        "격자별 내 영상 열람", "뱃지 목록·필터 확인", "스트릭 확인",
        "지역별 수집률 조회", "도감 공개범위 변경"]),
    ("안전", RED, ["영상 신고 사유 선택·제출", "신고 처리", "사용자 차단"]),
    ("운영", PURPLE, ["통계 모니터링", "Trust Score 관리", "미션 수동 등록"]),
    ("소셜 (P2)", GRAY, [
        "친구 찾기", "친구 요청 보내기", "요청 수락·거절", "친구 목록·삭제", "친구 도감 보기"]),
    ("스폰서 활동 (P2)", GRAY, ["캠페인 관리", "스폰서 격자 지정", "성과 리포트 조회"]),
]

# «include»/«extend»: (from, to, kind) — extend는 확장→기반 방향
RELS = [
    ("카카오 로그인", "위치·카메라 권한 동의", "include"),
    ("AI 하이라이트 구간 조정", "현재 위치 영상 촬영", "extend"),
    ("AI 블러 확인·토글", "현재 위치 영상 촬영", "extend"),
    ("미션 격자 촬영·스탬프 획득", "현재 위치 영상 촬영", "include"),
    ("검색 위치로 지도 이동", "행정동 검색", "include"),
    ("사용자 차단", "신고 처리", "extend"),
]

# (액터명, 이모지, 색, 연결 그룹)
ACTORS = [
    ("사용자", "🧑‍🎓", ("#EAF3E2", "#8FBF7B"),
     ["계정·권한", "5초 촬영·업로드", "지도 탐색·시청", "미션·이벤트 (신규)", "개인 도감·게임화", "안전", "소셜 (P2)"]),
    ("운영자", "🧑‍💼", ("#F6E4DC", "#C0684A"), ["안전", "운영"]),
    ("스폰서", "🧑‍💼", ("#FBF6E4", "#D6A34A"), ["스폰서 활동 (P2)"]),
]

GRID = [["계정·권한", "5초 촬영·업로드", "지도 탐색·시청"],
        ["미션·이벤트 (신규)", "개인 도감·게임화", "안전"],
        ["소셜 (P2)", "스폰서 활동 (P2)", "운영"]]

EW, EH, GX, GY = 168, 40, 16, 14
COLS = 2
HDR = 26
GW = COLS * (EW + GX) + GX
X0, Y0, GAPX, GAPY = 200, 140, 70, 60

cells, edges, nid = [], [], [0]
uc_id, grp_id = {}, {}
gmap = {g[0]: g for g in GROUPS}

def new_id(p="c"):
    nid[0] += 1
    return f"{p}{nid[0]}"

def add(s):
    cells.append(s)

# 행 y 좌표 (행 높이 = 그 행 그룹 최대 높이)
def g_height(name):
    rows = -(-len(gmap[name][2]) // COLS)
    return HDR + rows * (EH + GY) + GY

row_y, y = {}, Y0
for r, row in enumerate(GRID):
    row_y[r] = y
    y += max(g_height(n) for n in row if n) + GAPY
total_h = y
total_w = X0 + 3 * (GW + GAPX) - GAPX + 40

# ── 배경·헤더 (원본과 동일 구성) ──
add(f'<mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F2F4;strokeColor=none;" vertex="1" parent="1">'
    f'<mxGeometry x="-40" y="-40" width="{total_w+140}" height="{total_h+220}" as="geometry"/></mxCell>')
add(f'<mxCell id="frame" value="" style="rounded=1;arcSize=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#8A8F94;strokeWidth=1;" vertex="1" parent="1">'
    f'<mxGeometry x="0" y="60" width="{total_w+60}" height="{total_h+60}" as="geometry"/></mxCell>')
add('<mxCell id="ttl" value="FillMap · 유즈케이스 다이어그램 v2 (2026.07 · IA 리프 1:1)" '
    'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=15;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
    '<mxGeometry x="0" y="0" width="620" height="24" as="geometry"/></mxCell>')
add('<mxCell id="sub" value="액터 · 유즈케이스 · 관계 (include / extend) — 에픽은 그룹 박스, 유즈케이스는 IA 리프 단위" '
    'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#6B7075;" vertex="1" parent="1">'
    '<mxGeometry x="0" y="26" width="700" height="18" as="geometry"/></mxCell>')

# ── 그룹 + 타원 ──
for r, row in enumerate(GRID):
    for c, name in enumerate(row):
        if not name:
            continue
        _, (fill, stroke), items = gmap[name]
        gx = X0 + c * (GW + GAPX)
        gy = row_y[r]
        gh = g_height(name)
        gid = new_id("g")
        grp_id[name] = gid
        add(f'<mxCell id="{gid}" value="" style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor={fill};'
            f'strokeColor={stroke};strokeWidth=1.3;dashed=1;dashPattern=8 4;" vertex="1" parent="1">'
            f'<mxGeometry x="{gx}" y="{gy}" width="{GW}" height="{gh}" as="geometry"/></mxCell>')
        tid = new_id("t")
        add(f'<mxCell id="{tid}" value={quoteattr(escape(name))} '
            f'style="text;html=1;strokeColor=none;fillColor=#F1F2F4;align=center;verticalAlign=middle;'
            f'fontSize=11;fontStyle=1;fontColor={stroke};spacingLeft=8;spacingRight=8;" vertex="1" parent="1">'
            f'<mxGeometry x="{gx+12}" y="{gy-10}" width="{max(96, len(name)*11+16)}" height="20" as="geometry"/></mxCell>')
        for i, label in enumerate(items):
            ex = gx + GX + (i % COLS) * (EW + GX)
            ey = gy + HDR + (i // COLS) * (EH + GY)
            eid = new_id("u")
            uc_id[label] = eid
            add(f'<mxCell id="{eid}" value={quoteattr(escape(label))} '
                f'style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1.5;'
                f'fontSize=10.5;fontColor=#2B2B2B;fontStyle=1;align=center;verticalAlign=middle;shadow=1;" '
                f'vertex="1" parent="1"><mxGeometry x="{ex}" y="{ey}" width="{EW}" height="{EH}" as="geometry"/></mxCell>')

# ── include / extend ──
for src, dst, kind in RELS:
    eid = new_id("e")
    edges.append(
        f'<mxCell id="{eid}" value="&#171;{kind}&#187;" '
        f'style="endArrow=open;endFill=0;endSize=8;html=1;strokeColor=#7F868E;strokeWidth=1;dashed=1;dashPattern=6 4;'
        f'fontSize=9;fontStyle=2;fontColor=#6B7075;labelBackgroundColor=#F1F2F4;" edge="1" parent="1" '
        f'source="{uc_id[src]}" target="{uc_id[dst]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# ── 액터 (이모지 원 + 라벨) ──
actor_xy = {"사용자": (60, row_y[0] + 160),
            "운영자": (X0 + 3 * (GW + GAPX) - GAPX + 60, row_y[1] + 40),
            "스폰서": (60, row_y[2] + 40)}
for name, emoji, (fill, stroke), targets in ACTORS:
    ax, ay = actor_xy[name]
    aid = new_id("a")
    add(f'<mxCell id="{aid}" value={quoteattr(emoji)} '
        f'style="ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1.5;fontSize=34;shadow=1;" '
        f'vertex="1" parent="1"><mxGeometry x="{ax:.0f}" y="{ay:.0f}" width="64" height="64" as="geometry"/></mxCell>')
    add(f'<mxCell id="{aid}l" value={quoteattr(escape(name))} '
        f'style="text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=11;fontStyle=1;fontColor=#2B2B2B;" '
        f'vertex="1" parent="1"><mxGeometry x="{ax-18:.0f}" y="{ay+66:.0f}" width="100" height="18" as="geometry"/></mxCell>')
    for t in targets:
        eid = new_id("e")
        edges.append(
            f'<mxCell id="{eid}" style="endArrow=none;html=1;strokeColor=#B4B9BE;strokeWidth=1;edgeStyle=none;rounded=0;" '
            f'edge="1" parent="1" source="{aid}" target="{grp_id[t]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# ── 범례 ──
lx, ly = X0, total_h + 10
add(f'<mxCell id="lgbox" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#D3D3D3;strokeWidth=1;shadow=1;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx}" y="{ly}" width="760" height="66" as="geometry"/></mxCell>')
add(f'<mxCell id="lg_a" value="🧑‍🎓" style="ellipse;whiteSpace=wrap;html=1;fillColor=#EAF3E2;strokeColor=#8FBF7B;strokeWidth=1.5;fontSize=18;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx+16}" y="{ly+16}" width="34" height="34" as="geometry"/></mxCell>')
add(f'<mxCell id="lg_a2" value="액터" style="text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontColor=#2B2B2B;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx+54}" y="{ly+24}" width="40" height="18" as="geometry"/></mxCell>')
add(f'<mxCell id="lg_u" value="유즈케이스 (IA 리프)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6B7075;strokeWidth=1.5;fontSize=9;fontStyle=1;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx+110}" y="{ly+16}" width="130" height="34" as="geometry"/></mxCell>')
add(f'<mxCell id="lg_g" value="에픽 그룹" style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=#E7F4EE;strokeColor=#3E9E6D;'
    f'strokeWidth=1.3;dashed=1;dashPattern=8 4;fontSize=9;fontColor=#3E9E6D;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx+260}" y="{ly+16}" width="90" height="34" as="geometry"/></mxCell>')
add(f'<mxCell id="lg_l" value="─ 액터 참여 · ┄&#62; include/extend · 회색 그룹 = Phase 2" '
    f'style="text;html=1;strokeColor=none;fillColor=none;fontSize=10;fontColor=#6B7075;" '
    f'vertex="1" parent="1"><mxGeometry x="{lx+370}" y="{ly+24}" width="380" height="18" as="geometry"/></mxCell>')

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="UseCase v2 (IA 리프 1:1)" id="usecase-v2">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{total_w+160}" pageHeight="{total_h+260}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 0_FillMap_UseCase_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · usecases={len(uc_id)} groups={len(grp_id)}")
