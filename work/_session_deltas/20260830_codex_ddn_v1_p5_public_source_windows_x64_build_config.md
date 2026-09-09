# 2026-08-30 DDN V1 P5 public-source Windows x64 build config

- Live authority was revalidated read-only as internal SSOT v25.35.0 / RD-001~490 and public Language SPEC v0.6.0.
- Product baseline `3553735988dcb2476fda7d9c769552b56c8bb1c8` had no public-projection rule for `.cargo/config.toml`; the bounded check failed closed as `E_PUBLIC_WINDOWS_CARGO_CONFIG_MISSING`.
- Product fixed `b1fd4c174634a2a851e6c1a3e1fe72ab97f6db62` changes only `tools/public_cargo_config.toml` and adds the portable Windows `/STACK:16777216` linker setting.
- The projected config is byte-identical: 144 bytes / SHA-256 `454a4ba886da1e98d2d44bf85d91babd1a6a3d3178ae381195b759750404ede5`.
- Existing official tools produced and validated a 897-file public-source projection. Final tree identity is `sha256:b3777d6a62f3190e87f7bd6feb0128dbbf9960a59b2f2dcab9744ed88935876b`; validation receipt is 613 bytes / SHA-256 `8dab3c45cda2fd6c6a39a70a38adea5ab571373152b4d5d37c4478bdeb279415`.
- Offline Windows release builds of the workspace and `teul-cli` passed. Both `ddonirang-tool.exe` and `teul-cli.exe` start successfully and have PE stack reserve 16,777,216 bytes.
- Existing projection/remap/validator tests passed 61/61. New runner/pack/checker/meta-test count is 0.
- Candidate WASM is 5,559,604 bytes / SHA-256 `cf4062081dec66e74057b5029b90e198de5390610e7c0c71763a95edfee6c232`; candidate semantic identity is `sha256:1d6450b278eb8e92c56c79a4966bcb03b42332c53b4eea0b368c794c95aa3dbc`. Tracked WASM write is 0.
- Native binaries still contain build-host absolute path prefixes and remain external build output. Path-clean native artifact, package identity, rights/license/distribution, independent review, P5 closure and release remain OPEN.
- SSOT/SPEC/UI/membership/release transitions are 0. TCP 8787 listener is absent and protected process lifecycle commands are 0.
- Four pre-existing task-custody untracked session files remain preserved and unstaged.
