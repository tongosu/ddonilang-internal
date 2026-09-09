# Rights-excluded public projection R2 dry-run receipt

## 입력과 결정성

- source commit: `b8530bd6eadcf79658a821f4e9b4538991b89b80`
- source tree: `git-tree:d31e634f9ba6dc6530df84a90e882e3bb52fb79f`
- projection policy/manifest SHA-256: `b154e516bb0f2a9aeb7e4769b46077fc606fb20252b1c5929cbc160a47b13cdd`
- projection tool SHA-256: `43d925e831b7f2dbf47c7208f724feefde89304462a4ebcd3ee385bcd6472be3`
- output tree identity A/B: `sha256:9cbe474b7c9220ef22f42ba6ad382cc29afb7d76d087a0ad6ce90c9fcc7db16f`
- A/B tree manifest SHA-256: `ac6f0162809d552327d51223e64fa6cf4798c04d3054f89e2641d63ce3817daa`
- A/B receipt SHA-256: `67526f797c335d60792c7e1082f89630a9b07cda6bf54ec3e279cb536484cf2d`
- file count from projection receipt: `897`

A/B file set와 bytes는 동일하다. PC01 pack, projectile, Workbench tree, SSOT, work, official store, node_modules는 exclusion ledger대로 빠졌다.

## validation result

- workspace `cargo check --locked --offline`: PASS
- tracked WASM freshness: PASS
- release `teul-cli --help`: PASS
- debug `teul-cli --help`: FAIL, stack overflow; release/public entrypoint 결과로 확대하지 않음
- workspace test compile: FAIL, 13 missing private/rights-excluded `include_str!` dependencies
- G14 public runner: FAIL, three legacy input files were not included by the dry-run manifest
- validation receipt: `OPEN`

따라서 deterministic projection 자체만 검증됐고 public repository readiness나 publication authorization은 아니다.
