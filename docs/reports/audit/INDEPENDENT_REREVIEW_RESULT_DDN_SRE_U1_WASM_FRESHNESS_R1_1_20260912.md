# SRE-U1 tracked WASM freshness R1.1 — 좁은 독립 재검토

## 판정

```ini
VERDICT = PASS_TARGET_BOUND
TARGET = SRE_U1_TRACKED_WASM_FRESHNESS
```

이 판정은 아래의 고정 제품 target과, 그 제품 바이트를 바꾸지 않고 custody 해시만 바로잡은 handoff successor에 한정한다.

```ini
PRODUCT_COMMIT = be6e56cf5dda3afa38738cce8e19468e7920f5c1
PRODUCT_TREE = 1e9a6b38dde7facc0fec8eb305d3c7f635be5592
PRODUCT_PARENT = 4971b76c18a039f93fda01fbb744a80ed19100b1
ORIGINAL_HANDOFF = ff8316046c9d7651bf2ec6d94acc6caa2000bc5b
CUSTODY_CORRECTION_HANDOFF = e8bfcc75dc4062d6614a833d14b9fc12894d882f
CUSTODY_CORRECTION_TREE = 999c10196ff43e598b6193fe4ced68b87e5599da
CUSTODY_CORRECTION_PARENT = ff8316046c9d7651bf2ec6d94acc6caa2000bc5b
PRODUCT_PATH_DIFF_AFTER_CORRECTION = 0
```

## Custody correction

원 handoff에 적힌 manifest SHA-256 `3A1E2409AB46F1A280724717EBD6C2DB7A2E205C3262F82743FBEE3AA873CCD6`은 raw Git blob의 SHA-256과 달랐다. 이는 제품 manifest 바이트 결함이 아니라 handoff metadata 기록 오류였다. R1.1 handoff successor가 raw Git bytes의 올바른 값을 봉인했다.

```ini
ARTIFACT_BLOB = 7bdecd2206353557ce1b40465fec23bf78f42578
ARTIFACT_SHA256 = 9193D07F0438056F111A17250E81F39312DEBAF92CCE8E26D7E8A7EE2DF9CAC2
ARTIFACT_BYTES = 5710921
MANIFEST_BLOB = f35010928a26e4bc3755e2089c725ae858183672
MANIFEST_RAW_GIT_SHA256 = CF4AE8F3B6D4DF60101101B029046772012058BDE4C4F31A6FDFE1A5ED7015E3
MANIFEST_RAW_GIT_BYTES = 35028
```

## 실행 근거

제품 tree가 correction 전후 동일함을 확인한 clean detached rereview worktree에서 다음을 수행했다.

```text
python tests/run_ddn_cli_wasm_freshness_check.py                         PASS
cargo test -p ddonirang-lang sre_ --offline                              PASS (3/3)
cargo test -p ddonirang-tool sre_public_pin_binds_the_distinct_local_binder_at_runtime --offline
                                                                            PASS
```

동일 product tree에 대해 correction 이전 narrow review에서 이미 실행된 다음 제품 근거도 재사용했다.

```text
scripts/build_wasm_tool.ps1 -Profile release -Target web -CopyToUi:$false
  -> compiler stage PASS; produced artifact byte-identical to tracked artifact
cargo check -p ddonirang-tool --lib --target wasm32-unknown-unknown --features wasm --offline
  -> PASS
node tests/ddn_cli_wasm_post_wasm_shared_changes_runner.mjs              PASS
```

위 재사용은 product artifact/manifest path diff가 0인 것을 먼저 확인한 뒤에만 했다.

## Disposable mutation evidence

```text
M1 stale artifact reinjection
  RED: freshness checker reported wasm_sha256 and wasm_size mismatch.
  RESTORE: blob 7bdecd2206353557ce1b40465fec23bf78f42578,
           SHA-256 9193D07F0438056F111A17250E81F39312DEBAF92CCE8E26D7E8A7EE2DF9CAC2
  GREEN: freshness checker passed after exact restore.

M2 manifest source-tree hash corruption
  RED: freshness checker reported source_tree_sha256 mismatch.
  RESTORE: blob f35010928a26e4bc3755e2089c725ae858183672,
           SHA-256 CF4AE8F3B6D4DF60101101B029046772012058BDE4C4F31A6FDFE1A5ED7015E3
  GREEN: freshness checker passed after exact restore.
```

## Nonclaims

이 판정은 SRE-U1 ParamPin 일반 의미, 전체 CLI/WASM 동등성, 전체 Fixed64 migration, V1 readiness, release, public support 또는 Human PASS를 주장하지 않는다. 그 범위들은 이 좁은 tracked-WASM freshness target 밖이다.
