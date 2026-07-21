#!/usr/bin/env python3
"""유스케이스 다이어그램 v2 (목표 단위 세분화) → drawio.
실행: repo 루트에서 python3 00-meta/gen-usecase-drawio.py
근거: 02-planning/IA v2 초안 §2 유스케이스 세분화안"""
from xml.sax.saxutils import escape, quoteattr

# (그룹명, 테두리색, [유스케이스…]) — IA 리프(액션형)와 1:1. 표시 전용·시스템 규칙 리프는 제외
GROUPS = [
    ("계정·권한", "#6c8ebf", [
        "카카오 로그인", "Apple·로컬 로그인", "위치·카메라 권한 동의",
        "프로필 조회", "프로필 수정 (닉네임·색상·이미지)", "로그아웃", "계정 삭제"]),
    ("5초 촬영·업로드", "#d79b00", [
        "현재 위치 영상 촬영", "갤러리 영상 선택", "업로드 진행 확인",
        "AI 하이라이트 구간 조정", "AI 블러 확인·토글", "공개 범위 선택",
        "영상 교체", "영상 삭제"]),
    ("지도 탐색·시청", "#82b366", [
        "지도 이동으로 내 격자 확인", "행정동 검색", "검색 위치로 지도 이동",
        "격자 요약 확인", "격자 영상 목록 열람", "격자 상세 조회",
        "영상 재생", "영상 좋아요·취소", "미방문 격자 추천 확인", "핫구역 순위 조회"]),
    ("미션·이벤트 (신규)", "#b85450", [
        "지도에서 미션 영역 확인", "축제 칩으로 필터", "코스 칩으로 필터",
        "내 동네 채우기 보기", "미션 리스트 훑기", "미션 상세 확인",
        "미션 진행도 확인", "미션 위치로 길찾기", "미션 격자 촬영·스탬프 획득", "스탬프북 조회"]),
    ("개인 도감·게임화", "#9673a6", [
        "수집 요약 조회", "도감 지도 뷰 확인", "갤러리 열람·정렬 변경",
        "격자별 내 영상 열람", "뱃지 목록·필터 확인", "스트릭 확인",
        "지역별 수집률 조회", "도감 공개범위 변경"]),
    ("안전", "#b85450", ["영상 신고 사유 선택·제출", "신고 처리", "사용자 차단"]),
    ("운영", "#666666", ["통계 모니터링", "Trust Score 관리", "미션 수동 등록"]),
    ("소셜 (P2)", "#6c8ebf", [
        "친구 찾기", "친구 요청 보내기", "요청 수락·거절", "친구 목록·삭제", "친구 도감 보기"]),
    ("스폰서 활동 (P2)", "#6c8ebf", ["캠페인 관리", "스폰서 격자 지정", "성과 리포트 조회"]),
]

# «include»/«extend»: (from, to, label) — extend는 확장→기반 방향
RELS = [
    ("카카오 로그인", "위치·카메라 권한 동의", "include"),
    ("AI 하이라이트 구간 조정", "현재 위치 영상 촬영", "extend"),
    ("AI 블러 확인·토글", "현재 위치 영상 촬영", "extend"),
    ("미션 격자 촬영·스탬프 획득", "현재 위치 영상 촬영", "include"),
    ("검색 위치로 지도 이동", "행정동 검색", "include"),
    ("사용자 차단", "신고 처리", "extend"),
]

# 액터 → 그룹 연결
ACTORS = [
    ("사용자", 0, ["계정·권한", "5초 촬영·업로드", "지도 탐색·시청", "미션·이벤트 (신규)", "개인 도감·게임화", "안전", "소셜 (P2)"]),
    ("운영자", 1, ["안전", "운영"]),
    ("스폰서", 2, ["스폰서 활동 (P2)"]),
]

EW, EH, GX, GY = 175, 34, 14, 12      # 타원 크기·간격
COLS = 2                               # 그룹 내 타원 열 수
HDR = 30                               # 그룹 제목 높이
GW = COLS * (EW + GX) + GX             # 그룹 너비
GRID = [["계정·권한", "5초 촬영·업로드", "지도 탐색·시청"],
        ["미션·이벤트 (신규)", "개인 도감·게임화", "안전"],
        ["소셜 (P2)", "스폰서 활동 (P2)", "운영"]]
X0, Y0, GAPX, GAPY = 170, 60, 60, 50

cells, edges, nid = [], [], [0]
uc_id, grp_id, grp_pos = {}, {}, {}

def new_id(p="c"):
    nid[0] += 1
    return f"{p}{nid[0]}"

gmap = {g[0]: g for g in GROUPS}
for r, row in enumerate(GRID):
    for c, name in enumerate(row):
        if not name:
            continue
        title, color, items = gmap[name]
        rows = -(-len(items) // COLS)
        gh = HDR + rows * (EH + GY) + GY
        gx = X0 + c * (GW + GAPX)
        gy = Y0 + r * 0
        grp_pos[name] = (gx, gy, gh, rows)

# 행 높이는 그 행의 최대 그룹 높이로
row_y, y = {}, Y0
for r, row in enumerate(GRID):
    row_y[r] = y
    hmax = max(grp_pos[n][2] for n in row if n)
    y += hmax + GAPY
total_h = y

for r, row in enumerate(GRID):
    for c, name in enumerate(row):
        if not name:
            continue
        title, color, items = gmap[name]
        gx = X0 + c * (GW + GAPX)
        gy = row_y[r]
        gh = grp_pos[name][2]
        gid = new_id("g")
        grp_id[name] = gid
        cells.append(
            f'<mxCell id="{gid}" value={quoteattr(escape(title))} '
            f'style="rounded=1;whiteSpace=wrap;html=1;dashed=1;fillColor=none;strokeColor={color};'
            f'verticalAlign=top;fontStyle=1;fontSize=12;fontColor={color};" vertex="1" parent="1">'
            f'<mxGeometry x="{gx}" y="{gy}" width="{GW}" height="{gh}" as="geometry"/></mxCell>')
        for i, label in enumerate(items):
            ex = gx + GX + (i % COLS) * (EW + GX)
            ey = gy + HDR + (i // COLS) * (EH + GY)
            eid = new_id("u")
            uc_id[label] = eid
            cells.append(
                f'<mxCell id="{eid}" value={quoteattr(escape(label))} '
                f'style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333;fontSize=10;" '
                f'vertex="1" parent="1"><mxGeometry x="{ex}" y="{ey}" width="{EW}" height="{EH}" as="geometry"/></mxCell>')

# include/extend
for src, dst, kind in RELS:
    eid = new_id("e")
    edges.append(
        f'<mxCell id="{eid}" value="&#171;{kind}&#187;" '
        f'style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;strokeColor=#666666;'
        f'endArrow=open;endSize=8;fontSize=9;fontColor=#666666;" edge="1" parent="1" '
        f'source="{uc_id[src]}" target="{uc_id[dst]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# 액터 (사용자 좌중앙 / 운영자 우측 / 스폰서 좌하단)
actor_xy = {"사용자": (30, total_h * 0.35), "운영자": (X0 + 3 * (GW + GAPX) + 20, row_y[1] + 60), "스폰서": (30, row_y[2] + 60)}
for name, _, targets in ACTORS:
    ax, ay = actor_xy[name]
    aid = new_id("a")
    cells.append(
        f'<mxCell id="{aid}" value={quoteattr(escape(name))} '
        f'style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fontSize=11;fontStyle=1;" '
        f'vertex="1" parent="1"><mxGeometry x="{ax:.0f}" y="{ay:.0f}" width="30" height="60" as="geometry"/></mxCell>')
    for t in targets:
        eid = new_id("e")
        edges.append(
            f'<mxCell id="{eid}" style="rounded=0;html=1;strokeColor=#999999;endArrow=none;" '
            f'edge="1" parent="1" source="{aid}" target="{grp_id[t]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# 범례
legend = (
    '<mxCell id="lg1" value="리프 = 사용자 목표(user goal) 단위 · 실선 = 액터-에픽 · 점선 화살표 = include/extend · 빨강 테두리 = 신규(미션)·안전" '
    'style="text;html=1;fontSize=10;fontColor=#666666;" vertex="1" parent="1">'
    f'<mxGeometry x="{X0}" y="{total_h + 5}" width="900" height="20" as="geometry"/></mxCell>')

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="UseCase v2 (목표 단위)" id="usecase-v2">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="{int(total_h)+120}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges + [legend]) +
       '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 0_FillMap_UseCase_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · usecases={len(uc_id)} groups={len(grp_id)}")
