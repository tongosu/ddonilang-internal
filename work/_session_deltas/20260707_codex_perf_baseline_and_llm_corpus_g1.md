# 20260707 Codex session delta: perf baseline + LLM corpus G1

- 작성: 2026-07-07 (Asia/Seoul), Codex
- 범위: `PROPOSAL_SEVEN_PURPOSE_ADVANCEMENT_DESIGN_V1_20260706` 중 F0-2, P7-G1
- SSOT 수정: 없음
- parser/runtime 변경: 없음
- closure 주장: 없음

## 추가

### F0-2 결정적 벤치 계약

- `pack/perf_baseline_v1/`
- `tools/scripts/run_perf_baseline_v1.py`
- `tests/run_perf_baseline_v1_pack_check.py`

판단:

- 기존 `benchmark_baseline_v1`을 대체하지 않고 상위 회귀 계약으로 참조한다.
- 현재 baseline 값은 `pending_first_measurement`다.
- runner는 dry-run/self-check와 regression gate shape를 제공한다.
- 최초 측정값 고정 전까지 성능 충분 주장은 금지한다.

### P7-G1 LLM 코퍼스

- `pack/llm_corpus_extract_deterministic_v1/`
- `tools/extract_llm_corpus_v1.py`
- `tests/run_llm_corpus_extract_deterministic_check.py`

판단:

- 생성형 요약 없이 pack README/input/golden/contract만 읽는다.
- 정렬된 경로 순서와 stable JSON key order로 결정성을 고정한다.
- 같은 저장소 상태와 limit이면 같은 row order와 corpus hash가 나온다.

## 생성 산출물

- `I:/home/urihanl/ddn/codex/out/llm_corpus_v1.jsonl`
- `I:/home/urihanl/ddn/codex/out/llm_corpus_v1.manifest.detjson`
- corpus hash: `sha256:2b58affcceace7f164ff99a11b2b43c86e1d79f7aa05d3f8ec58b1df3e048f30`

## 검증

- `python tests/run_perf_baseline_v1_pack_check.py` PASS
- `python tests/run_llm_corpus_extract_deterministic_check.py` PASS
- `python tests/run_pack_golden.py perf_baseline_v1 llm_corpus_extract_deterministic_v1` PASS

## 남은 G1

- P5물리-G1 적분기 pack skeleton
- P5경제-G1 model-first skeleton 3종
