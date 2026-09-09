use crate::core::detbin::{encode_state, encode_trace_bundle, TraceMeta};
use crate::core::{State, Trace};

pub use ddonirang_tool::state_trace_wire::LEGACY_RUNTIME_SSOT_VERSION as SSOT_VERSION;

pub fn state_hash(state: &State) -> String {
    ddonirang_tool::state_trace_wire::blake3_wire_identity(&encode_state(state))
}

pub fn trace_hash(trace: &Trace, source: &str, state_hash: &str, madi: u64, seed: u64) -> String {
    let meta = TraceMeta {
        ssot_version: SSOT_VERSION,
        seed,
        madi,
    };
    let bytes = encode_trace_bundle(source, trace, state_hash, &meta);
    ddonirang_tool::state_trace_wire::blake3_wire_identity(&bytes)
}
