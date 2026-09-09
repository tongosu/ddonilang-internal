# Public repository dry-run result

## 결론

```text
DETERMINISTIC_PROJECTION: PASS
PUBLIC_SOURCE_BUILD: PASS_WITH_PORTABILITY_FOLLOW_UP
PUBLIC_REPO_SELF_CONTAINED_UNIT_TESTS: FAIL_CLOSED
PUBLIC_CONFORMANCE_CLOSURE: INCOMPLETE
PUBLICATION_READY: NO
PRODUCT_BASELINE_SAFE: YES_FOR_EXISTING_ISOLATED_PRODUCT_WORK
REPOSITORY_OPERATIONS_SAFE: YES_FOR_ADDITIVE_PROJECTION_WORK
```

이 결과는 현재 내부 제품이 실행 불가능하다는 뜻이 아니다. 내부 정본 경로에 있던 테스트 fixture와 운영 경로가 공개 후보에서 빠졌을 때 공개 저장소만으로 전체 테스트를 재현할 수 없다는 뜻이다.

## 결정적 출력

- source commit: `905efb4a1601b764e0f4f2554bef3fbd433172a3`
- source tree: `13b63d4b3485543a0b3fccd5677cb9bb8e8cc76b`
- projection file count: `3,468`
- projected bytes: `20,660,173`
- public tree identity A/B: `sha256:5f207cc6f160bc326a1e44574a356983f2a4d896c64669777e78fe54aaee5148`
- A/B tree-manifest file SHA-256: `94293a1f38de20815dafd6dd0b9edcd184b3f0446e319435d8c54172ae501e61`
- A/B receipt file SHA-256: `9ea4112e3945e2fac2037c8583d00986b3813541eccfe2f2d96a69aaf14d0169`
- output A: `I:/home/urihanl/ddn/codex/build/public-projection-r1/tree-a`
- output B: `I:/home/urihanl/ddn/codex/build/public-projection-r1/tree-b`

역할별 구성은 BUILD_REQUIRED 21, PRODUCT_SOURCE 3,067, PUBLIC_CONFORMANCE 217, PUBLIC_DOC 159, USER_EXAMPLE 4파일이다.

## 통과한 검사

- 동일 manifest/tool/source commit에서 A/B raw tree identity 일치
- projection output에 `.git`, `docs`, `work`, `official-store` 디렉터리 없음
- `cargo metadata --offline --no-deps`: PASS
- root Rust workspace `cargo check --workspace --offline`: PASS
- `tools/teul-cli` `cargo check --offline`: PASS
- 선택된 Python checker syntax compile: PASS
- 기본 secret signature scan: private-key/AWS/GitHub/OpenAI token pattern 0
- Workbench product source와 tracked WASM 포함

## fail-closed한 검사

### 1. 공개 저장소 unit-test fixture closure

- root workspace `cargo test --workspace --no-run --offline`: FAIL
- 누락 fixture: `pack/ddn_v25_pc01_definition_binding_v1/positive_definition_binding.ddn`
- teul-cli `cargo test --no-run --offline`: FAIL
- 누락 fixture: `docs/ssot/pack/edu_phys_p001_05_projectile_xy/lesson.ddn`

SSOT를 통째로 공개하는 방식으로 고치면 안 된다. 두 test fixture를 공개 역할의 별도 fixture로 승격하고 제품 테스트의 상대 경로를 그 공개 fixture로 교정하는 successor가 필요하다.

### 2. public conformance transitive closure

선택한 checker가 문자열로 참조하는 test/runner 21경로 중 18경로가 preview에 없다. 내부 giant test tree를 그대로 공개하는 대신, 실제 공개 workflow에 필요한 최소 checker dependency closure를 계산하고 PUBLIC_CONFORMANCE 역할로 승격해야 한다.

### 3. 내부 절대경로와 운영 가정

- `.cargo/config.toml`의 내부 target directory
- root `ddn.project.json`의 내부 teul-cli binary path
- 일부 runtime/tool/checker의 `I:/home/...` 우선 경로
- 일부 checker의 `git status -- docs/ssot` 운영 가정

대부분 fallback이 있어 제품 build는 통과하지만, 공개 facade 품질과 fresh-clone 계약에는 부적합하다. 공개-safe configuration과 내부 운영 configuration을 분리해야 한다.

### 4. 공개 저장소 기본 문서

`LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`가 없다. License는 법적 Owner 결정 없이 생성하거나 추정하지 않는다.

## 실행 가능한 현재 후보

공개 preview에 들어간 코드만으로 Rust core/lang/tool과 teul-cli의 일반 compile path는 성립한다. Workbench에는 tracked WASM과 다음 사용자 예제가 있다.

- 선 그래프와 포물선
- 진자와 2D 공간
- console grid 카운터, 미니 테트리스, 미로
- symbolic simplify와 등가성 증명 예제
- projectile physics public wedge
- 표, 구조, 텍스트, space2d/grid2d sample payload

다만 이 preview의 Workbench WASM은 3,979,001 bytes인 audit-baseline artifact다. W1C2, 수학 physical track, 최신 View/R10 등 서로 갈라진 계보를 하나로 통합한 release baseline이 아니므로 현재 전체 제품을 대표한다고 선언하지 않는다.
