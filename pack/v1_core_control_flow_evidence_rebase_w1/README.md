# VC11 control-flow evidence rebase W1

Status: `IMPLEMENTED_UNDER_REVIEW`

This packet rebinds existing control-flow behavior to the explicit
`v1-core-v25` supported-profile frontdoor. It is executable evidence, not a
new semantic authority or a V1 membership/readiness claim.

## Fixed cases

- CF01: condition true, false, and else selection
- CF02-CF04: while loop zero, one, and multiple iterations
- CF05-CF07: iterable zero, one, and multiple iterations with source order
- CF08: implicit current-item scope through a called routine, with a nested condition
- CF09: branch failure returns only a structured diagnostic
- CF10: loop failure returns only a structured diagnostic

The manifest fixes case order, profile identity, fixture hashes, receipt
hashes, and three deterministic repetitions. Expected receipts are captured
from the official native supported-profile product API. The WASM runner calls
the tracked official supported-profile export with the same raw Korean source
and requires exact structured payload parity with native execution.

For checkout-independent identity, fixture and receipt text bytes are
normalized only from CRLF to LF before hashing. Fixture source is passed to
both official frontdoors with that same line-ending normalization. No syntax,
token, or semantic lowering is performed.

## Fail-closed rules

The runners reject a missing or reordered case, missing fixture or receipt,
hash drift, an unknown profile identity, missing native/WASM frontdoor, stale
tracked WASM, zero-match focused tests, receipt drift, nondeterminism, outcome
drift, or partial publish fields in a failure diagnostic.

`tests/run_v1_core_control_flow_fault_injection_w1.py` performs four mutations
only in isolated temporary packet copies, observes RED, discards the copies,
then requires native and WASM GREEN plus byte-identical task-owned tracked
inputs. Product source and tracked WASM are never mutated by this packet.

## Nonclaims

This packet does not close VC11, P1-A, P1, V1 membership/readiness, public
command or executable membership, Workbench default ingress, release,
activation, or Human PASS. Independent review remains required.
