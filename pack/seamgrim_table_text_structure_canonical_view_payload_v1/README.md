# seamgrim_table_text_structure_canonical_view_payload_v1

T5D의 `table`, `text`, `structure` renderer-independent product-local candidate payload golden이다.

- 권위 입력은 exact `seamgrim.table.v0`, `seamgrim.text.v0`, `seamgrim.structure.v0` structured result뿐이다.
- raw observation, output text, resource-name heuristic, previous frame에서 canonical 의미를 만들지 않는다.
- `text_unsupported_format.payload.detjson`은 exact text schema라도 허용되지 않은 `format: "html"`을 `invalid` + `E_CANONICAL_TEXT_INVALID_CANDIDATE`로 거부하는 fail-closed golden이다.
- Run, Workbench, Playground가 같은 authoritative result에서 byte-equivalent payload를 반환해야 한다.
- unknown schema, malformed content, ambiguous resource, missing identity는 fail-closed한다.
