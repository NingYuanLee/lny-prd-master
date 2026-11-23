param(
  [string]$Name = "lny-prd",
  [string]$SourceRoot = "",
  [string]$InstallRoot = ""
)

$ErrorActionPreference = "Stop"

if ($Name -notmatch '^[a-z][a-z0-9-]*$') {
  throw "Invalid skill name: $Name"
}

if (-not $SourceRoot) {
  $SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}
if (-not $InstallRoot) {
  $InstallRoot = Join-Path $env:USERPROFILE ".agents\skills"
}

$source = (Resolve-Path (Join-Path $SourceRoot $Name)).Path
$destination = Join-Path $InstallRoot $Name

if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md") -PathType Leaf)) {
  throw "Source skill is missing SKILL.md: $source"
}

New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null
if (Test-Path -LiteralPath $destination) {
  $item = Get-Item -LiteralPath $destination -Force
  if ($item.LinkType -ne "Junction") {
    throw "Refusing to replace an existing non-junction path: $destination"
  }
  Remove-Item -LiteralPath $destination -Force
}

New-Item -ItemType Junction -Path $destination -Target $source | Out-Null
$installed = Get-Item -LiteralPath $destination -Force
if ($installed.Target -notcontains $source) {
  throw "Junction verification failed: $destination"
}

Write-Output "Installed $Name"
Write-Output "Source: $source"
Write-Output "Target: $destination"
