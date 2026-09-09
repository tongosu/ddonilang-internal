# seamgrim_wave3b_student_submission_v1

Wave3B G7 product gate for durable local student submissions.

The browser runner verifies:

- student assignment export as `classroom_exchange.v0 kind=student_submission`
- submission import/reopen in a fresh browser context
- origin hash, payload hash, run evidence, control snapshot, response text, and lineage fields
- changed student text changes the submission/evidence binding hash
- schema/hash/size tamper rejection
- student text is restored as text, not executable HTML

No server submission, account identity, public upload, new DDN syntax, or `state_hash` formula change is claimed.
