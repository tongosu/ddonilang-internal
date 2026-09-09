# R3M WASM 3-way provenance matrix

## 판정

```text
OVERALL_ROOT_CAUSE: UNKNOWN
IMPLEMENTER_CLAIM_LEG: SOURCE_IDENTITY_DRIFT
REVIEWER_A_B_LEG: UNKNOWN — review output deleted, exact input/environment unavailable
CURRENT_OFFICIAL_A_B: DETERMINISTIC_AND_BYTE_IDENTICAL_TO_TRACKED_WASM
NONDETERMINISTIC_BUILD_DEFECT: NOT_OBSERVED
TRACKED_WASM_REFRESH: 0
FINAL_PROMOTION: NOT_AUTHORIZED
```

세 과거 identity를 한 원인으로 과대 통합하지 않는다. 현행 입력의 공식 A/B는 tracked
WASM과 byte-identical하지만, 이는 reviewer의 삭제된 `046472...` artifact provenance를
복구하지 않는다.

## identity 비교

| Leg | Source commit/tree | Bytes | WASM SHA-256 | 분류 |
|---|---|---:|---|---|
| tracked | current tracked artifact | 5,541,461 | `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34` | 보존 |
| implementer claim | `756d14364b2a4f1441a46973de88969436f81040` / `0fba2a4ce4a07da58f17aee6df6f6775806aa9f8` | 5,541,333 | `186f4fec75bfa2e0059eeb8fe4e0b830aed5f04a24caf88b46b25a8bb432b171` | SOURCE_IDENTITY_DRIFT |
| external reviewer A/B | report only; build output deleted | 5,541,397 | `046472f930256eaa82e241eba81f4a5287c22a69f4c384e96051073db7180d24` | UNKNOWN |
| R3M official A | compile-input head `449805bcdf52353f4fbe5362a71d681375da4dc2` / `b90d2c0aea3205d1ca04124110ebef09fe4fbb1c` | 5,541,461 | `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34` | tracked와 동일 |
| R3M official B | same commit/tree, 별도 clean detached/target/output | 5,541,461 | `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34` | A/tracked와 동일 |

R3M product/test fixed HEAD `1e55e4b2...`와 build head `449805bc...` 사이의 변경은
projection Python tool/test 네 파일뿐이다. Cargo workspace, `Cargo.lock`, Rust source,
WASM build entrypoint 차이는 0이므로 R3M A/B는 fixed HEAD의 compile input과 동일하다.

## 공식 A/B 봉인 입력

```text
CARGO_LOCK_SHA256: 0d920f63fa1bfdfffb9980d9fa80adee0f431fdaae7b224a3a6d944183db5bd4
BUILD_ENTRYPOINT: scripts/build_wasm_tool.ps1
BUILD_ENTRYPOINT_SHA256: bac40dc66f79eab77cb9a56fd6bb134d31d069b02641925dcb79b9839921f26c
COPY_ENTRYPOINT_SHA256: 613fcdd525de1d811d1df4d86751c71eae24a612fbeac5bbf486f70e80c59398
CARGO: 1.92.0
RUSTC: 1.92.0
WASM_PACK: 0.14.0
POWERSHELL: 5.1.22621.6133 Desktop
CARGO_NET_OFFLINE: true
COPY_TO_UI: false
CORE_AUTOCRLF: true
TARGET_A_B: distinct clean directories
OUTPUT_A_B: distinct directories
SOURCE_REMAP: repo root mapped by official entrypoint; dependency/toolchain roots not remapped
NETWORK_DOWNLOAD: 0
```

## generated family

R3M A와 B raw bytes는 모두 일치한다.

```text
ddonirang_tool.js: 16b4de4cac8bfebbc7d7f881ab1241b0d22d652ff8ad00b9045f40c81d7c90a9
ddonirang_tool.d.ts: 3f7f02aaffc0fb50146f47c4350bcaadb607d26ab2dd88e9b03bb82d9a3f1fec
ddonirang_tool_bg.wasm.d.ts: 64b741262887ee24dc5101a0a36a2a8e29d238277f315c2bf1bf4c2cb389bcb4
package.json: 223687f3faa5ab0f3552070ca639ba343186ded73627b712cc2a5e27ef439fa3
```

tracked JS/d.ts/package bytes는 release packaging과 CRLF materialization 때문에 raw hash가
다르며, LF 정규화 비교에서는 공식 생성물과 일치했다. 의미상 WASM identity는 raw bytes로
비교했고 A/B/tracked가 정확히 동일하다.

## WASM section delta

implementer claim과 R3M current는 section 1~9와 두 custom section이 동일하다. 차이는
code section 10과 data section 11이다.

```text
SECTION_10_CURRENT: 4718518 bytes / 0fa9e9be4d060c44d8ff38c26f972b0e01949646a62f8d99e75e38361290a9b1
SECTION_10_IMPLEMENTER: 4718518 bytes / b2df6af1b5fe4cb7fd5da2e33fecac85a276953f4de75c4051e75020aa1e56f5
SECTION_11_CURRENT: 806371 bytes / 65f5900d4e27c3e837a021e75ab952b50951ec70f698d9678099b01c148170ac
SECTION_11_IMPLEMENTER: 806243 bytes / 300bf614398a3d7ec129ee1a0c3821bab42a72b4488b38d6b857306680fdca46
```

`756d1436...`에서 current compile input까지 `tool/src/main.rs`와
`tool/src/self_contained_test_sources.rs`가 변경됐다. 따라서 implementer leg의 차이는
`SOURCE_IDENTITY_DRIFT`로 확정한다.

external reviewer report는 격리된 A/B output과 target을 검토 종료 시 삭제했다고 명시한다.
source materialization, environment, target cleanliness, generated family, section bytes를
현재 다시 검사할 수 없으므로 그 leg는 bounded 두 번의 현행 공식 재현으로 소급 확정할 수
없다. `BUILD_ENTRYPOINT_BYPASS`, `TARGET_OR_ENVIRONMENT_CONTAMINATION`, toolchain drift 중
어느 하나로 추정하지 않고 `UNKNOWN`으로 유지한다.

## F2와의 관계

현행 공식 build조차 dependency/toolchain source path 115건을 WASM bytes에 포함한다.
현재 build가 tracked와 일치한다는 사실은 public security gate를 통과시킨다는 뜻이 아니다.
tracked WASM membership 또는 remap 정책에 대한 Owner 결정 전에는 validator를 완화하거나
binary allowlist를 추가하지 않는다.
