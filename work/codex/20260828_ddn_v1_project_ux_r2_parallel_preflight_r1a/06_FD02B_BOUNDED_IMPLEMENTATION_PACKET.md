# FD02B bounded implementation packet

Status: internal candidate contract only. Product implementation, public schema, stable wire, and default activation are not authorized by this packet.

## Typed state model

| Type | Identity owner | Mutable transition | Durable authority |
|---|---|---|---|
| `EditorGeneration` | in-memory editor/source-set generation plus canonical file identities | each accepted editor mutation creates a new generation | no durable revision per keystroke |
| `RecoveryCheckpoint` | complete editor generation snapshot/reference root plus monotonic local sequence | explicit bounded autosave phase | local recovery only; never silently promoted to saved project |
| `SavedProjectRevision` | project id, revision id, expected parent, semantic config, file/resource reference graph | explicit save CAS | server or explicit local mode, never ambiguous |
| `ExecutionSnapshot` | exact saved revision or explicit local snapshot, source/config/epoch/lock/resource identities, analysis identity | immutable once execution begins | receipt binds the same identity |

Each type must be structurally distinct. A string id from one state cannot be accepted as another state's identity.

## Candidate storage graph

```text
SavedProjectRevision / RecoveryCheckpoint / ExecutionReceipt / ReplayCapsule
                              |
                              v
                   small canonical snapshot node
                  /       |         |          \
        config blob   file blobs  resource blobs  lock blob
```

- file and resource blobs use canonical bytes and domain-separated SHA-256 identities;
- snapshot nodes contain only stable relative names, roles, blob identities, and semantic metadata;
- local absolute paths, mtimes, inode/file ids, OS casing behavior, editor selection, and presentation state are excluded;
- unchanged content reuses the same blob identity across revisions and runs;
- the same resource referenced more than once is stored once and referenced many times;
- unknown blob role/schema or missing referenced blob fails closed before HEAD mutation.

## Write protocol and CAS

1. Canonicalize and validate all candidate bytes in a task-owned staging area.
2. Materialize missing immutable blobs idempotently.
3. Write the snapshot node and an orphan-ledger candidate entry.
4. In one DB transaction, compare `expected_head` with current HEAD, insert revision metadata, and move HEAD.
5. Commit, then mark candidate references reachable/settled.
6. On any failure, readers see the old complete HEAD or the new complete HEAD, never a mixed graph.

CAS failure has revision/head/receipt/output/effect mutation 0. Prewritten immutable blobs may remain only as explicit orphan-ledger entries and are not visible project state.

## Recovery and retention

- recovery is explicit local or server mode; silent fallback is 0;
- checkpoints point to complete snapshot nodes and are not SavedProjectRevision;
- retention is bounded by Owner-approved count/bytes/age constants; this packet does not invent the constants;
- pruning is reachability-based and never treats current saved HEAD, retained receipts, replay capsules, or pinned recovery checkpoints as garbage;
- crash recovery validates every referenced blob and chooses an old-or-new complete root;
- malformed, unsupported, or partially present roots fail closed and remain observable for custody.

## GC roots

Required roots are:

1. every live `SavedProjectRevision` required by retention/history;
2. source/snapshot roots named by retained execution receipts;
3. replay capsule roots;
4. pinned and retention-live `RecoveryCheckpoint` roots;
5. in-flight orphan-ledger candidates until reconciled.

Mark/sweep deletes only unreachable immutable blobs. A bounded dry-run receipt must enumerate kept/deleted identities before actual deletion; deletion authorization is outside this packet.

## Run invariants

```yaml
RUN_MUTATES_SAVED_REVISION: 0
RUN_MUTATES_LOCK: 0
RUN_PERFORMS_NETWORK_RESOLUTION: 0
RUN_REWRITES_SOURCE_RESOURCE_BLOBS: 0
RUN_USES_EXACT_EXECUTION_SNAPSHOT: YES
SERVER_LOCAL_MODE: EXPLICIT
SILENT_FALLBACK: 0
```

## Required evidence before implementation closure

- PUX19-PUX26 and PUX34-PUX35 product runners;
- editor 100 mutations with durable revision growth 0;
- Run×100 with source/resource blob growth 0;
- one-file edit with exactly one changed file blob plus one new small snapshot;
- repeated large resource with one blob identity;
- expected-head race and every prewrite/object/snapshot/HEAD/orphan/GC fault phase;
- save/reopen/restart identity preservation;
- CLI/WASM/Workbench identity parity where each surface participates;
- actual browser plus clean A/B and independent fixed-head review.

## Open Owner inputs

Exact retention limits, maximum blob/snapshot sizes, GC scheduling, public diagnostic codes, and public/stable schemas remain OPEN. Their absence does not block reversible code-independent preflight, but it blocks a total product-success or stable-wire claim.

## 2026-08-29 semantic-readiness gate

The typed state model is not by itself permission to choose observable behavior. Before this
packet can become implementation-ready:

- Owner must select file-only resource declarations or exact recursive-directory semantics;
- SSOT clarification must bind save visibility to old-complete or new-complete, never half;
- SSOT clarification must bind reopen identity mismatch to fail-closed or a separately typed
  non-authoritative recovery candidate, never silent repair;
- v25.17 must be promoted before recovery/saved/Run role separation is current authority.

Already bounded as product policy:

- expected-head stale writer fails closed (PUX26);
- Run does not save or mutate lock;
- only an explicit successful Save may create a durable revision from a recovery candidate;
- host symlink/reparse containment and physical CAS layout are private product choices.

```yaml
FD02B_READINESS: PARTIAL_WITH_SEMANTIC_AND_OWNER_BLOCKERS
IMPLEMENTATION_AUTHORIZED: false
```
