#!/usr/bin/env python3
"""FillMap Cloud Architecture v2 → drawio. EDGE 4번 장 스타일: 흰 배경 + AWS 공식 아이콘 + VPC/서브넷 중첩.
실행: repo 루트에서 python3 00-meta/gen-ca-drawio.py
근거: 기존 5_final_CA (Multi-AZ·EC2×2·RDS Primary/Standby·ElastiCache·Kafka·FastAPI AI·CI/CD SSM)"""
from xml.sax.saxutils import escape, quoteattr

cells, edges, n = [], [], [0]
ids = {}

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def aws(key, label, res, color, x, y, s=46):
    gid = nid("i")
    ids[key] = gid
    cells.append(
        f'<mxCell id="{gid}" value={quoteattr(escape(label))} '
        f'style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor={color};strokeColor=#ffffff;'
        f'dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=9.5;aspect=fixed;'
        f'shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{res};" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{s}" height="{s}" as="geometry"/></mxCell>')
    return gid

def grp(key, label, x, y, w, h, stroke, fill="none", dashed=0, gr=None, fc=None):
    gid = nid("g")
    ids[key] = gid
    gri = f"shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.{gr};grStroke=1;" if gr else ""
    cells.append(
        f'<mxCell id="{gid}" value={quoteattr(escape(label))} '
        f'style="{gri}rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=1.2;'
        f'dashed={dashed};verticalAlign=top;align=left;spacingLeft={30 if gr else 8};spacingTop=2;'
        f'fontSize=10.5;fontStyle=1;fontColor={fc or stroke};" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return gid

def box(key, label, x, y, w, h, stroke="#232F3E", fill="#FFFFFF"):
    gid = nid("b")
    ids[key] = gid
    cells.append(
        f'<mxCell id="{gid}" value={quoteattr(escape(label))} style="rounded=0;whiteSpace=wrap;html=1;'
        f'fillColor={fill};strokeColor={stroke};strokeWidth=1;fontSize=10;fontColor=#232F3E;" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return gid

def edge(s, t, extra="", dashed=False, label="", color="#545B64"):
    eid = nid("e")
    v = f' value={quoteattr(escape(label))}' if label else ''
    d = "dashed=1;dashPattern=4 4;" if dashed else ""
    edges.append(
        f'<mxCell id="{eid}"{v} style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={color};'
        f'strokeWidth=1;endArrow=open;endSize=6;{d}fontSize=9;fontColor=#545B64;labelBackgroundColor=#FFFFFF;{extra}" '
        f'edge="1" parent="1" source="{ids[s]}" target="{ids[t]}"><mxGeometry relative="1" as="geometry"/></mxCell>')

NET, CMP, DB, STG, MGT, SEC = "#8C4FFF", "#ED7100", "#C925D1", "#7AA116", "#E7157B", "#DD344C"

# ── 제목 (흰 배경 — bg 없음) ──
cells.append('<mxCell id="ttl" value="FillMap · Cloud Architecture v2 (2026.07) — AWS ap-northeast-2 · Multi-AZ · fillmap.kr" '
             'style="text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=16;fontStyle=1;fontColor=#232F3E;" '
             'vertex="1" parent="1"><mxGeometry x="20" y="10" width="900" height="26" as="geometry"/></mxCell>')

# ── 좌측: 액터·클라이언트 ──
for key, label, y in [("u1", "사용자", 300), ("u2", "운영자", 420)]:
    gid = nid("a")
    ids[key] = gid
    cells.append(f'<mxCell id="{gid}" value={quoteattr(escape(label))} style="shape=umlActor;verticalLabelPosition=bottom;'
                 f'verticalAlign=top;html=1;fontSize=10;strokeColor=#232F3E;" vertex="1" parent="1">'
                 f'<mxGeometry x="30" y="{y}" width="28" height="52" as="geometry"/></mxCell>')
box("client", "Mobile · Web Client&#10;(React Native · React)", 100, 330, 150, 60)
edge("u1", "client", "exitX=1;exitY=0.5;entryX=0;entryY=0.3;")
edge("u2", "client", "exitX=1;exitY=0.5;entryX=0;entryY=0.8;")

# ── AWS Cloud > Region > VPC ──
grp("cloud", "AWS Cloud", 300, 60, 1560, 1000, "#232F3E", gr="group_aws_cloud_alt")
grp("region", "Region · ap-northeast-2", 320, 100, 1250, 940, "#00A4A6", dashed=1, gr="group_region")

# 엣지 서비스 (VPC 밖, Region 안)
aws("r53", "Route 53&#10;fillmap.kr", "route_53", NET, 360, 160)
aws("cf", "CloudFront&#10;static.fillmap.kr", "cloudfront", NET, 360, 300)
aws("s3s", "S3&#10;정적 웹", "simple_storage_service", STG, 360, 440)

grp("vpc", "VPC · 10.0.0.0/16", 500, 140, 1040, 880, "#8C4FFF", gr="group_vpc2")
aws("igw", "Internet&#10;Gateway", "internet_gateway", NET, 980, 170)
aws("alb", "ALB&#10;(Active-Active)", "elastic_load_balancing", NET, 980, 300)

# AZ 2개
for az, x0, tag in [("aza", 540, "AZ a (ap-northeast-2a)"), ("azc", 1060, "AZ c (ap-northeast-2c)")]:
    grp(az, tag, x0, 420, 450, 580, "#147EBA", dashed=1)

# Public subnet (NAT)
grp("puba", "Public subnet", 560, 450, 410, 110, "#7AA116", "#F2F6E8")
aws("nata", "NAT Gateway", "nat_gateway", NET, 720, 470)
grp("pubc", "Public subnet", 1080, 450, 410, 110, "#7AA116", "#F2F6E8")
aws("natc", "NAT Gateway", "nat_gateway", NET, 1240, 470)

# App private subnet
grp("appa", "Private subnet · App", 560, 580, 410, 220, "#00A4A6", "#E6F6F7")
aws("ec2a", "Spring Boot&#10;API 서버 #1", "ec2", CMP, 585, 615)
aws("ai", "FastAPI&#10;AI 서버 (상시)", "ec2", CMP, 715, 615)
aws("kafka", "Kafka&#10;(EC2)", "ec2", CMP, 845, 615)
grp("appc", "Private subnet · App", 1080, 580, 410, 220, "#00A4A6", "#E6F6F7")
aws("ec2c", "Spring Boot&#10;API 서버 #2", "ec2", CMP, 1110, 615)

# Data private subnet
grp("dataa", "Private subnet · Data", 560, 820, 410, 160, "#D6A34A", "#FDF6E3")
aws("rdsp", "RDS PostgreSQL&#10;+PostGIS (Primary)", "rds", DB, 585, 855)
aws("redp", "ElastiCache&#10;Redis (Primary)", "elasticache", DB, 745, 855)
grp("datac", "Private subnet · Data", 1080, 820, 410, 160, "#D6A34A", "#FDF6E3")
aws("rdss", "RDS&#10;(Standby·Read)", "rds", DB, 1110, 855)
aws("reds", "ElastiCache&#10;(Replica)", "elasticache", DB, 1270, 855)

# 공용 서비스 (Region 안 우측)
aws("s3v", "S3&#10;영상 원본·인코딩본", "simple_storage_service", STG, 1620, 220)
aws("ecr", "ECR", "elastic_container_registry", CMP, 1620, 380)
aws("ssm", "Systems Manager&#10;(배포 Run Command)", "systems_manager", MGT, 1620, 520)
aws("cw", "CloudWatch&#10;Logs·Metrics", "cloudwatch_2", MGT, 1620, 660)
aws("sm", "Secrets&#10;Manager", "secrets_manager", SEC, 1620, 800)

# ── 하단: CI/CD · 외부 SaaS ──
box("gh", "GitHub · Actions&#10;(Build → Test → Push)", 100, 1100, 170, 56)
box("kakao", "카카오 OAuth", 640, 1100, 130, 44)
box("naver", "네이버 지도 SDK", 800, 1100, 130, 44)
box("fcm", "Firebase FCM (푸시)", 960, 1100, 140, 44)

# ── 연결 ──
edge("client", "r53", "exitX=1;exitY=0.3;entryX=0;entryY=0.5;", label="HTTPS")
edge("r53", "cf", "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("cf", "s3s", "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("r53", "igw", "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", label="api.fillmap.kr")
edge("igw", "alb", "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
edge("alb", "ec2a", "exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
edge("alb", "ec2c", "exitX=0.7;exitY=1;entryX=0.5;entryY=0;")
edge("ec2a", "rdsp", "exitX=0.3;exitY=1;entryX=0.5;entryY=0;")
edge("ec2c", "rdsp", "exitX=0.3;exitY=1;entryX=0.9;entryY=0;")
edge("ec2a", "redp", "exitX=0.7;exitY=1;entryX=0.5;entryY=0;")
edge("rdsp", "rdss", "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", dashed=True, label="복제·Failover")
edge("redp", "reds", "exitX=1;exitY=0.7;entryX=0;entryY=0.7;", dashed=True)
edge("ec2a", "kafka", "exitX=1;exitY=0.5;entryX=0;entryY=0.5;", label="이벤트")
edge("kafka", "ai", "exitX=0.5;exitY=1;entryX=0.9;entryY=1;", dashed=True)
edge("ai", "s3v", "exitX=1;exitY=0.2;entryX=0;entryY=0.9;", label="인코딩본")
edge("ec2a", "s3v", "exitX=1;exitY=0.1;entryX=0;entryY=0.5;", label="presigned")
edge("gh", "ecr", "exitX=1;exitY=0.5;entryX=0;entryY=1;", label="Docker push")
edge("ssm", "ec2c", "exitX=0;exitY=0.5;entryX=1;entryY=0.3;", dashed=True, label="배포")
edge("cw", "vpc", "exitX=0;exitY=0.5;entryX=1;entryY=0.65;", dashed=True)
edge("sm", "vpc", "exitX=0;exitY=0.5;entryX=1;entryY=0.85;", dashed=True)
edge("client", "kakao", "exitX=0.3;exitY=1;entryX=0.3;entryY=0;", dashed=True, label="OAuth·SDK")
edge("client", "fcm", "exitX=0.7;exitY=1;entryX=0.1;entryY=0;", dashed=True)

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="CA v2 — Cloud Architecture" id="ca-v2">'
       '<mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
       'arrows="1" fold="1" page="1" pageScale="1" pageWidth="1920" pageHeight="1220" math="0" shadow="0" background="#FFFFFF">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 5_FillMap_CA_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · 아이콘·박스={len(cells)} 연결={len(edges)}")
