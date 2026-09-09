use crate::core::fixed64::Fixed64;
use crate::core::geoul::InputSnapshotV1;
use crate::core::state::Key;
use crate::core::unit::UnitDim;
use crate::core::value::{Quantity, Value};
use crate::core::State;
use ddonirang_tool::geoul_snapshot::{project_snapshot_state, SnapshotStateValue};

pub use ddonirang_tool::geoul_snapshot::snapshot_from_held_mask;

pub fn apply_snapshot(state: &mut State, snapshot: &InputSnapshotV1) {
    clear_sam_keys(state);
    for entry in project_snapshot_state(snapshot) {
        match entry.value {
            SnapshotStateValue::Number(value) => set_flag_number(state, entry.key, value),
            SnapshotStateValue::Text(value) => set_flag_text(state, entry.key, value),
        }
    }
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

fn set_flag_number(state: &mut State, key: String, value: i64) {
    let qty = Quantity::new(Fixed64::from_int(value), UnitDim::zero());
    state.resources.insert(Key::new(key), Value::Num(qty));
}

fn set_flag_text(state: &mut State, key: String, value: String) {
    state.resources.insert(Key::new(key), Value::Str(value));
}

#[cfg(test)]
mod tests {
    use super::{apply_snapshot, InputSnapshotV1, Key, State, Value};
    use crate::core::geoul::NetEventV1;
    use ddonirang_tool::runtime_surface::InputSource;

    #[test]
    fn snapshot_adapter_consumes_shared_keyboard_and_network_projection() {
        let snapshot = InputSnapshotV1 {
            madi: 0,
            held_mask: 1,
            pressed_mask: 1,
            released_mask: 0,
            rng_seed: 7,
            frame_source: InputSource::Relay,
            net_events: vec![NetEventV1 {
                sender: "peer".to_string(),
                seq: 2,
                order_key: "peer#2".to_string(),
                payload: "payload".to_string(),
                source: InputSource::ExternalTask,
            }],
        };
        let mut state = State::new();
        apply_snapshot(&mut state, &snapshot);

        assert!(state
            .resources
            .contains_key(&Key::new("입력상태.키_누르고있음.왼쪽")));
        assert_eq!(
            state.resources.get(&Key::new("샘.네트워크.이벤트_요약")),
            Some(&Value::Str("peer\t2\tpeer#2\tpayload".to_string()))
        );
    }
}
