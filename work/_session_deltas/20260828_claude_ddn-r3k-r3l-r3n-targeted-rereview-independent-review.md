# 2026-08-28 — Claude 독립검증 세션: DDN-R-LONG-RELINT-R3K-R3L-R3N-TARGETED-REREVIEW-01

- 과업: R3K/R3L/R3N 통합 후속 fixed-head 독립 재검토
- REVIEW_PARENT: `a34ee611e4c82d70e35d89c23869016c76813e78` (fixed head `5c4a7684...`)
- 격리 worktree 2개: `review-ddn-r3k-r3l-r3n-20260828`(CRLF checkout, B역할), `review-ddn-r3n-lf-checkout-20260828`(LF 강제 checkout, A/C역할)

## 결정/미완료

- VERDICT: PASS_WITH_FOLLOW_UP.
- F1(`ddn.project.json`의 `teul_cli_bin` 내부경로): 소스 파일 자체는 그대로 두고 projection manifest에 `json_remove_paths` 구조적 제거 규칙 추가됨을 확인. 투영본 직접 열람해 `"toolchain":{}` 확인 — CLOSED.
- F2: 895/895/18 role/0 미스캔을 투영+검증 양쪽에서 직접 재현.
- R3N candidate 재빌드: **공식 `scripts/build_wasm_tool.ps1 -SourceRemapMode candidate`**를 세 번(LF worktree, CRLF worktree, LF worktree 반복) 독립 실행 — WASM/JS/d.ts/package 4종 전부 byte-identical이고 문서 기재 예상 해시(`48be0af0...`)와 정확히 일치. 이전 세 차례 리뷰(RELINT-COMPLETION/V1-FD01A/R3K)에서 반복 관찰한 "독자 재빌드가 tracked/claimed와 어긋난다"는 패턴이 **공식 candidate entrypoint 사용 시 완전히 해소됨**을 확인 — 중요한 교차-세션 발견.
- isolated projection substitution(item 8): 구조 수치(895/895/18/0)는 정확히 일치했으나 `validation_receipt_identity`/`public_tree_identity`가 문서 기재값과 달랐음 — 근본 원인 미확정, 정직하게 기록. 이것이 PASS_WITH_FOLLOW_UP의 핵심 근거.
- fault injection: 기존 pytest 53/53(복사 아님, 직접 실행) + 독자 CLI attack 3건(drive-case 정규화, required-root-missing 2종) 추가 수행. 15축 전체를 CLI로 재구현하지는 못함(시간 제약, 명시적 범위 제한 기록).

## 검증 결과

- 계보: c177f5e9→...→5c4a7684→a34ee611, 6 commits, merge 0, 제품 diff 0(review parent까지)
- F1: `ddn.project.json` 투영본에서 `toolchain:{}` 직접 확인
- F2: TOTAL/SCANNED 895/895, ROLE_COUNT 18, UNSCANNED 0
- 115-row inventory: CARGO_REGISTRY_ROOT 94 + RUSTUP_TOOLCHAIN_ROOT 21 = 115, UNKNOWN 0
- candidate A/B/C: 공식 entrypoint로 3회 독립 빌드, WASM/JS/d.ts/package 전부 byte-identical, 예상 해시와 완전 일치
- Python 53/53(10+25+13+5), tool lib 517/517, tool binary 405/2(source/projection 완전 동일), G14 3/3(source/projection), public SPEC seal 29/29(raw git blob)
- tracked WASM/manifest/JS/Workbench UI/docs-ssot/publish-spec diff 0
- R3L custody 4개 해시 전부 일치
- 공식 DB/포트/PID 불변
- 두 worktree git status: 세션 종료 시 모두 공백, 격리 산출물 전부 삭제

## 다음 우선순위

- substitute-projection 이후 validation receipt/tree identity 불일치 원인 규명
- 115-row WASM section byte offset 전수 대조
- fault-injection 15축 전체 CLI 직접 재구현
