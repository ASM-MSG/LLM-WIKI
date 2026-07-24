#!/usr/bin/env python3
"""FillMap User Journey v2 → drawio. v2 세트 공통 문법: 무채색 구조 + 색 = 화면(SA v2와 동일 hue).
외출 여정(전·중·후) 3페이즈 × 5단계 × 6행(목표·행동·터치포인트·시스템·감정·기회). 보조자료(Not Architecture).
실행: repo 루트에서 python3 00-meta/gen-userjourney-drawio.py
근거: 기존 2_FillMap_UserJourney(외출 전·중·후 프레임) · PRD(cf-18972709) · 미션 기획회의 7/23 ·
AI 실측 4.3분(cf-21102593) · 탐험률 동 단위·서면 A-14(cf-23035906) · 30초 상한(cf-18579466)"""
from xml.sax.saxutils import quoteattr

def q(t):
    """라벨 → XML 속성값. 이스케이프 1회, &#10;(개행)은 보존."""
    return quoteattr(t).replace('&amp;#10;', '&#10;')


# SA v2(AppArch)와 동일한 화면 hue — 터치포인트 칩에만 색을 쓴다
SCR = {
    "로그인·온보딩": ("#E8F0F8", "#4E7EA8"),
    "① 지도 홈":     ("#E7F4EE", "#3E9E6D"),
    "② 격자 썸네일": ("#FDF1DE", "#E58E1C"),
    "③ 핫구역":      ("#FBEBE8", "#C15848"),
    "④ 격자 상세":   ("#F0EBF8", "#8A6ABF"),
    "⑥ 촬영·업로드": ("#FBF6E4", "#D6A34A"),
    "⑦ 개인 도감":   ("#E0F4F8", "#2FA4C7"),
}

# (단계 제목, 목표, 행동, [터치포인트 칩], 시스템, 감정, 기회)
S1 = ("1. 발견·탐색",
      "가고 싶은 곳·요즘 뜨는 곳을 찾는다",
      "지도 격자 탐색 · 행정동 검색&#10;핫구역 순위·격자 썸네일 미리보기&#10;미션(축제·코스) 훑기",
      ["로그인·온보딩", "① 지도 홈", "③ 핫구역", "② 격자 썸네일"],
      "GET /api/grids (뷰포트 bbox)&#10;GET /api/missions/active (TTL 1h)&#10;GET /api/grids/hot (Redis ZSET)",
      "“어디가 요즘 예쁠까?” 기대감 · 발견의 즐거움",
      "핫구역 신선도 · 미션 칩 노출 기준")
S2 = ("2. 촬영·점령",
      "그 순간을 짧게 남기고 칸을 점령한다",
      "현장 촬영 또는 갤러리 선택 (≤30초)&#10;공개 범위 선택 (기본 PRIVATE)&#10;업로드 · 진행 확인",
      ["⑥ 촬영·업로드"],
      "격자 내 GPS 검증&#10;presigned PUT → S3 → 메타 저장&#10;점령·재방문 판정 · Kafka 발행",
      "“빠르고 부담 없이 남기고 싶다”",
      "촬영→업로드 단계 수 최소화")
S3 = ("3. 미션·스탬프 (신규)",
      "축제·코스를 돌며 스탬프를 모은다",
      "미션 확인 — 면(축제)·마커(팝업)·폴리라인(코스)&#10;미션 격자에서 촬영&#10;스탬프 획득 연출",
      ["① 지도 홈", "⑥ 촬영·업로드"],
      "GET /api/missions/active&#10;코스 포토스팟 판정 (스팟 N곳 중 target)&#10;user_missions 진행도 갱신",
      "‘N칸 중 M칸’ 수집 재미",
      "코스 시작점·순번 표기 (미결)")
S4 = ("4. 처리 대기·시청",
      "내 영상이 잘 나왔는지 확인하고 나눈다",
      "인코딩 상태 확인 (4단계)&#10;AI 하이라이트 구간 조정 · 블러 토글&#10;재생 · 좋아요",
      ["⑥ 촬영·업로드", "④ 격자 상세", "② 격자 썸네일"],
      "FastAPI 파이프라인 — 1080p 30초 실측 4.3분&#10;processing_status = READY 갱신&#10;presigned GET 재생",
      "“AI가 알아서 골라준다” · 처리 대기 지루함",
      "처리 지연 체감 최소화 (상태 표시·푸시)")
S5 = ("5. 도감·리텐션",
      "내 지도가 채워지는 재미를 확인한다",
      "도감 지도·갤러리·뱃지 확인&#10;지역별 탐험률 (동 단위) 확인&#10;스탬프북 ‘15개 중 3개’",
      ["⑦ 개인 도감"],
      "GET /collections/summary·grids&#10;region_stats (동 단위 탐험률)&#10;badges · streaks",
      "“내 지도가 채워진다” 성취감 · 공유 욕구",
      "스트릭·뱃지 알림 타이밍")

PHASES = [("1. 외출 전", [S1]), ("2. 외출 중", [S2, S3]), ("3. 외출 후", [S4, S5])]

ROWS = [("목표", 44), ("행동", 92), ("터치포인트", 108), ("시스템", 92), ("감정", 50), ("기회", 50)]
COLW, CGAP, GPAD, PGAP, RGAP = 300, 18, 14, 26, 10
X0, Y0 = 180, 70
STAGE_H = 26
content_h = STAGE_H + RGAP + sum(h for _, h in ROWS) + (len(ROWS) - 1) * RGAP
GH = 30 + content_h + 12

cells, n = [], [0]

def nid(p="c"):
    n[0] += 1
    return f"{p}{n[0]}"

def text(label, x, y, w, h, style):
    cells.append(f'<mxCell id="{nid()}" value={q((label))} style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" as="geometry"/></mxCell>')

# ── 페이즈 그룹 + 단계 컬럼 ──
x = X0
row_y = {}
for ptitle, stages in PHASES:
    gw = 2 * GPAD + len(stages) * COLW + (len(stages) - 1) * CGAP
    cells.append(f'<mxCell id="{nid("g")}" value={q((ptitle))} style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;'
                 f'fillColor=none;strokeColor=#8A8F94;strokeWidth=1.2;dashed=1;dashPattern=6 4;'
                 f'verticalAlign=top;align=left;spacingLeft=8;fontStyle=1;fontSize=11.5;fontColor=#5B6066;" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{Y0}" width="{gw}" height="{GH}" as="geometry"/></mxCell>')
    for si, (title, 목표, 행동, chips, 시스템, 감정, 기회) in enumerate(stages):
        cx = x + GPAD + si * (COLW + CGAP)
        cy = Y0 + 30
        text(title, cx, cy, COLW, STAGE_H,
             "text;html=1;strokeColor=none;fillColor=#EEF0F2;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;fontColor=#2B2B2B;")
        cy += STAGE_H + RGAP
        for rname, rh in ROWS:
            row_y[rname] = cy
            if rname == "터치포인트":
                for ci, chip in enumerate(chips):
                    tf, ts = SCR[chip]
                    text(chip, cx + 8, cy + 4 + ci * 26, COLW - 16, 22,
                         f"rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor={tf};strokeColor={ts};fontSize=9;fontStyle=1;fontColor=#2B2B2B;")
            else:
                val = {"목표": 목표, "행동": 행동, "시스템": 시스템, "감정": 감정, "기회": 기회}[rname]
                it = "fontStyle=2;" if rname == "감정" else ""
                text(val, cx, cy, COLW, rh,
                     f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C6CBD1;{it}"
                     f"fontSize=9.5;fontColor=#2B2B2B;align=left;verticalAlign=middle;spacingLeft=8;spacingRight=6;")
            cy += rh + RGAP
    x += gw + PGAP
total_w = x - PGAP + 40

# ── 행 라벨 (무채색) ──
for rname, rh in ROWS:
    text(rname, 40, row_y[rname] + rh / 2 - 13, 120, 26,
         "rounded=1;arcSize=30;whiteSpace=wrap;html=1;fillColor=#4A5560;strokeColor=none;fontSize=10.5;fontStyle=1;fontColor=#FFFFFF;")

# ── 제목·배지·하단 주석 ──
text("FillMap · User Journey v2 — 외출 여정 (2026.07)", 20, 8, 700, 26,
     "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=17;fontStyle=1;fontColor=#232F3E;")
text("보조자료 (Not Architecture) — 사용자 관점 흐름 · UX 참고용", total_w - 460, 10, 420, 24,
     "rounded=1;arcSize=12;whiteSpace=wrap;html=1;fillColor=#FDF1F0;strokeColor=#C15848;fontSize=10;fontStyle=1;fontColor=#C15848;")
text("터치포인트 색 = SA v2(Application Architecture) 화면 색과 동일 · 시스템 행의 정본은 SA v2·SysA v2·CA v2 · "
     "수치: 영상 30초 상한 · AI 처리 1080p 30초 실측 4.3분 · 탐험률 동 단위",
     X0, Y0 + GH + 16, total_w - X0 - 40, 20,
     "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=9.5;fontColor=#6B7075;")

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       '<diagram name="UserJourney v2 — 외출 여정" id="uj-v2">'
       f'<mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{total_w:.0f}" pageHeight="{Y0 + GH + 70}" '
       'math="0" shadow="0" background="#FFFFFF">'
       '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
       + "\n".join(cells) + '\n</root></mxGraphModel></diagram></mxfile>\n')

out = "raw/Architecture Map/2026-07-21 2_FillMap_UserJourney_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: {out} · 셀={len(cells)}")
