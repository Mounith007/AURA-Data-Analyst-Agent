#!/usr/bin/env powershell
# Quick Start Script for AURA Development

Write-Host "🚀 Quick AURA Startup" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Gray

# Check if we're in the right directory
if (-not (Test-Path "aurabackend")) {
    Write-Host "❌ Please run this from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📊 Starting Database Service (Port 8002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'aurabackend\database'; python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload"

Start-Sleep -Seconds 3

Write-Host "🌐 Starting API Gateway (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", ".\.venv\Scripts\Activate.ps1; cd 'aurabackend\api_gateway'; python main.py"

Start-Sleep -Seconds 3

Write-Host "🎨 Starting Frontend (Port 5173)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'frontend'; npm run dev"

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ All services starting!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:5173" -ForegroundColor Blue
Write-Host "🌐 API Gateway: http://localhost:8000" -ForegroundColor Blue  
Write-Host "📊 Database API: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host ""
Write-Host "🎯 AURA is ready for development!" -ForegroundColor Magenta