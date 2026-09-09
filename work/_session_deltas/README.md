# work/_session_deltas/

여러 AI가 이어서 작업할 수 있도록 세션 중 결정과 미완료 작업을 남기는 중앙 큐다.

파일명:

```text
YYYYMMDD_agent_session-name.md
```

예:

```text
20260706_codex_ai_collab_bootstrap.md
20260706_claude_settings_header_review.md
```

상태값:

- `Pending`: 반영 검토 필요
- `Reflected`: 문서/코드/운영 규칙에 반영됨
- `Rejected`: 반영하지 않기로 결정

반영 완료 후 장기 보관이 필요한 델타는 `_merged/`로 이동한다.
