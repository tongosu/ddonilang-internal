# llm_corpus_extract_deterministic_v1

Deterministic LLM corpus extraction contract for seven-purpose G1.

- evidence_tier: `tool_runner`
- closure_claim: `no`
- generated_summary_claim: `no`

The extractor entrypoint is `tests/tools/extract_llm_corpus_v1.py`. It delegates
to the implementation under `tools/`, reads grammar manifest rows plus existing
pack README/input/golden/contract files in sorted path order, and writes JSONL
rows without generated summaries. The corpus also carries separated
`ssot_term`, `diagnostic_card`, `pack_summary`, and `example` rows. The same
repository state and the same limit produce the same row order and corpus hash.

Verification:

- `python tests/run_llm_corpus_extract_deterministic_check.py`
- `python tests/run_llm_corpus_v1_dayrun_check.py`
- `python tests/run_pack_golden.py llm_corpus_extract_deterministic_v1`
