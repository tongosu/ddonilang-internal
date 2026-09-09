# 결정론 계약 — Language SPEC v0.2.1

> 상태: current public pre-release draft / consistency-cleaned 2026-07-17
> trace: Language SPEC `v0.2.1` ← installed current SSOT `v24.15.1`
> 권위: 충돌하면 설치된 internal current SSOT가 우선한다.
> 구현 경계: G7과 함수 타입 `-->`는 설계 확정, K0~K7·A1 제품 증거는 아직 OPEN이다.


## 의미 ID와 파일 봉인

| 역할 | 알고리즘 | 예 |
|---|---|---|
| 타입·구실·구현 실행 의미 ID | BLAKE3-256 + domain-separated DetBin | `applied_type_id = blake3:...` |
| 승인·build·source·canon·manifest·lock·receipt bytes | SHA-256 | `build_artifact_sha256 = sha256:...` |

알고리즘 없는 `Hash256`과 모호한 `build_artifact_hash`는 쓰지 않는다. 모든 hash 필드는
알고리즘이 드러나는 이름과 `blake3:` 또는 `sha256:` 값 접두를 갖는다.

## 실행과 build의 경계

specialization manifest는 실행 중 세계 상태인 `state_hash` 밖에 있다. 그러나 어떤
타입 인자와 구실 구현으로 프로그램을 만들었는지는 프로그램 정체성이므로 build
artifact와 replay pin 안에 있다. replay는 필요한 BLAKE3 의미 ID와 SHA-256 artifact
seal을 서로 다른 이름의 필드로 함께 고정한다.

## 구실의 결정성

모든 구실 요구는 `보기만/누리바꿈` 상한을 갖고 구현은 그 상한을 넘을 수 없다.
V1 구실 구현은 `open_kinds={}`와 `D-STRICT`를 만족해야 한다. 위반하면 최초 call path를
가리키며 compile/build 단계에서 실패한다. pack ID와 content hash도 artifact evidence에
기록한다.
