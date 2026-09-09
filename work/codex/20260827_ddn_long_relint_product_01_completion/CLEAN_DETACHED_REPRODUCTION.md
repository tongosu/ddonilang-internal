# Clean-detached A/B 재현

## 고정점

- fixed product/test HEAD: `b8530bd6eadcf79658a821f4e9b4538991b89b80`
- detached A/B worktree: 별도 외부 경로, 시작·종료 tracked clean
- Cargo target: A/B 분리
- merge commits from minimum ancestor: `0`

## 결과

- A CLI build: PASS
- B CLI build: PASS
- A G14 parity: 3/3 PASS
- B G14 parity: 3/3 PASS
- A/B tracked WASM freshness: PASS/PASS
- official web WASM A/B/tracked raw bytes: `5,541,461`, SHA-256 `77c787961f2902745845d907c8f2528d56e063d4a41373f4e7d605e195269f34`
- source-built web glue A/B: byte-identical
- source-built node glue A/B: byte-identical
- tracked glue differs from direct wasm-pack output because tracked family carries its bound wrapper/package form; raw `.wasm` and freshness manifest agree.

Mutation runners were restored before detached reproduction; tracked residue is `0`.
