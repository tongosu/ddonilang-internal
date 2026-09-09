param(
    [string]$OutputRoot = "",
    [bool]$Offline = $true
)

$ErrorActionPreference = "Stop"

function Get-AsciiOccurrenceCount {
    param(
        [byte[]]$Bytes,
        [string]$Needle
    )
    if ([string]::IsNullOrWhiteSpace($Needle)) {
        return 0
    }
    $text = [Text.Encoding]::ASCII.GetString($Bytes)
    return ([regex]::Matches(
        $text,
        [regex]::Escape($Needle),
        [Text.RegularExpressions.RegexOptions]::IgnoreCase
    )).Count
}

function Get-PeStackReserve {
    param([string]$Path)
    $stream = [IO.File]::OpenRead($Path)
    $reader = [IO.BinaryReader]::new($stream)
    try {
        $stream.Position = 0x3c
        $peOffset = $reader.ReadInt32()
        $stream.Position = $peOffset + 24
        $magic = $reader.ReadUInt16()
        if ($magic -ne 0x20b) {
            throw "E_WINDOWS_CANDIDATE_PE32_PLUS_REQUIRED: $Path"
        }
        $stream.Position = $peOffset + 24 + 72
        return $reader.ReadUInt64()
    } finally {
        $reader.Dispose()
        $stream.Dispose()
    }
}

function Test-ByteEqual {
    param([string]$Left, [string]$Right)
    [byte[]]$leftBytes = [IO.File]::ReadAllBytes($Left)
    [byte[]]$rightBytes = [IO.File]::ReadAllBytes($Right)
    return $leftBytes.Length -eq $rightBytes.Length -and
        [Linq.Enumerable]::SequenceEqual($leftBytes, $rightBytes)
}

function Get-CargoConfigSemanticText {
    param([string]$Path)
    return ((Get-Content -LiteralPath $Path | ForEach-Object { $_.Trim() } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) -and -not $_.StartsWith("#") }) -join "`n")
}

function Remove-LocalCargoTargetDir {
    param([string]$SemanticText)
    return [regex]::Replace(
        $SemanticText,
        '(?ms)^\[build\]\r?\ntarget-dir\s*=\s*"[^"\r\n]+"\r?\n?',
        ""
    )
}

function Test-RetiredTeulArtifact {
    param([string]$RelativePath)
    $normalized = $RelativePath.Replace("\", "/")
    return $normalized -match '(?i)(^|/)teul-cli($|[._-])'
}

$sourceRoot = Split-Path -Parent $PSScriptRoot
if (-not $IsWindows -and [Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw "E_WINDOWS_CANDIDATE_WINDOWS_HOST_REQUIRED"
}
if (-not [string]::IsNullOrWhiteSpace($env:RUSTFLAGS) -or
    -not [string]::IsNullOrWhiteSpace($env:CARGO_ENCODED_RUSTFLAGS)) {
    throw "E_WINDOWS_CANDIDATE_INHERITED_RUSTFLAGS_UNSUPPORTED"
}

$cargo = Get-Command cargo -ErrorAction Stop
$rustc = Get-Command rustc -ErrorAction Stop
$python = Get-Command python -ErrorAction Stop
$hostLine = (& $rustc.Path -vV | Select-String '^host:').Line
if ($LASTEXITCODE -ne 0 -or $hostLine -ne 'host: x86_64-pc-windows-msvc') {
    throw "E_WINDOWS_CANDIDATE_X64_MSVC_HOST_REQUIRED: $hostLine"
}

$portableConfig = Join-Path $sourceRoot "tools\public_cargo_config.toml"
$projectedConfig = Join-Path $sourceRoot ".cargo\config.toml"
$expectedConfigSha256 = "454a4ba886da1e98d2d44bf85d91babd1a6a3d3178ae381195b759750404ede5"
if (-not (Test-Path -LiteralPath $projectedConfig)) {
    throw "E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH"
}
$projectedConfigHash = Get-FileHash -Algorithm SHA256 -LiteralPath $projectedConfig
if (-not (Test-Path -LiteralPath $portableConfig)) {
    throw "E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH"
}
$portableConfigHash = Get-FileHash -Algorithm SHA256 -LiteralPath $portableConfig
$portableSemantic = Get-CargoConfigSemanticText -Path $portableConfig
$projectedSemantic = Remove-LocalCargoTargetDir -SemanticText (Get-CargoConfigSemanticText -Path $projectedConfig)
if ($portableConfigHash.Hash.ToLowerInvariant() -ne $expectedConfigSha256 -or
    $projectedSemantic -ne $portableSemantic) {
    throw "E_WINDOWS_CANDIDATE_PUBLIC_CONFIG_MISMATCH"
}

$buildBase = if (-not [string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot
} elseif (-not [string]::IsNullOrWhiteSpace($env:DDN_BUILD_DIR)) {
    Join-Path $env:DDN_BUILD_DIR "native-windows-x64-public-candidate"
} elseif (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
    Join-Path $env:LOCALAPPDATA "ddonirang\build\native-windows-x64-public-candidate"
} else {
    Join-Path ([IO.Path]::GetTempPath()) "ddonirang\native-windows-x64-public-candidate"
}
$buildBase = [IO.Path]::GetFullPath($buildBase)
if (Test-Path -LiteralPath $buildBase) {
    throw "E_WINDOWS_CANDIDATE_OUTPUT_EXISTS: $buildBase"
}
$targetRoot = Join-Path $buildBase "target"
$artifactRoot = Join-Path $buildBase "artifact"
New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
New-Item -ItemType Directory -Path $artifactRoot -Force | Out-Null

$cargoHome = if (-not [string]::IsNullOrWhiteSpace($env:CARGO_HOME)) {
    $env:CARGO_HOME
} elseif (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
    Join-Path $env:USERPROFILE ".cargo"
} else {
    throw "E_WINDOWS_CANDIDATE_REQUIRED_ROOT_MISSING: CARGO_HOME"
}
$rustSysroot = (& $rustc.Path --print sysroot).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($rustSysroot)) {
    throw "E_WINDOWS_CANDIDATE_REQUIRED_ROOT_MISSING: RUST_SYSROOT"
}
$policyRaw = & $python.Path (Join-Path $sourceRoot "tools\wasm_candidate_remap.py") contract `
    --repo-root $sourceRoot --cargo-home $cargoHome --rust-sysroot $rustSysroot
if ($LASTEXITCODE -ne 0) {
    throw "E_WINDOWS_CANDIDATE_REMAP_POLICY_INVALID"
}
$policy = $policyRaw | ConvertFrom-Json
$flags = @($policy.compiler_flags) + @(
    "-C",
    "link-arg=/STACK:16777216",
    "-C",
    "link-arg=/PDBALTPATH:%_PDB%",
    "-C",
    "link-arg=/Brepro"
)
if ($policy.compiler_flags.Count -ne 3) {
    throw "E_WINDOWS_CANDIDATE_REMAP_POLICY_INVALID: expected three compiler mappings"
}

$previousEncodedRustFlags = $env:CARGO_ENCODED_RUSTFLAGS
$previousRustFlags = $env:RUSTFLAGS
$previousTargetDir = $env:CARGO_TARGET_DIR
$previousOffline = $env:CARGO_NET_OFFLINE
$previousBuildRoot = $env:DDN_BUILD_REPO_ROOT
try {
    $env:RUSTFLAGS = $null
    $env:CARGO_ENCODED_RUSTFLAGS = [string]::Join([char]0x1f, $flags)
    $env:CARGO_TARGET_DIR = $targetRoot
    $env:DDN_BUILD_REPO_ROOT = "/ddn-src"
    if ($Offline) {
        $env:CARGO_NET_OFFLINE = "true"
    }
    Push-Location $sourceRoot
    try {
        & $cargo.Path build --release --locked --workspace
        if ($LASTEXITCODE -ne 0) {
            throw "E_WINDOWS_CANDIDATE_WORKSPACE_BUILD_FAILED: $LASTEXITCODE"
        }
        & $cargo.Path build --release --locked -p ddonirang-tool --bin ddonilang
        if ($LASTEXITCODE -ne 0) {
            throw "E_WINDOWS_CANDIDATE_OFFICIAL_CANONICAL_CLI_BUILD_FAILED: $LASTEXITCODE"
        }
        & $cargo.Path build --release --locked -p ddonirang-tool --bin 또니랑
        if ($LASTEXITCODE -ne 0) {
            throw "E_WINDOWS_CANDIDATE_OFFICIAL_KOREAN_CLI_BUILD_FAILED: $LASTEXITCODE"
        }
        & $cargo.Path build --release --locked -p ddonirang-tool --bin ddonirang
        if ($LASTEXITCODE -ne 0) {
            throw "E_WINDOWS_CANDIDATE_COMPATIBILITY_ALIAS_BUILD_FAILED: $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }
} finally {
    $env:CARGO_ENCODED_RUSTFLAGS = $previousEncodedRustFlags
    $env:RUSTFLAGS = $previousRustFlags
    $env:CARGO_TARGET_DIR = $previousTargetDir
    $env:CARGO_NET_OFFLINE = $previousOffline
    $env:DDN_BUILD_REPO_ROOT = $previousBuildRoot
}

$koreanCli = [string]::Concat([char[]]@(0xB610, 0xB2C8, 0xB791))
$expectedOfficialArtifactNames = @(
    "ddonilang.exe"
    "ddonirang.exe"
    "$koreanCli.exe"
) | Sort-Object
$built = @(
    (Join-Path $targetRoot "release\ddonilang.exe")
    (Join-Path $targetRoot "release\ddonirang.exe")
    (Join-Path $targetRoot ("release\$koreanCli.exe"))
)
foreach ($path in $built) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "E_WINDOWS_CANDIDATE_ARTIFACT_MISSING: $path"
    }
    Copy-Item -LiteralPath $path -Destination $artifactRoot
}

$licensePath = Join-Path $sourceRoot "LICENSE"
if (-not (Test-Path -LiteralPath $licensePath)) {
    throw "E_WINDOWS_CANDIDATE_LICENSE_MISSING"
}
Copy-Item -LiteralPath $licensePath -Destination (Join-Path $artifactRoot "LICENSE")

$sbomGenerator = Join-Path $sourceRoot "tools\generate_public_candidate_sbom.py"
if (-not (Test-Path -LiteralPath $sbomGenerator)) {
    throw "E_WINDOWS_CANDIDATE_SBOM_GENERATOR_MISSING"
}
$sbomPath = Join-Path $artifactRoot "SBOM.detjson"
& $python.Path $sbomGenerator --repo-root $sourceRoot --out $sbomPath --verify-repeat
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $sbomPath)) {
    throw "E_WINDOWS_CANDIDATE_SBOM_GENERATION_FAILED"
}

$workbenchProjector = Join-Path $sourceRoot "tools\project_offline_workbench_assets.py"
if (-not (Test-Path -LiteralPath $workbenchProjector)) {
    throw "E_WINDOWS_CANDIDATE_WORKBENCH_PROJECTOR_MISSING"
}
$workbenchRoot = Join-Path $artifactRoot "workbench"
& $python.Path $workbenchProjector --repo-root $sourceRoot --out-root $workbenchRoot --verify-repeat
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath (Join-Path $workbenchRoot "asset_manifest.detjson"))) {
    throw "E_WINDOWS_CANDIDATE_WORKBENCH_PROJECTION_FAILED"
}

$actualOfficialArtifactNames = @(Get-ChildItem -LiteralPath $artifactRoot -Filter "*.exe" -File |
    Select-Object -ExpandProperty Name | Sort-Object)
if (@(Compare-Object -ReferenceObject $expectedOfficialArtifactNames -DifferenceObject $actualOfficialArtifactNames).Count -ne 0) {
    throw "E_WINDOWS_CANDIDATE_OFFICIAL_ARTIFACT_SET_MISMATCH"
}

foreach ($entry in (Get-ChildItem -LiteralPath $artifactRoot -Recurse -Force)) {
    $relative = $entry.FullName.Substring($artifactRoot.Length).TrimStart([char[]]"\/")
    if (Test-RetiredTeulArtifact -RelativePath $relative) {
        throw "E_WINDOWS_CANDIDATE_RETIRED_TEUL_ARTIFACT: $relative"
    }
}

$forbiddenRoots = @($sourceRoot, $buildBase, $cargoHome, $rustSysroot, $env:USERPROFILE)
$rows = @()
foreach ($path in (Get-ChildItem -LiteralPath $artifactRoot -Filter "*.exe" -File)) {
    [byte[]]$bytes = [IO.File]::ReadAllBytes($path.FullName)
    $seen = @{}
    $occurrences = 0
    foreach ($root in $forbiddenRoots) {
        if ([string]::IsNullOrWhiteSpace($root)) {
            continue
        }
        foreach ($pattern in @($root, $root.Replace("\", "/"))) {
            $key = $pattern.ToLowerInvariant()
            if (-not $seen.ContainsKey($key)) {
                $seen[$key] = $true
                $occurrences += Get-AsciiOccurrenceCount -Bytes $bytes -Needle $pattern
            }
        }
    }
    if ($occurrences -ne 0) {
        throw "E_WINDOWS_CANDIDATE_INTERNAL_PATH: $($path.Name) count=$occurrences"
    }
    $stackReserve = Get-PeStackReserve -Path $path.FullName
    if ($stackReserve -ne 16777216) {
        throw "E_WINDOWS_CANDIDATE_STACK_RESERVE: $($path.Name) bytes=$stackReserve"
    }
    & $path.FullName --help | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "E_WINDOWS_CANDIDATE_STARTUP_FAILED: $($path.Name) exit=$LASTEXITCODE"
    }
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $path.FullName
    $rows += [pscustomobject]@{
        name = $path.Name
        bytes = $path.Length
        sha256 = $hash.Hash.ToLowerInvariant()
        stack_reserve_bytes = $stackReserve
        forbidden_path_occurrences = $occurrences
    }
}

$payloadRows = @(
    Get-ChildItem -LiteralPath $artifactRoot -Recurse -File |
        Where-Object { $_.FullName -ne (Join-Path $artifactRoot "CANDIDATE_MANIFEST.detjson") } |
        Sort-Object FullName |
        ForEach-Object {
            $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName
            [ordered]@{
                path = $_.FullName.Substring($artifactRoot.Length).TrimStart([char[]]"\\/").Replace("\", "/")
                bytes = $_.Length
                sha256 = $hash.Hash.ToLowerInvariant()
            }
        }
)
$candidateManifest = [ordered]@{
    schema = "ddonirang.windows_public_candidate_manifest.v1"
    files = $payloadRows
}
$manifestPath = Join-Path $artifactRoot "CANDIDATE_MANIFEST.detjson"
[IO.File]::WriteAllText(
    $manifestPath,
    (($candidateManifest | ConvertTo-Json -Depth 5 -Compress) + "`n"),
    [Text.UTF8Encoding]::new($false)
)
$manifestHash = Get-FileHash -Algorithm SHA256 -LiteralPath $manifestPath
$archiveBuilder = Join-Path $sourceRoot "tools\create_deterministic_windows_candidate_archive.py"
if (-not (Test-Path -LiteralPath $archiveBuilder)) {
    throw "E_WINDOWS_CANDIDATE_ARCHIVE_BUILDER_MISSING"
}
$archivePath = Join-Path $buildBase "ddonirang-windows-x64-candidate.zip"
& $python.Path $archiveBuilder --artifact-root $artifactRoot --manifest $manifestPath --out $archivePath --verify-repeat
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $archivePath)) {
    throw "E_WINDOWS_CANDIDATE_ARCHIVE_GENERATION_FAILED"
}
$archiveHash = Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath
$buildResult = [ordered]@{
    schema = "ddonirang.windows_public_candidate_result.v1"
    status = "PASS"
    artifact_manifest = "artifact/CANDIDATE_MANIFEST.detjson"
    artifact_manifest_sha256 = $manifestHash.Hash.ToLowerInvariant()
    artifact_file_count = $payloadRows.Count
    candidate_archive = "ddonirang-windows-x64-candidate.zip"
    candidate_archive_sha256 = $archiveHash.Hash.ToLowerInvariant()
}
[IO.File]::WriteAllText(
    (Join-Path $buildBase "WINDOWS_CANDIDATE_SUCCESS.detjson"),
    (($buildResult | ConvertTo-Json -Depth 4 -Compress) + "`n"),
    [Text.UTF8Encoding]::new($false)
)

$rows | Sort-Object name | Format-Table -AutoSize
Write-Host "WINDOWS_X64_PUBLIC_CANDIDATE_BUILD_PASS: $artifactRoot"
