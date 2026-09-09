use std::path::PathBuf;

use clap::ValueEnum;

pub use ddonirang_tool::live_input::LiveInputTick;

/// Retained CLI spelling adapter. Transport, timing, key mapping, HTTP input,
/// and tape-recording semantics are owned by `ddonirang_tool`.
#[derive(Clone, Copy, Debug, ValueEnum)]
pub enum SamLiveMode {
    Console,
    Web,
}

impl From<SamLiveMode> for ddonirang_tool::live_input::LiveInputMode {
    fn from(value: SamLiveMode) -> Self {
        match value {
            SamLiveMode::Console => Self::Console,
            SamLiveMode::Web => Self::Web,
        }
    }
}

pub struct LiveInput(ddonirang_tool::live_input::LiveInput);

impl LiveInput {
    pub fn new(
        mode: SamLiveMode,
        host: String,
        port: u16,
        madi_hz: u32,
        record_path: Option<PathBuf>,
    ) -> Result<Self, String> {
        ddonirang_tool::live_input::LiveInput::new(mode.into(), host, port, madi_hz, record_path)
            .map(Self)
    }

    pub fn sample_tick(&mut self, madi: u64) -> LiveInputTick {
        self.0.sample_tick(madi)
    }

    pub fn finish(self) -> Result<(), String> {
        self.0.finish()
    }

    pub fn input_url(&self) -> Option<&str> {
        self.0.input_url()
    }
}
