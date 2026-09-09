use blake3;
pub use ddonirang_tool::geoul_bundle::{
    audit_hash, AuditFrameHeader, AuditHeader, GeoulBundleReader, GeoulBundleWriter, GeoulFrame,
    GeoulFramePayload, GeoulSummary, TraceTier, DEFAULT_CHECKPOINT_STRIDE,
};
pub use ddonirang_tool::geoul_snapshot::{
    decode_input_snapshot, encode_input_snapshot, InputSnapshotV1, NetEventV1,
};

use crate::core::detbin::encode_state;
use crate::core::state::State;

pub fn encode_state_for_geoul(state: &State) -> Vec<u8> {
    let mut cleaned = state.clone();
    clear_sam_keys(&mut cleaned);
    encode_state(&cleaned)
}

pub fn geoul_state_hash_bytes(state: &State) -> [u8; 32] {
    let detbin = encode_state_for_geoul(state);
    *blake3::hash(&detbin).as_bytes()
}

fn clear_sam_keys(state: &mut State) {
    let keys = state
        .resources
        .keys()
        .filter(|key| {
            let name = key.as_str();
            name.starts_with("샘.") || name.starts_with("입력상태.")
        })
        .cloned()
        .collect::<Vec<_>>();
    for key in keys {
        state.resources.remove(&key);
    }
}
