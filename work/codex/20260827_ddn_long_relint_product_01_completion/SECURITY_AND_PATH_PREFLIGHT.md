# Security·private path preflight

## deterministic scan

- `C:\Users\...` source leaks: `0`
- simple credential assignment pattern: `0`
- `I:/` or `I:\` references in projected non-doc source: `11`
- `work/codex` source/test dependencies: `8`
- `docs/ssot` references in non-doc source/tests: `44`

대표 private path는 `.cargo/config.toml`, `ddn.project.json`, WASM scripts, `tool/src/paths.rs`, `tools/teul-cli/src/paths.rs`, G14 runner이다. `tool` tests에는 compile-time `work/codex/**` 및 rights-excluded pack dependency가 남았다.

```text
SECRET_PREFLIGHT: PASS_FOR_SIMPLE_STATIC_PATTERN
PRIVATE_PATH_PREFLIGHT: FAIL
COMPILE_TIME_PRIVATE_INCLUDE_PREFLIGHT: FAIL
GENERATED_CACHE_INCLUDED: NO
TECHNICAL_PUBLICATION_READINESS: NO
LEGAL_PUBLICATION_AUTHORIZATION: NO
```

비밀 scan은 제한된 정적 패턴 결과이며 법적·보안 감사를 대신하지 않는다.
