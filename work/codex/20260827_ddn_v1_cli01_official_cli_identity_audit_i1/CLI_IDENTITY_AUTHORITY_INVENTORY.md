# CLI identity·권위 inventory

## 결론

현재 저장소에는 하나의 공식 CLI가 완전히 수렴한 상태가 아니다.

- `ddonirang-tool`: 현재 릴리스 파일명과 WASM 제품 경로를 소유하지만 수동 명령 분기와 데모 명령이 섞여 있다.
- `teul-cli`: 사용자 문서·팩·골든의 넓은 표면을 소유하지만 자체 parser/runtime와 연구·운영 명령 63개를 함께 가진다.
- 두 실행 파일은 독립 구현이 아니라 서로의 소스를 path-import하는 구조다.

따라서 `teul-cli를 지우고 tool만 남긴다`는 즉시 조치는 안전하지 않다. 먼저 공통 Rust 제품 권위로 의미 구현을 모으고, 동일 frontdoor를 사용하는 하나의 공개 CLI에 필요한 명령만 투영해야 한다.

## 권위 기준

| 항목 | 현재 값 | 경계 |
|---|---|---|
| internal SSOT | v25.15.0 | V1 실제 membership 0, maturity floor UNCLAIMABLE |
| public Language SPEC | v0.5.0 | 내부 SSOT와 별도 계보 |
| audit baseline | e5454ef5858af4f48a202cffe30ceef010e35162 | Wave 0 handoff |
| 공개 실행 파일 identity | OPEN | 이 감사가 확정하지 않음 |
| 제품 구현 권한 | 없음 | 읽기 전용 I1 |

## 명령 inventory

| 실행 파일 | 명령 수 | 현행 성격 |
|---|---:|---|
| ddonirang-tool | 28 | runtime 핵심 4, 공유화 후보 2, 내부 4, 데모·팩 도구 18 |
| teul-cli | 63 | 핵심 이행 후보 15, 공유화 후보 15, internal/deferred 33 |
| 합계 | 91 | binary-command identity 기준 |

정확한 91행은 `cli_command_registry.detjson`에 봉인했다. I1에서 `DROP`으로 분류한 명령은 0개다.

## 사용자·검증 의존도

현재 문자열 참조는 다음처럼 양쪽 이름에 분산되어 있다.

| 이름 | publish | pack | tests |
|---|---:|---:|---:|
| teul-cli | 58회/50파일 | 600회/367파일 | 526회/188파일 |
| ddonirang-tool | 160회/50파일 | 42회/30파일 | 21회/13파일 |

이는 곧바로 공개 지원 범위를 뜻하지 않는다. 다만 이름을 한 번에 제거하면 대규모 문서·골든·팩 파손이 생길 수 있음을 뜻한다.

## 제품 identity의 현재 불일치

`publish/QUICKSTART.md`는 개발 빌드 도움말을 `teul-cli`로 안내하면서, 내려받는 실행 파일은 `ddonirang-tool`로 안내한다. 사용자는 같은 제품인지, 기능이 다른 두 CLI인지 알기 어렵다.

이 불일치는 V1 전에 닫아야 하지만, 해결은 이름 치환이 아니라 semantic frontdoor 수렴 이후여야 한다.
