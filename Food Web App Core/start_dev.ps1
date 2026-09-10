# ============================================================
# TCS Food Formulator - Local Development Startup Script
# ============================================================
# Usage: Run from the "Food web App" root directory
#   powershell -ExecutionPolicy Bypass -File start_dev.ps1
# ============================================================

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  TCS FOOD FORMULATOR - LOCAL DEVELOPMENT LAUNCHER" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$rootDir = $PSScriptRoot

# --- BACKEND SETUP ---
Write-Host "[1/4] Setting up Python virtual environment..." -ForegroundColor Yellow
$backendDir = Join-Path $rootDir "backend"

if (-not (Test-Path (Join-Path $backendDir "venv"))) {
    python -m venv (Join-Path $backendDir "venv")
    Write-Host "      Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "      Virtual environment already exists." -ForegroundColor Green
}

# Install backend dependencies
Write-Host "[2/4] Installing Python backend dependencies..." -ForegroundColor Yellow
$pipPath = Join-Path $backendDir "venv\Scripts\pip.exe"
$requirementsPath = Join-Path $backendDir "requirements.txt"
& $pipPath install -r $requirementsPath --quiet
Write-Host "      Dependencies installed." -ForegroundColor Green

# Copy env file if needed
$envFile = Join-Path $backendDir ".env"
$envExample = Join-Path $backendDir ".env.example"
if (-not (Test-Path $envFile)) {
    Copy-Item $envExample $envFile
    Write-Host ""
    Write-Host "  [IMPORTANT] Backend .env file created from template." -ForegroundColor Magenta
    Write-Host "  Please edit backend\.env and add your GROQ_API_KEY before running!" -ForegroundColor Magenta
    Write-Host ""
}

# --- FRONTEND SETUP ---
Write-Host "[3/4] Installing Node.js frontend dependencies..." -ForegroundColor Yellow
$frontendDir = Join-Path $rootDir "frontend"
Set-Location $frontendDir
npm install --silent
Write-Host "      Dependencies installed." -ForegroundColor Green

# --- LAUNCH SERVICES ---
Write-Host ""
Write-Host "[4/4] Starting services..." -ForegroundColor Yellow

# Start backend in new terminal window
$uvicornPath = Join-Path $backendDir "venv\Scripts\uvicorn.exe"
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host 'TCS Food Formulator - Backend Server' -ForegroundColor Cyan; & '$uvicornPath' main:app --reload --host 0.0.0.0 --port 8000 --app-dir '$backendDir'"
) -WindowStyle Normal

Start-Sleep -Seconds 3

# Start frontend in new terminal window
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Write-Host 'TCS Food Formulator - Frontend Server' -ForegroundColor Cyan; Set-Location '$frontendDir'; npm run dev"
) -WindowStyle Normal

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  Services launching..." -ForegroundColor Green
Write-Host "  Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend App: http://localhost:3000" -ForegroundColor White
Write-Host "  API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "  Default Login: admin@tcs.com / admin123" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
