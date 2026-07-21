#!/usr/bin/env python3
"""IA v2 트리 → drawio 생성. 트리(T) 수정 후 실행: python3 00-meta/gen-ia-drawio.py (repo 루트에서)"""
from xml.sax.saxutils import escape, quoteattr

def N(label, status=None, *children):
    return (label, status, list(children))

# status: 구현|부분|미구현|P2|결정필요|None(그룹)
T = N("FillMap", None,
 N("사용자 앱", None,
  N("로그인 전", None,
    N("온보딩", "미구현",
      N("서비스 소개", "미구현"),
      N("위치·카메라 권한 요청", "미구현"),
    ),
    N("로그인", None,
      N("카카오 소셜 로그인 (OIDC)", "구현"),
      N("Apple · 로컬(dev) 로그인", "결정필요"),
      N("세션 유지 (Refresh Token)", "미구현"),
    ),
  ),
  N("① 지도 홈", None,
    N("내 점령 격자 색칠", "구현",
      N("뷰포트 bbox 조회 (폴링)", "구현"),
      N("내 색 팔레트 8색", "구현"),
      N("미점령 격자 미표시", "구현"),
    ),
    N("미션 레이어", "미구현",
      N("축제·팝업 — 면 오버레이", "미구현"),
      N("코스 — 폴리라인", "미구현"),
      N("테마 — 격자 점", "미구현"),
      N("구역 — 행정동 경계", "미구현"),
    ),
    N("행정동 검색", "미구현",
      N("자동완성·동명이인 표기", "미구현"),
      N("선택 → fitBounds 이동", "미구현"),
      N("랜드마크(홍대) 검색 불가", "결정필요"),
    ),
    N("미션 칩 (배지·0이면 숨김)", "미구현",
      N("🎪 지역축제 (팝업 통합)", "미구현"),
      N("🥾 추천코스", "미구현"),
      N("🔥 핫구역", "결정필요"),
      N("내 동네 채우기 (fallback)", "미구현"),
    ),
    N("미션 바텀시트 (3단)", "미구현",
      N("리스트 — 기간·거리·참여 수", "미구현"),
      N("상세 — 내용·기간·홈페이지", "미구현"),
      N("진행도 — ✓ 또는 'N칸 중 M칸'", "미구현"),
      N("CTA — 여기서 찍기 / 길찾기", "미구현"),
    ),
    N("요약 카드", None,
      N("핫구역 TOP 5", "결정필요"),
      N("미방문 격자 추천", "결정필요"),
      N("내 수집 현황", "미구현"),
      N("지역별 수집률", "미구현"),
    ),
  ),
  N("② 격자 썸네일 뷰", None,
    N("썸네일 그리드", "미구현",
      N("정렬 — 조회수→최신 고정", "미구현"),
      N("PUBLIC·READY만 노출", "미구현"),
      N("좋아요 ♥ / 취소 (멱등)", "미구현"),
    ),
    N("격자 요약", "부분",
      N("점령 여부·영상 수", "구현"),
      N("최근 업로드·누적 조회수", "미구현"),
      N("핫구역 지수·대표 태그", "미구현"),
    ),
  ),
  N("③ 핫구역 뷰", "결정필요",
    N("순위 리스트 (10분 업로드)", "결정필요"),
    N("갱신 시각·카운트다운", "미구현"),
    N("Redis ZSET 산식·TTL", "결정필요"),
  ),
  N("④ 격자 상세", None,
    N("격자 표시명 '홍대입구 A-14'", "결정필요"),
    N("행정 지역명·활동 지표", "미구현"),
    N("영상 목록·재생", "미구현",
      N("presigned GET 재생", "미구현"),
      N("인코딩 중 — 대기 표시", "미구현"),
      N("실패·블라인드 — 처리 방식", "결정필요"),
      N("조회수 증가 시점", "결정필요"),
    ),
    N("영상 신고", "결정필요",
      N("사유 선택 (enum 미정)", "결정필요"),
      N("제출 → 접수 안내", "미구현"),
    ),
  ),
  N("⑥ 촬영·업로드", None,
    N("촬영·선택", "구현",
      N("격자 내 GPS 검증", "구현"),
      N("갤러리 선택 (1~30초)", "구현"),
    ),
    N("업로드 파이프라인", "구현",
      N("presigned → S3 → 메타 저장", "구현"),
      N("점령/재방문 판정", "구현"),
    ),
    N("인코딩 상태 표시", "구현",
      N("4단계 상태 머신", "구현"),
      N("진행률 폴링", "결정필요"),
    ),
    N("AI 하이라이트·블러", "결정필요"),
    N("공개 범위 선택 (기본 PRIVATE)", "결정필요"),
    N("스탬프 획득 연출 🎆", "미구현"),
    N("교체 / 삭제 (점령 롤백)", "구현"),
  ),
  N("⑦ 개인 도감", None,
    N("요약 — 격자·영상·뱃지·스트릭", "미구현"),
    N("지도 뷰 (기존 API 재사용)", "구현"),
    N("갤러리 뷰", "미구현",
      N("정렬 — 최근 / 처음 수집", "미구현"),
      N("페이지네이션 방식", "결정필요"),
      N("격자별 내 영상 목록", "미구현"),
    ),
    N("뱃지 뷰", "미구현",
      N("전체/획득 필터", "미구현"),
      N("진행률·마스터 시딩", "결정필요"),
    ),
    N("지역별 수집률", "미구현",
      N("표시 레벨 (동/구/시)", "결정필요"),
    ),
    N("스탬프북 — '15개 중 3개'", "결정필요"),
    N("공개 범위 (친구는 P2)", "결정필요"),
  ),
  N("설정·프로필", None,
    N("프로필 조회", "미구현"),
    N("수정 — 닉네임·색상·이미지", "결정필요"),
    N("로그아웃", "구현"),
    N("계정 삭제 (하드/소프트 미정)", "결정필요"),
    N("알림 설정", "P2"),
  ),
  N("소셜", "P2",
    N("친구 찾기 (방식 미해결)", "결정필요"),
    N("요청·수락·목록·차단", "P2"),
    N("친구 도감 보기", "P2"),
  ),
 ),
 N("운영자 콘솔 (Admin)", None,
   N("신고 처리 → 영상 블라인드", "미구현"),
   N("사용자 차단·Trust Score", "미구현"),
   N("통계 모니터링", "미구현"),
   N("미션 수동 등록 (데모 팝업)", "미구현"),
 ),
 N("스폰서 포털", "P2",
   N("캠페인·스폰서 격자 관리", "P2"),
   N("성과 리포트 조회", "P2"),
 ),
)


FILL = {"구현": ("#d5e8d4", "#82b366"), "부분": ("#fff2cc", "#d6b656"),
        "미구현": ("#ffffff", "#666666"), "P2": ("#dae8fc", "#6c8ebf"),
        "결정필요": ("#f8cecc", "#b85450"), None: ("#ffffff", "#000000")}
ROW, H, GAP = 32, 26, 55

def leaves(n):
    return 1 if not n[2] else sum(leaves(c) for c in n[2])

def depth_of(n):
    return 1 if not n[2] else 1 + max(depth_of(c) for c in n[2])

class B:
    def __init__(self):
        self.cells, self.edges, self.n = [], [], 0

    def nid(self):
        self.n += 1
        return f"n{self.n}"

    def box(self, label, status, x, y, w, big=False, has_kids=False):
        i = self.nid()
        fill, stroke = FILL[status if status in FILL else None]
        bold = "fontStyle=1;" if (has_kids or big) else ""
        fs = 13 if big else 10
        h = 34 if big else H
        self.cells.append(
            f'<mxCell id="{i}" value={quoteattr(escape(label))} '
            f'style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};{bold}fontSize={fs};" '
            f'vertex="1" parent="1"><mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    def edge(self, s, t, extra):
        i = self.nid()
        self.edges.append(
            f'<mxCell id="e{i}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;'
            f'strokeColor=#999999;endArrow=blockThin;endSize=4;{extra}" '
            f'edge="1" parent="1" source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    def emit(self, node, depth, y0, x0, W):
        h_total = leaves(node) * ROW
        y = y0 + h_total / 2 - H / 2
        x = x0 + sum(W[min(d, len(W)-1)] + GAP for d in range(depth))
        i = self.box(node[0], node[1], x, y, W[min(depth, len(W)-1)], has_kids=bool(node[2]))
        cy = y0
        for c in node[2]:
            ci = self.emit(c, depth + 1, cy, x0, W)
            cy += leaves(c) * ROW
            self.edge(i, ci, "exitX=1;exitY=0.5;entryX=0;entryY=0.5;")
        return i

    def legend(self, x, y):
        self.cells.append(f'<mxCell id="lg0" value="범례" style="text;html=1;fontStyle=1;fontSize=12;" vertex="1" parent="1">'
                          f'<mxGeometry x="{x}" y="{y}" width="60" height="20" as="geometry"/></mxCell>')
        for j, (k, (f, s)) in enumerate([(k, v) for k, v in FILL.items() if k]):
            self.cells.append(
                f'<mxCell id="lg{j+1}" value="{k}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontSize=10;" '
                f'vertex="1" parent="1"><mxGeometry x="{x+70+j*95}" y="{y}" width="85" height="20" as="geometry"/></mxCell>')

    def xml(self, name, pw, ph):
        return (f'<diagram name="{name}" id="{name}">'
                f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0">'
                '<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n'
                + "\n".join(self.cells + self.edges) + '\n</root></mxGraphModel></diagram>')

def col_width(node, W):
    return sum(W[min(i, len(W)-1)] + GAP for i in range(depth_of(node))) - GAP

# ── A. 9시 단일 트리 (루트 좌측 중앙에서 오른쪽으로) ──
def build_A():
    b = B()
    W = [120, 150, 190, 220, 235, 250]
    b.legend(0, 0)
    b.emit(T, 0, 50, 0, W)
    return b.xml("A. 좌측 단일 트리", 1800, 3000)

# ── B. 3컬럼 (사용자 앱 2분할 + 운영·스폰서 스택) ──
def build_B():
    b = B()
    W = [170, 190, 220, 235]
    app = T[2][0]
    g1 = N("사용자 앱 — 탐색·시청", None, *app[2][0:5])   # 로그인전·①·②·③·④
    g2 = N("사용자 앱 — 기록·도감", None, *app[2][5:])    # ⑥·⑦·설정·소셜
    rest = T[2][1:]                                        # 운영자·스폰서
    x1 = 0
    x2 = x1 + col_width(g1, W) + 90
    x3 = x2 + col_width(g2, W) + 90
    total = x3 + max(col_width(c, W) for c in rest)
    b.legend(0, 0)
    root = b.box("FillMap", None, total/2 - 70, 40, 140, big=True)
    for node, x in [(g1, x1), (g2, x2)]:
        cid = b.emit(node, 0, 140, x, W)
        b.edge(root, cid, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    sy = 140
    for node in rest:
        cid = b.emit(node, 0, sy, x3, W)
        b.edge(root, cid, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
        sy += leaves(node) * ROW + 60
    return b.xml("B. 3컬럼 (사용자 앱 분할)", 2600, 1800)

# ── C. 좌 대형 + 우 스택 (현재안) ──
def build_C():
    b = B()
    W = [150, 190, 220, 235]
    first, rest = T[2][0], T[2][1:]
    rx = col_width(first, W) + 90
    total = rx + max(col_width(c, W) for c in rest)
    b.legend(0, 0)
    root = b.box("FillMap", None, total/2 - 70, 40, 140, big=True)
    cid = b.emit(first, 0, 140, 0, W)
    b.edge(root, cid, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
    sy = 140
    for node in rest:
        cid = b.emit(node, 0, sy, rx, W)
        b.edge(root, cid, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")
        sy += leaves(node) * ROW + 60
    return b.xml("C. 좌 대형 + 우 스택", 2400, 2800)

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net">\n'
       + build_B() + "\n</mxfile>\n")

out = "raw/Architecture Map/2026-07-21 1_FillMap_IA_v2_draft.drawio.xml"
open(out, "w").write(xml)

import xml.etree.ElementTree as ET
ET.parse(out)
print(f"OK: 3 tabs written · leaves={leaves(T)}")
