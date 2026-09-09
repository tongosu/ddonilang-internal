# T4 기대 진단표

| 파일 | 실행 명령 | 기대 결과 | 기대 진단 조각 |
|---|---|---|---|
| `syntax_bad_identifier.ddn` | `check` | 실패 | `E_LEX_UNEXPECTED_CHAR`, `예상치 못한 문자: ?` |
| `type_bad_iterable.ddn` | `run` | 실패 | `E_RUNTIME_TYPE_MISMATCH`, `iterable list/set/map` |
| `contract_bad_mode.ddn` | `check` | 실패 | `E_PARSE_UNEXPECTED_TOKEN`, `예상: '알림' or '물림' or '중단'` |

진단 메시지만으로 무엇을 고쳐야 할지 설명할 수 있는지 기록합니다.
