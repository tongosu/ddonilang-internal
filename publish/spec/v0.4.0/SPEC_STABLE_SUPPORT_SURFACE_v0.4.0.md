# 지원 범위 — Language SPEC v0.4.0 공개판

> 상태: `public current / owner-approved / docs-first / product-open`
> trace: Language SPEC `v0.4.0` public current ← independently reviewed `v0.4.0-candidate` ← internal live SSOT `v24.22.1`
> 이전 공개판: Language SPEC `v0.3.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 정본과 parser/runtime/default-product 지원을 분리한다.

## 상태 읽는 법

- `공개 current`: 현재 `publish/spec/CURRENT.md`가 가리키는 v0.4.0.
- `public docs-first`: v0.4.0 공개판에 투영됐으나 제품 수직은 OPEN.
- `검증 후보`: 격리 계보에서 증거가 있으나 기본 제품 HEAD에는 미승격.
- `기본 제품`: 기본 배포 경로에서 확인된 표면.

## 사용자 표면

| 표면 | 공개 문서 상태 | 기본 제품 상태 |
|---|---|---|
| 값·계산·`<-`·`보여주기` | v0.3 계승 | 기본 제품 진입 경로 |
| `(이름: 값, ...) 보임.` | canonical docs-first | 검증 후보; 기본 HEAD 미포함 |
| 이름씨·짧은 계약·표준 보기 | v0.3 계승 | 제품 관문 OPEN |
| `(T,E)맺음`, `값 아니면 되돌림` | public docs-first | parser/canon/golden OPEN |
| `(T)가리킴`, `===`, `끊김` | public docs-first | 공통 CLI/WASM runtime OPEN |
| `두고` 정적 머리 | public docs-first | TypeParamDef 제품 구현 OPEN |
| `#원자`·`고름씨.$갈래`·`$!말결` | public docs-first | lexer/AST/canon/migration OPEN |
| exact 수·`roundTiesToEven`·`mol` | public docs-first | 공통 runtime·wire·30식 corpus OPEN |
| 바이트열·UTF-8·NFC·범위 | public docs-first | parser/runtime parity OPEN |
| 함수값·효과·골라부름 | public docs-first | artifact/lock/runtime OPEN |
| `T?.바꾸기`, `있는가`, `없는가` | public docs-first | stdlib·타입·효과 parity OPEN |
| 세움·매마디 순환 검사 | public docs-first | canon graph·runtime guard OPEN |
| 위치형/이름형 값꾸러미 의미 | public docs-first | P1 `NOT FIXED` |
| 공개 API 명시 실패씨 | public docs-first | C-05 export 표 의존 OPEN |
| `얼개 {}` clean-break | canonical direction | migration/export·제품 OPEN |
| 가지·잠금글 V1 | public docs-first | exact wire·verifier·UI OPEN |
| 선언형 모델 내부 의미 | semantic docs-first | 공개 syntax·typed IR·solver OPEN |

## 고정 비주장

이 공개판의 문서 current 승격은 parser/runtime landed, 기본 제품 승격,
구실 최종 syntax, exact wire, 일반 DAE, 외부 solver, corpus 완료 또는 외부
사용자 성공을 뜻하지 않는다.
