param(
    [switch]$GenerateEnvExamples
)

$ErrorActionPreference = "Stop"

Write-Host "[setup] Creating Python virtual environment" -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "[setup] Installing Python dependencies" -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend\requirements.txt
deactivate

if ($GenerateEnvExamples) {
    Write-Host "[setup] Creating backend .env template" -ForegroundColor Cyan
    Set-Content -Path backend\.env -Value "# Populate with your configuration`nDATABASE_URL=sqlite:///./appointments.db`nTWILIO_ACCOUNT_SID=`nTWILIO_AUTH_TOKEN=`nWHATSAPP_FROM_NUMBER=`nREMINDER_LEAD_MINUTES=60`nREMINDER_CHECK_INTERVAL_MINUTES=5"

    Write-Host "[setup] Creating frontend env template" -ForegroundColor Cyan
    Set-Content -Path frontend\.env.local -Value "VITE_API_BASE_URL=http://localhost:8000"
}

Write-Host "[setup] Installing frontend dependencies" -ForegroundColor Cyan
Push-Location frontend
npm install
Pop-Location

Write-Host "[setup] Environment ready" -ForegroundColor Green

