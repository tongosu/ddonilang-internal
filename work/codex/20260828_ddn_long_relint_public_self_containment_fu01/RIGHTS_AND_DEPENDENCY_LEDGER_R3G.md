# R3G 공개 후보 권리·의존성 원장

## 증거 고정점

```text
SOURCE_FIXED_HEAD: a4d103ad9d8e52c360b5c1607cb658d4b041627a
NETWORK_ACCESS: 0
PRODUCT_WRITE_COUNT: 0
SSOT_WRITE_COUNT: 0
LEGAL_REVIEW_CLAIM: false
RELEASE_INCLUSION_CLAIM: false
NOTICE_RESOLUTION_CLAIM: false
```

clean detached fixed HEAD에서 같은 생성 절차를 두 번 실행했다. A는 이 인계 경로에,
B는 `I:/home/urihanl/ddn/codex/build/public-self-containment-fu01/ledger-r3g-b`에
보존했다. 세 원장의 A/B SHA-256은 각각 일치한다.

```text
DEPENDENCY_RIGHTS_LEDGER_R3G.detjson:
  a8c522020b73c099d05faff4946cf6ffa0b70a5f5d6a298a15aa1c1b2d68c7ad
DEPENDENCY_LICENSE_MATERIAL_CUSTODY_R3G.detjson:
  1746857d617ab4de40d313f86016e6d57474aee79fa60b0bf6981a773d05bee2
PUBLIC_RIGHTS_PROVENANCE_R3G.detjson:
  28c3e5b430a48f4df4c4b0bb7ff26b6e889c267aca78f26b791cb53d57084442
A_B_BYTE_IDENTITY: PASS_3_OF_3
```

## G24 의존성·라이선스 material custody

- 원장 행: 199개(Cargo 196, npm lock 3), Cargo license 미선언 0개.
- 고유 Cargo package/version 196개 중 로컬 license material이 있는 항목은 191개,
  없는 항목은 5개다.
- material 누락: `r-efi@5.3.0`, `wasip2@1.0.1+wasi-0.2.4`,
  `wasip2@1.0.2+wasi-0.2.9`, `winapi-i686-pc-windows-gnu@0.4.0`,
  `winapi-x86_64-pc-windows-gnu@0.4.0`.
- 선택을 요구하는 결합 표현에는 `ring@0.17.14`의 `Apache-2.0 AND ISC`,
  `unicode-ident@1.0.22`의 `(MIT OR Apache-2.0) AND Unicode-3.0`이 있다.
- `r-efi@5.3.0`은 `MIT OR Apache-2.0 OR LGPL-2.1-or-later` 대안 표현이므로
  구현자가 임의의 selected license를 정하지 않았다.
- selected license, required notice, 실제 release inclusion은 199/199 모두
  `UNRESOLVED_FOR_RELEASE` 또는 candidate 상태다.
- npm 3행은 full candidate source의 root lock custody다. 현재 894-file non-browser
  projection이 browser dependency를 포함한다는 뜻이 아니다.
- WASM 제품 source는 별도 package registry를 만들지 않고 root `Cargo.lock`과
  `tool/Cargo.toml`의 Cargo dependency graph를 사용한다. 따라서 해당 package/version은
  위 Cargo 196행에 포함된다. 로컬 `wasm-pack`/Rust target 같은 build toolchain 자체의
  재배포 권리와 browser/offline bundle은 이번 원장으로 닫히지 않는다.

따라서 G24의 deterministic inventory/material custody candidate는 결속됐지만,
license selection·notice·실제 배포 membership·법률 검토는 OPEN이다.

## G23 first-party와 예제 권리 provenance

Git history에서 기여자·마지막 commit·경로 수를 추출했지만 Git authorship을 법적
ownership 또는 공개 허가로 간주하지 않았다.

```text
CODE_RIGHTS_INPUT: tracked 1050 / git identities 2
DOCS_RIGHTS_INPUT: tracked 20 / git identities 2
PC01_FIXTURE_RIGHTS_INPUT: tracked 5 / git identities 1
SELECTED_EXAMPLE_RIGHTS_INPUT: tracked 33 / git identities 1
ASSET_AND_TRADEMARK_RIGHTS_INPUT: tracked 2 / git identities 1
```

live projectile lesson은 1,848 bytes, SHA-256
`cdd39d09770bb2c54817722da871d4aed8b07876b5df4107055bd2c11a47fc77`이며 exact
blob이 fixed-head Git object database에 없다. 역사 제품 후보 두 개도 live bytes와
동일하지 않다. 그러므로 이를 public selected example로 자동 복사하지 않았다.

다음은 모두 `false`로 보존한다.

- code/docs/lesson-sample/asset/trademark/third-party rights resolved
- Git authorship equals legal ownership proof
- live projectile와 역사 제품 후보 identity equivalence

G23의 요구 분류를 다음처럼 서로 섞지 않고 유지한다.

```text
CODE_RIGHTS: UNKNOWN / Git provenance input only
DOCUMENTATION_RIGHTS: UNKNOWN / Git provenance input only
ASSET_RIGHTS: UNKNOWN / wordmark custody input only
THIRD_PARTY_RIGHTS: UNKNOWN / G24 candidate dependency ledger only
TRADEMARK_RIGHTS: UNKNOWN / wordmark custody input only
LESSON_AND_SAMPLE_RIGHTS: UNKNOWN / PC01, selected examples, projectile custody only
```

따라서 G23 provenance candidate는 결속됐지만 public membership과 권리 확인은 OPEN이다.

## 비주장과 재개 조건

이 원장은 법률 의견, 라이선스 선택, NOTICE 완결, 공개 허가, public release readiness,
Human PASS가 아니다. Owner 또는 권리 관리자가 exact path membership, first-party
권리, third-party license 선택·notice, projectile lesson custody를 결정한 뒤 fixed-head
원장을 다시 생성하고 독립 검토해야 한다.
