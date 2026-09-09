# [Codex관리Work -> 독립검증ClaudeCode] DDN-R-V1-CLI01-I1-01 최종 요청

```text
TASK: DDN-R-V1-CLI01-I1-01
AUDIT_FIXED_HEAD: 4a68c9f19ec385e6c13c80caed9ff4615692f43b
REQUIRED_REVIEW_PARENT: 603fbccbda6fec77dba218230c0caefe70b318a3
AUDIT_BASELINE: e5454ef5858af4f48a202cffe30ceef010e35162
EXPECTED_MERGE_COMMIT_COUNT: 0
EXPECTED_PRODUCT_DIFF: 0
EXPECTED_SSOT_SPEC_UI_WASM_DIFF: 0
```

새 clean-detached worktree에서 [AUDIT_HANDOFF.md](AUDIT_HANDOFF.md)의 8개 검토 항목을 독립 재현하라. 구현자 generator의 결과를 답으로 사용하지 말고 source에서 명령과 edge를 다시 산출한 뒤 기계 원장과 비교하라.

특히 다음 공격을 포함한다.

1. clap variant의 explicit `#[command(name=...)]`와 자동 kebab-case를 바꿔 계산해 누락 탐색
2. `tool/src/main.rs`의 nested match를 top-level command로 잘못 세는 반례
3. path-import를 정상 shared-crate API로 오판하는 반례
4. `teul-cli -> ddonirang-tool` Cargo edge만 보고 소스 권위를 단방향이라 주장하는 반례
5. publish/pack/tests reference count 재계산
6. migration DAG에서 retirement가 parity review보다 앞서는 mutation RED
7. disposition 문자열에 DROP 또는 public-membership 확정이 들어가는 mutation RED

보고서는 review branch의 문서 전용 commit으로 남기고 다음을 반환한다.

```text
VERDICT:
SCOPE:
AUDIT_FIXED_HEAD:
REVIEW_PARENT:
REVIEW_COMMIT:
REPORT_PATH:
REPORT_BYTES:
REPORT_SHA256:
TOOL_COMMAND_COUNT:
TEUL_COMMAND_COUNT:
OWNERSHIP_VERDICT:
PRODUCT_DIFF:
SSOT_DIFF:
PUBLIC_SPEC_DIFF:
UI_DIFF:
WASM_DIFF:
FOLLOW_UPS:
```

이 요청은 제품 구현, 공개 이름 선택, SSOT/SPEC 수정, command 제거, release, activation, Human PASS를 승인하지 않는다.
