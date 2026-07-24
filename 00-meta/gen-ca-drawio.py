#!/usr/bin/env python3
"""FillMap Cloud Architecture v2 → drawio. 흰 배경 + AWS 공식 그라데이션 아이콘 + 서브넷 중첩 + 선 점프.
실행: repo 루트에서 python3 00-meta/gen-ca-drawio.py
근거: 기존 5_final_CA (Multi-AZ·EC2×2·RDS Primary/Standby·ElastiCache·Kafka·FastAPI AI·CI/CD SSM)"""
from xml.sax.saxutils import escape, quoteattr

def q(t):
    """라벨 → XML 속성값. 이스케이프 1회, &#10;(개행)은 보존."""
    return quoteattr(t).replace('&amp;#10;', '&#10;')


# AWS 2019 카테고리 그라데이션 (fill, gradient)
CAT = {
    "net": ("#4D27AA", "#945DF2"),   # 네트워킹 (보라)
    "cmp": ("#D05C17", "#F78E04"),   # 컴퓨트 (주황)
    "db":  ("#3334B9", "#4D72F3"),   # 데이터베이스 (남보라)
    "stg": ("#277116", "#60A337"),   # 스토리지 (초록)
    "mgt": ("#BC1356", "#F34482"),   # 관리 (핑크)
    "sec": ("#C7131F", "#F54749"),   # 보안 (빨강)
}

# 선 종류
TRAFFIC = ("#232F3E", False)   # 사용자 트래픽 (진남색 실선)
DATA    = ("#6B7280", False)   # 서비스→데이터 (회색 실선)
ASYNC   = ("#8C4FFF", True)    # 비동기 이벤트 (보라 점선)
DEPLOY  = ("#BC1356", True)    # CI/CD·배포 (핑크 점선)
EXT     = ("#9AA0A6", True)    # 외부·관측 (연회색 점선)

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def aws(key, label, res, cat, x, y, s=50):
    f_, g_ = CAT[cat]
    gid = nid("i")
    ids[key] = gid
    cells.append(
        f'<mxCell id="{gid}" value={q((label))} '
        f'style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor={g_};gradientDirection=north;'
        f'fillColor={f_};strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;'
        f'html=1;fontSize=9.5;fontStyle=1;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};" '
        f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{s}" height="{s}" as="geometry"/></mxCell>')
    return gid

def grp(key, label, x, y, w, h, stroke, fill="none", dashed=0, gr=None):
    gid = nid("g")
    ids[key] = gid
    gri = f"shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr};grStroke=1;" if gr else ""
    cells.append(
        f'<mxCell id="{gid}" value={q((label))} '
        f'style="{gri}rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1.3;'
        f'dashed={dashed};verticalAlign=top;align=left;spacingLeft={30 if gr else 8};spacingTop=2;'
        f'fontSize=10.5;fontStyle=1;fontColor={stroke};" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return gid

def box(key, label, x, y, w, h, stroke="#232F3E", fill="#FFFFFF"):
    gid = nid("b")
    ids[key] = gid
    cells.append(
        f'<mxCell id="{gid}" value={q((label))} style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;'
        f'fillColor={fill};strokeColor={stroke};strokeWidth=1;fontSize=10;fontColor=#232F3E;shadow=1;" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return gid

def edge(s, t, kind, extra="", label="", points=None):
    color, dashed = kind
    eid = nid("e")
    v = f' value={q((label))}' if label else ''
    d = "dashed=1;dashPattern=5 4;" if dashed else ""
    pts = ('<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + '</Array>') if points else ''
    edges.append(
        f'<mxCell id="{eid}"{v} style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={color};'
        f'strokeWidth=1.6;endArrow=blockThin;endFill=1;endSize=5;{d}jumpStyle=arc;jumpSize=8;'
        f'fontSize=9;fontStyle=1;fontColor={color};labelBackgroundColor=#FFFFFF;{extra}" '
        f'edge="1" parent="1" source="{ids[s]}" target="{ids[t]}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')

# ── 제목 ──
cells.append('<mxCell id="ttl" value="FillMap · Cloud Architecture v2 (2026.07) — AWS ap-northeast-2 · Multi-AZ · fillmap.kr" '
             'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=17;fontStyle=1;fontColor=#232F3E;" '
             'vertex="1" parent="1"><mxGeometry x="20" y="8" width="960" height="26" as="geometry"/></mxCell>')

# ── 좌측: 액터·클라이언트 ──
for key, label, y in [("u1", "사용자", 290), ("u2", "운영자", 410)]:
    gid = nid("a")
    ids[key] = gid
    cells.append(f'<mxCell id="{gid}" value={q((label))} style="shape=umlActor;verticalLabelPosition=bottom;'
                 f'verticalAlign=top;html=1;fontSize=10;fontStyle=1;strokeColor=#232F3E;strokeWidth=1.5;" vertex="1" parent="1">'
                 f'<mxGeometry x="30" y="{y}" width="30" height="55" as="geometry"/></mxCell>')
box("client", "Mobile · Web Client&#10;(React Native · React)", 100, 325, 155, 62)
edge("u1", "client", TRAFFIC, "exitX=1;exitY=0.5;entryX=0;entryY=0.15;")
edge("u2", "client", TRAFFIC, "exitX=1;exitY=0.5;entryX=0;entryY=0.38;")

# ── AWS Cloud > Region > VPC ──
grp("cloud", "AWS Cloud", 300, 60, 1650, 1010, "#232F3E", gr="group_aws_cloud_alt")
grp("region", "Region · ap-northeast-2", 320, 100, 1340, 950, "#00A4A6", dashed=1, gr="group_region")

aws("r53", "Route 53&#10;fillmap.kr", "route_53", "net", 360, 170)
aws("cf", "CloudFront&#10;static.fillmap.kr", "cloudfront", "net", 360, 320)
aws("s3s", "S3 · 정적 웹", "s3", "stg", 360, 470)

grp("vpc", "VPC · 10.0.0.0/16", 510, 140, 1120, 890, "#8C4FFF", gr="group_vpc2")
aws("igw", "Internet&#10;Gateway", "internet_gateway", "net", 1048, 170)
# EDGE 방식: ALB는 두 AZ 사이 통로에, 서비스와 같은 높이로 → 좌우 짧은 화살표 2개
aws("waf", "AWS WAF&#10;(ALB·CloudFront)", "waf", "sec", 1048, 375)
aws("alb", "ALB&#10;(Active-Active)", "elastic_load_balancing", "net", 1048, 622)

for az, x0, tag in [("aza", 545, "가용영역 a"), ("azc", 1140, "가용영역 c")]:
    grp(az, tag, x0, 425, 460, 585, "#147EBA", dashed=1)

grp("puba", "Public subnet", 565, 455, 420, 112, "#7AA116", "#F2F6E8")
aws("nata", "NAT Gateway", "nat_gateway", "net", 730, 478)
grp("pubc", "Public subnet", 1160, 455, 420, 112, "#7AA116", "#F2F6E8")
aws("natc", "NAT Gateway", "nat_gateway", "net", 1325, 478)

# ALB 타깃(API #1)이 통로 쪽 최우측, 이벤트 흐름은 API→Kafka→AI 좌향
grp("appa", "Private subnet · App", 565, 585, 420, 225, "#00A4A6", "#E6F6F7")
aws("ai", "FastAPI&#10;AI 서버 (상시)", "ec2", "cmp", 592, 622)
aws("kafka", "Kafka&#10;(EC2)", "ec2", "cmp", 728, 622)
aws("ec2a", "Spring Boot&#10;API #1", "ec2", "cmp", 864, 622)
grp("appc", "Private subnet · App", 1160, 585, 420, 225, "#00A4A6", "#E6F6F7")
aws("ec2c", "Spring Boot&#10;API #2", "ec2", "cmp", 1190, 622)

grp("dataa", "Private subnet · Data", 565, 828, 420, 165, "#D6A34A", "#FDF6E3")
aws("rdsp", "RDS PostgreSQL&#10;+PostGIS (Primary)", "rds", "db", 592, 864)
aws("redp", "ElastiCache&#10;Redis (Primary)", "elasticache", "db", 756, 864)
grp("datac", "Private subnet · Data", 1160, 828, 420, 165, "#D6A34A", "#FDF6E3")
aws("rdss", "RDS&#10;(Standby·Read)", "rds", "db", 1190, 864)
aws("reds", "ElastiCache&#10;(Replica)", "elasticache", "db", 1354, 864)

aws("s3v", "S3&#10;영상 원본·인코딩본", "s3", "stg", 1710, 230)
aws("ecr", "ECR", "ecr", "cmp", 1710, 390)
aws("ssm", "Systems Manager&#10;(배포 Run Command)", "systems_manager", "mgt", 1710, 540)
aws("cw", "CloudWatch&#10;Logs·Metrics", "cloudwatch_2", "mgt", 1710, 700)
aws("sm", "Secrets&#10;Manager", "secrets_manager", "sec", 1710, 850)

# ── 하단: CI/CD · 외부 SaaS ──
box("gh", "GitHub · Actions&#10;(Build → Test → Push)", 100, 1110, 175, 58)
box("kakao", "카카오 OAuth", 620, 1120, 135, 46)
box("naver", "네이버 지도 SDK", 780, 1120, 135, 46)
box("fcm", "Firebase FCM (푸시)", 940, 1120, 145, 46)

# ── 연결 ──
edge("client", "r53", TRAFFIC, "exitX=1;exitY=0.3;entryX=0;entryY=0.5;", "HTTPS")
edge("r53", "cf", TRAFFIC, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("cf", "s3s", TRAFFIC, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("r53", "igw", TRAFFIC, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", "api.fillmap.kr")
edge("igw", "waf", TRAFFIC, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("waf", "alb", TRAFFIC, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("alb", "ec2a", TRAFFIC, "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
edge("alb", "ec2c", TRAFFIC, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
edge("ec2a", "rdsp", DATA, "exitX=0.3;exitY=1;entryX=0.5;entryY=0;", points=[(879, 790), (617, 790)])
edge("ec2c", "rdsp", DATA, "exitX=0.3;exitY=1;entryX=0.9;entryY=0;", points=[(1205, 818), (637, 818)])
edge("ec2a", "redp", DATA, "exitX=0.7;exitY=1;entryX=0.5;entryY=0;", points=[(899, 760), (781, 760)])
edge("ai", "rdsp", DATA, "exitX=0.3;exitY=1;entryX=0.2;entryY=0;", "READY 갱신")
edge("rdsp", "rdss", EXT, "exitX=0.5;exitY=1;entryX=0.5;entryY=1;", "복제·Failover", points=[(617, 950), (1215, 950)])
edge("redp", "reds", EXT, "exitX=0.5;exitY=1;entryX=0.5;entryY=1;", points=[(781, 968), (1379, 968)])
edge("ec2a", "kafka", ASYNC, "exitX=0;exitY=0.5;entryX=1;entryY=0.5;", "이벤트")
edge("kafka", "ai", ASYNC, "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
edge("ai", "s3v", ASYNC, "exitX=0.5;exitY=0;entryX=0;entryY=0.3;", "인코딩본")
edge("ec2a", "s3v", DATA, "exitX=0.5;exitY=0;entryX=0;entryY=0.7;", "presigned")
edge("gh", "ecr", DEPLOY, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", "Docker push", points=[(1120, 1139), (1120, 415)])
edge("ecr", "ssm", DEPLOY, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("ssm", "ec2c", DEPLOY, "exitX=0;exitY=0.5;entryX=1;entryY=0.5;", "배포", points=[(1615, 565), (1615, 647)])
edge("cw", "vpc", EXT, "exitX=0;exitY=0.5;entryX=1;entryY=0.65;", "관측")
edge("sm", "vpc", EXT, "exitX=0;exitY=0.5;entryX=1;entryY=0.85;")
edge("client", "kakao", EXT, "exitX=0;exitY=0.6;entryX=0.4;entryY=1;", "OAuth", points=[(84, 362), (84, 1196), (674, 1196)])
edge("client", "naver", EXT, "exitX=0;exitY=0.75;entryX=0.5;entryY=1;", "지도 타일", points=[(78, 371), (78, 1204), (847, 1204)])
edge("fcm", "client", EXT, "exitX=0.5;exitY=1;entryX=0;entryY=0.9;", "푸시 수신", points=[(1012, 1212), (72, 1212), (72, 381)])

# ── 범례 ──
LX, LY = 1310, 1105
cells.append(f'<mxCell id="lg" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#FFFFFF;'
             f'strokeColor=#D3D3D3;strokeWidth=1;shadow=1;" vertex="1" parent="1">'
             f'<mxGeometry x="{LX}" y="{LY}" width="620" height="72" as="geometry"/></mxCell>')
LG = [("사용자 트래픽", TRAFFIC), ("데이터 접근", DATA), ("비동기 이벤트", ASYNC), ("CI/CD·배포", DEPLOY), ("복제·외부·관측", EXT)]
for i, (name, (color, dashed)) in enumerate(LG):
    x = LX + 16 + i * 120
    d = "dashed=1;dashPattern=5 4;" if dashed else ""
    cells.append(f'<mxCell id="lgl{i}" value="" style="endArrow=blockThin;endFill=1;endSize=5;html=1;strokeColor={color};'
                 f'strokeWidth=1.6;{d}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                 f'<mxPoint x="{x}" y="{LY+26}" as="sourcePoint"/><mxPoint x="{x+46}" y="{LY+26}" as="targetPoint"/>'
                 f'</mxGeometry></mxCell>')
    cells.append(f'<mxCell id="lgt{i}" value={q((name))} style="text;html=1;strokeColor=none;fillColor=none;'
                 f'fontSize=9;fontColor=#232F3E;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x-8}" y="{LY+36}" width="110" height="16" as="geometry"/></mxCell>')

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="CA v2 — Cloud Architecture" id="ca-v2">'
       '<mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
       'arrows="1" fold="1" page="1" pageScale="1" pageWidth="2010" pageHeight="1240" math="0" shadow="0" background="#FFFFFF">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 5_FillMap_CA_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · 셀={len(cells)} 연결={len(edges)}")
