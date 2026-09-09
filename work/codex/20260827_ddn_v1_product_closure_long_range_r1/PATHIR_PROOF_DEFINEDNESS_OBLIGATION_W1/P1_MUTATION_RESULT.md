# PathIR/Proof XP02·XP05·XP06 successor mutation result

## Actual source mutations in this successor

The final formatted `proof/src/lib.rs` identity before each mutation was:

- bytes: 44,995;
- SHA-256:
  `03a2fa7678d1b1a8c3fd51bf8975ca1b683a508cd7c46ba63775410e8d5da176`.

| ID | Mutation | RED | Exact restore | GREEN |
|---|---|---|---|---|
| P1-M11 | disable request schema-version rejection | exit 1; unknown version reached an `Ok(DefinednessExecution)` | exact SHA above | proof 12/12 |
| P1-M12 internal seam | replace request closure with empty closure | exit 1; `E_SYMBOLIC_DEFINEDNESS_OBLIGATION_REQUIRED_INTERNAL nonzero(x)` | exact SHA above | proof 12/12 |

Mutation residue: 0. Build/test process residue: 0.

P1-M12 is proven only at the internal typed ingress. The required public
CLI/WASM/Workbench field-loss mutation remains
`OWNER_DECISION_REQUIRED / NOT_RUN` because no approved physical field exists.
This report does not rename the internal seam result as public-frontdoor parity.

## Existing fixed predecessor axes

M01~M10 and M13~M14 remain exercised by the existing symbolic/proof tests and
finished GREEN at the successor fixed head. This successor did not fabricate
new mutation infrastructure or claim that an in-memory tamper equals an
additional public wire mutation.

## WASM freshness fail-open correction

Initial observation after changing `proof/src/lib.rs`:

- old checker result: incorrectly PASS;
- root cause: direct `proof/symbolic/numeric` dependencies absent from source
  fingerprint.

After extending the existing checker:

- expected RED: `source_roots/source_file_count/source_tree/source_files mismatch`;
- official rebuild and manifest refresh;
- final GREEN: freshness PASS;
- deterministic repeat artifact SHA exact;
- residue: 0.
