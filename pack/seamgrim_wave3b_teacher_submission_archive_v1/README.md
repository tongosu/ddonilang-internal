# seamgrim_wave3b_teacher_submission_archive_v1

Wave3B G8 product gate for local teacher review of student submissions.

Scope:

- collect three `classroom_exchange.v0 kind=student_submission` payloads under one original lesson bundle
- reject duplicate submissions deterministically
- reject submissions from a different lesson/origin
- display prediction/explanation presence, run evidence, observation refs, integrity/version status, and control diff rows
- reopen one submission through the product import path
- export the local review list without auto-scoring or account/cloud claims

Verification:

```bash
python tests/run_seamgrim_wave3b_teacher_submission_archive_check.py
python tests/run_pack_golden.py seamgrim_wave3b_teacher_submission_archive_v1
```
