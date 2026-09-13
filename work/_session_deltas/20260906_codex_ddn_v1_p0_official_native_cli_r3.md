# DDN V1 P0 official Native CLI R3 session delta

- product fixed `dfa7d3d17b25ffbe394df7f1a44184c01844a2ae` is a direct child of
  `ceb549ba7afceded268d316b60684bf150ff0697`; merge count `0`.
- only the Windows public-candidate projection script changed in the product
  fixed commit.
- a missing `ddonilang.exe` copy-list entry previously produced a two-file
  artifact directory without rejection. The fixed script requires exactly the
  three official executable names before later candidate checks run.
- protected untracked custody remains untouched and unstaged.
- next gate: one coherent independent review of this P0 Native CLI row; do not
  infer broader teul retirement or V1 closure from this handoff.
