# DDN-LONG-RELINT 공개 비브라우저 자체완결성 FU01 결과

## 판정

```text
TASK: DDN-LONG-RELINT-PRODUCT-01 / G18~G30 safe non-browser follow-up
BASELINE: 799ac30a2cff8ecb0b93379840bb7faee50eefef
PRODUCT_TEST_FIXED_HEAD: b88d7a9016d1a03c54b62f9ad76b7a7f78e653bc
STATUS: PARTIAL_TECHNICAL_CANDIDATE_REVIEWABLE_OVERALL_GATE_OPEN
SELF_PASS: NO
CLOSED: NO
PUBLICATION_READY: NO
```

G18의 정확한 전체 공개 범위에는 Workbench, selected examples와 browser/offline
dependency가 포함된다. 이번 fixed HEAD는 Owner 결정 없이 안전한 language/runtime,
CLI, WASM build, public SPEC custody와 G14 closure만 교정했다. 전체 public source
self-containment나 G31 실제 Edge를 PASS로 확대하지 않는다.

## 선형 구현 계보

```text
799ac30a2cff8ecb0b93379840bb7faee50eefef
-> 9f3c0d7c8c4cda9c13bfd3146cbee2100f30e344
-> 6965a0e71cc3fcc8f4658ac632615fdbddf1c662
-> fa15d1d0c3e7b47e4e46c1eca08e8607099316b6
-> 756d14364b2a4f1441a46973de88969436f81040
-> 82455cbba907a7cb12c0c4b46cda30416d8401f3 (docs)
-> 852f561f1ddc82f3b7a179439a21b62d3b6e124c (docs)
-> a4d103ad9d8e52c360b5c1607cb658d4b041627a
-> a48e8eac5e4319b3ced8f833c0b4fbea5cc928fa (docs)
-> c541fa41942102da6425f5292debc8c508018b06 (docs)
-> 47b9ba0d271fe045f2f72d39811e98aca59f59d8 (docs)
-> c0c5371f24965df05bf548464d391a4588f2b582 (docs)
-> 6c9300516135dc011839f6e5de41f8bce4ec37ff
-> 7d7624ea4fbb8ce2fa936cfcaf5609ef9a16188c
-> b88d7a9016d1a03c54b62f9ad76b7a7f78e653bc
```

- merge commit: 0
- history rewrite: 0
- shared dirty root mutation: 0
- `docs/ssot/**` diff: 0
- Workbench UI diff: 0
- tracked WASM diff: 0

## 구현 결과

1. 제품 Rust test source의 `include_str!`/`include_bytes!`가 private `pack/**`,
   `work/**`, `docs/ssot/**`에 compile-time 의존하던 13개 경로를 repository-local
   synthetic source로 교체했다.
2. V25 Definition/Binding matrix는 rights-gated five-file pack을 읽지 않고 동일한
   diagnostic/category를 synthetic source로 검증한다.
3. build/out 경로는 `DDN_BUILD_DIR`, platform cache 또는 temp 순으로 결정하며
   `I:/home/...`, `C:/ddn/...` 고정 경로를 제거했다.
4. G14 runner의 세 실제 입력 closure를 manifest에 명시했다.
5. deterministic projection tool을 추가했다. dirty worktree가 아니라 exact full Git
   commit만 authority로 받으며 zero-match, duplicate output, unsafe path와 non-regular
   entry를 fail-closed한다.
6. Windows에서 `git archive`가 text checkout filter를 적용해 exact public SPEC bytes를
   CRLF로 바꾸는 결함을 발견했다. 투영 입력을 `git ls-tree` + `git cat-file blob`으로
   교정해 commit blob bytes를 그대로 보존했다.
7. projection validator를 추가해 exact file set, byte/hash/tree identity, required role,
   local SPEC link, private path/include와 source-commit authority를 fail-closed한다.
8. clean detached fixed HEAD에서 rights provenance와 locked Cargo/npm dependency 및
   local license-material custody 원장을 A/B로 생성해 바이트 동일성을 확인했다.

## R3J deterministic projection과 fresh repository

```text
SOURCE_COMMIT: b88d7a9016d1a03c54b62f9ad76b7a7f78e653bc
SOURCE_TREE: git-tree:8c38d26bbce348b51d5a335fe1678c676ba97194
FILE_COUNT: 894
PROJECTION_A: I:/home/urihanl/ddn/codex/build/public-self-containment-fu01/projection-r3j-a
PROJECTION_B: I:/home/urihanl/ddn/codex/build/public-self-containment-fu01/projection-r3j-b
PUBLIC_TREE_A: sha256:64ae162a4217c45c2d2636cbbe91e6354da0b13c893de371a80b0be3c2cf4b58
PUBLIC_TREE_B: sha256:64ae162a4217c45c2d2636cbbe91e6354da0b13c893de371a80b0be3c2cf4b58
A_B_BYTE_IDENTITY: PASS
VALIDATION_RECEIPT_A_B: sha256:72d76baff99fe731d91dac7bd51e32556a65c065f57a4efc94a6ed2b3736f39e
FRESH_REPOSITORY_COMMIT_A_B: ac98fe511ee4f79b4939bef4b3a87f04257b02e3
FRESH_REPOSITORY_TREE_A_B: d7fe9054139f9b99f5a776749f7e4ac38ea5ed6c
FRESH_REPOSITORY_STATUS_A_B: CLEAN_0
PUBLIC_SPEC_SEAL_ROWS: PASS_29_OF_29
PUBLIC_SPEC_MANIFEST_SHA256: c3768144f426b84ef0bc4db5b4e1198948473c67e9a297e8f7b0bbf5e6e90bfb
PUBLIC_SPEC_SEAL_SHA256: caa0d1df749216daa46b1db68db48aad5595d40b622d7601f9903b60a5e2b887
PUBLIC_SPEC_CURRENT_SHA256: 6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0
```

R3D/R3E의 CRLF output과 R3H/R3I의 checkout-relative tool identity는 실패 후보로
보존하며 PASS 근거로 사용하지 않는다. R3J는 projection/validator identity를 projected
exact blob에서 도출해 checkout filter와 독립적이다.

## 검증

```text
projection tool tests: PASS 6/6
projection validator tests: PASS 12/12
fresh repository combined tests: PASS 18/18
R3J non-browser role/hash/security/validation-receipt validation: PASS 894/894 A/B
R3J full SPEC link validation: EXPECTED RED / 10 missing linked trees
R3J full Workbench role validation: EXPECTED RED / WORKBENCH_RUNTIME missing
fresh root workspace test compile --no-run: PASS
fresh ddonirang-tool library: PASS 517/517
fresh G14 CLI/WASM expected-rejection parity: PASS 3/3
official source-built WASM A/B: PASS byte-identical 6/6 files
R3J versus R3F Rust/WASM source inventory diff: 0
active source private-path scan: PASS 0 findings
source fixed-head gaji/std_math test: PASS 1/1
source fixed-head tool binary tests: 405 PASS / 2 FAIL
fresh projected tool binary tests: 388 PASS / 19 FAIL
fresh projected teul-cli tests: 1145 PASS / 15 FAIL
```

## R3K projected tool runtime fixture successor

R3J의 projected tool 추가 17 RED를 직접 분류해 `#[cfg(test)]` runtime fixture
custody만 교정했다. private pack 공개 membership, 제품 runtime fallback과 의미 변경은
없다.

```text
PRODUCT_TEST_FIXED_HEAD: 91e56e597a920a8346e18bf68fa80afadf92d3aa
SOURCE_TREE: git-tree:7033fa8e8385bf0c6ab832b7bb64d3f5b0ffbde1
R3K_PUBLIC_TREE: sha256:7459ce5d8894cce06756fb804ce1d5dcc8be1c69266ddc9927030cf2cfc17031
R3K_VALIDATION_RECEIPT: sha256:41b4e5b925991d91182ffaa53ff4991939eebe1e8958527a6c43e5afc1707015
R3K_FRESH_COMMIT_A_B: bb5b646ed72620f9942a460f9ea8bf4c744b7dbd
R3K_FRESH_TREE_A_B: a3bc8b2da6392734e07add737e4b9a1de8578fb9
SOURCE_TOOL_BINARY: 405 PASS / 2 ai-prompt RED
PROJECTED_TOOL_BINARY: 405 PASS / 2 ai-prompt RED
PROJECTION_CAUSED_TOOL_RED: 0
```

`teul-cli`의 real `gaji/std_math` parity 1건은 D3 rights/membership 결정 없이
synthetic으로 바꾸거나 공개 projection에 포함하지 않았다. 따라서 G28 전체는 PARTIAL,
G18/G21/G27~G31과 publication readiness는 계속 OPEN이다.

`git diff --check 799ac30a..fixed-head`는 exact live public SPEC custody 파일
`publish/spec/CURRENT.md`의 기존 trailing blank line을 보고한다. 이 파일은 shared live
pointer와 SHA-256 `6ca95223...`가 같은 입력이므로 경고 제거를 위해 바이트를 고치지
않았다. 해당 exact authority file을 제외한 구현·테스트·인계 diff check는 PASS다.

source-built WASM identity:

```text
ddonirang_tool_bg.wasm: 186f4fec75bfa2e0059eeb8fe4e0b830aed5f04a24caf88b46b25a8bb432b171
ddonirang_tool.js: 16b4de4cac8bfebbc7d7f881ab1241b0d22d652ff8ad00b9045f40c81d7c90a9
ddonirang_tool.d.ts: 3f7f02aaffc0fb50146f47c4350bcaadb607d26ab2dd88e9b03bb82d9a3f1fec
package.json: 223687f3faa5ab0f3552070ca639ba343186ded73627b712cc2a5e27ef439fa3
```

tracked WASM은 수정하지 않았다. tracked `ddonirang_tool_bg.wasm`은
`77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34`로
source-built와 다르므로 final promotion은 OPEN이다.
R3J successor correction은 projection Python source/tests만 바꿨고 Rust/WASM
inventory diff가 0이므로
R3F official A/B 결과를 그대로 재사용할 수 있음을 직접 확인했다.

## G23/G24 candidate evidence

```text
DEPENDENCY_ROWS: 199 (Cargo 196 / npm 3)
UNDECLARED_CARGO_LICENSE: 0
LOCAL_CARGO_LICENSE_MATERIAL: 191_OF_196
MISSING_LOCAL_LICENSE_MATERIAL: 5
SELECTED_LICENSE_RESOLVED: 0_OF_199
REQUIRED_NOTICE_RESOLVED: 0_OF_199
RELEASE_INCLUSION_RESOLVED: 0_OF_199
LEDGER_A_B_BYTE_IDENTITY: PASS_3_OF_3
```

세 원장의 SHA-256은 `RIGHTS_AND_DEPENDENCY_LEDGER_R3G.md`에 봉인했다. first-party
provenance는 code 1,050 files, docs 20, PC01 pack 5, selected examples 33, assets 2를
분류했지만 Git authorship을 ownership/public permission으로 승격하지 않았다. live
projectile lesson exact blob도 fixed-head object database에 없으므로 자동 포함하지 않았다.
G23/G24는 `CANDIDATE_EVIDENCE_LANDED / RELEASE_RESOLUTION_OPEN`이다.

## RED 분류

- source fixed-head의 2건: `ai-prompt`가 branch에 없는 internal SSOT directory를
  runtime에 요구한다. public SPEC으로 자동 대체하면 authority meaning을 바꾸므로
  교정하지 않았다.
- fresh projection의 추가 17건: `tool/src/main.rs` unit tests가 internal pack fixture를
  runtime에 읽는다. source fixed-head에서는 모두 GREEN이므로 product regression이
  아니라 public test closure/rights 문제다.
- fresh teul-cli의 추가 1건: 제외된 `gaji/std_math`를 읽는 unit test다. source
  fixed-head에서 1/1 GREEN이다.
- teul-cli 공통 14건은 baseline `799ac30a...`에서도 같은 의미 RED였던 기존 debt다.
- exact public `CURRENT.md` 링크 11개 중 v0.6.0 하나만 존재하고 historical/candidate
  10개가 누락된다. shared live root에서 열 개 tree 모두 존재하지만 Git 미추적임을
  확인했다. CURRENT bytes를 고치거나 untracked history를 자동 포함하지 않았다.

## 아직 통과하지 않은 gate

```text
G18_EXACT_PUBLIC_SCOPE: OPEN
G21_FULL_RECURSIVE_CLOSURE: OPEN
G22_PUBLIC_FACADE: CANDIDATE_PREPARED / PUBLIC_MEMBERSHIP_AND_LICENSE_FINALIZATION_OPEN
G23_RIGHTS_LEDGER: CANDIDATE_EVIDENCE_LANDED / RELEASE_RESOLUTION_OPEN
G24_DEPENDENCY_LICENSE_LEDGER: CANDIDATE_EVIDENCE_LANDED / LICENSE_NOTICE_OPEN
G28_ALL_UNIT_AND_LINK_TESTS: OPEN
G25_DETERMINISTIC_PROJECTION: NON_BROWSER_CANDIDATE_PASS_WITH_CONCRETE_VALIDATION_RECEIPT
G26_FRESH_REPOSITORY: NON_BROWSER_CANDIDATE_PASS_A_B_IDENTICAL
G30_TEN_MUTATIONS: EXACT_STRUCTURAL_MATRIX_PASS_10_OF_10 / ACTUAL_FULL_PRODUCT_GATE_OPEN
G31_REAL_EDGE: NOT_RUN
G32_NEXT_PRODUCT_VERTICAL: NOT_STARTED
```

Owner 결정을 기다리는 동안 임의의 공개 membership, license, public authority bundle,
Workbench/browser bundle 또는 tracked WASM promotion을 선택하지 않는다. 다음 안전 관문은
위 항목의 exact Owner 입력과 이 제한 fixed-head에 대한 독립 검토다.

## 보호 자원

```text
OFFICIAL_DB: 573440 bytes / 3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0
OFFICIAL_DB_WRITE_COUNT: 0
PID_53196: ABSENT / NOT TOUCHED
127.0.0.1:8787: NOT LISTENING / NOT TOUCHED
ACTIVATION_CALL_COUNT: 0
GITHUB_MUTATION_COUNT: 0
HUMAN_PASS_NOT_CLAIMED
external_user_success_count: 0
```
