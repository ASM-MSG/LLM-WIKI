---
name: wiki-lint
description: compiled 노트·raw의 무결성을 점검한다. "lint 돌려줘", "위키 점검해줘" 요청 시 사용.
---

# wiki-lint — 무결성 점검

```
node .claude/skills/wiki-lint/lint.js .
```

## 점검 유형
| 유형 | 의미 |
| --- | --- |
| `broken-link` | `[[X]]`가 없는 노트를 가리킴 |
| `frontmatter` | `title` 또는 `source` 누락 |
| `format` | `> [!tldr]` 또는 `## 이 노트로 답할 수 있는 질문` 누락 |
| `orphan` | 노트인데 `index.md`에 미등록 (01~06 대상, 07 제외) |
| `un-ingested` | raw인데 어떤 노트도 `source`로 참조 안 함 |
| `raw-naming` | raw 파일명이 `YYYY-MM-DD ` 위반 |
| `field` | `product:`/`class:` 누락 (권장) |

## 종료 코드
- `0` = 깨끗
- `1` = 문제 발견

## 비고
- `raw/`가 심볼릭 링크 미연결이면 `raw-naming`/`un-ingested`는 자동 skip.
- 지원 파일(`index`/`hot`/`log`/`README`/`_index`)과 `00-meta/templates/`는 일부 규칙 면제.
