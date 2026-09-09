# DDN-LONG-RELINT-PRODUCT-01 G23 provenance custody checkpoint

이 문서는 제품 source `905efb4a...`와 live projectile fixture의 bounded Git provenance를
봉인한다. Git author identity와 commit count는 법적 소유권·재배포권·상표권의 증명이
아니며, Owner attestation을 대신하지 않는다.

## bounded provenance

| scope | tracked files | Git identities |
|---|---:|---|
| code input | 1,033 | `urihanl <urihanl@gmail.com>` 341 commits; `또니 <tongosu@myarts.kr>` 20 commits |
| docs input at `905efb4a...` | 2 | `urihanl <urihanl@gmail.com>` 6 commits |
| PC-01 exact pack | 5 | `또니 <tongosu@myarts.kr>` 1 commit |
| selected examples | 33 | `urihanl <urihanl@gmail.com>` 8 commits |
| wordmark assets | 2 | `urihanl <urihanl@gmail.com>` 1 commit |

`QUICKSTART.md`와 `publish/spec/v0.5.0`은 제품 source `905efb4a...`에 없으므로 docs
input 2개에는 포함되지 않는다. 이는 live v0.5.0 custody를 D4에서 exact 18-file bytes로
별도 결속해야 한다는 기존 판단과 일치한다.

주요 last-commit custody:

```text
PC01_PACK: cf97f134aebc4889bd3e13ff4850cbf76ca4c2d6 / 또니 <tongosu@myarts.kr>
SAMPLE_TREE: b3516c3ef03a77312a01e4e92c6e200d61f7317e / urihanl <urihanl@gmail.com>
PHYSICS_WEDGE: 004399566ef3861d87873c9ff74a8551130ef29f / urihanl <urihanl@gmail.com>
WORDMARKS: 6d42f88cfd8f9ffa70513ce25882e74b767ea0c2 / urihanl <urihanl@gmail.com>
```

## projectile exact-byte custody

live SSOT projectile fixture:

```text
PATH: I:/dev/ddonilang/codex/docs/ssot/pack/edu_phys_p001_05_projectile_xy/lesson.ddn
BYTES: 1848
SHA256: cdd39d09770bb2c54817722da871d4aed8b07876b5df4107055bd2c11a47fc77
GIT_BLOB_OID: c1567c205fa303efdb311b31804069464667e34d
EXACT_BLOB_EXISTS_IN_REPOSITORY_OBJECT_DATABASE: false
```

제품 계보에 같은 lesson 이름을 가진 두 historical file은 있으나 exact bytes가 아니다.

| path | bytes | SHA-256 |
|---|---:|---|
| `solutions/seamgrim_ui_mvp/lessons/ssot_edu_phys_p001_05_projectile_xy/lesson.ddn` | 654 | `fdcd1ce852a0684732e34303e165ac2835a6fd78f76a5a86dbf1a9c49c789fb3` |
| `solutions/seamgrim_ui_mvp/lessons_rewrite_v1/ssot_edu_phys_p001_05_projectile_xy/lesson.ddn` | 1,255 | `45b763aa090c3a3b1012d16b8ca723f8b7505120e71db2d69352a660f8a5c59f` |

따라서 historical product lesson을 live fixture의 provenance 또는 byte-identical public
대체물로 간주할 수 없다. D6 승인 없이 셋 중 하나를 선택하거나 내용을 합성하지 않는다.

## unresolved rights

다음은 이번 Git provenance 감사로 닫히지 않는다.

```text
GIT_IDENTITIES_SAME_LEGAL_OWNER: UNRESOLVED
CODE_RIGHTS: OPEN
DOCS_RIGHTS: OPEN
ASSET_RIGHTS: OPEN
TRADEMARK_RIGHTS: OPEN
LESSON_AND_SAMPLE_RIGHTS: OPEN
THIRD_PARTY_RIGHTS: OPEN
APACHE_2_0_FINAL_LANDING: NOT_AUTHORIZED
```

특히 `urihanl`과 `또니` identity가 같은 법적 권리 주체인지, 외부 기여가 섞였는지,
wordmark와 lesson/sample의 재배포가 허용되는지는 Owner attestation이 필요하다.

## custody

```text
AUDIT_TOOL: audit_public_rights_provenance.py
LEDGER: PUBLIC_RIGHTS_PROVENANCE_CUSTODY.detjson
LEDGER_BYTES: 6204
LEDGER_SHA256: de725288dbf8375dab285f849e9643f1ba68956ddec8fe49f638f3da767c7a17
NETWORK_ACCESS: 0
PRODUCT_WRITE_COUNT: 0
SSOT_WRITE_COUNT: 0
```
