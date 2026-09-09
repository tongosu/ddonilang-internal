# seamgrim_live_trace_reaction_v1

셈그림 Wave 2A G2의 live committed observation reaction을 고정하는 검증 pack이다.

- 제품 경로: `solutions/seamgrim_ui_mvp/ui/screens/run.js`
- live adapter: `solutions/seamgrim_ui_mvp/ui/live_trace_reaction_runtime.js`
- browser runner: `tests/seamgrim_live_trace_reaction_runner.mjs`
- 범위: commit 뒤 마디당 1회 평가, duplicate/idempotency, tick mismatch/order/gap diagnostics, lineage reset, product UI live reaction evidence, fired tick/action emission history
- 제외: world write, `state_hash` 참여, 새 DDN 문법, world hook runtime, live authoring UI

이 pack의 golden은 실행 마커만 검증한다. 실제 제품 행동은 checker가 vector/browser runner로 검증한다.
