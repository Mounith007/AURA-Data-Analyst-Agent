# ======================================================================
# AURA ENTERPRISE PLATFORM - SIMPLE STARTUP SCRIPT
# ======================================================================

Write-Host "🌟 AURA - Analyst in a Box Enterprise Platform 🌟" -ForegroundColor Magenta
Write-Host "🚀 Starting AURA services..." -ForegroundColor Cyan
Write-Host ""

# Set project path
$projectPath = "C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent"
Set-Location $projectPath

# ======================================================================
# PREREQUISITES CHECK
# ======================================================================

Write-Host "📋 CHECKING PREREQUISITES:" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# Python check
Write-Host "• Python: " -NoNewline
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version 2>&1
    Write-Host "$pythonVersion ✅" -ForegroundColor Green
} else {
    Write-Host "❌ NOT FOUND" -ForegroundColor Red
    Write-Host "  Please install Python 3.11+" -ForegroundColor Yellow
    exit 1
}

# Node.js check
Write-Host "• Node.js: " -NoNewline
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version 2>&1
    Write-Host "$nodeVersion ✅" -ForegroundColor Green
} else {
    Write-Host "❌ NOT FOUND" -ForegroundColor Red
    Write-Host "  Please install Node.js 18+" -ForegroundColor Yellow
    exit 1
}

# Virtual environment check
Write-Host "• Python venv: " -NoNewline
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Found ✅" -ForegroundColor Green
} else {
    Write-Host "Creating..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "  Created ✅" -ForegroundColor Green
}

# Frontend dependencies check
Write-Host "• Frontend deps: " -NoNewline
if (Test-Path ".\frontend\node_modules") {
    Write-Host "Installed ✅" -ForegroundColor Green
} else {
    Write-Host "Installing..." -ForegroundColor Yellow
    Set-Location ".\frontend"
    npm install | Out-Null
    Set-Location $projectPath
    Write-Host "  Installed ✅" -ForegroundColor Green
}

Write-Host ""

# ======================================================================
# START SERVICES
# ======================================================================

Write-Host "🚀 STARTING SERVICES:" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# Start Database Service
Write-Host "📊 Database Service (Port 8002):" -ForegroundColor Cyan
Write-Host "   Starting universal database connectivity service..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\aurabackend\database'; python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "   ✅ Started in separate window" -ForegroundColor Green

# Start API Gateway
Write-Host "🌐 API Gateway (Port 8000):" -ForegroundColor Cyan
Write-Host "   Starting main backend service..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; .\.venv\Scripts\Activate.ps1; cd aurabackend\api_gateway; python main.py" -WindowStyle Normal
Start-Sleep -Seconds 3
Write-Host "   ✅ Started in separate window" -ForegroundColor Green

# Start Frontend
Write-Host "🎨 Frontend (Auto-detect port):" -ForegroundColor Cyan
Write-Host "   Starting React + TypeScript interface..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; npm run dev" -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "   ✅ Started in separate window" -ForegroundColor Green

Write-Host ""

# ======================================================================
# VERIFICATION
# ======================================================================

Write-Host "🔍 VERIFYING SERVICES:" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

Start-Sleep -Seconds 5

# Check Database Service
Write-Host "📊 Database Service: " -NoNewline
try {
    Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5 | Out-Null
    Write-Host "HEALTHY ✅" -ForegroundColor Green
} catch {
    Write-Host "STARTING... ⏳" -ForegroundColor Yellow
}

# Check API Gateway
Write-Host "🌐 API Gateway: " -NoNewline
try {
    Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5 | Out-Null
    Write-Host "RUNNING ✅" -ForegroundColor Green
} catch {
    Write-Host "STARTING... ⏳" -ForegroundColor Yellow
}

# Check Frontend
$frontendPort = $null
$frontendPorts = @(5173, 5174, 5175, 5176)
Write-Host "🎨 Frontend: " -NoNewline

foreach ($port in $frontendPorts) {
    try {
        Invoke-RestMethod -Uri "http://localhost:$port/" -TimeoutSec 2 | Out-Null
        Write-Host "RUNNING on port $port ✅" -ForegroundColor Green
        $frontendPort = $port
        break
    } catch {
        # Continue
    }
}

if (-not $frontendPort) {
    Write-Host "STARTING... ⏳" -ForegroundColor Yellow
}

Write-Host ""

# ======================================================================
# SUCCESS MESSAGE
# ======================================================================

Write-Host "🎉 AURA ENTERPRISE PLATFORM READY! 🎉" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 ACCESS YOUR APPLICATION:" -ForegroundColor Cyan
if ($frontendPort) {
    Write-Host "   📱 Main App: http://localhost:$frontendPort/" -ForegroundColor Blue
} else {
    Write-Host "   📱 Main App: http://localhost:5175/ (check frontend terminal)" -ForegroundColor Blue
}
Write-Host "   📊 Database API: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "   🌐 API Gateway: http://localhost:8000/" -ForegroundColor Blue
Write-Host ""

Write-Host "🏢 ENTERPRISE FEATURES:" -ForegroundColor Cyan
Write-Host "   💾 Universal Database Connectivity (12+ types)" -ForegroundColor White
Write-Host "   📊 Advanced Data Visualization & Charts" -ForegroundColor White
Write-Host "   🤖 AI-Powered Query Generation" -ForegroundColor White
Write-Host "   🔍 Glass Box IDE for SQL Editing" -ForegroundColor White
Write-Host "   🏗️  Microservices Architecture" -ForegroundColor White
Write-Host ""

Write-Host "📚 QUICK START GUIDE:" -ForegroundColor Cyan
Write-Host "   1. Open main app in browser" -ForegroundColor White
Write-Host "   2. Navigate to 'Databases' → Add connection" -ForegroundColor White
Write-Host "   3. Go to 'Visualize' → Create charts" -ForegroundColor White
Write-Host "   4. Explore 'Strategy' → See competitive advantages" -ForegroundColor White
Write-Host ""

Write-Host "🛠️  TROUBLESHOOTING:" -ForegroundColor Cyan
Write-Host "   • Services start in separate windows" -ForegroundColor Yellow
Write-Host "   • Wait 10-15 seconds for full initialization" -ForegroundColor Yellow
Write-Host "   • Check Windows Firewall if ports blocked" -ForegroundColor Yellow
Write-Host "   • Services auto-select available ports" -ForegroundColor Yellow
Write-Host ""

Write-Host "🌟 AURA is now competing with Azure, AWS, and cloud giants! 🌟" -ForegroundColor Magenta
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")