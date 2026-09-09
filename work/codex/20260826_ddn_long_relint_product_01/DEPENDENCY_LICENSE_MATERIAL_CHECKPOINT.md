# DDN-LONG-RELINT-PRODUCT-01 G24 dependency license material checkpoint

source `905efb4a...`의 root workspace와 teul-cli를 `cargo metadata --offline --locked`로
읽고, 로컬 registry crate root의 LICENSE/COPYING/COPYRIGHT/NOTICE/PATENT 계열 파일을
해시했다. 라이선스를 선택하거나 legal interpretation을 하지 않았다.

## result

```text
CARGO_PACKAGES: 196
DECLARED_LICENSE_EXPRESSIONS: 24
PACKAGES_WITH_LOCAL_MATERIAL: 191
PACKAGES_WITHOUT_LOCAL_MATERIAL: 5
AND_EXPRESSION_PACKAGES: 2
LGPL_MENTION_PACKAGES: 1
NETWORK_ACCESS: 0
```

로컬 material이 없는 5 packages:

| package | version | declared expression |
|---|---|---|
| `r-efi` | `5.3.0` | `MIT OR Apache-2.0 OR LGPL-2.1-or-later` |
| `wasip2` | `1.0.1+wasi-0.2.4` | `Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT` |
| `wasip2` | `1.0.2+wasi-0.2.9` | `Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT` |
| `winapi-i686-pc-windows-gnu` | `0.4.0` | `MIT/Apache-2.0` |
| `winapi-x86_64-pc-windows-gnu` | `0.4.0` | `MIT/Apache-2.0` |

local material 부재는 곧바로 사용 금지나 위반 판정이 아니다. 다만 fresh public release
NOTICE/license bundle을 현재 offline custody만으로 완결할 수 없다는 뜻이므로 fail-open하지
않는다.

동시 의무 가능성이 있는 `AND` expression:

```text
ring 0.17.14: Apache-2.0 AND ISC
unicode-ident 1.0.22: (MIT OR Apache-2.0) AND Unicode-3.0
```

`r-efi`의 LGPL은 `MIT OR Apache-2.0 OR LGPL-2.1-or-later` 중 alternative다. 구현자가
LGPL 적용 또는 회피를 임의 주장하지 않고 selected license를 Owner/legal review에 남긴다.

## boundaries

```text
SELECTED_LICENSE: 0/196
REQUIRED_NOTICE_RESOLVED: 0/196
RELEASE_INCLUSION_RESOLVED: 0/196
NPM_MATERIAL_AUDIT: NOT_PERFORMED_LOCKFILE_ONLY_NO_FRESH_PUBLIC_NPM_INSTALL
APACHE_2_0_FINALIZATION: OPEN_NOT_AUTHORIZED
LEGAL_REVIEW_CLAIM: false
```

G27 fresh repository build로 실제 target/feature inclusion을 계산한 뒤에만 release inclusion을
좁힌다. 모든 registry package를 실제 binary inclusion으로 간주하지 않는다.

## custody

```text
AUDIT_TOOL: audit_dependency_license_materials.py
LEDGER: DEPENDENCY_LICENSE_MATERIAL_CUSTODY.detjson
LEDGER_BYTES: 106138
LEDGER_SHA256: 48f48cbad63b54aa51673be7bd62f3a2681bcdbe8b78e04441e507eb72224e13
SOURCE_HEAD: 905efb4a1601b764e0f4f2554bef3fbd433172a3
```
