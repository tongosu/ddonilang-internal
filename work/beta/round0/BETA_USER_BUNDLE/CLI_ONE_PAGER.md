# CLI 실행 1쪽

모든 명령은 저장소 루트에서 실행합니다.

## 파일 확인

```bash
cargo run --manifest-path tools/teul-cli/Cargo.toml -- check work/beta/round0/BETA_USER_BUNDLE/samples/pendulum_edit.ddn
```

## 파일 실행

```bash
cargo run --manifest-path tools/teul-cli/Cargo.toml -- run work/beta/round0/BETA_USER_BUNDLE/samples/pendulum_edit.ddn --madi 10
```

## 콘솔 격자 샘플

```bash
cargo run --manifest-path tools/teul-cli/Cargo.toml -- run work/beta/round0/BETA_USER_BUNDLE/samples/grid_maze_probe.ddn --madi 8
```

## 오류 fixture 실행

```bash
cargo run --manifest-path tools/teul-cli/Cargo.toml -- check work/beta/round0/BETA_USER_BUNDLE/fixtures/T4/syntax_bad_identifier.ddn
cargo run --manifest-path tools/teul-cli/Cargo.toml -- run work/beta/round0/BETA_USER_BUNDLE/fixtures/T4/type_bad_iterable.ddn
cargo run --manifest-path tools/teul-cli/Cargo.toml -- check work/beta/round0/BETA_USER_BUNDLE/fixtures/T4/contract_bad_mode.ddn
```

기대 진단은 `fixtures/T4/expected_diagnostics.md`에 있습니다.
