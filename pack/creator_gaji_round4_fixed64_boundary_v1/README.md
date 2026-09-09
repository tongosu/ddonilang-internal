# Creator Gaji Round 4 — Fixed64 Boundary Evidence v1

R4는 결정 코어의 이진 부동소수 입력을 제거하고, 실제 제품 입력 경계에만 변환을 남긴다.

- `core`: raw 정수, 정수, 유리수, 십진 문자열만 받는다.
- `lang`: 리터럴과 문자열 숫자를 정수 기반 십진 파서로 읽는다.
- `tool`: host 수학/WASM 숫자 입력은 `fixed64_boundary` 어댑터를 명시적으로 통과한다.
- `teul-cli`: JSON 보상 가중치의 이진 부동소수 입력은 CLI 경계에서 변환한다.
- `FIXED64_LINT_ALLOW`로 위반을 숨기지 않는다.

WASM은 시작 전 미커밋 `lang/src/stdlib.rs`와 줄바꿈 차이를 산출물에 섞지 않도록 HEAD와 R4 대상 diff만 가진 별도 worktree에서 release/web로 빌드했다. 저장소가 추적하지 않지만 `include_str!`가 요구하는 dialect TSV 한 파일만 동일 경로에 제공했다.

R5 portable checkout 재검증에서 Windows Git checkout의 CRLF 변환을 freshness가 내용 변경으로 오인하는 문제가 드러났다. 텍스트 소스·metadata·JS binding은 CRLF를 LF로 정본화한 뒤 해시하고, WASM binary만 raw byte hash를 사용하도록 manifest에 hash mode를 명시했다.

검사:

```text
python tests/run_creator_gaji_round4_fixed64_boundary_check.py
cargo test -p ddonirang-core fixed64
cargo test -p ddonirang-lang q32_32_raw_value
cargo test -p ddonirang-tool fixed64_boundary
cargo test -p ddonirang-tool state_hash_is_stable
cargo check --manifest-path tools/teul-cli/Cargo.toml
python tests/run_ddn_cli_wasm_freshness_check.py
python tests/run_ddn_cli_wasm_true_parity_equality_check.py
```

마지막 두 검사는 evidence의 clean worktree에서 수행했다. 현재 주 작업 폴더의 unrelated dirty/untracked는 보존하며, 외부 창작자 시험 성공 수는 계속 `0`이다.
