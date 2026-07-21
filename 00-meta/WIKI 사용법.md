# 📖 WIKI 사용법 (5분 가이드)

## 읽기
- Obsidian으로 이 폴더를 열고 `index.md`에서 시작.
- 아니면 그냥 Claude에게 질문하면 관련 노트를 찾아 출처와 함께 답해준다.

## 쓰기
1. Google Drive의 raw 폴더에 파일을 넣는다 (드래그만 하면 됨).
2. Claude에게 **"ingest하고 푸시해줘"** 라고 말한다.
3. 끝. Confluence에 새로 쓴 문서도 이때 자동으로 같이 수집된다 (데일리 스크럼·스프린트 회고 제외).

## 규칙 3개
1. `raw/`는 안 고친다 (원본 불변).
2. canon 문서(GOAL·ICP·VALUE·SCHEMA·glossary) 변경은 사람 승인 필요.
3. compiled 노트(.md)는 자유롭게 수정 가능.

## 최초 1회 세팅 (팀원 각자)

### ① 공유받은 fillmap-raw를 내 드라이브에 연결
1. https://drive.google.com → 왼쪽 **"공유 문서함"**
2. `fillmap-raw` 우클릭 → **정리 → 바로가기 추가** → 위치: **내 드라이브**

### ② Google Drive 데스크탑 설치 + 로그인
- Mac: `brew install --cask google-drive` (또는 https://www.google.com/drive/download/)
- Windows: 같은 링크에서 설치
- 실행 후 fillmap-raw를 공유받은 구글 계정으로 로그인

### ③ 위키 저장소 클론
```bash
git clone <repo 주소> && cd fillmap-wiki
```

### ④ .env에 자기 Drive 경로 입력
```bash
cp .env.example .env
```
- Mac 경로 확인: `ls ~/Library/CloudStorage/GoogleDrive-*/`
  - `내 드라이브/fillmap-raw`가 보이면 그 경로 사용
  - 안 보이면(바로가기라서) `ls ~/Library/CloudStorage/GoogleDrive-*/.shortcut-targets-by-id/*/`로 찾은 전체 경로 사용
- Windows(git-bash): `G:\내 드라이브\fillmap-raw` → `/g/내 드라이브/fillmap-raw`
- 공백·한글 있으니 **경로를 따옴표로 감싸기**

### ⑤ raw 링크 걸고 확인
```bash
bash 00-meta/setup-raw-link.sh
ls raw/confluence   # 파일이 보이면 성공
```
