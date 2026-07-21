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
```bash
cp .env.example .env
# .env의 GDRIVE_RAW_LOCAL_PATH에 자기 Drive 경로 입력
bash 00-meta/setup-raw-link.sh
```
