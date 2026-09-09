# T5B console·graph canonical view payload structured golden

`semantic_view_payload.js`의 product-local candidate payload를 pixel이 아닌 exact
structured bytes로 봉인한다.

- G1: ordered native runtime output → canonical console payload
- G2: `seamgrim.graph.v0` → canonical graph payload
- 같은 authoritative state에서 Run과 Workbench가 같은 공통 builder를 사용해
  byte-equivalent payload를 내야 한다.
- public ABI, SSOT schema, Native ABI 또는 compatibility freeze를 뜻하지 않는다.
- missing identity, invalid/unsupported graph는 legacy inference로 복구하지 않고
  explicit outcome을 낸다.

실행:

```text
node tests/seamgrim_console_graph_canonical_view_payload_runner.mjs
```
