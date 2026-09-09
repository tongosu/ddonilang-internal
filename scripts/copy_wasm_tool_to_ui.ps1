param(
    [string]$SourceRoot = "",
    [string]$TargetRoot = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $SourceRoot) {
    $buildRoot = if (-not [string]::IsNullOrWhiteSpace($env:DDN_BUILD_DIR)) {
        $env:DDN_BUILD_DIR
    } elseif (-not [string]::IsNullOrWhiteSpace($env:LOCALAPPDATA)) {
        Join-Path $env:LOCALAPPDATA "ddonirang\\build"
    } else {
        Join-Path ([System.IO.Path]::GetTempPath()) "ddonirang\\build"
    }
    $SourceRoot = Join-Path $buildRoot "wasm\\ddonirang_tool"
}
if (-not $TargetRoot) {
    $TargetRoot = Join-Path $repoRoot "solutions\\seamgrim_ui_mvp\\ui\\wasm"
}

if (-not (Test-Path $SourceRoot)) {
    Write-Error "WASM 산출물 폴더가 없습니다: $SourceRoot"
    exit 1
}

New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null

$files = @(
    "ddonirang_tool.js",
    "ddonirang_tool_bg.wasm",
    "ddonirang_tool.d.ts",
    "package.json"
)

foreach ($name in $files) {
    $src = Join-Path $SourceRoot $name
    if (-not (Test-Path $src)) {
        Write-Error "필수 파일 누락: $src"
        exit 1
    }
    Copy-Item -Path $src -Destination (Join-Path $TargetRoot $name) -Force
}

Write-Host "WASM 산출물 복사 완료: $TargetRoot"
