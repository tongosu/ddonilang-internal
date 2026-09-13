# DDN-LONG-RELINT-PRODUCT-01 G22 facade reproducibility audit

대상은 R1 projection root의 `README.md`와 `QUICKSTART.md`다. 파일 존재 여부가 아니라
fresh public repository에서 링크와 명령이 자체완결되는지를 읽기 전용으로 확인했다.

## custody

```text
PROJECTION: I:/home/urihanl/ddn/codex/build/public-projection-r1/tree-a
README_BYTES: 9540
README_SHA256: eaa302822c53f780970eea294ed7e6c1751b6017f51d7708bb3f677b62622edc
QUICKSTART_BYTES: 1738
QUICKSTART_SHA256: 00e7277625861e8d6f18b4204a1db713e1fd005b4caee6bb77a2657b71672332
SOURCE_WRITE_COUNT: 0
PROJECTION_WRITE_COUNT: 0
```

## README findings

### F1 broken root image

```text
REFERENCE: assets/ddonirang_wordmark.png
PROJECTED_TARGET_EXISTS: false
ACTUAL_PROJECTED_PATH: publish/assets/ddonirang_wordmark.png
```

`publish/README.md`를 projection root로 복사하면서 상대 image path를 그대로 보존한
결과다. deterministic projection이 root facade 경로를 소유해야 한다.

### F2 contribution policy incomplete

README의 일반 기여 안내는 존재하지만 Owner-approved `DCO_FIRST`, Signed-off-by 요구,
public-source-only reproduction, private SSOT/activation/release authority 분리는 없다.
`CONTRIBUTING.md` 자체도 없다.

### F3 release wording exceeds current state

README는 GitHub release/tag를 공개 채널로 설명하고 QUICKSTART는 “GitHub Releases에
배포된 바이너리” 실행을 안내한다. 현재 권위는 public push/release not authorized이며
verified release artifact도 없다. 계획과 현재 사용 가능 상태를 분리해야 한다.

## QUICKSTART command closure

존재하는 command owner:

```text
Cargo.toml: present
tools/teul-cli/Cargo.toml: present
solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py: present
solutions/seamgrim_ui_mvp/samples/index.json: present
```

누락된 재현 command dependency:

```text
tests/run_seamgrim_product_stabilization_smoke_check.py: missing
tests/seamgrim_sample_grid_space_runner.mjs: missing
tests/seamgrim_studio_layout_contract_runner.mjs: missing
tests/seamgrim_run_toolbar_compact_runner.mjs: missing
tests/run_ddonirang_vol4_bundle_cli_wasm_parity_check.py: missing
```

따라서 QUICKSTART의 5개 test command는 fresh projection에서 실행할 수 없다.
또한 `cargo build --release`는 private absolute `.cargo/config.toml target-dir`에 영향을
받고, Workbench server는 private I:/C: build root fallback을 가진다. 파일이 존재해도
portable build/run PASS가 아니다.

## successor requirements

G25 facade successor는 다음을 모두 만족해야 한다.

1. root에서 실제 존재하는 image/link path만 사용한다.
2. D7에서 승인된 public conformance root만 명령으로 제시한다.
3. command가 참조하는 runner/fixture closure를 manifest가 exact 포함한다.
4. private target/build/output fallback 제거 뒤 clean public tree에서 명령을 문자 그대로
   재실행한다.
5. DCO-first policy는 `CONTRIBUTING.md`와 README에서 같은 의미를 갖는다.
6. LICENSE/NOTICE/SECURITY/SUPPORT의 unresolved Owner input을 숨기지 않는다.
7. public release가 실제 승인·발행되기 전 binary download를 현재 사용 가능 경로로
   설명하지 않는다.
8. `README.md`, `QUICKSTART.md`, public checker가 서로 다른 command owner를 만들지
   않는다.

## result

```text
README_LINK_CLOSURE: FAIL
QUICKSTART_COMMAND_CLOSURE: FAIL
MISSING_QUICKSTART_RUNNERS: 5
PRIVATE_PATH_AFFECTED_COMMANDS: YES
DCO_POLICY_COMPLETE: NO
CURRENT_RELEASE_WORDING_ACCURATE: NO
PUBLIC_FACADE_REPRODUCIBLE: NO
IMPLEMENTATION: NOT_STARTED_PENDING_G8_AND_D7
```
