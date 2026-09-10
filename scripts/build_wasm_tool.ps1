param(
    [ValidateSet("release", "debug")]
    [string]$Profile = "release",
    [ValidateSet("web", "bundler", "nodejs", "no-modules")]
    [string]$Target = "web",
    [bool]$CopyToUi = $true,
    [ValidateSet("default", "candidate")]
    [string]$SourceRemapMode = "default"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot

$buildRoot = if (-not [string]::IsNullOrWhiteSpace($env:DDN_BUILD_DIR)) {
    $env:DDN_BUILD_DIR
} elseif (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    Join-Path $env:LOCALAPPDATA "ddonirang\\build"
} else {
    Join-Path ([System.IO.Path]::GetTempPath()) "ddonirang\\build"
}
New-Item -ItemType Directory -Path $buildRoot -Force | Out-Null

# Candidate builds compile a fixed-HEAD LF materialization. This keeps the
# official entrypoint deterministic even when the invoking clean worktree was
# checked out with CRLF. The clone is local-only and never becomes release
# authority.
if ($SourceRemapMode -eq "candidate" -and
    $env:DDN_WASM_CANONICAL_SOURCE_MATERIALIZED -ne "1") {
    if ($CopyToUi) {
        throw "E_WASM_CANDIDATE_TRACKED_COPY_FORBIDDEN"
    }
    if (-not [string]::IsNullOrWhiteSpace($env:RUSTFLAGS) -or
        -not [string]::IsNullOrWhiteSpace($env:CARGO_ENCODED_RUSTFLAGS)) {
        throw "E_WASM_BUILD_INHERITED_RUSTFLAGS_UNSUPPORTED"
    }
    & git -C $repoRoot diff --quiet HEAD --
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_SOURCE_DIRTY"
    }
    & git -C $repoRoot diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_SOURCE_DIRTY"
    }
    $sourceHead = (& git -C $repoRoot rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_SOURCE_IDENTITY_UNAVAILABLE"
    }
    $materializedRoot = Join-Path $buildRoot "r3n-candidate-source-lf"
    if (Test-Path -LiteralPath $materializedRoot) {
        throw "E_WASM_CANDIDATE_MATERIALIZATION_TARGET_EXISTS: $materializedRoot"
    }
    & git clone --quiet --shared --no-checkout $repoRoot $materializedRoot
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_MATERIALIZATION_FAILED: clone"
    }
    & git -C $materializedRoot config core.autocrlf false
    & git -C $materializedRoot config core.longpaths true
    & git -C $materializedRoot checkout --quiet --detach $sourceHead
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_MATERIALIZATION_FAILED: checkout"
    }
    & git -C $materializedRoot diff --quiet HEAD --
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_MATERIALIZATION_INCOMPLETE"
    }
    $env:DDN_WASM_CANONICAL_SOURCE_MATERIALIZED = "1"
    & (Join-Path $materializedRoot "scripts\build_wasm_tool.ps1") `
        -Profile $Profile -Target $Target -CopyToUi $false -SourceRemapMode candidate
    exit $LASTEXITCODE
}

$outDir = Join-Path $buildRoot "wasm\\ddonirang_tool"
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

# Default behavior remains repository-root-only. R3N candidate mode is explicit,
# rejects inherited flags, and seals a multi-root policy outside tracked assets.
$previousRustFlags = $env:RUSTFLAGS
$previousEncodedRustFlags = $env:CARGO_ENCODED_RUSTFLAGS
$candidatePolicy = $null
if ($SourceRemapMode -eq "candidate") {
    if ($CopyToUi) {
        throw "E_WASM_CANDIDATE_TRACKED_COPY_FORBIDDEN"
    }
    if (-not [string]::IsNullOrWhiteSpace($previousRustFlags) -or
        -not [string]::IsNullOrWhiteSpace($previousEncodedRustFlags)) {
        throw "E_WASM_BUILD_INHERITED_RUSTFLAGS_UNSUPPORTED"
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "E_WASM_REMAP_POLICY_TOOL_UNAVAILABLE: python"
    }
    $cargoHome = if (-not [string]::IsNullOrWhiteSpace($env:CARGO_HOME)) {
        $env:CARGO_HOME
    } elseif (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        Join-Path $env:USERPROFILE ".cargo"
    } else {
        throw "E_WASM_REMAP_REQUIRED_ROOT_MISSING: CARGO_HOME"
    }
    $rustc = Get-Command rustc -ErrorAction SilentlyContinue
    if (-not $rustc) {
        throw "E_WASM_REMAP_POLICY_TOOL_UNAVAILABLE: rustc"
    }
    $rustSysroot = (& $rustc.Path --print sysroot).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_REMAP_REQUIRED_ROOT_MISSING: RUST_SYSROOT"
    }
    $policyJson = & $python.Path (Join-Path $repoRoot "tools\wasm_candidate_remap.py") contract `
        --repo-root $repoRoot --cargo-home $cargoHome --rust-sysroot $rustSysroot
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_REMAP_POLICY_INVALID"
    }
    $candidatePolicy = $policyJson | ConvertFrom-Json
    $flags = @($candidatePolicy.compiler_flags)
    if ($flags.Count -ne 3) {
        throw "E_WASM_REMAP_POLICY_INVALID: expected three compiler mappings"
    }
    $env:RUSTFLAGS = $null
    $env:CARGO_ENCODED_RUSTFLAGS = [string]::Join([char]0x1f, $flags)
} else {
    $sourceRemapFlag = "--remap-path-prefix=$repoRoot=/ddn-src"
    $env:RUSTFLAGS = if ([string]::IsNullOrWhiteSpace($previousRustFlags)) {
        $sourceRemapFlag
    } else {
        "$previousRustFlags $sourceRemapFlag"
    }
}

$wasmPack = Get-Command wasm-pack -ErrorAction SilentlyContinue
if ($wasmPack) {
    if ($SourceRemapMode -eq "candidate") {
        $cargo = Get-Command cargo -ErrorAction Stop
        $rustcVersion = (& $rustc.Path --version).Trim()
        $cargoVersion = (& $cargo.Path --version).Trim()
        $wasmToolVersion = (& $wasmPack.Path --version).Trim()
    }
    Push-Location (Join-Path $repoRoot "tool")
    try {
        $profileFlag = if ($Profile -eq "release") { "--release" } else { "" }
        & $wasmPack.Path build . --target $Target $profileFlag --out-dir $outDir --out-name ddonirang_tool -- --features wasm
        $buildExitCode = $LASTEXITCODE
    } finally {
        Pop-Location
        $env:RUSTFLAGS = $previousRustFlags
        $env:CARGO_ENCODED_RUSTFLAGS = $previousEncodedRustFlags
    }
    if ($buildExitCode -ne 0) {
        throw "wasm-pack build failed with exit code $buildExitCode"
    }
    if ($CopyToUi) {
        & (Join-Path $repoRoot "scripts\\copy_wasm_tool_to_ui.ps1") -SourceRoot $outDir
    }
    if ($SourceRemapMode -eq "candidate") {
        & $python.Path (Join-Path $repoRoot "tools\wasm_candidate_remap.py") seal `
            --repo-root $repoRoot --cargo-home $cargoHome --rust-sysroot $rustSysroot `
            --output-dir $outDir --profile $Profile --target $Target `
            --rustc-version $rustcVersion --cargo-version $cargoVersion --wasm-tool-version $wasmToolVersion
        if ($LASTEXITCODE -ne 0) {
            throw "E_WASM_CANDIDATE_SEAL_FAILED"
        }
    }
    Write-Host "WASM build complete (wasm-pack): $outDir"
    exit 0
}

$wasmBindgen = Get-Command wasm-bindgen -ErrorAction SilentlyContinue
if (-not $wasmBindgen) {
    Write-Error "wasm-pack or wasm-bindgen not found in PATH."
    exit 1
}

$profileFlag = if ($Profile -eq "release") { "--release" } else { "" }
try {
    & cargo build -p ddonirang-tool --target wasm32-unknown-unknown --features wasm $profileFlag
    $buildExitCode = $LASTEXITCODE
} finally {
    $env:RUSTFLAGS = $previousRustFlags
    $env:CARGO_ENCODED_RUSTFLAGS = $previousEncodedRustFlags
}
if ($SourceRemapMode -eq "candidate") {
    $cargo = Get-Command cargo -ErrorAction Stop
    $rustcVersion = (& $rustc.Path --version).Trim()
    $cargoVersion = (& $cargo.Path --version).Trim()
    $wasmToolVersion = (& $wasmBindgen.Path --version).Trim()
}
if ($buildExitCode -ne 0) {
    throw "cargo wasm build failed with exit code $buildExitCode"
}

# Cargo honors CARGO_TARGET_DIR, so the bindgen input must be resolved from
# the same target root.  Looking only in the worktree target directory could
# otherwise bind a stale artifact after a clean isolated build.
$cargoTargetRoot = if ([string]::IsNullOrWhiteSpace($env:CARGO_TARGET_DIR)) {
    Join-Path $repoRoot "target"
} else {
    $env:CARGO_TARGET_DIR
}
$wasmIn = Join-Path $cargoTargetRoot ("wasm32-unknown-unknown\\{0}\\ddonirang_tool.wasm" -f $Profile)
if (-not (Test-Path $wasmIn)) {
    Write-Error "WASM not found: $wasmIn"
    exit 1
}

& $wasmBindgen.Path $wasmIn --target $Target --out-dir $outDir --out-name ddonirang_tool --no-typescript
if ($LASTEXITCODE -ne 0) {
    throw "wasm-bindgen failed with exit code $LASTEXITCODE"
}
if ($CopyToUi) {
    & (Join-Path $repoRoot "scripts\\copy_wasm_tool_to_ui.ps1") -SourceRoot $outDir
}
if ($SourceRemapMode -eq "candidate") {
    & $python.Path (Join-Path $repoRoot "tools\wasm_candidate_remap.py") seal `
        --repo-root $repoRoot --cargo-home $cargoHome --rust-sysroot $rustSysroot `
        --output-dir $outDir --profile $Profile --target $Target `
        --rustc-version $rustcVersion --cargo-version $cargoVersion --wasm-tool-version $wasmToolVersion
    if ($LASTEXITCODE -ne 0) {
        throw "E_WASM_CANDIDATE_SEAL_FAILED"
    }
}
Write-Host "WASM build complete (wasm-bindgen): $outDir"
