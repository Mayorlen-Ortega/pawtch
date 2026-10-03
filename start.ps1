$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot
$backendRoot = Join-Path $repoRoot "backend"
$frontendRoot = Join-Path $repoRoot "frontend"

function Stop-ProcessOnPort {
    param([int]$Port)

    Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
        if ($_.OwningProcess) {
            Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}

Stop-ProcessOnPort -Port 8000
Stop-ProcessOnPort -Port 4200

$backendCommand = @"
Set-Location '$backendRoot'
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
"@

$frontendCommand = @"
Set-Location '$frontendRoot'
npm start -- --port 4200
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand

Write-Host "Servicios iniciados."
Write-Host "Frontend: http://localhost:4200"
Write-Host "API: http://localhost:8000/docs"
