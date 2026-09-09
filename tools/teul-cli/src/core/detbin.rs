use crate::core::state::State;
use crate::core::trace::{Trace, TraceEvent};

pub use ddonirang_tool::state_trace_wire::TraceWireMeta as TraceMeta;

pub fn encode_state(state: &State) -> Vec<u8> {
    ddonirang_tool::state_trace_wire::encode_state_canon_entries(
        state
            .resources
            .iter()
            .map(|(key, value)| (key.as_str(), value.canon())),
    )
}

pub fn encode_trace_bundle(
    source: &str,
    trace: &Trace,
    state_hash: &str,
    meta: &TraceMeta,
) -> Vec<u8> {
    ddonirang_tool::state_trace_wire::encode_trace_output_bundle(
        source,
        trace.events.iter().map(|event| match event {
            TraceEvent::Log(text) => text,
        }),
        state_hash,
        meta,
    )
}
