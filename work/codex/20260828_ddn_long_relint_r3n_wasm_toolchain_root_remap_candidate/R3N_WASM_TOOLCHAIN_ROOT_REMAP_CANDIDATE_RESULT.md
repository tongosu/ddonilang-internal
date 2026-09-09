# R3N WASM toolchain-root remap candidate 결과

## 판정

```text
DDN_LONG_RELINT_R3N_WASM_TOOLCHAIN_ROOT_REMAP_CANDIDATE_IMPLEMENTED_UNDER_REVIEW
OPTION_A_REMAP_TOOLCHAIN_ROOTS_IMPLEMENTED_UNDER_REVIEW
CANDIDATE_A_B_C_RAW_BYTE_IDENTICAL
EMBEDDED_INTERNAL_ABSOLUTE_PATH_COUNT_0
FULL_PROJECTION_VALIDATOR_PASS
SECURITY_SCAN_ALL_FILES
TRACKED_WASM_DIFF_0
DEFAULT_BUILD_CONTRACT_NOT_PROMOTED
PUBLIC_NON_BROWSER_WASM_MEMBERSHIP_OPEN
HUMAN_PASS_NOT_CLAIMED
```

독립 판정, tracked refresh, public membership, publication readiness 또는 release를
주장하지 않는다.

## 권위와 계보

- 시작 parent: `c177f5e9829c5d5d5baab8f1beb39718423e05e7`
- Owner 결정 결속: `652db180aaa78cbf29c42a0815875a2aa1f7555d`
- 제품·테스트 fixed HEAD: `5c4a7684e3a041a4e5775ec14fac93aa40db0f09`
- fixed tree: `49f280bc93ea0733100772f316987f1f8f314f5b`
- live internal SSOT: v25.15.0, 읽기 전용
- live public SPEC pointer: v0.6.0
- `docs/ssot/CURRENT.md`의 v0.5.0 표기는 `AUTHORITY_METADATA_DRIFT`; 실제
  `publish/spec/CURRENT.md` v0.6.0이 통제하며 SSOT는 수정하지 않았다.

## G1~G2: 115건과 RED 기준선

정확한 115행 원장은 `R3N_115_PATH_EXACT_INVENTORY.detjson`에 있으며 SHA-256은
`d7b03da90186cf1ef334a34f214be0a5cc22f3ab34693c0cf436294b7abc191a`이다.
tracked, official A, official B 원장은 모두 이 hash와 byte identity가 같았다.

| family | count |
|---|---:|
| CARGO_REGISTRY_ROOT | 94 |
| RUSTUP_TOOLCHAIN_ROOT | 21 |
| REPOSITORY_ROOT | 0 |
| CARGO_HOME_OTHER | 0 |
| TOOLCHAIN_OTHER | 0 |
| UNKNOWN | 0 |

115개는 모두 WASM section id 11에 있었고 문자열 중복 0, credential 표시 0,
compile-input remap 가능으로 분류됐다. 기존 official repository-only build는 A/B가
deterministic하고 tracked WASM과 hash가 같지만 115건을 유지했다. candidate 이전
projection validator는 tracked WASM에서 정확히
`E_PUBLIC_INTERNAL_ABSOLUTE_PATH`로 RED였다. repository root remap만으로 registry 94와
toolchain 21이 남는 반례를 보존했다.

## G3~G4: candidate contract와 공격

기본 `scripts/build_wasm_tool.ps1` 동작은 기존 repository-only remap으로 유지하고,
명시적 `-SourceRemapMode candidate`만 다음을 수행한다.

- fixed HEAD Git blob의 LF local materialization
- repository → `/ddn-src`
- Cargo registry → `/ddn-cargo-registry`
- Rust sysroot/toolchain → `/ddn-rust-toolchain`
- inherited Rust flags, tracked copy, dirty source, missing/duplicate/overlap root를 fail-closed
- physical root를 제외한 policy identity와 artifact identity 봉인

policy identity는
`sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a`이다.
drive/case/slash/trailing separator, sibling-prefix, nested root, missing registry/sysroot,
duplicate root, URI/UNC/device, spaces/Unicode, unknown path, policy/receipt 변조를 unit 및
targeted probe로 공격했다. source suite 53/53과 별도 normalization/policy probe 7/7이
GREEN이었다. validator의 UNC 정규식은 arbitrary binary backslash를 경로로 오인하지
않도록 exact host/share grammar로 정밀화했으며, 실제 UNC/device/drive/file URI는 계속
RED다. binary/hash 예외와 broad allowlist는 0이다.

## G5~G6: A/B/C와 전수 검사

최종 fixed HEAD에서 서로 다른 clean-detached worktree, fresh target/output을 사용했다.

- A: LF invoking checkout
- B: CRLF invoking checkout
- C: 반복 LF invoking checkout

초기 시도에서 A=C였지만 B WASM은 CRLF compile-time included bytes 때문에 달랐다.
이를 실패 증거로 보존하고 source를 수정하지 않은 fixed-HEAD LF materialization을
candidate contract에 결속했다. 최종 A/B/C는 7개 artifact와 receipt 전부 byte-identical이다.

- candidate WASM: `48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f`
- receipt semantic identity:
  `sha256:77e707bc2733ef4d7914455b9436e6d23704b19070fb1fd3cbd76e8a1b75a5d1`
- build entrypoint Git blob:
  `33b2db4e0707c034ce8ac239dc85e90b05829e73293ac9fa3405ca8cd645636a`

7개 artifact 전수 검사 결과는 internal absolute 0, private include 0,
official-store 0, unknown 0이다. WASM 12개 section의 size/hash는
`R3N_CANDIDATE_FAMILY_INVENTORY.detjson`에 봉인했고 그 파일 SHA-256은
`c533c07053fff98863930d6922dc09f60b39e0dca410dcaf8267dc32ebef4ee1`이며 A/B/C 원장도
byte-equivalent다. candidate receipt `.detjson`은 key 이름이 아니라 모든 string value를
구조적으로 검사하며 악성 value fixture는 RED다.

## G7: isolated projection

tracked family를 수정하지 않고 projection output에서만 A/B candidate family를
substitute했다.

```text
TOTAL_PROJECTED_FILES: 895
SECURITY_SCANNED_FILES: 895
SCANNED_ROLE_COUNT: 18
UNSCANNED_SECURITY_RELEVANT_FILES: 0
PUBLIC_TREE_IDENTITY: sha256:7f2bcb7ddc3689f013d1757ab4c7b91422dee4173c447cb1226a79443a12ab6c
VALIDATION_RECEIPT: sha256:c63d09f7c08916e08400edf4f090d69cf732fa9d7a0d8f79ba79510224e72351
```

projection A/B의 tree, projection receipt, validation receipt, substitution receipt가 모두
byte-identical이다. `--require-spec-links`의 10개 historical link RED는 기존 D2
review-bound history membership OPEN을 그대로 드러내며 R3N 성공 관문으로 재해석하지
않았다.

## G8 회귀

```text
source projection/remap/entrypoint/validator Python: PASS 53/53
projection R3M projector/validator Python: PASS 35/35
source ddonirang-tool library: PASS 517/517
projection ddonirang-tool library: PASS 517/517
source tool binary: 405 PASS / expected ai-prompt authority RED 2
projection tool binary: 405 PASS / same expected ai-prompt authority RED 2
projection-caused additional RED: 0
source G14: PASS 3/3
projection G14: PASS 3/3
public SPEC raw-git-blob seal: PASS 29/29
```

R3L custody byte 보존:

- 107-path ledger: `704d48bd3ef50a28d1a800162312edc03ef75e54cf8f65790597121fe7b18321`
- NOTICE draft: `dbdf6b2671eba3002e86e9255a1ebaf6d0143a566810c3dfdbe342f2fcedd540`
- read-only audit: `0e1b666cd55bd10c99588af210dcf9b2c0d756e21a3b32d4716e02d37f8a4a08`
- facade NOTICE: `bc08698db3f17bcaed0f07784610234f0998dd50250cca76b5e1efb13f42a479`

## 보호 경계와 OPEN

- tracked WASM/manifest/JS/d.ts/package diff 0, write 0
- Workbench UI diff 0
- `docs/ssot/**` diff 0
- `publish/spec/**` diff 0
- official DB: 573440 bytes,
  `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`, write 0
- PID 53196: 시작·종료 모두 ABSENT / not touched
- 127.0.0.1:8787: 시작·종료 모두 NOT LISTENING / not touched
- activation, public push, network download: 0

OPEN: independent rereview, public SPEC linked-history membership, five missing local license
materials/legal selection, browser/offline bundle membership, tracked candidate refresh,
public non-browser WASM membership, publication/release/activation/Human PASS.
