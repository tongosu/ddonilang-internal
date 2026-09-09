# [Codex관리Work -> 독립검증ClaudeCode] DDN-R-V1-EX01-I1-01

V1 공개 제품 예제 membership 후보 감사를 독립 검토하라.

```text
REVIEW_ID: DDN-R-V1-EX01-I1-01
SCOPE: PUBLIC_EXAMPLE_MEMBERSHIP_CANDIDATE_AUDIT_ONLY
AUDIT_FIXED_HEAD: ef35bf02a192f24add5737d2ccb25db4dbf2de22
REQUIRED_REVIEW_PARENT: 5c81d3238d610c01659083f9f408b2af3cb79ada
BASELINE: 07c0ba1f21c047f8339334d1a4191f0bf6ee4f1a
```

## 독립 확인

1. 계보가 선형이고 audit diff에 제품 source, UI source, tracked WASM, SSOT, public
   SPEC 변경이 0인지 확인한다.
2. 15개 후보 파일의 bytes/SHA-256을 ledger와 독립 재계산한다.
3. 실제 `DdnProgram::from_source`와 `from_v25_source`를 사용해 15개를 처음부터
   재분류한다.
4. 다음 수치를 확인한다.

```text
public_spec_docs_first=7
pre_v25_parse=6
v25_parse=1
neither_parser=8
proposed_tier_0_or_1=4
release_members=0
```

5. public SPEC v0.5.0 예제가 실제로 docs-first/product-open인지 원문과 제품 실행을
   구분한다. 공개 경로에 있다는 이유로 product PASS를 주지 않는다.
6. PC01이 유일한 V25 parser PASS인지, targeted plain PASS와 rights가 아직 별도 gate인지
   확인한다.
7. HELLO, GRID_CURRENT, TENSOR가 첫 사용자 workflow 후보로 합리적인지 검토하되
   release membership으로 승격하지 않는다.
8. PROJECTILE rights와 core dependency 때문에 Tier 2인 처분이 기존 rights ledger와
   일치하는지 확인한다.
9. 추천 네 후보가 557개 전체 migration을 대신하는 최종 membership이 아니라 bounded
   migration proposal인지 확인한다.

## 실행

```powershell
python tools/generate_v1_ex01_public_example_membership_audit_i1.py
python tests/run_v1_ex01_public_example_membership_audit_i1.py
cargo test -p ddonirang-tool --test v1_ex01_public_example_epoch_inventory --offline --locked -- --nocapture
```

## 최소 fault injection

각각 GREEN→실제 변이 RED→exact restore→GREEN을 수행한다.

1. 후보 ID 중복
2. source path 교환 또는 source byte 1개 변경
3. public SPEC 예제 하나를 V25 PASS로 거짓 분류
4. PC01 rights를 `RIGHTS_CLOSED`로 거짓 승격
5. release member를 1로 승격
6. Owner promotion보다 앞서 release membership이 생기도록 DAG 변이
7. Rust test의 expected parser class 또는 diagnostic family 변경

## 판정

```text
PASS
PASS_WITH_FOLLOW_UP
FAIL
BLOCKED_BY_AUTHORITY
BLOCKED_BY_MISSING_EVIDENCE
```

plain PASS는 audit classification에만 적용된다. 제품 구현, exact V1 membership,
rights/license, public copy, SSOT/SPEC 변경, release, activation, Human PASS를 승인하지 않는다.

review 결과는 required parent의 직접 후손에 report와 session delta만 commit한다.
검토용 worktree/target/process를 정리하고 다음 제목으로 반환한다.

```text
[독립검증ClaudeCode -> Codex관리Work] DDN-R-V1-EX01-I1-01 — 결과
```

