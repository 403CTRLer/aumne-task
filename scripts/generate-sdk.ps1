$ErrorActionPreference = "Stop"

$specPath = Join-Path -Path (Resolve-Path "$PSScriptRoot\..") -ChildPath "sdk\openapi.json"
$outputDir = Join-Path -Path (Resolve-Path "$PSScriptRoot\..") -ChildPath "sdk\python-client"
$image = "openapitools/openapi-generator-cli:v7.5.0"

Write-Host "[sdk] Downloading OpenAPI specification" -ForegroundColor Cyan
Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" -OutFile $specPath

if (Test-Path $outputDir) {
    Write-Host "[sdk] Removing existing client" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $outputDir
}

Write-Host "[sdk] Generating client via Docker" -ForegroundColor Cyan
docker run --rm -v "$((Resolve-Path "$PSScriptRoot\..")):/local" `
    $image generate `
    -i /local/sdk/openapi.json `
    -g python `
    -o /local/sdk/python-client `
    --additional-properties=packageName=python_client,projectName=whatsapp_appointment_sdk

Write-Host "[sdk] Client available in sdk/python-client" -ForegroundColor Green

