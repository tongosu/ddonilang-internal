# [DDN V1 개발 독립검토 Work -> DDN V1제품마감Codex] DDN-V1-P5-CURRENT-SOURCE-WINDOWS-CANDIDATE-I1 — 독립검토 결과

## 판정

`PASS_TARGET_BOUND`

blocking finding은 0건이다. P5 public projection manifest의 `source_commit`은
current product source `873d3cb236e9f7ab40307bc55c305861e2d7aeef` / tree
`bf753c9d47c1d3706b27da2531aa619ea1c85309`에 정확히 결속되며, fresh
171-file projection, remapped candidate WASM custody, Windows x64 build와 실제
`project-run` output까지 같은 source identity chain으로 수렴했다. Historical
`27418362...` source를 재사용하면 reviewer primary Gate가 RED를 낸다.

이 판정은 product fixed `3e205ce8...`의 current-source Windows candidate slice에만
결속된다. strict SPEC-link closure, public command membership, whole P5/V1
closure/readiness, release/publication/activation/legal, Owner Human Smoke와 Human
PASS는 승인하지 않는다.

## 검토 계약

- `CLAIM`: public projection manifest가 historical snapshot이 아니라 current
  product source를 선택하고 그 source로 Windows x64 candidate가 재현되는가
- `TARGET_IDENTITY`: product fixed
  `3e205ce816e47d29f6488bd86d029750e6afaaf5` / tree
  `53ccc5091ef2722bca4e9dcc107960c830838e9f`
- canonical primary Gate: manifest, projection receipt, source tree, WASM
  substitution receipt와 validation receipt의 source commit/tree가 모두 exact
  current product source여야 함
- `CLOSURE_EVIDENCE`: direct Git lineage, one-line manifest diff, fresh Git-blob
  projection, source tamper, 56 reused tests, remap/validation, fresh Windows build와
  existing project-run byte parity
- `STOP_CONDITION`: historical source가 Gate를 통과하거나 current source projection,
  Windows build, teul exclusion 또는 project-run parity가 실패함
- `DEEP_RESEARCH_CHECK`: `NOT_USE` — fixed local Git/artifact evidence로 충분함

## Reviewer와 lineage custody

- reused reviewer worktree:
  `I:\home\urihanl\ddn\codex\build\worktrees\review-ddn-v1-vc09-named-callable-evidence-rebase-i1-20260829`
- 시작 HEAD: prior CLI authority review
  `181896585e6a5ce39a18a1a6a009e3ce50e7d9bf`
- 시작 상태: detached / clean / staged 0 / untracked 0 / merge 0
- baseline: `82faac1fce862543cf4e48a11adcbf3a94bb4965` / tree
  `0f2b160e9e19327409db4a6fb5bbcc60073fb37b`
- product fixed: `3e205ce816e47d29f6488bd86d029750e6afaaf5` /
  `53ccc5091ef2722bca4e9dcc107960c830838e9f`
- handoff/review parent: `ccaa7132e9192a26f003917ae4f2795482c4e74f` /
  `8d162131f0288c74a7e54952a69ea1638f8e7f80`
- fixed parent는 exact baseline, handoff parent는 exact fixed, 각각 parent 1 /
  merge 0 / direct lineage
- prior CLI review `18189658...`는 current product source의 direct parent이며
  baseline ancestor다. 그 PASS는 native shared test-workflow target에만 유지되고
  본 P5 판정으로 확대되지 않는다.
- new reviewer/task/worktree/branch/pack/runner/checker/meta-test: 0
- producer/shared dirty root write, stage, reset, clean, stash: 0

Fixed diff는 정확히 다음 manifest 한 경로의 `source_commit` 한 줄이다.

`work/codex/20260827_ddn_v1_product_closure_long_range_r1/P5_WINDOWS_X64_PUBLIC_SOURCE_RC_W1/PUBLIC_PROJECTION_V25_35_WINDOWS_X64_PATH_CLEAN_MANIFEST.detjson`

값은 historical `274183623f43c526975c7402ffa0fdf6e0d11e66`에서 current
`873d3cb236e9f7ab40307bc55c305861e2d7aeef`로 바뀐다. Fixed manifest는
8,695 bytes / SHA-256
`89176bca8386d2d3381d13df11d3fd9c555ab8f95aeb819f544ae5814b114e2c` /
Git blob `b20a9fa9459bb036bc74b31c5a56ae7ba3808cc3`다.

core/lang/numeric/proof/symbolic/tool/tools/tests/pack/solutions, tracked WASM,
`docs/ssot/**`, `publish/spec/**` diff는 전부 0이다. Handoff diff도 handoff와
producer session delta 두 문서뿐이다.

## Live authority refresh와 successor impact

검토 시작 시 shared Work root에서 read-only 재검증했다.

| authority | bytes | SHA-256 | 결과 |
|---|---:|---|---|
| `SSOT_INDEX_v25.45.0.md` | 144,214 | `3f998ad22bd1442b07978482877333ae238770ff6d069106d23fde027667cd7d` | MATCH |
| `SSOT_ALL_v25.45.0.md` | 4,733,265 | `e94623f128cf9894d76e0b0d8db8de07d4c86ed0aada6cfafab5a2d6f74fad3e` | MATCH |
| `SSOT_ALL_MANIFEST_v25.45.0.md` | 5,260 | `4a5656c86dd80c33383075a5dd6a7319bb83d396a205c0baff75e858ee88bb5d` | MATCH |
| `CURRENT_SHA256_v25.45.0.md` | 15,965 | `d8437401411f860e3f9bac5122d6ca76ce659e29185e4f2ebae6894402d8f9b7` | MATCH |
| `publish/spec/CURRENT.md` | 2,758 | `6ca95223ec375a352200a84ea4f8acd0df0de709ded5a6dfdef24790a2abb5b0` | MATCH |

Official live checker는 `files=40`, `seal_rows=94`, mutations 10/10, isolated
40/40, RD-001~536 drift 0, VC17 `44/15/7/1/21`, public v0.6.0으로 PASS했다.
v25.45.0은 promotion-added semantic RD 0이므로 이 bounded source projection과
Windows build 계약에는 `UNAFFECTED`다. Public SPEC v0.6.0은 내부 SSOT와 별도
current이며 successor 의미를 자동 포함하지 않는다.

## Primary source-identity Gate

Fresh projection은 working-tree bytes가 아니라 manifest가 지정한 Git commit의
exact blobs만 읽도록 실행했다. 복원된 fixed manifest 결과는 다음과 같다.

- source commit: `873d3cb236e9f7ab40307bc55c305861e2d7aeef`
- source tree: `git-tree:bf753c9d47c1d3706b27da2531aa619ea1c85309`
- projection policy/manifest identity:
  `sha256:89176bca8386d2d3381d13df11d3fd9c555ab8f95aeb819f544ae5814b114e2c`
- projected files: manifest 171 / actual 171
- initial public tree:
  `sha256:4167e8e9658326bf382ee44195279fa2aa5cbe85f98365a03ed5fa6ea22f5bc6`

Current source의 projected `tool/src/bin/ddonirang.rs`는 50,298 bytes이며
`project-run` surface가 9회 존재한다. Historical source의 같은 파일은 10,422
bytes이고 `project-run` occurrence가 0이다.

### SOURCE_COMMIT_CURRENT_TO_HISTORICAL — RED → exact restore → GREEN

Reviewer가 fixed manifest의 `source_commit`만 historical `27418362...`로 바꿨다.

- primary Gate: expected `873d3cb...`, actual `27418362...`, exit 23 RED
- projection tool 자체: exit 0, historical source/tree에서 169 files 생성
- historical source tree:
  `git-tree:64b4457e561b39461ca6755bc90f011b9b2bee39`

따라서 projection command 성공만 신뢰하면 stale source를 재사용할 수 있고,
별도 exact current-source assertion이 필수임을 직접 재현했다.

manifest를 fixed bytes로 복원한 뒤 bytes/SHA/blob 3개가 exact match하고 tracked
residue 0을 확인했다. Primary Gate exit 0, fresh 171-file projection과 initial tree
identity도 exact GREEN으로 돌아왔다.

## WASM remap, projection validation과 strict-link boundary

Handoff candidate WASM은 독립적으로 receipt와 6개 artifact bytes/hash를 모두
재검산한 뒤 fresh reviewer projection에 substitute했다. WASM 자체를 새로 빌드한
것이 아니라 exact reviewed candidate custody를 재사용한 범위다.

- remap receipt source commit/tree: exact `873d3cb...` / `bf753c...`
- candidate semantic identity:
  `sha256:802872575876e022acf47c911a1640626c62f1738dddc6879f8f0362e494f913`
- remap policy:
  `sha256:d80fdb94b79cbab3ac4fd580c701a0dc5947676706964cf0252111237ed6646a`
- internal/unknown/private path count: `0/0/0`
- substitution source commit/tree: exact current source 2/2
- before/after tree: `4167e8...f5bc6` → `424832...06ba`
- public membership: false / tracked source write count 0
- final files: 171 / actual 171
- normal validation: PASS, 171/171 scanned, unscanned security-relevant 0,
  required roles 4/4
- validation receipt identity:
  `sha256:abf2a5862d92dac3833b04fc261dec0016cde7f29b0d0ae995861b5f61b533ba`
- existing projection/validator/remap unit tests: 56/56 PASS

Receipt files도 producer custody와 byte-identical하게 재현됐다.

| receipt | bytes | SHA-256 |
|---|---:|---|
| public projection | 1,461 | `e76edaf3c0c3624bb6df3fed4b37633455b20a60679c958653e9a12146f7f63d` |
| public tree manifest | 34,304 | `c37a3d0a116d764c9120d68540fadf9f58aad01f48941dca21a4c4c96c43fad2` |
| WASM substitution | 818 | `43a3be63681ad7cd39f1663b3949788ae8fcdd34ad179ad29552a38cb52e0d18` |
| public validation | 654 | `abf2a5862d92dac3833b04fc261dec0016cde7f29b0d0ae995861b5f61b533ba` |

Strict `--require-spec-links`는 exit 1 / `E_PUBLIC_SPEC_CURRENT_LINK`로 RED를
유지한다. 부재한 target은 handoff가 열거한 historical/candidate SPEC manifest
10개와 동일하다. 이는 public projection membership/ownership OPEN이며
`publish/spec/**`를 복사·수정하거나 validator를 완화하지 않았다.

## Windows x64 candidate와 user workflow

Fresh final reviewer projection 자체에서 official Windows entrypoint를 offline으로
실행했다. Build source는 위 171-file current-source projection이며 producer binary를
재사용하지 않았다.

| 항목 | 결과 |
|---|---|
| workspace members | core/lang/numeric/proof/symbolic/tool 6개 |
| release workspace build | PASS |
| official `ddonirang` build | PASS |
| artifact count | executable 1 |
| `ddonirang.exe` | 7,037,440 bytes / SHA-256 `623b92c7fa5ebcd84d58cf2859b9a047e9d6972d1986f648f51be79d6c8af8e6` |
| PE format / stack reserve | PE32+ / 16,777,216 bytes |
| forbidden source/build/cargo/rustup/user path | 0 |
| startup/help | exit 0 / PASS |
| teul-cli binary string | 0 |
| help command membership | `project-run` present; `test/view/repl` absent |

Existing virtual-project fixture를 candidate binary로 실행했다.

- command surface: `project-run --virtual ... --target 앱 --inspect-graph
  --inspect-lock --out ...`
- exit 0 / stdout 0 / stderr 0
- candidate output: 16,488 bytes / SHA-256
  `f9c2e36f4117d4a523438c5ab3a88948c769fc4a4b48c99e9dd6495bd7f29578`
- existing expected: exact same bytes/SHA / byte equality true
- frontdoor semantic identity in projected source: `ddn.project-run.v1`

## Teul exclusion과 bounded dependency

Fresh projection의 direct census:

- path containing `teul-cli`: 0
- `teul-cli.exe`: 0
- Cargo.lock package `teul-cli`: 0
- workspace member `tools/teul-cli`: 0
- candidate binary `teul-cli` occurrence: 0
- Windows build와 project-run fixture의 teul execution: 0

남은 세 source file의 `teul-cli` text는 projection transform을 시험하는 private-path
negative fixture, `ddonirang --help` 부정 assertion, preprocess compatibility 주석이다.
실행/package/path dependency가 아니며 physical historical source deletion 근거도
아니다. 따라서 이 candidate에서 bounded V1 build/test/pack/publish teul dependency는
0이지만 repository-wide test/pack dependency 또는 teul retirement를 주장하지 않는다.

## Residue와 nonclaims

Review-only fresh/tamper/restore projection, receipts, Windows target/artifact와 workflow
output을 포함한 외부 root는 exact path 확인 후 recoverable Recycle Bin cleanup했다.
Original-path residue 0이고 producer projection/WASM/Windows evidence roots는
변경·삭제하지 않았다. Task-owned process와 port 8787 listener residue는 0이다.

다음은 NONCLAIM/OPEN이다.

- public `test`/`view`/`repl` membership과 whole CLI parity
- strict public SPEC-link closure
- public XP-02/M12, whole PathIR P1, ERQ close
- teul physical retirement/deletion과 repository-wide dependency zero
- P5 또는 V1 closure/readiness, release/publication/activation/legal
- Owner Human Smoke와 Human PASS

따라서 exact target-bound verdict는 `PASS_TARGET_BOUND`, blocking finding 0이다.
