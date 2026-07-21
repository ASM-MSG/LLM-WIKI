#!/usr/bin/env python3
"""FillMap AI 처리 파이프라인 → drawio (EDGE Data Pipeline 장 스타일).
실행: repo 루트에서 python3 00-meta/gen-ai-pipeline-drawio.py
근거: ADR MSG-143(상시 FastAPI·1080p 다운스케일 전제) · SysA(Kafka→AI Highlight-Blur) · SA(FFmpeg·PySceneDetect·CLIP·pHash)"""
from xml.sax.saxutils import escape, quoteattr

# (제목, 색(fill,stroke), [박스…])  — 좌→우 단계 컬럼
STAGES = [
    ("Source\n(사용자 영상)", ("#ffe6cc", "#d79b00"), [
        "모바일 촬영 (격자 내 GPS)", "갤러리 선택 (mp4·mov)", "1~30초 · 검증된 s3Key"]),
    ("Ingestion\n(적재 · 원본 불변)", ("#dae8fc", "#6c8ebf"), [
        "presigned PUT → S3 pending/", "메타 저장 (videos row)", "상태 = UPLOADED"]),
    ("Preprocess\n(전처리)", ("#fff2cc", "#d6b656"), [
        "1080p·30fps 다운스케일 ★필수 전제", "FFmpeg 인코딩·썸네일 추출", "상태 = ENCODING"]),
    ("AI Analyze\n(분석)", ("#d0e8e4", "#4a9086"), [
        "PySceneDetect 장면 분할", "CLIP 하이라이트 스코어링", "YOLO 얼굴·차량번호 탐지 → 블러", "pHash 중복 검사", "상태 = BLURRING"]),
    ("Output\n(산출)", ("#d5e8d4", "#82b366"), [
        "인코딩본·썸네일 S3 저장", "하이라이트 구간 메타 갱신", "상태 = READY (실패 시 FAILED)"]),
]

CW, BH, PAD, GAPX = 220, 30, 12, 60
X0, Y0 = 40, 150

cells, edges, n = [], [], [0]

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def box(label, x, y, w, h, style):
    i = nid()
    cells.append(f'<mxCell id="{i}" value={quoteattr(escape(label))} style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    return i

def edge(s, t, extra="", label=""):
    i = nid("e")
    v = f' value={quoteattr(escape(label))}' if label else ''
    edges.append(f'<mxCell id="{i}"{v} style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
                 f'strokeColor=#666666;fontSize=9;fontColor=#666666;{extra}" edge="1" parent="1" '
                 f'source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# 단계 컬럼
stage_ids, col_h = [], []
for i, (title, (fill, stroke), items) in enumerate(STAGES):
    x = X0 + i * (CW + GAPX)
    h = 34 + len(items) * (BH + 8) + PAD
    col_h.append(h)
    gid = box(title.replace("\n", "&#10;"), x, Y0, CW, h,
              f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};verticalAlign=top;fontStyle=1;fontSize=11;")
    for j, it in enumerate(items):
        st = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;fontSize=10;"
        if "★" in it:
            st = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10;"
        box(it, x + PAD, Y0 + 34 + j * (BH + 8), CW - 2 * PAD, BH, st)
    stage_ids.append(gid)

for a, b in zip(stage_ids, stage_ids[1:]):
    edge(a, b, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=block;strokeWidth=2;")

W_total = X0 + len(STAGES) * (CW + GAPX) - GAPX
H_max = max(col_h)

# 제어 밴드 (상단)
ctrl = box("제어 — 상시 Python FastAPI AI 서버 (ADR MSG-143 · Lambda/GPU 기각)", X0, 40, W_total - X0, 70,
           "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;verticalAlign=top;fontStyle=1;fontSize=11;")
k1 = box("Kafka video.uploaded 컨슈머", X0 + PAD, 40 + 30, 230, BH,
         "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontSize=10;")
k2 = box("상태 머신 UPLOADED→ENCODING→BLURRING→READY/FAILED", X0 + PAD + 250, 40 + 30, 420, BH,
         "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontSize=10;")
k3 = box("실패 시 재시도·FAILED 마킹", X0 + PAD + 690, 40 + 30, 220, BH,
         "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontSize=10;")
edge(ctrl, stage_ids[2], "exitX=0.5;exitY=1;entryX=0.5;entryY=0;dashed=1;endArrow=open;", "트리거")

# 저장 계층 (하단)
SY = Y0 + H_max + 70
store = box("저장 계층", X0, SY, W_total - X0, 90,
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;verticalAlign=top;fontStyle=1;fontSize=11;")
s1 = box("S3 pending/ (원본 · 불변)", X0 + PAD, SY + 32, 230, 40,
         "shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=10;")
s2 = box("S3 encoded/ · thumbnails/", X0 + PAD + 290, SY + 32, 230, 40,
         "shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10;")
s3 = box("PostgreSQL videos (상태·메타)", X0 + PAD + 580, SY + 32, 240, 40,
         "shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10;")
edge(stage_ids[1], s1, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=open;", "load")
edge(stage_ids[4], s2, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=open;", "write")
edge(stage_ids[4], s3, "exitX=0.7;exitY=1;entryX=0.5;entryY=0;endArrow=open;", "READY 갱신")

# 소비자 (우측)
cons = box("소비자&#10;앱 재생 (presigned GET)&#10;격자 썸네일 · 하이라이트 확인", W_total + 30, Y0 + 40, 200, 80,
           "rounded=1;whiteSpace=wrap;html=1;dashed=1;fillColor=#ffffff;strokeColor=#666666;fontSize=10;verticalAlign=top;")
edge(s2, cons, "exitX=1;exitY=0.5;entryX=0;entryY=1;dashed=1;endArrow=open;", "read")

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="+ AI Pipeline Architecture" id="ai-pipeline">'
       f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W_total+280}" pageHeight="{SY+180}" math="0" shadow="0">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells + edges) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 6_FillMap_AI_Pipeline_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · cells={len(cells)} edges={len(edges)}")
