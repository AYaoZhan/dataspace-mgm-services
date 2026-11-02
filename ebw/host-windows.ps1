# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
#
# Host the EBW stack (EBW-Connector, Business Wallet, OSP 2.0 demo portal) with Cloudflare quick tunnels
# on a Windows machine, so that the phones and laptops of all teams can use the same addresses.
# No admin rights, no git needed. Run in PowerShell:
#   irm https://raw.githubusercontent.com/tx-arena-events/portal-backend/main/ebw/host-windows.ps1 | iex
# Stop with Ctrl+C. Keep the window open during the event. A second run keeps keys and data; the addresses change.

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Root = Join-Path $env:USERPROFILE "ebw-host"
$Bin = Join-Path $env:USERPROFILE ".local\bin"
New-Item -ItemType Directory -Force -Path $Root, $Bin | Out-Null
$env:Path = "$Bin;$env:Path"
function Ok($m) { Write-Host "  [OK] $m" -ForegroundColor Green }
function Bad($m) { Write-Host "  [!!] $m" -ForegroundColor Red }

Write-Host "== 1/5 Network: outgoing port 7844 to Cloudflare (needed for the tunnels)"
if (Test-NetConnection region1.v2.argotunnel.com -Port 7844 -InformationLevel Quiet -WarningAction SilentlyContinue) {
  Ok "Port 7844 open"
} else {
  Bad "Port 7844 is blocked in this network. The tunnels will not work (HTTP 530). Use another network, then start again."
  return
}

Write-Host "== 2/5 Code of portal-backend (download as ZIP on the first run only)"
# Keys and data of the services live in .keys\ and data\ inside this folder. Replacing the folder would create
# new keys, and every phone would have to fetch its credentials again. So a second run keeps it.
# To force a fresh download: $env:EBW_FRESH = "1" before the command.
$Ebw = Join-Path $Root "portal-backend-main\ebw"
if ($env:EBW_FRESH -eq "1" -and (Test-Path (Join-Path $Root "portal-backend-main"))) { Remove-Item -Recurse -Force (Join-Path $Root "portal-backend-main") }
if (-not (Test-Path $Ebw)) {
  $Zip = Join-Path $Root "portal-backend.zip"
  Invoke-WebRequest "https://github.com/tx-arena-events/portal-backend/archive/refs/heads/main.zip" -OutFile $Zip
  Expand-Archive $Zip -DestinationPath $Root -Force
  Ok "code downloaded to $Ebw"
} else {
  Ok "code already in $Ebw (keys and data kept)"
}

Write-Host "== 3/5 uv and Python 3.12"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  powershell -ExecutionPolicy ByPass -NoProfile -Command "irm https://astral.sh/uv/install.ps1 | iex" | Out-Null
  $env:Path = "$Bin;$env:Path"
}
Set-Location $Ebw
uv venv -q --python 3.12 .venv
uv pip install -q --python .venv\Scripts\python.exe -r requirements.txt
Ok "Python environment ready"

Write-Host "== 4/5 cloudflared"
if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
  Invoke-WebRequest "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile (Join-Path $Bin "cloudflared.exe")
}
Ok ((cloudflared --version) | Select-Object -First 1)

Write-Host "== 5/5 Start (the five addresses appear in a moment; keep this window open; stop with Ctrl+C)"
Write-Host "   If an address shows 'Error 530' in the browser, the tunnel does not get through (port 7844)."
.\.venv\Scripts\python.exe -m tools.start --tunnel
