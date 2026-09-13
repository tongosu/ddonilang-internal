# 호환성·비주장 정책 — Language SPEC v0.5.0 공개판

> 상태: `public current / owner-approved / independently reviewed / docs-first / product-open`
> trace: Language SPEC `v0.5.0` public current ← independently reviewed `v0.5.0-candidate-r3` ← internal live SSOT `v24.24.1`
> 이전 공개판: Language SPEC `v0.4.0` (고정판, 불변)
> 권위: 충돌하면 internal live SSOT가 우선한다.
> 제품 경계: 문서 public current와 parser/runtime/default-product 지원을 분리한다.

## 계보

- v0.3.0과 이전 공개판은 byte를 바꾸지 않는 고정 공개 스냅샷이다.
- 이 디렉터리는 독립 PASS 13/13과 owner 최종 승격을 거친 v0.5.0 공개판이다.
- `publish/spec/CURRENT.md`의 public current는 이 family를 가리킨다.
- 내부 SSOT와 외부 Language SPEC은 별도 버전 계보다.

## v0.x clean break

- `보임 {}`는 제거됐고 호환 alias를 제공하지 않는다.
- `#잘됨/#안됨`은 제거됐으며 `맺음.$잘됨/.$안됨`을 쓴다.
- `#원자`와 `고름씨.$갈래`를 다른 값 범주로 구분한다.
- 값꾸러미 위치형·이름형 혼합, 중복 이름, 필드 수 유실은 오류다.
- `프로젝트 {}` 대신 `얼개 {}`가 정본 방향이지만 제품 migration과
  export 분류표가 닫히기 전까지 실행 지원을 주장하지 않는다.
- `project.obs.N`, `output_N` 같은 합성 영문 ID가 공개 의미 정체성을
  만들지 않는다.

## 호환으로 오인하면 안 되는 것

- `(T)있없`, `(T)잘안`, `(T,E)잘안`은 타입 입력 별칭일 뿐 정본 출력·
  TypeId·hash·lock·직렬화에 남지 않는다.
- `맺음<T>`, `List<T>`, `Result<T>`는 설명용 표기이며 사용자 정본 입력이 아니다.
- internal schema·wire field와 영어 객체명은 한국어 사용자 의미를 대신하지 않는다.

## 비주장

공개 문서 승격과 checker PASS는 제품 동작 PASS가 아니다. C-02 exact 30식,
C-04 기호 corpus, C-05 `얼개` migration/export 표, C-06 다섯 층 노출표,
KS 최종 syntax, exact wire, P1 parser 결함을 계속 OPEN으로 둔다.

## v0.5.0 추가 clean boundary

- `보임`을 graph로 재해석하지 않는다. explicit graph syntax가 OPEN인 동안
  제품의 기존 renderer 추론을 정본으로 간주하지 않는다.
- `::`는 사용자 임의 attribute map이 아니며 `내줌꼴`, 공개 `이음자리 {}`와
  `풀이차림 {}`을 V1 문법으로 추가하지 않는다.
- 방향별 `넘을때`, native PDE·SDE·최적화·동적 ECS 표면을 조용히 열지 않는다.
- 과거 공개판 입력을 위한 호환층을 이 공개판이 제품에 구현했다고 주장하지 않는다.
