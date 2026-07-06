# MUST_GAP_DEEPDIVE_A26_semsi_result_slot_V1

## 대상

- Track A item: `A26`
- SSOT rule: `SEMSI-RESULT-01 셈씨 결과칸`
- SSOT anchor: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7057`
- Audit source: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:58`
- 산출물 성격: red conformance 심화조사

## 현재 재검증

SSOT는 `(…)이름:형:셈씨 = { ... }.` 형태에서 본문 안의 `이름`을 암묵 결과칸으로 취급하고, 마지막 결과칸 대입을 셈씨 결과로 삼는다고 정한다. 현재 `teul-cli`에는 `셈씨` seed kind와 `돌려주기`/`Return` 실행 경로는 있지만, 셈씨 이름을 암묵 결과칸으로 예약하고 최소 1회 대입/섀도잉 금지/마지막 대입 반환을 집행하는 전용 parser/runtime 경로는 확인되지 않는다.

## 근거

- SSOT SEMSI-RESULT-01 시작: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7057`
- 셈씨 이름을 결과칸으로 취급한다는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7060`
- 마지막 결과칸 대입이 결과라는 요구: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7061`
- 섀도잉 금지/최소 1회 대입/마지막 대입 규칙: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7069`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7071`, `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7072`
- 반환은 결과칸 대입으로만 표현한다는 설명: `docs/ssot/ssot/SSOT_LANG_v24.12.9.md:7087`
- 현재 AST는 `SeedKind::Semssi`를 인식한다: `tools/teul-cli/src/lang/ast.rs:16`, `tools/teul-cli/src/lang/ast.rs:26`
- 현재 AST/runtime 반환은 `Return` 문장으로 구현되어 있다: `tools/teul-cli/src/lang/ast.rs:147`, `tools/teul-cli/src/runtime/eval.rs:1040`, `tools/teul-cli/src/runtime/eval.rs:1042`
- 직접 검색: `rg -n '결과칸|SEMSI|결과 이름|E-SEMSI|E_SEMSI|result_slot' tools/teul-cli/src lang/src tool/src core/src` = NO_MATCH
- 감사 행은 결과칸/결과 이름 대입 전용 경로 부재로 미구현 판정했다: `docs/context/reports/SSOT_MUST_RULE_AUDIT_TIER4_V1.md:58`

## 판정

- 현재 판정: red 유지
- 언어 커널 구현 변경: 없음
- 신규 red pack: `pack/must_gap_a26_semsi_result_slot_red_v1`

## 결정 필요

- 기존 `돌려주기` 반환과 SEMSI 결과칸 대입을 병행 허용할지, 셈씨 내부에서는 결과칸 대입만 허용할지 결정 필요.
- 결과칸 미대입과 섀도잉 오류의 diagnostic 이름을 확정해야 한다.
