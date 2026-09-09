# DDN-R-V1-VC06-FU02-MATERIALIZATION-GUARD-I1 독립 재검토

## Verdict

`PASS`

이 판정은 VC06 FU02 reused-worktree materialization guard에만 한정한다. stale CRLF checkout은 semantic 실행 전에 명시적 materialization 진단으로 fail closed되고, runner가 source bytes를 자동 정규화하거나 다시 쓰지 않으며, Git blob과 일치하도록 명시적으로 복원한 뒤 기존 VC06 제품 검증이 그대로 통과했다.

## 고정 identity와 계보

- 선행 scoped review: `61c8dce6b9fbdb9921a71339ae7d788e6534f016`, tree `88c96cc0f3e8e473086fb5f055ac9fcbe010bc0e`
- FU02 correction fixed: `eefef28db6a9e3bf660331dca8568829e8b41c45`, tree `6e62ed2087871c1bb8f13fc445366eee1f37e504`
- correction exact parent: `61c8dce6b9fbdb9921a71339ae7d788e6534f016`
- handoff/review parent: `2a71996c616d626d4c7850675a096ba42311ee0d`, tree `1c2b600ffad5a68b42c11eded2086c23f3689a65`
- handoff exact parent: `eefef28db6a9e3bf660331dca8568829e8b41c45`
- correction 및 handoff merge count: 각각 `0`
- correction diff: `tests/run_v1_core_text_byte_nfc_rebase_w1.py` 정확히 1개
- handoff diff: FU02 handoff와 writer session delta 정확히 2개
- 기존 review commit `61c8dce6…`와 역사 branch `e72df779…`는 삭제·rewrite 없이 보존했다.

## 구현 범위 검토

correction runner의 Git blob은 `15,445 bytes`, SHA-256 `817b9b05367bb3cdf6d84513065fe76e64072d8ad45680eb0cb18717f672655b`다. 추가된 preflight는 다음 순서로만 동작한다.

1. 대상 경로가 repository 안의 tracked path인지 확인한다.
2. `HEAD:<path>` Git blob bytes와 checkout raw bytes를 별도로 읽는다.
3. `git check-attr eol`이 `lf`인지 확인한다.
4. checkout에 CRLF, 다른 CR, 또는 Git blob과의 byte mismatch가 있으면 semantic probe 전에 명시적으로 실패한다.
5. 성공한 경우 receipt에 Git blob identity와 checkout raw identity 두 집합을 별도로 기록한다.

runner에는 source write, newline 변환, fallback, semantic lowering 또는 별도 Python/JavaScript 언어 구현이 없다. 새 runner, 새 framework, meta-test 추가도 모두 `0`이다.

## Git blob identity와 checkout raw-byte identity

재사용 worktree는 Git status가 clean이어도 VC06 pack 12개가 실제 CRLF materialization인 상태였다. 이를 정상이라고 간주하지 않고 원시 bytes를 독립적으로 확인했다.

- manifest Git blob: `4,082 bytes`, SHA-256 `0240865da6ef1e5e722886d1d25e7936a522ad71727c56dbdefb947fef977884`
- manifest stale checkout raw: `4,107 bytes`, SHA-256 `65a7358586b0e3638b00dc9e44a3f92c82be93282979133209effb5007460357`
- T01 Git blob: `276 bytes`, SHA-256 `c0f201ec2c1b378047d888600e417a0033bbe00e9880e79046f2f3e32d4aae15`
- T01 stale checkout raw: `286 bytes`, SHA-256 `cce147687ae6dbda410555d3caf3db6b0d174e7f9f8c674d72c5ca321e0499f2`
- `.gitattributes` 조회: manifest와 T01 모두 `eol: lf`

stale checkout에서 `--validate-only` 실제 결과는 exit `1`이며 exact diagnostic은 다음과 같다.

`E_CHECKOUT_MATERIALIZATION_CRLF:pack/v1_core_text_byte_nfc_rebase_w1/manifest.detjson:git_blob_sha256=0240865da6ef1e5e722886d1d25e7936a522ad71727c56dbdefb947fef977884:checkout_sha256=65a7358586b0e3638b00dc9e44a3f92c82be93282979133209effb5007460357`

RED 전후 manifest와 T01 checkout SHA-256은 동일했고 Git status도 clean이었다. 따라서 runner의 silent normalization·rewrite는 `0`이다.

## 명시적 materialization, GREEN, exact 복원

stale RED 뒤 manifest와 fixture 11개를 명시적으로 LF materialize했다. preflight가 `files=12`, `declared_eol=lf`, `cases=11`로 통과했고, checkout raw identity 12개가 각각 대응 Git blob identity와 byte-exact 일치했다.

그 상태에서 기존 `tests/run_v1_core_text_byte_nfc_rebase_w1.py` 전체 runner를 변경 없이 재사용한 결과:

- process exit: `0`
- VC06 matrix: `GREEN=7 / RED=0 / PRODUCT_GAP=4`
- native/tracked-WASM structured run payload exact parity: `11/11`
- deterministic repeats: `3`
- native repeat digest: `29b563b4ce7a9c8c0e4519330ae27c71993472aaf0d030d91454fa7613b0f925` × 3
- WASM repeat digest: `31b13be8f68e9eff5cf868bcad5d0b416173fdcf3b6fda8ff199ce077bdffffc` × 3
- native/WASM payload digest: `d0caae998b6821fec3fae6349a4371c5cb8fb8498a581f7c6928f3ab5071c9e9`
- official tracked-WASM freshness: `PASS`
- 기존 local-project CRLF unit: `PASS`

검증 뒤 시작 시점의 reused-worktree CRLF raw bytes로 12개를 되돌렸고, 저장해 둔 시작 SHA-256과 `12/12` 일치했다. 최종 Git status clean, staged `0`, untracked `0`, ignored `0`이다.

## tracked WASM identity와 freshness

- checkout/Git blob WASM: `5,561,603 bytes`, SHA-256 `74e935d194173bb3199bd7573d320742ca928cd5899c6a4567b3b065b4bbe170`, 서로 exact 일치
- checkout manifest raw: `19,550 bytes`, SHA-256 `d25f1ef349dd34fdaac0337a2e1f21bbda7f0cbe4f603fa7d30ef8e9c7cb73af`
- manifest Git blob: `18,981 bytes`, SHA-256 `ba35aa3b9adb19c681e19ec131738cb9900bb8c987d385ffef825e2b0c03042e`
- freshness checker: `PASS`

manifest checkout/Git blob 차이는 이 review가 검출한 동일한 CRLF materialization 현상이며, correction은 WASM artifact·manifest를 변경하지 않았다.

## diff와 보호 범위

`61c8dce6… → eefef28d…`에서 `.gitattributes`, `core/**`, `lang/**`, `tool/**`, `tools/**`, `pack/**`, tracked WASM, `docs/ssot/**`, `publish/spec/**` diff는 각각 `0`이다. correction은 기존 evidence runner 1개만 변경한다. handoff는 정확히 2개 문서만 추가한다. 제품 source, fixture/manifest, WASM, visible UI, public surface와 command membership은 바뀌지 않았다.

테스트 중 사용한 것은 기존 VC06 runner, 기존 freshness checker, 기존 local-project CRLF unit뿐이다. 새 runner/framework/meta-test는 만들지 않았고, stale checkout이라는 결정적 위험을 한 번 확인한 뒤 중단 규칙을 적용했다.

## v25.32.0 successor impact

읽기 전용으로 확인한 live internal `v25.32.0`은 RD-001~469의 v25.25.0 의미를 보존하고 RD-470~483 GAJI module·잔여 compile-ready surface 및 dual BT-DIGEST custody correction을 결속한다. actual membership `40 = 28 REQUIRED + 2 OPTIONAL + 10 DEFERRED`, blocker `28`, readiness `UNCLAIMABLE`, numeric maturity `0 / NOT ASSIGNED`, `SUPPORTED_FOR_V1` `0`도 유지한다. 공개 Language SPEC 진입점은 `v0.6.0`이며 내부 successor를 자동 투영하지 않는다.

FU02 correction의 exact product-impact classification은 `NO_RELEVANT_PRODUCT_SEMANTIC_IMPACT / EVIDENCE_RUNNER_ONLY`다. 기존 `61c8dce6…`의 VC06/VC12/VC04 fixed-target product PASS 근거는 이 runner-only correction과 v25.32 docs authority successor 때문에 훼손되지 않는다. 이는 그 PASS를 다른 product target, 현재 제품 HEAD 또는 v25.32 전체로 자동 상속한다는 주장이 아니다.

## Nonclaims

이 `PASS`는 FU02 materialization guard만 승인한다. VC06·VC12·VC04 전체 closure, P1-A/P1/V1 whole closure, 18/18 또는 40-row membership/readiness, `SUPPORTED_FOR_V1`, public command/WASM membership, public docs promotion, release, activation, 법적 상태, 외부 사용자 성공, Owner Human Smoke 또는 Human PASS를 승인하지 않는다.
