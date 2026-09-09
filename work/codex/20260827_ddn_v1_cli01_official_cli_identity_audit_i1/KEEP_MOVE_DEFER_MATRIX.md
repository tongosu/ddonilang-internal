# KEEP / MOVE / DEFER matrix

이 표는 구현 명령이 아니라 migration proposal이다. 실제 V1 membership은 SSOT에서 0행이므로 공개 포함을 확정하지 않는다.

## ddonirang-tool

| 분류 | 수 | 명령 | 제안 |
|---|---:|---|---|
| KEEP core candidate | 4 | run, run-summary, test, canon | 동일 shared frontdoor 위에서 공식 CLI 핵심 후보로 보존 |
| MOVE shared first | 2 | geoul, query | 의미 구현을 library로 분리한 뒤 public/internal 노출 결정 |
| INTERNAL pending membership | 4 | ai, prompt, preprocess-ai, build-schema | V1 membership 전까지 공개 핵심에서 제외 |
| PACK/DEMO preserve | 18 | run-grid, run-maze-*, eco-*, 기타 run-* | 제거하지 않고 팩·개발 도구 역할로 격리 |

## teul-cli

| 분류 | 수 | 대표 명령 | 제안 |
|---|---:|---|---|
| MIGRATE core frontdoor | 15 | run, check, test, canon, build, lint, repl, view, currentline-run, project-* | 공통 제품 경로로 옮긴 뒤 공식 CLI가 제공 |
| MOVE semantics to shared library | 15 | replay, geoul, bogae, asset, patch, numeric, symbolic, proof 등 | semantic owner를 공통 crate로 만든 뒤 노출 정책 결정 |
| PRESERVE internal/deferred | 33 | ai, train, imitation, evolve, swarm, social, universe, tensor 등 | 연구·내부 도구로 보존, V1 공개 CLI에 자동 포함하지 않음 |

## 금지된 지름길

- teul-cli directory 삭제
- teul-cli의 1,000개 이상 골든을 공식 CLI 증거로 자동 상속
- `run` 명령 이름만 맞추고 서로 다른 runtime을 그대로 유지
- 모든 teul 명령을 V1 public CLI에 평면적으로 노출
- 공개 문서 문자열 일괄 치환으로 migration 완료 주장

## binary retirement 조건

`teul-cli` binary retirement는 다음이 모두 충족된 뒤 별도 승인한다.

1. 공개/내부 명령 membership 확정
2. 선택 명령의 shared semantic owner 착지
3. 원문 source·진단·state hash·artifact parity
4. pack/tests/publish 참조 migration 원장 완성
5. legacy alias 기간과 오류 안내 결정
6. fresh-clone public build·conformance PASS
7. 독립 검토 plain PASS
