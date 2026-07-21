---
name: wiki-ingest-and-push
description: confluence-sync + wiki-ingest + push를 한 번에. "ingest하고 푸시해줘" 요청 시 사용.
---

# wiki-ingest-and-push — 원스톱

0. `confluence-sync` 스킬 실행 (Confluence 새/수정 문서 → raw/confluence/ 스냅샷)
1. `wiki-ingest` 스킬 실행 (raw → compiled + index/hot/log 갱신 + lint) — Drive에 새로 들어온 raw와 방금 sync된 Confluence 스냅샷 모두 대상
2. lint 통과하면 `push` 스킬 실행 (pull --rebase → commit → push → Slack)
3. lint 실패 시 push하지 않고 멈춤

## 언제 무엇을 쓰나
| 목적 | 스킬 |
| --- | --- |
| Confluence만 가져오기 | `confluence-sync` |
| 정리만 | `wiki-ingest` |
| 올리기만 | `push` |
| 전부 한 번에 | **`wiki-ingest-and-push`** |
