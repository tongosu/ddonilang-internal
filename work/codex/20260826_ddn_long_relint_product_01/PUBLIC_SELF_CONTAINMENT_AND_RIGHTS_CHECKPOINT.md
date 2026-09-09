# DDN-LONG-RELINT-PRODUCT-01 G18~G24 safe audit checkpoint

이 checkpoint는 unresolved product integration과 독립적으로 가능한 R1 public projection의 읽기 전용 감사다. 공개 tree, GitHub, 제품, SSOT, public SPEC를 수정하지 않았다.

## G18 exact public scope

R2 owner-bound manifest의 모든 top-level role member는 R1 projection에 존재한다.

```text
LANGUAGE_RUNTIME: 6/6
CLI: 2/2
WORKBENCH: 3/3
REQUIRED_WASM: 2/2
WORKBENCH_RUNTIME: 3/3
PUBLIC_SPEC_ENTRYPOINT: 1/1, but v0.3.0 not current v0.5.0
SELECTED_EXAMPLES: 2/2 trees
PUBLIC_CONFORMANCE_ROOTS: 13/13
TOP_LEVEL_MISSING_MEMBER: 0
```

Top-level membership은 self-contained closure를 증명하지 않는다.

## G19 private fixture dependency

Rust compile/test 경로에서 세 include occurrence가 확인됐다.

| source | private target | occurrence | projection |
|---|---|---:|---|
| `tool/src/ddn_runtime.rs` | `pack/ddn_v25_pc01_definition_binding_v1/positive_definition_binding.ddn` | 1 | missing |
| `tools/teul-cli/src/cli/frontdoor_parse.rs` | `docs/ssot/pack/edu_phys_p001_05_projectile_xy/lesson.ddn` | 2 | missing |

또한 `lang/tests/v25_definition_binding_pack.rs`가 같은 internal pack directory를 runtime file read로 요구한다. SSOT 전체 공개는 금지하며, 공개 역할 fixture와 provenance를 별도 생성해야 한다.

Successor custody 확인 결과 projectile target은 projection에만 없는 것이 아니라
`905efb4a...`와 `fab6315c...` Git tree에도 없다. shared root에만 존재하는 untracked/ignored
live SSOT 파일이다.

```text
LIVE_PROJECTILE_FIXTURE_BYTES: 1848
LIVE_PROJECTILE_FIXTURE_SHA256: cdd39d09770bb2c54817722da871d4aed8b07876b5df4107055bd2c11a47fc77
CLEAN_COMMIT_FIXTURE_CUSTODY: ABSENT
```

PC-01 pack 5파일 exact inclusion과 projectile selected-example migration 후보는
`PRIVATE_FIXTURE_MIGRATION_PLAN.md`에 분리했다. rights 승인 전 복사·재작성하지 않는다.

```text
PRIVATE_COMPILE_TIME_FIXTURE_DEPENDENCY: FAIL_CLOSED
SSOT_PUBLICATION_AS_FIX: FORBIDDEN
```

## G20 public-safe path

projection 안 marker hit:

```text
I:/home/urihanl/ddn/codex: 11 files
docs/ssot/ssot: 4 files
```

주요 경로는 `.cargo/config.toml`, `ddn.project.json`, server/tool paths, parity checker와 AI prompt golden이다. fallback 존재 여부와 무관하게 public portability는 fail-closed다.

후속 역할 분류에서 15 files를 다음으로 완전 분류했다.

```text
PRODUCT_PORTABILITY_OR_ROOT_CONFIG: 5
INTERNAL_UTILITY_EXCLUDE: 4
D7_CONFORMANCE_DEPENDENT: 5
PUBLIC_DOC_CUSTODY: 1
UNCLASSIFIED: 0
```

`PUBLIC_PATH_PORTABILITY_MIGRATION_PLAN.md`에 exact file과 successor 처리를 기록했다.
내부 utility 원본이나 public SPEC v0.5.0 의미는 변경하지 않으며 실제 path 교정은 G8
이후 결합 제품 경로에서 수행한다.

G29 preliminary scanner는 C:/ fallback과 broader private SSOT marker를 포함해 범위를
넓혔고 101 occurrences / 28 paths를 확인했다. 최초 15-file 수치는 하한선으로 보존한다.
또한 source Git tree에는 없는 `tests/__pycache__/*.pyc` 15 files가 mutable R1 projection에
생성돼 있어 output immutability가 깨졌다. strong secret pattern은 0이지만 projection
security/portability 상태는 계속 FAIL_CLOSED다.

## G21 public conformance closure

13개 root checker에서 `tests/...` 문자열 참조를 재귀 계산한 최초 하한선은 다음과
같았다.

```text
ROOTS: 13
RECURSIVE_CLOSURE: 46
REFERENCE_EDGES: 62
MISSING_IN_SOURCE: 0
MISSING_IN_PROJECTION: 32
```

이 46-path / missing 32 수치는 실행 파일 import와 실제 pack tree를 포함하지 않은
하한선이었다. 후속 bounded audit가 실행 파일 import, 저장소 경로, pack tree를
포함해 다시 계산한 결과는 다음과 같다.

```text
SCRIPT_CLOSURE: 82
PACK_ROOTS: 43
REQUIRED_FILES: 433
REQUIRED_RAW_BYTES: 3310511
MISSING_IN_SOURCE: 0
MISSING_IN_PROJECTION: 381
UNRESOLVED_DYNAMIC_REFERENCES: 0
STATIC_COMPLETENESS_CLAIM: false
```

두 umbrella root가 각각 43개와 30개의 script closure를 끌어온다. 이를 진단
목적으로 제외한 leaf candidate도 23 scripts, 1 pack, 56 files이고 projection에
26 files가 없다. 이는 manifest rewrite가 아니며 public-specific aggregate와
curated parity/durability case를 사용할지 Owner 결정 D7이 필요하다. 상세 근거는
`PUBLIC_CONFORMANCE_CLOSURE_CHECKPOINT.md`에 봉인했다.

## G22 public facade candidate

```text
README.md: PRESENT
QUICKSTART.md: PRESENT
LICENSE: ABSENT / FINAL LANDING NOT AUTHORIZED
NOTICE: ABSENT
SECURITY.md: ABSENT
CONTRIBUTING.md: ABSENT
SUPPORT.md: ABSENT
CODE_OF_CONDUCT.md: ABSENT
```

실제 root facade 파일은 만들지 않았다. 별도 candidate packet에 허용된 DCO-first 구조와 unresolved Owner 입력을 기록했다.

후속 reproducibility audit에서 root image link 1개와 QUICKSTART가 호출하지만 projection에
없는 runner 5개를 확인했다. private `.cargo` target과 Workbench server build fallback도
문자 그대로의 fresh public 실행을 방해한다. 따라서 facade 존재와 facade 재현 가능성을
분리하며 `PUBLIC_FACADE_REPRODUCIBLE: NO`를 유지한다.

## G23 rights ledger

### CODE_RIGHTS

```text
GIT_IDENTITIES: urihanl <urihanl@gmail.com> 857; 또니 <tongosu@myarts.kr> 70
IDENTITIES_SAME_LEGAL_OWNER: UNVERIFIED
EXTERNAL_CONTRIBUTION_ORIGIN: OPEN
OUTBOUND_LICENSE_AUTHORITY: OPEN
```

### DOCS_RIGHTS

public SPEC, public docs, QUICKSTART와 lesson 설명은 code와 별도다. exact docs license는 OPEN이다.

### ASSET_RIGHTS / TRADEMARK_RIGHTS

| asset | bytes | SHA-256 | status |
|---|---:|---|---|
| `publish/assets/ddonirang_wordmark.png` | 158,799 | `126cd087156278841860532796e7de9ef950ae65a0ae752f0fc02e9a631b13cc` | origin/right/trademark OPEN |
| `publish/assets/ddonirang_wordmark.svg` | 1,797 | `6c5091ca4cf32b97f5652dd2a9f1e4a04652466a993d46c9eb697f9c4ff7a5e9` | origin/right/trademark OPEN |

### LESSON_AND_SAMPLE_RIGHTS

`solutions/seamgrim_ui_mvp/samples`와 `pack/seamgrim_public_physics_wedge_v1`의 exact author/source/redistribution ledger는 아직 없다. unknown은 public projection에서 제외한다.

후속 bounded Git provenance 감사로 author/source custody는 다음까지 좁혀졌다.

```text
PC01_PACK: 5 files / 또니 <tongosu@myarts.kr> / cf97f134...
SELECTED_EXAMPLES: 33 files / urihanl <urihanl@gmail.com>
WORDMARKS: 2 files / urihanl <urihanl@gmail.com> / 6d42f88c...
LIVE_PROJECTILE_EXACT_BLOB_IN_GIT_OBJECT_DATABASE: false
```

하지만 Git author identity는 법적 소유권이나 재배포권 증명이 아니다. 두 Git identity의
법적 주체 동일성, 외부 기여, asset/trademark 및 lesson/sample 권리는 계속 OPEN이다.
상세 원장은 `PUBLIC_RIGHTS_PROVENANCE_CUSTODY.detjson`에 있다.

## G24 dependency ledger

offline `cargo metadata --locked`와 root `package-lock.json`만 사용했다.

```text
UNIQUE_ROWS: 199
CARGO_ROWS: 196
NPM_ROWS: 3
CARGO_DECLARED_LICENSE_MISSING: 0
NPM_LOCKFILE: PRESENT
NETWORK_ACCESS: 0
SELECTED_LICENSE: 0/199 / all UNRESOLVED_FOR_RELEASE
REQUIRED_NOTICE_RESOLVED: 0/199
```

Rust expression 중 `MIT OR Apache-2.0 OR LGPL-2.1-or-later` 1건을 포함해 alternative license 선택과 실제 release inclusion을 결정하지 않았다. Node는 Playwright, playwright-core, optional fsevents의 locked source/integrity를 기록했다.

후속 offline material custody는 Cargo 196 packages 중 191 packages에서 local license/notice
candidate를 찾았고 5 packages에는 local material이 없음을 확인했다. `AND` expression은
2건, LGPL mention은 alternative expression 1건이다. 이 증거는 selected license,
required notice 또는 actual release inclusion을 닫지 않으며 상세 hash는
`DEPENDENCY_LICENSE_MATERIAL_CUSTODY.detjson`에 있다.

## fail-closed result

```text
PUBLIC_SPEC_IDENTITY_MISMATCH
PUBLIC_FACADE_RIGHTS_POLICY_FILES_MISSING
PUBLIC_CONFORMANCE_TRANSITIVE_CLOSURE_MISSING
PRIVATE_COMPILE_TIME_FIXTURE_DEPENDENCY
INTERNAL_PATH_MARKERS_PRESENT

PUBLIC_SOURCE_READY: NO
RELEASE_READY: NO
APACHE_2_0_FINALIZATION: OPEN_NOT_AUTHORIZED
```

Evidence:

- `PUBLIC_SELF_CONTAINMENT_AUDIT.detjson` — SHA-256 `939a85d0774e255ef83eabd5aa92897e4c9af89a61429fb9a9742ea4bba6e123`
- `DEPENDENCY_RIGHTS_LEDGER_CANDIDATE.detjson` — SHA-256 `2832acaf7baee8d5a19409907615b4c1a75a3015faf46489f3dc02a445700a08`
- `PUBLIC_CONFORMANCE_BOUNDED_CLOSURE_AUDIT.detjson` — SHA-256 `3486773d80d0ebe488eb918712186095c011c1e3ec5cf0a7e1d25c854e728568`
- `PUBLIC_RIGHTS_PROVENANCE_CUSTODY.detjson` — SHA-256 `de725288dbf8375dab285f849e9643f1ba68956ddec8fe49f638f3da767c7a17`
- `PUBLIC_PROJECTION_SECURITY_PREFLIGHT.detjson` — SHA-256 `3ce54d8ce776ced0d83e4b7f45fd61c6994bdbc2c6022a6a71814f286bec029c`
- `DEPENDENCY_LICENSE_MATERIAL_CUSTODY.detjson` — SHA-256 `48f48cbad63b54aa51673be7bd62f3a2681bcdbe8b78e04441e507eb72224e13`

```text
G18_G24_SAFE_AUDIT: COMPLETE
PUBLIC_SELF_CONTAINMENT_IMPLEMENTATION: NOT_STARTED_PENDING_INTEGRATION_BASELINE
```
