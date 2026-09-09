# seulgi_ai_gate_no_authority_g7_v1

G7 Seulgi AI gate fixture for no-authority proposal handling.

Evidence tier: `pack_skeleton_plus_existing_gatekeeper_reference`.

This pack does not implement natural-language execution. It records the consumer/gate boundary:

- AI proposal text is inert input.
- Gate accept/reject is explicit.
- Reject never commits.
- Accept still has no authority until a sealed artifact is produced.
- Only a sealed artifact can be replayed or handed to a later executor.

Verification:

```bash
python tests/run_ai_friendly_corpus_and_seulgi_gate_g7_check.py
```
