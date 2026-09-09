# DDN execution concurrency W1-C~F migration/ownership map

## 현재 제품 구조

| surface/path | typed IR | 현재 선택·fan-out | ordering/identity 결함 | successor disposition |
|---|---|---|---|---|
| `lang/src/ast.rs` `Receive` | kind/binding/condition/body | sender predicate 없음 | route/provider identity 없음 | sender predicate와 typed binding surface 추가 |
| `lang/src/parser.rs` | `MessageTransfer`는 shared typed | receive는 legacy hook shape | sender-filter 없음 | exact `에게서 (이름:형)를 받으면`만 추가 |
| `lang/src/normalizer.rs` | transfer identity 보존 | legacy receive canon만 출력 | typed sender canon 없음 | exact surface round-trip |
| `lang/src/delivery.rs` | transfer/route/provider marker와 queue | cardinality helper | route/provider가 `u64` wrapper뿐 | semantic identity, trace, dedup, WAIT/outbox authority owner |
| `lang/src/currentline.rs` | 별도 regex/callback | missing no-op, duplicate overwrite, direct dispatch | shared route/queue 미사용 | adapter화; historical surface는 자동 승격 금지 |
| `tool/src/ddn_runtime.rs` | shared AST를 소비 | route 후보가 statement vector index | 바깥 sender `누리` fallback, full 오류, provider 없음 | shared delivery authority와 typed pending state 사용 |
| `tool/src/preprocess.rs` | static preprocessing | receive expansion/lowering 잔존 | runtime semantic owner 우회 가능 | parsing/I/O adapter로 축소 |
| `tool/src/runtime_surface.rs`/`wasm_api.rs` | shared tool 결과 노출 | logical trace 없음 | native/WASM observable 부족 | 동일 trace/diagnostic/receipt 노출 |
| `tools/teul-cli/src/lang/**` | AST/parser 사본 | 독립 receive/send parse | shared lang drift 위험 | 원 source shared frontdoor로 수렴 |
| `tools/teul-cli/src/runtime/eval.rs` | shared transfer enum 일부 사용 | rank와 vector index 후보, local queue | declaration/rank dependency와 `누리` fallback | shared route cardinality/identity/queue authority 호출 |
| `tools/teul-cli/src/canon.rs` | private projection lowerer | rank/source_order fan-out | semantic owner 중복 | typed transfer/receive는 shared canon만 사용 |
| successor pack | W1-B 13 physical cases | W1-C~F logical rows 미지원 | worker/provider/wait/outbox 증거 없음 | 65 logical inventory와 지원 case를 구분 |

## historical disposition

- old `~~>`: 39 files/95 occurrences, 원문 보존.
- old `<<-`: 5 files/7 occurrences, 원문 보존.
- historical receive/multi-handler corpus: 자동 successor 변환 금지.
- migration은 명시적 변환 artifact와 별도 parity evidence가 있을 때만 수행.

## 단일 writer

```text
typed route/provider/delivery authority: lang
native/WASM adapter: tool
legacy teul adapter: tools/teul-cli
successor oracle: pack/future_grammar_atlas_owner_closed_delta_r2
```

제품 vertical은 typed identity → exactly-one route → internal provider → shared adapters →
WAIT/outbox → oracle/parity 순으로 진행한다.
