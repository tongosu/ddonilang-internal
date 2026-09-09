# seamgrim_private_pilot_release_contract_v1

G2 immutable release contract marker for the Seamgrim private IDC pilot release.

This pack does not claim a remote IDC deployment. The paired checker builds a
local release artifact from an explicit allowlist, verifies the artifact from
inside the artifact directory, and rejects internal docs, work files, test logs,
local data, and floating `latest` dependency tags.
