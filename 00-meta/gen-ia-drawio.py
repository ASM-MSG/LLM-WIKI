#!/usr/bin/env python3
"""IA v2 트리 → drawio 생성. 트리(T) 수정 후 실행: python3 00-meta/gen-ia-drawio.py (repo 루트에서)"""
from xml.sax.saxutils import escape, quoteattr

def q(t):
    """라벨 → XML 속성값. 이스케이프 1회, &#10;(개행)은 보존."""
    return quoteattr(t).replace('&amp;#10;', '&#10;')


def N(label, status=None, *children):
    return (label, status, list(children))

# 라벨 원칙(EDGE IA 방식): 리프 = 사용자 언어 명사구 2~4단어. 미결은 "(미정)", P2는 "(P2)"만.
# 기술 계약(API·enum·산식)은 SA v2·스펙 문서 소관 — 여기 싣지 않는다. 상태 태그는 렌더 안 함.
T = N("FillMap", None,
 N("사용자 앱", None,
  N("로그인 전", None,
    N("온보딩", None,
      N("서비스 소개", None),
      N("위치·카메라 권한", None),
    ),
    N("로그인", None,
      N("카카오 로그인", None),
      N("Apple 로그인 (미정)", None),
      N("로컬 로그인 (dev)", None),
      N("세션 유지", None),
    ),
  ),
  N("① 지도 홈", None,
    N("내 격자 색칠", None,
      N("뷰포트 격자 조회", None),
      N("내 색 팔레트 8색", None),
      N("미점령 격자 미표시", None),
    ),
    N("지도 모드 나·친구 (P2)", None),
    N("미션 레이어", None,
      N("축제 · 면", None),
      N("팝업 · 마커", None),
      N("코스 · 폴리라인", None),
      N("테마 · 격자 점", None),
      N("구역 · 행정동 경계", None),
    ),
    N("행정동 검색", None,
      N("자동완성", None),
      N("검색 위치로 이동", None),
      N("랜드마크 검색 (미정)", None),
    ),
    N("미션 칩", None,
      N("지역축제", None),
      N("추천코스", None),
      N("핫구역 (미정)", None),
      N("내 동네 채우기", None),
    ),
    N("미션 바텀시트", None,
      N("미션 리스트", None),
      N("항목 탭 → 지도 이동", None),
      N("미션 상세", None),
      N("진행도 표기", None,
        N("다녀옴 체크", None),
        N("'스팟 N곳 중 M곳'", None),
      ),
      N("거리별 버튼", None,
        N("여기서 찍기", None),
        N("길찾기 (미정)", None),
      ),
    ),
    N("요약 카드", None,
      N("핫구역 TOP 5", None),
      N("미방문 격자 추천", None),
      N("내 수집 현황", None),
      N("지역별 탐험률", None),
    ),
  ),
  N("② 격자 썸네일", None,
    N("썸네일 그리드", None,
      N("조회수·최신 정렬", None),
      N("공개·완료 영상만", None),
      N("좋아요·취소", None),
    ),
    N("격자 요약", None,
      N("점령 여부·영상 수", None),
      N("최근 업로드·조회수", None),
      N("핫구역 지수·태그", None),
    ),
  ),
  N("③ 핫구역", None,
    N("실시간 순위", None),
    N("갱신 카운트다운", None),
    N("순위 산정 기준 (미정)", None),
  ),
  N("④ 격자 상세", None,
    N("격자 표시명", None,
      N("구역명 '서면 A-14'", None),
      N("폴백 · 행정동 이름", None),
      N("무귀속 · 이름 없음", None),
    ),
    N("활동 지표", None,
      N("동 탐험률", None),
      N("핫구역 지수", None),
      N("영상 수", None),
    ),
    N("영상 목록·재생", None,
      N("영상 재생", None),
      N("인코딩 대기 표시", None),
      N("실패·블라인드 (미정)", None),
      N("조회수 시점 (미정)", None),
    ),
    N("영상 신고", None,
      N("사유 선택 (미정)", None),
      N("접수 안내", None),
    ),
  ),
  N("⑥ 촬영·업로드", None,
    N("촬영·선택", None,
      N("격자 GPS 검증", None),
      N("갤러리 선택 (≤30초)", None),
    ),
    N("업로드", None,
      N("영상 업로드", None),
      N("점령·재방문 판정", None),
    ),
    N("인코딩 상태", None,
      N("업로드됨", None),
      N("인코딩 중", None),
      N("블러 처리 중", None),
      N("완료 · 실패", None),
    ),
    N("AI 하이라이트·블러 (미정)", None),
    N("공개 범위 선택", None),
    N("스탬프 획득 연출", None),
    N("교체·삭제", None),
  ),
  N("⑦ 개인 도감", None,
    N("요약", None,
      N("수집 격자 수", None),
      N("방문 지역 수", None),
      N("영상 수", None),
      N("스트릭", None),
    ),
    N("지도 뷰", None),
    N("갤러리 뷰 · 격자 중심", None,
      N("최근 수집 격자 30", None),
      N("격자 → 동 탐험률", None),
      N("격자별 내 영상", None),
    ),
    N("뱃지 뷰", None,
      N("전체·획득 필터", None),
      N("진행률 표시", None),
    ),
    N("지역별 탐험률", None,
      N("동 단위 산식", None),
      N("현재 위치 초기값", None),
      N("위치 폴백", None),
    ),
    N("스탬프북", None),
    N("공개 범위 (친구 P2)", None),
  ),
  N("설정·프로필", None,
    N("프로필 조회", None),
    N("프로필 수정", None),
    N("로그아웃", None),
    N("계정 삭제 (미정)", None),
    N("알림 설정 (P2)", None),
  ),
  N("소셜 (P2)", None,
    N("친구 찾기 (미정)", None),
    N("요청·수락·차단", None),
    N("친구 도감", None),
  ),
 ),
 N("운영자 콘솔", None,
   N("신고 처리", None),
   N("사용자 차단", None),
   N("통계 모니터링", None),
   N("미션 수동 등록", None),
 ),
 N("스폰서 포털 (P2)", None,
   N("캠페인 관리", None),
   N("스폰서 격자", None),
   N("성과 리포트", None),
 ),
)


# EDGE IA 방식(무채색): 상태는 색으로 싣지 않는다 — 미정·P2 등은 라벨 텍스트가 담는다
ROW, H, GAP = 36, 28, 60

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
        fill, stroke = "#ffffff", "#333333"
        bold = "fontStyle=1;" if (has_kids or big) else ""
        fs = 13 if big else 10
        h = 34 if big else H
        self.cells.append(
            f'<mxCell id="{i}" value={q((label))} '
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
    b.emit(T, 0, 50, 0, W)
    return b.xml("A. 좌측 단일 트리", 1800, 3000)

# ── B. 3컬럼 (사용자 앱 2분할 + 운영·스폰서 스택) ──
def build_B():
    b = B()
    W = [150, 165, 180, 185]
    app = T[2][0]
    g1 = N("사용자 앱 — 탐색·시청", None, *app[2][0:5])   # 로그인전·①·②·③·④
    g2 = N("사용자 앱 — 기록·도감", None, *app[2][5:])    # ⑥·⑦·설정·소셜
    rest = T[2][1:]                                        # 운영자·스폰서
    x1 = 0
    x2 = x1 + col_width(g1, W) + 90
    x3 = x2 + col_width(g2, W) + 90
    total = x3 + max(col_width(c, W) for c in rest)
    root = b.box("FillMap", None, total/2 - 70, 40, 140, big=True)
    for node, x, ex in [(g1, x1, "exitX=0;exitY=0.5;entryX=0.5;entryY=0;"),
                        (g2, x2, "exitX=0.5;exitY=1;entryX=0.5;entryY=0;")]:
        cid = b.emit(node, 0, 140, x, W)
        b.edge(root, cid, ex)
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
print(f"OK: build B · leaves={leaves(T)}")
