# P5 offline Workbench candidate R1 session delta

Product fixed lineage is `39fc67d5 -> 8c988c00 -> 436cbbfa`; the working tree
is tracked clean and four pre-existing protected untracked deltas are unchanged.

Implemented the deterministic Workbench asset projection, manifest-verified
loopback host, three-name `workbench --no-open` HTTP verification, candidate
archive recursion, and archive executable-set guard.  The Workbench token is
only process-local/temporary and is intentionally absent from this file.

Actual browser automation could not attach to the in-app webview and Edge denied
the local URL because its administrator policy check was unavailable.  This is
an external browser-policy evidence gap, not a product PASS.  No bypass, push,
tag, release, SSOT, SPEC, or protected-custody mutation occurred.
