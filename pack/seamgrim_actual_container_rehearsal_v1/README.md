# seamgrim_actual_container_rehearsal_v1

Integrated pack for Seamgrim actual container rehearsal gates.

G5-G9 status:

- Verifies the sealed private-pilot release source inputs.
- Verifies Dockerfile, Compose, and nginx edge policy statically without installing or pulling images.
- Records runtime and approval availability separately from product readiness.
- Records G6-G8 actual runtime gates as blocked when no runtime/pull approval is available.
- Verifies local G9 storage/error hardening without container runtime: project/run/checkpoint limits, public error redaction, raw capability storage rejection, and checkpoint tamper detection.
- Does not claim an actual OCI image build, container run, operational TLS, private IDC deployment, or external user success.

No DDN syntax, parser/runtime semantics, `state_hash`, or `docs/ssot/**` behavior is changed by this pack.
