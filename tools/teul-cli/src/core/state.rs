use crate::core::value::Value;

pub use ddonirang_tool::state_trace_wire::StateKey as Key;

pub type State = ddonirang_tool::state_trace_wire::DeterministicState<Key, Value>;
