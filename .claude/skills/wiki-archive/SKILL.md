---
name: wiki-archive
description: 완료·비활성 노트를 90-archive/<연도>/로 이동. "아카이브해줘" 요청 시 사용.
---

# wiki-archive — 보관

## 절차
1. `git mv <노트> 90-archive/<연도>/`
2. frontmatter에 `status: archived`, `archived: YYYY-MM-DD` 추가
3. `index.md`에서 아카이브 섹션으로 이동
4. `log.md`에 기록 추가

## 규칙
- raw는 아카이브 안 함 (Layer 1 그대로)
- 내용 삭제 금지, 이동만
- wikilink는 파일명 기반이라 이동해도 안 깨짐
