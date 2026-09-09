# V1 Public Docs Latest Authority Refresh R1 — Handoff

## Fixed lineage

- predecessor adoption: `363f3e15f1ca149cb6d630469d49782902ca5ef1`
- predecessor independent FAIL custody: `d08d67b95789154992c05515ce9648d99f5fc453` (not merged/reverted/rewritten)
- product baseline: `2c78dad8d4ce9732054ced6441b830ce4e5b032d`
- factual-refresh fixed commit: `ee700e8e73b4213104d7f4f7517b0a3cb3f006cc`
- fixed tree: `28c4ed65e554c16283dca7445bb8bfacca9b17d1`
- fixed parent: exactly `2c78dad8d4ce9732054ced6441b830ce4e5b032d`
- fixed diff: exactly `publish/v1/CURRENT.md`, one factual line

## Live authority verification

- internal CURRENT: `v25.22.0 / RD-001~469`
- `docs/ssot/ssot/CURRENT.md`: SHA-256 `6fa12c5420a44939eeaa09e09653da952daa0b5fc5624590e1e7dede215e9f0e`
- `SSOT_ALL_v25.22.0.md`: SHA-256 `9ff9a3110cd95604834d32568f3395d798b2a30bac4e7c7ab4feaeab3760ee73`
- `SSOT_ALL_MANIFEST_v25.22.0.md`: SHA-256 `0c2029ac4a00b88b84c91a66701c79d3661dd0367d07d35f53dbf21d49ed91fa`
- `CURRENT_SHA256_v25.22.0.md`: SHA-256 `d2d0d67b36bca2bb4ed9ce0ea82dc0d14f9a2915f9239a5a66deb424c9fd50a8`
- public SPEC CURRENT: v0.6.0, SHA-256 `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0`
- authority source preserves v25.21.0 as displaced-live custody and not automatically merged.

## Frozen public-document set

| path | bytes | SHA-256 | content change reason |
|---|---:|---|---|
| `publish/v1/CURRENT.md` | 2209 | `f556fa811245bab0b23c43f05c7099f00cf0ff05ac9b444025f8ef5ca70c1082` | factual authority reference `v25.19.0` → `v25.22.0 / RD-001~469` |
| `publish/v1/QUICKSTART.md` | 1469 | `3465f74ed2b19bb7cc42b1c9df82dbc78505363e295ea444a72cbea2299890b5` | unchanged; predecessor hash preserved |
| `publish/v1/LANGUAGE_GUIDE.md` | 2867 | `dd904ce39b7e9f203d9efe9ee5f2a6bac2c633444258fa65980da411383b5d71` | unchanged; predecessor hash preserved |
| `publish/v1/SUPPORT_MATRIX.md` | 5896 | `cdd6d2517e418afb6b0c9589971c7310798e8148635f91866a4002c85b454695` | unchanged; predecessor hash preserved |
| `publish/v1/DETERMINISM_AND_PROJECTS.md` | 1465 | `7152a6e4880c82b408427252548fb06a7de4358bb5bb526a95475ce063bb0bdb` | unchanged; predecessor hash preserved |
| `publish/v1/ROADMAP.md` | 1911 | `5121f45d96bdca57a31164a71589318421103ca4bb5851f5294db4dbad43f369` | unchanged; predecessor hash preserved |

## Direct validation

- `INTERNAL_CURRENT_REFERENCE=v25.22.0/RD-001~469`: PASS
- `PUBLIC_SPEC=v0.6.0`: PASS
- PRE_RELEASE: YES
- PRODUCT_RELEASED: NO
- `SUPPORTED_FOR_V1_COUNT=0`
- `PRODUCT_PASS_MEMBERSHIP_PENDING_COUNT=0`
- `VERIFIED_PUBLIC_EXAMPLE_COUNT=0`
- UTF-8 without BOM and LF-only: 6/6
- local links: 7/7
- product code/test/pack/WASM/UI diff: 0
- docs/ssot diff: 0
- publish/spec diff: 0
- membership/release transition: 0
- task-owned VC17 census/validation residue: byte-preserved, unstaged/uncommitted

## Review contract

Reuse only reviewer thread `01a04b17-66bb-7fa3-b827-53ad450005b4` and existing worktree `C:/Users/ddongosu/.codex/worktrees/3a1f/codex` after management binding. Review the fixed six-file set and this factual refresh at fixed commit `ee700e8e73b4213104d7f4f7517b0a3cb3f006cc`. New reviewer/worktree/branch: 0. This handoff does not dispatch review.

## Anti-meta and nonclaims

- concrete blocker removed: stale internal normative-source identity in public CURRENT
- existing direct hash/link/text/Git checks reused; new test/pack/checker/framework 0
- meta-test 0
- independent PASS, P5/release, membership/readiness, activation and Human PASS remain OPEN
