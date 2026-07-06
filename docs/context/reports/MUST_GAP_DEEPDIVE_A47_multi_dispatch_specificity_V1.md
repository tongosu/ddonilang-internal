# MUST_GAP_DEEPDIVE_A47_multi_dispatch_specificity_V1

## 대상

- Track A item: `A47`
- SSOT rule: `14. 다중 디스덧댐`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3979`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:18`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 overload 후보가 여러 개일 때 가장 구체적인 타입을 고르고, 구체성 동률이나 비교 불가는 컴파일 오류로 처리하며, 선언 순서 tie-break는 금지한다고 정한다. 현재 `teul-cli` runtime은 사용자 seed를 `BTreeMap<String, UserSeed>`에 단일 이름으로 저장하고, 호출 시 이름으로 단일 seed를 조회한다. 같은 이름의 여러 후보를 보존하거나, 후보 signature를 모아 타입 구체성을 비교하거나, 동률/비교 불가 전용 오류를 내는 경로는 확인되지 않는다.

## 근거

- SSOT 다중 디스덧댐 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3979`
- 가장 구체적인 타입 우선: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3983`
- 동률/비교 불가 컴파일 오류: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3984`
- 선언 순서 tie-break 금지: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3985`
- 구체성 판정 알고리즘: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3990`
- 비교 불가 예시: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:3996`
- 감사 행은 후보/구체성/모호성 오류 구현 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:18`
- 감사 요약도 제품 경로 후보/구체성/모호성 오류 부재를 기록했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER3_V1.md:76`
- 현재 runtime의 사용자 seed 저장소는 이름당 단일 `UserSeed`다: `tools/teul-cli/src/runtime/eval.rs:98`
- seed defs는 `user_seeds.insert`로 등록되어 같은 이름 후보를 보존하지 않는다: `tools/teul-cli/src/runtime/eval.rs:702`
- 호출 dispatch는 단일 이름 조회 후 바로 `bind_seed_args`/`eval_user_seed`로 간다: `tools/teul-cli/src/runtime/eval.rs:2416`, `tools/teul-cli/src/runtime/eval.rs:2417`, `tools/teul-cli/src/runtime/eval.rs:2418`
- call-tail 후보 수집은 이름 stem 후보에 한정되고 type specificity 후보가 아니다: `tools/teul-cli/src/runtime/eval.rs:2422`, `tools/teul-cli/src/runtime/eval.rs:2435`
- `bind_seed_args`는 단일 seed의 핀/조사/위치 바인딩만 처리한다: `tools/teul-cli/src/runtime/eval.rs:6634`, `tools/teul-cli/src/runtime/eval.rs:6668`, `tools/teul-cli/src/runtime/eval.rs:6697`
- 직접 검색: `rg -n '다중 디스|overload|dispatch.*candidate|specific.*type' tools/teul-cli/src core/src tool/src`에서 SSOT 14 후보/구체성 집행 근거 없음

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a47_multi_dispatch_specificity_red_v1`

## 결정 필요

- 같은 이름 seed를 parser 단계에서 다중 후보로 허용할지, 현재처럼 단일 이름 충돌을 금지하고 별도 overload 문법을 둘지 결정 필요.
- 타입 구체성 lattice를 `셈수/바른수/정수32` 같은 numeric family부터 최소 구현할지, 전체 타입/고름씨/엔티티까지 확장할지 결정 필요.
- 오류 코드는 `E_MULTI_DISPATCH_AMBIGUOUS`류로 새로 둘지, 기존 type mismatch 계열에 포함할지 결정 필요.
