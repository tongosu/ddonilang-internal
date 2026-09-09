# VC09 named-callable evidence rebase W1

Status: `IMPLEMENTED_UNDER_REVIEW`

This packet rebinds existing non-recursive named-callable behavior to the
explicit `v1-core-v25` supported-profile frontdoor. It is executable evidence,
not a new semantic authority or a V1 membership/readiness claim.

## Fixed cases

- NC01: two numeric arguments flow through a named callable and return `5`
- NC02: a text argument returns unchanged as `IDENTITY`
- NC03: an unknown callable fails closed
- NC04: an arity mismatch fails closed
- NC05: a declared type mismatch fails closed
- NC06: a named-callable recursion attempt is explicitly unsupported

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

`tests/run_v1_core_named_callable_fault_injection_w1.py` performs six tamper
axes only in isolated temporary packet copies: case omission, case order,
fixture hash, receipt, outcome, and profile identity. Each must turn RED. The
temporary copies are then discarded and the runner requires native and WASM
GREEN plus byte-identical task-owned inputs. Product source and tracked WASM
are never mutated by this packet.

## Nonclaims

This packet does not close VC09, P1-A, P1, V1 membership/readiness, public
command or executable membership, Workbench default ingress, release,
activation, or Human PASS. Independent review remains required.
