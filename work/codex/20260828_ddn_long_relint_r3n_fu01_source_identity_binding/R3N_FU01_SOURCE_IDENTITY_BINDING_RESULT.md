# R3N FU01 source identity 결속 결과

## 상태

```text
R3N_FU01_SOURCE_IDENTITY_BINDING_IMPLEMENTED_UNDER_REVIEW
R3N_FU01_TARGETED_REREVIEW_PENDING
R3K_R3L_R3N_PLAIN_PASS_NOT_YET_ISSUED
PUBLIC_RELEASE_NOT_AUTHORIZED
HUMAN_PASS_NOT_CLAIMED
```

이 문서는 독립 PASS 또는 public membership을 주장하지 않는다.

## 계보와 권위

- starting parent: `614d1b5f5ee77036fa84077bd18d899e1a6d5839`
- reviewed product HEAD: `5c4a7684e3a041a4e5775ec14fac93aa40db0f09`
- reviewed handoff: `a34ee611e4c82d70e35d89c23869016c76813e78`
- product/test fixed HEAD: `9389563e752fcc63b0425e05671473e1adb42ced`
- fixed tree: `bb48137289d0a2907039f902451764ad0a61e060`
- internal SSOT: v25.15.0, read-only
- public SPEC: v0.6.0, `publish/spec/CURRENT.md` 기준
- `docs/ssot/CURRENT.md`의 과거 public SPEC 표기는 metadata drift이며 이 세션은 수정하지 않았다.

## F1 — candidate/projection source identity

`tools/wasm_candidate_remap.py substitute-projection`은 출력 파일을 쓰기 전에 다음을
검사한다.

```text
candidate_receipt.source_commit == projection_receipt.source_commit
"git-tree:" + candidate_receipt.source_tree == projection_receipt.source_tree_identity
```

누락·malformed·불일치 진단은 모두
`E_WASM_CANDIDATE_PROJECTION_SOURCE_IDENTITY_MISMATCH`이다. Candidate semantic receipt를
identity 재계산 없이 변조하면 기존 `E_WASM_CANDIDATE_RECEIPT_IDENTITY`가 먼저 발생한다.

docs-only successor, candidate commit/tree, projection commit/tree, 필드 누락, malformed,
semantic receipt 변조를 unit test와 실제 CLI subprocess로 공격했다. 모든 source mismatch
RED에서 artifact copy, manifest, tree, receipt, partial output mutation은 각각 0이다. Exact
fixed product HEAD candidate와 projection은 정상 결속됐다.

## F2 — 115 offset bijection

`R3N_FU01_115_OFFSET_BIJECTION.detjson`은 각 원본 문자열에 다음 필드를 봉인한다.

```text
ORIGINAL_PATH
ROOT_CLASS
RAW_WASM_BYTE_OFFSET
BYTE_LENGTH
ORIGINAL_BYTE_SLICE_SHA256
REMAP_TARGET
CANDIDATE_OCCURRENCE_COUNT
```

- CARGO_REGISTRY_ROOT: 94
- RUSTUP_TOOLCHAIN_ROOT: 21
- UNKNOWN: 0
- TOTAL: 115
- original offset bijection: 115/115
- duplicate or missing offset: 0
- candidate internal path: 0
- candidate occurrence mismatch: 0
- ledger SHA-256: `4fbef623a721b92a3e62964543750d92dd573630931bc46ac1c70ecdcda6c7e2`

## F3 — 실제 CLI 15축

`tests/run_r3n_fu01_cli_attacks.py`는 내부 함수를 직접 호출하지 않고 모든 축에서
`python tools/wasm_candidate_remap.py ...` subprocess를 실행한다.

- DIRECT_CLI_ATTACKS: 15/15
- EXPECTED_RED: 15/15
- EXACT_RESTORE_GREEN: 15/15
- RESIDUE_COUNT: 0
- ledger SHA-256: `f651a5ca199c81f2bdbc8b275491008386c840b95d576955bb58e2d75a0aff18`

공격 축은 duplicate/overlap/missing root, drive/file URI/UNC/device path, docs successor,
candidate/projection commit/tree 변조, missing/malformed identity, semantic receipt 변조다.

## candidate A/B/C

공식 `scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi $false
-SourceRemapMode candidate`만 사용했다. `CARGO_NET_OFFLINE=true`, 서로 다른 fresh output
root, tracked copy 0이다.

- A/B/C source commit: `9389563e752fcc63b0425e05671473e1adb42ced`
- A/B/C source tree: `bb48137289d0a2907039f902451764ad0a61e060`
- A/B/C WASM: `48be0af0f5cdb3cae78414b42d7cb519961994b9df387cdcc2dbc985487e043f`
- A/B/C semantic receipt: `sha256:f5c86581aa156e9c3b7416172bcad1c35197e581af61c4bf7126e17d2d24e40d`
- receipt file SHA-256: `d6a2c10ce9a0274560796af3c0fa98bb7b3f6b46b6eb30163473dc694dc5e004`
- 7/7 artifact and receipt bytes: A == B == C
- internal/private/official-store/unknown path: 0/0/0/0

## projection A/B

FU01 manifest SHA-256는
`77871658ebdb354ad9e3677423bba8d394a0c73cedd7e34a70e7d52a9c49d415`이다. Candidate와
projection을 모두 product/test fixed HEAD에서 생성했다.

- before tree: `sha256:e5d22628708d8c7b1a44b2be26a054e06530ba44e1a008b4a9ffa9dc17e60e60`
- substituted tree: `sha256:e56f10a18feeb7a9f27522abd3977dc0bb90d499194d9d64091968456b9c0dab`
- validation receipt identity: `sha256:d980d13ed353a5bdbdb1d324caa434b8d4e4a61b9c83c87343123a782aa66434`
- total/scanned files: 895/895
- scanned roles: 18
- unscanned security-relevant files: 0
- projection/tree/projection-receipt/validation/substitution bytes: A == B

과거 tree/receipt hash를 보존하지 않고 새 fixed HEAD identity로 정직하게 재계산했다.

## 회귀와 custody

- Python projection/validator/remap/entrypoint: 61/61 PASS
- source tool lib: 517/517 PASS
- projection tool lib: 517/517 PASS
- source binary: 405 PASS / 기존 ai-prompt authority RED 2
- projection binary: 405 PASS / 동일 RED 2 / 추가 RED 0
- source G14: 3/3 PASS
- projection G14: 3/3 PASS
- public SPEC v0.6.0 raw Git blob seal: 29/29 PASS
- R3L 107-path ledger: `704d48bd3ef50a28d1a800162312edc03ef75e54cf8f65790597121fe7b18321`
- R3L NOTICE: `dbdf6b2671eba3002e86e9255a1ebaf6d0143a566810c3dfdbe342f2fcedd540`
- R3L custody audit: `0e1b666cd55bd10c99588af210dcf9b2c0d756e21a3b32d4716e02d37f8a4a08`
- facade NOTICE: `bc08698db3f17bcaed0f07784610234f0998dd50250cca76b5e1efb13f42a479`
- official DB: 573440 bytes / `3fbf028e852dd3a13c3b84f812254de30c55113140f2b7869ff81a2a3b2b65f0`
- PID 53196: absent, not touched
- port 8787: not listening, not touched

## 보호 경계

tracked WASM/manifest refresh 0, public membership change 0, UI diff 0,
`docs/ssot/**` diff 0, `publish/spec/**` diff 0, official write 0, activation 0,
public push 0이다.
