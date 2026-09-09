# v0.4.0 → v0.5.0 공개판 이행 안내

> 상태: `public current / owner-approved / independently reviewed / docs-first / product-open`
> trace: Language SPEC `v0.5.0` public current ← independently reviewed `v0.5.0-candidate-r3` ← internal live SSOT `v24.24.1`
> 이전 공개판: Language SPEC `v0.4.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 public current와 parser/runtime/default-product 지원을 분리한다.

## 새 docs-first 공개 표면

| v0.4.0 상태 | v0.5.0 공개판 | 처리 |
|---|---|---|
| `보임` 뒤 renderer가 graph를 추정할 수 있었음 | 명시 보기 없으면 결과표 | 제품 이행 전 추론 제거 계획 필요 |
| 공개 model 문법 OPEN | `모형 {}`·`모형값` | docs-first 추가; 제품 OPEN |
| 역할·초기화 표면 OPEN | 닫힌 `::`, `처음::고정/어림/계산`, `처음받음` | typed AST 필요 |
| 출력·미지수 표면 OPEN | `::내줌`, `내줌=(...)`, `이름::구함` | schema·solver 검증 필요 |
| model event·합성 표면 OPEN | 조건절 사건, `><`, N항 `잇기` | 제품 corpus 필요 |
| 일반 solve 요청 OPEN | 이름 핀을 받는 `풀기` | SolveRecipe·RunRequest lowering 필요 |

## 결속 기호

- `풀기` 바깥 고정 핀은 `이름=값`이다.
- `방법` 값과 `들임`·`처음` 안의 열린 이름형 값꾸러미 필드는 `이름: 값`이다.
- 기존 pack P1 결함이 고쳐지기 전에는 문서 예제가 제품에서 안전하게 보존된다고
  주장하지 않는다.

## 제품 이행 관문

1. lexer/parser/typed AST/canon에서 `모형`, `::`, `><`와 각 역할을 분리한다.
2. graph default 추론을 제거하고 typed 자료열·결측 상태·hash 경계를 구현한다.
3. ModelDefinition→Instance→SolveRecipe→RunRequest→receipt 수직을 봉인한다.
4. CLI/WASM/browser가 같은 원문·typed 의미·결과를 내는지 검증한다.
5. 문서 public current 승격 뒤에도 제품 source 일괄 rewrite와 runtime 지원은
   별도 제품 관문으로 처리한다.

이 공개판의 문서 current 승격은 migration 도구, parser/runtime landed, 기본
제품 전환 또는 과거 입력 호환 지원을 뜻하지 않는다.
