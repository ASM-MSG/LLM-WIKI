#!/usr/bin/env python3
"""FillMap System Architecture v2 (논리 뷰) → drawio. EDGE 3번 장 스타일: 기술명 없이 역할 그룹만.
기술 선택·구현 상태는 SA v2(Application Architecture)·CA(물리 배치)가 담당한다.
실행: repo 루트에서 python3 00-meta/gen-sysa-drawio.py
근거: SysA v4(8서비스·데이터 계층) · 미션 설계검토(cf-19857410) · ADR MSG-143"""
from xml.sax.saxutils import escape, quoteattr

def q(t):
    """라벨 → XML 속성값. 이스케이프 1회, &#10;(개행)은 보존."""
    return quoteattr(t).replace('&amp;#10;', '&#10;')


GOLD = "#D6A34A"      # 신규(미션) 강조
INK = "#333333"
GRAYS = "#8A8F94"

# (그룹명, x, y, w, 박스 [ (이름, 신규여부) ], cols)
# 좌표는 아래에서 계산 — 여기선 내용만
CLIENTS = [("Mobile App (사용자)", 0), ("Web App (사용자)", 0), ("Admin Console (운영자)", 0), ("Sponsor Portal (광고주·P2)", 0)]
# 배치 원칙: 오른쪽(캐시·데이터)으로 선이 나가는 박스는 맨 오른쪽 열(c2)에 — 같은 행 박스 관통 방지
SERVICES = [("Auth Service", 0), ("Social Service", 0), ("Collection Service", 0),
            ("Region Service", 0), ("Moderation Service", 0), ("Grid Service", 0),
            ("Notification Service", 0), ("Video Service", 0), ("Mission Service", 1)]
CACHES = [("Token Cache", 0), ("Hot Zone Cache", 0), ("Mission Cache", 1)]
# 트리거 경로별 분리: Event Queue → 이벤트 소비형 · Batch Scheduler → 주기 실행형
EVENT_WORKERS = [("Encoding Worker", 0), ("AI Highlight·Blur Worker", 0)]
BATCH_WORKERS = [("Badge·Streak Batch Worker", 0), ("Region Stats Batch Worker", 0),
                 ("Mission Sync Worker (축제·코스)", 1)]
EXTERNALS = [("OAuth 제공자", 0), ("지도 타일 제공자", 0), ("푸시 게이트웨이", 0)]

BW, BH, GPAD, GHDR, BGAP = 190, 36, 14, 30, 12

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def box(key, label, x, y, w=BW, h=BH, new=False, shape=None):
    gid = nid("b")
    ids[key] = gid
    stroke = GOLD if new else INK
    extra = "strokeWidth=1.5;" if new else "strokeWidth=1;"
    shp = f"shape={shape};" if shape else ""
    cells.append(f'<mxCell id="{gid}" value={q((label))} style="{shp}rounded=0;whiteSpace=wrap;html=1;'
                 f'fillColor=#FFFFFF;strokeColor={stroke};{extra}fontSize=10.5;fontColor=#2B2B2B;shadow=0;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return gid

def group(key, title, x, y, w, h):
    gid = nid("grp")
    ids[key] = gid
    cells.append(f'<mxCell id="{gid}" value={q((title))} style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;'
                 f'fillColor=none;strokeColor={GRAYS};strokeWidth=1.2;dashed=1;dashPattern=6 4;'
                 f'verticalAlign=top;align=left;spacingLeft=8;fontStyle=1;fontSize=11;fontColor=#5B6066;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
    return gid

def vgroup(key, title, x, y, items, w=BW + 2 * GPAD):
    h = GHDR + len(items) * (BH + BGAP) + GPAD - BGAP + GPAD
    group(key, title, x, y, w, h)
    for i, (name, new) in enumerate(items):
        box(name, name, x + GPAD, y + GHDR + i * (BH + BGAP), new=bool(new))
    return h

def edge(s, t, extra="exitX=1;exitY=0.5;entryX=0;entryY=0.5;", dashed=False, label="", color="#6B7075", points=None):
    eid = nid("e")
    v = f' value={q((label))}' if label else ''
    d = "dashed=1;dashPattern=5 4;" if dashed else ""
    pts = ('<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + '</Array>') if points else ''
    edges.append(f'<mxCell id="{eid}"{v} style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                 f'strokeColor={color};strokeWidth=1;endArrow=open;endSize=6;{d}jumpStyle=arc;jumpSize=8;'
                 f'fontSize=9;fontColor={color};'
                 f'labelBackgroundColor=#FFFFFF;{extra}" edge="1" parent="1" '
                 f'source="{ids[s]}" target="{ids[t]}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')

Y0 = 90

# ── Client ──
h_cli = vgroup("Client", "Client", 40, Y0, CLIENTS)

# ── Gateway ──
group("GatewayG", "Gateway", 330, Y0 + 60, BW + 2 * GPAD, GHDR + BH + 2 * GPAD)
box("API Gateway", "API Gateway", 330 + GPAD, Y0 + 60 + GHDR, )

# ── Service (3×3) ──
SX, SY = 630, Y0
scols = 3
sw = scols * (BW + BGAP) - BGAP + 2 * GPAD
srows = -(-len(SERVICES) // scols)
sh = GHDR + srows * (BH + BGAP) - BGAP + 2 * GPAD
group("ServiceG", "Service", SX, SY, sw, sh)
for i, (name, new) in enumerate(SERVICES):
    box(name, name, SX + GPAD + (i % scols) * (BW + BGAP), SY + GHDR + (i // scols) * (BH + BGAP), new=bool(new))

# ── Message Queue (Video Service(c1) 바로 아래 — 업로드 이벤트 수직 직결) ──
QY = SY + sh + 40
QX = SX + BW + BGAP
group("QueueG", "Message Queue", QX, QY, BW + 2 * GPAD, GHDR + BH + 2 * GPAD)
box("Event Queue", "Event Queue", QX + GPAD, QY + GHDR)

# ── Scheduler (Queue 옆) ──
SCX = QX + BW + 2 * GPAD + 30
group("SchedG", "Scheduler", SCX, QY, BW + 2 * GPAD, GHDR + BH + 2 * GPAD)
box("Batch Scheduler", "Batch Scheduler", SCX + GPAD, QY + GHDR)

# ── Worker (하단, 트리거 경로별 2그룹: Queue 아래 이벤트형 · Scheduler 아래 배치형) ──
WY = QY + GHDR + BH + 2 * GPAD + 40
evw = 2 * (BW + BGAP) - BGAP + 2 * GPAD
group("EventWorkerG", "Worker · Event-driven", SX, WY, evw, GHDR + BH + 2 * GPAD)
for i, (name, new) in enumerate(EVENT_WORKERS):
    box(name, name, SX + GPAD + i * (BW + BGAP), WY + GHDR, new=bool(new))
BWX = 1090
wh = GHDR + 2 * (BH + BGAP) - BGAP + 2 * GPAD
group("BatchWorkerG", "Worker · Batch", BWX, WY, evw, wh)
for i, (name, new) in enumerate(BATCH_WORKERS):
    box(name, name, BWX + GPAD + (i % 2) * (BW + BGAP), WY + GHDR + (i // 2) * (BH + BGAP), new=bool(new))

# ── Cache (Service 오른쪽) ──
CX = SX + sw + 60
h_cache = vgroup("CacheG", "Cache", CX, Y0, CACHES)

# ── Data (맨 오른쪽) ──
DX = CX + BW + 2 * GPAD + 60
group("DataG", "Data", DX, Y0, BW + 2 * GPAD, GHDR + 2 * (56 + BGAP) + GPAD)
box("Main Database", "Main Database&#10;(관계형 · 공간 질의)", DX + GPAD, Y0 + GHDR, h=56, shape="cylinder3")
box("Object Storage", "Object Storage&#10;(원본·인코딩 영상)", DX + GPAD, Y0 + GHDR + 56 + BGAP, h=56, shape="cylinder3")

# ── External (Client 아래) ──
EY = Y0 + h_cli + 50
h_ext = vgroup("ExternalG", "External", 40, EY, EXTERNALS)

# ── 연결 ──
for name, _ in CLIENTS:
    edge(name, "API Gateway")
edge("API Gateway", "ServiceG")
edge("ServiceG", "Main Database", "exitX=1;exitY=0.1;entryX=0.5;entryY=0;", points=[(1699, 109)])
edge("Grid Service", "Hot Zone Cache")
edge("Auth Service", "Token Cache", "exitX=0.7;exitY=0;entryX=0.5;entryY=0;", points=[(777, 66), (1421, 66)])
edge("Mission Service", "Mission Cache", color=GOLD)
edge("Video Service", "Object Storage", "exitX=0.8;exitY=1;entryX=0.5;entryY=1;", points=[(998, 300), (1699, 300)])
edge("Video Service", "Event Queue", "exitX=0.3;exitY=1;entryX=0.5;entryY=0;", dashed=True, label="업로드 이벤트")
edge("Event Queue", "AI Highlight·Blur Worker", "exitX=0.5;exitY=1;entryX=0.5;entryY=0;", dashed=True)
edge("Event Queue", "Encoding Worker", "exitX=0.2;exitY=1;entryX=0.5;entryY=0;", dashed=True)
edge("Batch Scheduler", "BatchWorkerG", "exitX=0.5;exitY=1;entryX=0.24;entryY=0;", dashed=True, label="주기 실행")
edge("BatchWorkerG", "Main Database", "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(1840, 525), (1840, 148)])
edge("AI Highlight·Blur Worker", "Object Storage", "exitX=0.5;exitY=1;entryX=0;entryY=0.9;", dashed=True, points=[(941, 616), (1560, 616), (1560, 238)])
edge("Auth Service", "OAuth 제공자", "exitX=0;exitY=0.5;entryX=1;entryY=0.2;", dashed=True)
edge("Mobile App (사용자)", "지도 타일 제공자", "exitX=0;exitY=0.5;entryX=0;entryY=0;", dashed=True)
edge("Notification Service", "푸시 게이트웨이", "exitX=0;exitY=1;entryX=1;entryY=0.5;", dashed=True)

# ── 배경·헤더 (뒤에 깔기) ──
total_w = DX + BW + 2 * GPAD + 60
total_h = WY + wh + 80
env = []
env.append(f'<mxCell id="bg" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F2F4;strokeColor=none;" vertex="1" parent="1">'
           f'<mxGeometry x="-30" y="-70" width="{total_w+120}" height="{total_h+150}" as="geometry"/></mxCell>')
env.append(f'<mxCell id="frame" value="" style="rounded=1;arcSize=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
           f'strokeColor={GRAYS};strokeWidth=1;" vertex="1" parent="1">'
           f'<mxGeometry x="10" y="{Y0-50}" width="{total_w}" height="{total_h}" as="geometry"/></mxCell>')
env.append('<mxCell id="ttl" value="FillMap · System Architecture v2 — 논리 뷰 (2026.07)" '
           'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=16;fontStyle=1;fontColor=#2B2B2B;" vertex="1" parent="1">'
           '<mxGeometry x="30" y="-46" width="700" height="26" as="geometry"/></mxCell>')
env.append(f'<mxCell id="sub" value="역할(Client·Gateway·Service·Cache·Queue·Worker·Scheduler·Data)만 표기 — 기술 선택·구현 상태는 SA v2와 CA가 담당 · 금색 = 신규 미션 도메인" '
           f'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#6B7075;" vertex="1" parent="1">'
           f'<mxGeometry x="30" y="-18" width="1100" height="18" as="geometry"/></mxCell>')
cells[:0] = env

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="SysA v2 — 논리 뷰" id="sysa-v2">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{total_w+100}" pageHeight="{total_h+160}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 4_FillMap_SysA_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · 박스={len(cells)} 연결={len(edges)}")
