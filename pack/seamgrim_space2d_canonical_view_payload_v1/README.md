# T5C space2d canonical view payload structured golden

기존 `semantic_view_payload.js`의 product-local candidate 계층에 추가한
`space2d` family를 pixel이 아닌 exact structured bytes로 봉인한다.

- G1: authoritative `seamgrim.space2d.v0` → canonical space2d exact payload
- G2: Run / Playground / Bogae가 같은 semantic portion을 소비
- G3: missing / invalid / unsupported / identity missing을 fail-closed
- G4: view-plan은 base entity의 identity, 값, 순서를 유지하는 presentation adapter
- G5: renderer 선택과 무관하게 candidate semantic identity가 유지됨

출력 문자열·raw observation·이전 frame·진자/투사체 heuristic은 canonical
입력이 아니다. 별도 legacy 경로가 필요한 경우에도
`EXPLICIT_COMPATIBILITY_ADAPTER` 또는 `LEGACY_DEBT`로 표시하며 native identity로
승격하지 않는다.

실행:

```text
node tests/seamgrim_space2d_canonical_view_payload_runner.mjs
node tests/seamgrim_space2d_canonical_view_payload_mutation_runner.mjs
```

이 candidate payload/hash는 public ABI, SSOT schema 또는 장기 호환 계약이 아니다.
