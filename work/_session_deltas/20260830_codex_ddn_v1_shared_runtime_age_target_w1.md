# 2026-08-30 DDN V1 shared runtime AGE target W1 session delta

## 결정

- live v25.35.0/RD-001~490와 public SPEC v0.6.0을 read-only 재검증했다.
- P2 durable save/reopen은 exact physical contract가 Owner-open이고, VC15는 typed morphology physical schema가 product-open이라 구현을 추론하지 않았다.
- 이미 존재하는 public CLI `--age-target`이 shared runtime에서 거부되는 실제 workflow blocker를 다음 safe product vertical로 선택했다.

## 구현

- `DdnProgram`의 기존 default 생성자는 그대로 두고 explicit `AgeTarget` 생성자를 추가했다.
- runtime surface가 invocation-local AGE target을 shared parser/canon/runtime gate에 전달한다.
- teul-cli는 기존 `AgeTarget::parse`를 사용하며 unknown 값은 `E_CLI_AGE_TARGET`으로 fail-closed한다.
- 명시 AGE identity는 summary/envelope/run identity에 결속했다.
- model source에서 명시 AGE 옵션은 묵살하지 않고 기존 unsupported contract를 유지한다.

## 검증

- RED: shared runtime이 explicit AGE를 generic unsupported로 거부.
- GREEN: native 1/1, CLI 1/1.
- mutation: explicit target -> global default fallback 주입 시 RED exit 1; exact restore 후 GREEN.
- tool lib: 526/526 PASS.
- clean-target teul full: 1044/1058 PASS; AGE 새 test PASS, 비관련 기존 축 14 FAIL 보존.
- product fixed: `926175c52b42fca0e36d2891a37260ec3f69f6d1` / tree `15b0295f55e2b7ab6b32ca6c5a65566d15491361`.

## custody

- 같은 worktree/branch/single writer를 재사용했다.
- 기존 VC17/P1 custody untracked 4개는 byte 수정/stage/commit 0으로 보존했다.
- docs/ssot, publish/spec, tracked WASM, visible UI, public membership/release transition 0.
- 새 review task/worktree/branch/pack/runner/meta-test 0.

## 다음

- 이 fixed product vertical은 기존 rolling reviewer의 다음 coherent product milestone 후보로 관리에 반환한다.
- P2 physical contract 또는 VC15 physical schema가 Owner-bound되기 전에는 해당 의미를 구현하지 않는다.
