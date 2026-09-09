# 2026-08-29 DDN V1제품마감Codex — P1-A handoff delta

## 역할

- AI_PROVIDER: OpenAI
- AI_SURFACE: Codex local task / VSCode-compatible project session
- AI_CAPABILITY: long-running product implementation, testing, handoff
- SESSION_NICKNAME: DDN V1제품마감Codex
- PROJECT_ROLE: DDN V1 제품 마감 전담 실행 세션
- RETURN_LABEL: `[DDN V1제품마감Codex -> Codex관리Work]`
- thread: `01a04a01-b812-7840-a2a3-33208dd36e36`

## 이번 delta

- P0 limited closure `fe7c38c5...`와 P1-A lease `0d9dd609...`를 predecessor로 보존했다.
- leased product/test 16 paths에 explicit V1-Core supported-profile ingress를 구현했다.
- product/test fixed HEAD `bc883fd1444bfad86c4ebbf92a84ffa6d84d027c`, tree `a0d46873734ad50a8e5d4a8dbb5f84f73c03f23a`를 고정했다.
- supported path는 V25 `:=`/`<-`를 수용하고 legacy `=`, profile 누락/미지원, direct/mutual recursion을 구조화 진단으로 fail closed한다.
- source analysis/native/WASM이 shared resolver를 소비하며 hidden PreV25 retry와 전역 default switch는 0이다.
- tracked WASM을 공식 build entrypoint로 갱신하고 freshness manifest를 재생성했다.

## 근거

- 최초 RED: 4/4 expected boundary failures
- lib regression: 523/523 PASS
- P1-A native: 6/6 PASS
- native/WASM exact: 1/1 PASS
- tracked-WASM: 8/8 PASS, deterministic repeat 3
- freshness: PASS
- mutation: 3/3 RED → exact restore → GREEN, residue 0
- clean-detached `bc883fd1...`: 동일 focused/parity/freshness/mutation PASS, final clean
- WASM: 5,553,353 bytes / `29480a59d264cffa280d6c1fb8a5a74da857955a6f028cd8b2adaf71e2366f51`
- fixed Git manifest blob: 18,938 bytes / `7ad02442eb9b6542e586b86880b7814560611cf927a51cd657e2c72ddc7b843e`

## 상태

- `P1A_V1_CORE_SUPPORTED_INGRESS_IMPLEMENTED_UNDER_REVIEW`
- independent PASS, P1-A closure, V1 membership/readiness, release, activation, Human PASS는 미주장이다.
- P1-A handoff commit 이후 독립검토 task를 exact fixed target으로 요청한다.
- 기존 task-owned untracked `20260829_codex_v1_core_supported_subset_preflight_r1.md`는 수정·stage하지 않고 보존했다.
