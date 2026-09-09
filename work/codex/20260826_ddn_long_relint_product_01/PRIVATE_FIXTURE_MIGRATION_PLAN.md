# Public self-containment private fixture migration plan — candidate only

```text
STATUS: CANDIDATE_ONLY
PRODUCT_SOURCE_CHANGED: 0
SSOT_CHANGED: 0
PUBLIC_RIGHTS_APPROVAL: OPEN
```

## F1 — PC-01 public conformance closure

다음 세 consumer는 repository-root `pack/ddn_v25_pc01_definition_binding_v1`에
의존한다.

- `lang/tests/v25_definition_binding_pack.rs` — runtime file reads
- `tool/src/ddn_runtime.rs` test module — compile-time `include_str!`
- PC-01 mutation runner

자가완결 후보는 pack 전체 5파일을 `PUBLIC_CONFORMANCE_SUBSET` 역할로 exact path에
포함하는 것이다. 경로를 바꾸지 않으면 Rust source 수정 없이 public cargo test가
재현된다.

| path | bytes | SHA-256 |
|---|---:|---|
| `README.md` | 807 | `18de2b358b61d653fbd2c579ee7dbc31c27b96bba1f7ea15dfd8d5f5a3be3b8e` |
| `expected.jsonl` | 318 | `92b1c855f884b47b4b661c0f0c26774327e7538a4d9eed51c3b73450c384dce6` |
| `negative_binding_as_definition.ddn` | 55 | `e1dc132e11cbcbd889457c74dd53f8ebe7b5bdc8a9fe1b5d12ef2056ee8d6adb` |
| `negative_old_equals.ddn` | 23 | `8c22d6b995757759df93ee1264774dbf6d3292e4bbfa1ed284c0fafaa7333aee` |
| `positive_definition_binding.ddn` | 78 | `cdb647ab6e48f988871afb3cabccf7b3dad630825e15d01bae81a07cdd2d6a36` |

공개 포함은 PC-01 membership과 lesson/sample rights가 승인된 경우에만 수행한다.

## F2 — projectile SSOT path dependency

`tools/teul-cli/src/cli/frontdoor_parse.rs`의 test 2개는 다음 path를 compile-time으로
읽는다.

```text
../../../../docs/ssot/pack/edu_phys_p001_05_projectile_xy/lesson.ddn
```

해당 파일은 `905efb4a...`와 `fab6315c...` Git tree에 존재하지 않는다. shared root의
읽기 전용 live 파일만 존재하며 Git tracked status도 아니다.

```text
LIVE_BYTES: 1848
LIVE_SHA256: cdd39d09770bb2c54817722da871d4aed8b07876b5df4107055bd2c11a47fc77
CLEAN_COMMIT_CUSTODY: ABSENT
PUBLIC_BUILD_SELF_CONTAINMENT: FAIL_CLOSED
```

추가 object-custody 감사에서도 live exact blob OID
`c1567c205fa303efdb311b31804069464667e34d`는 repository object database에 없었다.
제품 계보의 같은 이름 historical lesson 2개는 각각 654 bytes와 1,255 bytes이며 live
1,848-byte fixture와 SHA-256이 다르다. historical file을 byte-identical 대체물로
재사용하지 않는다.

권고 migration은 Owner가 rights와 selected-example membership을 승인한 뒤 exact bytes를
public source의 `examples/physics/projectile_xy.ddn`으로 결속하고 두 `include_str!`을
그 public path로 전환하는 것이다. `docs/ssot/**`는 복사 원본 권위로만 읽으며 수정하지
않는다.

승인이 없으면 fixture를 자동 축약·재작성하거나 hidden fallback으로 대체하지 않고
public source gate를 계속 RED로 유지한다.

## Required Owner inputs

```text
PC01_PUBLIC_CONFORMANCE_MEMBERSHIP:
PC01_PACK_RIGHTS:
PROJECTILE_SELECTED_EXAMPLE_MEMBERSHIP:
PROJECTILE_LESSON_RIGHTS:
PROJECTILE_PUBLIC_TARGET_PATH:
```
