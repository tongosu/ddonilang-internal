# 셈그림 lesson SourceEpoch 호환성

## 실행 범위

`solutions/seamgrim_ui_mvp/lessons/**/*.ddn` 557개를 제품 Rust 코드의
`DdnProgram::from_source`와 `DdnProgram::from_v25_source`에 각각 직접 넣었다.
파일 이름이나 내용으로 epoch를 추정하지 않았다.

| 분류 | 개수 |
|---|---:|
| 전체 | 557 |
| pre-V25와 V25 모두 통과 | 0 |
| pre-V25만 통과 | 127 |
| V25만 통과 | 0 |
| 둘 다 실패 | 430 |
| V25 통과 총계 | 0 |

V25 오류 family:

| 코드 | 개수 |
|---|---:|
| `E_BOIM_LEGACY_REMOVED` | 414 |
| `E_V25_DEFINITION_MIGRATION_REQUIRED` | 135 |
| `E_V25_DEFINITION_BINDING_CATEGORY` | 8 |

한 파일이 여러 진단 family에 기여할 수 있으므로 오류 family 합은 파일 수와 같지 않다.

## 해석

- `V25_PASS=0`은 V25 parser가 쓸 수 없다는 뜻이 아니다. 현재 lesson corpus가 V25
  membership으로 migration되지 않았다는 뜻이다.
- `NEITHER=430`은 현 lesson corpus 자체에 보임 legacy 제거 등 다른 현행 경계가
  섞여 있음을 뜻한다. 전역 parser switch 하나로 해결할 문제가 아니다.
- 현재 557개는 역사·실험·제품 예제를 함께 담는다. 전부를 V1 공개 예제로 선언하면
  안 된다.

## 안전한 migration 원칙

1. V1 공개 예제 membership을 먼저 작고 명시적으로 선택한다.
2. 선택한 예제만 V25 원문으로 migration하고 native CLI/WASM/Workbench parity를 묶는다.
3. historical lesson은 원본 identity와 epoch를 보존한다.
4. 선택되지 않은 파일에 content sniffing이나 자동 fallback을 적용하지 않는다.
5. 전역 V25 기본값 전환은 선택 membership의 100% migration과 독립검토 뒤 별도
   Owner gate로 둔다.

