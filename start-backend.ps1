# AURA Backend Startup Script
Write-Host "🚀 Starting AURA Backend Services..." -ForegroundColor Cyan

# Set project path
$projectPath = "C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent"
Set-Location $projectPath

Write-Host "📊 Starting Database Service on port 8002..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\aurabackend\database'; python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload"

Write-Host "🌐 Starting API Gateway on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; .\.venv\Scripts\Activate.ps1; cd aurabackend\api_gateway; python main.py"

Write-Host ""
Write-Host "✅ Backend services starting in separate windows!" -ForegroundColor Green
Write-Host "📊 Database Service: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "🌐 API Gateway: http://localhost:8000/" -ForegroundColor Blue
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")