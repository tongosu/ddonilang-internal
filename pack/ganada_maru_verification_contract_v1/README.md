# ganada_maru_verification_contract_v1

Ganada 15-branch x 6-maru verification contract pack.

This pack does not rejudge the 90 roadmap cells and does not claim product behavior closure. It fixes the evidence contract that later audits must use before any `닫힘-동작` claim is accepted.

Contract rules:

- All 90 cells must be present.
- Every cell must carry file:line evidence references.
- Status reports, proposals, markdown-existence checkers, unrun packs, and external AI claims are excluded as behavior-close evidence.
- `닫힘-동작` requires product-path execution evidence plus reproducible pack/checker evidence.
- UI/workshop/share maru entries require browser or UI runner evidence when behavior closure is claimed.

Boundary:

- No parser/runtime/product UI change.
- No `docs/ssot/**` change.
- No matrix state rejudgement.

Verification:

- `python tests/run_pack_golden.py ganada_maru_verification_contract_v1`
- `python tests/run_ganada_maru_verification_contract_check.py`
