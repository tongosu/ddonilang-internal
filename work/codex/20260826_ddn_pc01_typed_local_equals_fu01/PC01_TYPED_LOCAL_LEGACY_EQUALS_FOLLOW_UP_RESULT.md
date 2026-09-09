# PC01 typed-local legacy equals follow-up 결과

## 계보와 custody

- 기존 PC01 fixed integration parent: `fc09a1f4c857c97db20194173b19e17a3b83f9aa`
- Claude review commit: `8e395f560d6f8913816cbcf9c6e7ce3b9065f8cb`
- verdict: `PASS_WITH_FOLLOW_UP` — plain PASS 아님
- review report: `work/claude/20260826_ddn_pc01_fresh_fixed_head_independent_review/REVIEW_RESULT.md`
- report bytes: `12,582`
- report SHA-256: `fe24cf6b6c19db2c81f86b5ba7107580cf80ff6c202337f38f34b8ab92cecb06`

아직 독립검토되지 않은 G14 successor 네 commit은 review commit 뒤에 patch로
재적용했다. merge와 history rewrite는 없으며 identity 대응은 다음과 같다.

| 원래 G14 commit | review 후 successor commit |
|---|---|
| `fcd3ed516221942ca97a96b1aa7a82d4a94f8e9e` | `fceba9aab07aec0a54f04d23fa88aca4625d3279` |
| `530a39fe35b3b254fd719d8b42f68fa47f50f758` | `579b1e9a9e1870af94d2c0046d97d95a86239836` |
| `64f8556c92bdbad4ff4c796082cea2d7f07f382f` | `12e0439282c32af890f26177bf0ea91ee8ccd953` |
| `c9dcacb3dff9ffe7433a0faec48c7233662fcf9f` | `5a50a58e6dde1c48b18a5148fb05e2f767628d5c` |

- correction commit: `5332841a14dc490e320e886da999e6b5ce99cf98`
- product/test fixed HEAD: `b8530bd6eadcf79658a821f4e9b4538991b89b80`
- merge count `fc09a1f4..b8530bd6`: `0`

## 구현 선택

`OPTION_B_RECOMMENDED`를 선택했다. `parse_definition_stmt`가 이름 뒤의 타입
주석을 `parse_type_ref()`로 완전히 해석한 다음, V25에서 현재 token이 `=`이면
`E_V25_DEFINITION_MIGRATION_REQUIRED`를 반환한다.

이 위치는 토큰 수 lookahead를 쓰지 않으므로 named, applied, function type을 같은
규칙으로 다룬다. malformed type은 기존 type parser에서 먼저 거부되어 migration
오류로 오분류되지 않는다. `채비`의 `DeclKind::Butbak`은 별도 `parse_decl_block`
경로이므로 보존된다.

`ParseError::code()`에도 기존 message prefix의 exact code projection을 추가했다.
pre-V25 parser와 기본 CLI/WASM/Workbench frontdoor 선택 정책은 바꾸지 않았다.

## 정확한 결과

```text
SOURCE: 값:수 = 1.
ACCEPTED: NO
DIAGNOSTIC_CODE: E_V25_DEFINITION_MIGRATION_REQUIRED
RECOMMENDED_SURFACE: :=
STATE_MUTATION: 0
PARTIAL_OUTPUT_EFFECT: 0
```

오류는 `DdnProgram` 생성 전에 반환되므로 AST/runtime state/output/effect가 만들어질
수 없다.

## targeted matrix

1. typed-local old `=`: exact migration diagnostic
2. untyped-local old `=`: 기존 exact diagnostic 유지
3. top-level old `=`: 기존 exact diagnostic 유지
4. typed Definition `:=`: 성공
5. Binding `<-`: 성공
6. 같은 이름 Definition 두 건: Definition identity `2/2`
7. `채비` Butbak `=`: `DeclKind::Butbak` 유지
8. malformed type: migration 오분류 0
9. applied/function type 뒤 `=`: exact migration diagnostic
10. 오류 뒤 program/state/output/effect 생성 0

## 검증

- PC01 pack integration: 기존 3/3 + targeted matrix 1/1 PASS
- full `ddonirang-lang`: unit `363/363`, integration `4/4` PASS
- runtime fail-before-state test: PASS
- existing Definition/Binding runtime test: PASS
- original M1/M2/M3: 모두 RED, restored GREEN, residue 0
- FU01 M1~M5: 모두 RED, restored GREEN, residue 0
- G14 current rejection parity: `3/3 PASS`
- G14 five mutations: 모두 RED, restored GREEN, residue 0
- D7 files-only: exact leaf 11, PC01 membership pending 유지
- clean-detached fixed HEAD reproduction: PASS, residue 0

## WASM provenance

parser source inventory가 실제로 변경되어 기존 freshness가
`source_tree_sha256/source_files mismatch`로 RED가 됐다. fixed source
`5332841a...`의 detached A/B release build를 offline으로 수행해 다음 네 파일이
모두 byte-identical임을 확인한 뒤 단일 A family를 tracked artifact로 결속했다.

- WASM SHA-256: `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34`
- WASM bytes: `5,541,461`
- JS SHA-256: `16b4de4cac8bfebbc7d7f881ab1241b0d22d652ff8ad00b9045f40c81d7c90a9`
- d.ts SHA-256: `3f7f02aaffc0fb50146f47c4350bcaadb607d26ab2dd88e9b03bb82d9a3f1fec`
- package SHA-256: `223687f3faa5ab0f3552070ca639ba343186ded73627b712cc2a5e27ef439fa3`
- freshness: PASS
- network download: 0

## 보호 경계

- 기존 five-file pack diff: 0
- `docs/ssot/**` diff: 0
- public SPEC diff: 0
- Workbench UI source diff: 0
- PC01 public membership: 0
- projectile public copy: 0
- activation call: 0
- Human PASS claim: 0

현재 상태는 구현 완료·독립 재검토 대기다. plain PASS와 PC01 release membership
closure는 주장하지 않는다.
