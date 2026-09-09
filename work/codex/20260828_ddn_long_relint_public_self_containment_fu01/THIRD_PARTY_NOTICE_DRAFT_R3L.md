# Third-party inventory and NOTICE draft — R3L

Owner가 허용한 것은 draft inventory와 notice 준비뿐이다. 이 파일은 license selection,
required notice 확정, legal approval 또는 release inclusion이 아니다.

## 현재 inventory

```text
CARGO_PACKAGE_VERSION_ROWS: 196
NPM_LOCK_ROWS: 3
TOTAL_ROWS: 199
CARGO_DECLARED_LICENSE_MISSING: 0
LOCAL_LICENSE_MATERIAL_PRESENT: 191_OF_196
MISSING_LOCAL_LICENSE_MATERIAL: 5_OPEN
SELECTED_LICENSE_RESOLVED: 0_OF_199
REQUIRED_NOTICE_RESOLVED: 0_OF_199
LEGAL_REVIEW_CLAIM: false
RELEASE_INCLUSION_CLAIM: false
```

로컬 material 미확보 목록:

1. `r-efi@5.3.0`
2. `wasip2@1.0.1+wasi-0.2.4`
3. `wasip2@1.0.2+wasi-0.2.9`
4. `winapi-i686-pc-windows-gnu@0.4.0`
5. `winapi-x86_64-pc-windows-gnu@0.4.0`

`ring`의 `Apache-2.0 AND ISC`, `unicode-ident`의
`(MIT OR Apache-2.0) AND Unicode-3.0`, `r-efi`의 LGPL 포함 OR 표현 등은 법률·Owner
선택 없이 한 항으로 축약하지 않는다.

## Owner membership disposition 반영

PC01 five-file pack, projectile lesson, `gaji/std_math`, 권리 미확인 경로는 first
publication 후보에서 제외한다. Workbench/browser stack은 D6 read-only custody일 뿐
public membership이 아니다. 따라서 root lock의 npm 3행도 실제 release inclusion으로
간주하지 않는다.

최종 NOTICE 생성은 exact release membership, 5개 local material, selected license,
required notice, legal approval이 모두 결속된 후 별도 fixed-head에서 수행한다.
