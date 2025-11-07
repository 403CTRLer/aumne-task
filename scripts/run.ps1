param(
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    throw "Virtual environment not found. Run scripts/setup.ps1 first."
}

Write-Host "[run] Starting FastAPI backend" -ForegroundColor Cyan
$backendCommand = "cd `"$PSScriptRoot\..\backend`"; ..\..\.venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand

Write-Host "[run] Starting React frontend" -ForegroundColor Cyan
$frontendCommand = "cd `"$PSScriptRoot\..\frontend`"; npm run dev -- --host"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand

if ($OpenBrowser) {
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:5173"
}

Write-Host "[run] Backend @ http://localhost:8000  Frontend @ http://localhost:5173" -ForegroundColor Green

