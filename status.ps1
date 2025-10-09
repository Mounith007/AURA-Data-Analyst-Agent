# AURA Project Status Script
Write-Host "🌟 AURA - Analyst in a Box - System Status" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check Frontend
Write-Host "🎨 Frontend Service:" -ForegroundColor Magenta
$frontendPorts = @(5173, 5174, 5175, 5176)
$frontendRunning = $false
foreach ($port in $frontendPorts) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$port/" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "  ✅ Frontend running on port $port" -ForegroundColor Green
        Write-Host "  🔗 http://localhost:$port/" -ForegroundColor Blue
        $frontendRunning = $true
        break
    } catch {
        # Continue checking other ports
    }
}
if (-not $frontendRunning) {
    Write-Host "  ❌ Frontend not running" -ForegroundColor Red
}

Write-Host ""

# Check Database Service
Write-Host "🗄️ Database Service (Port 8002):" -ForegroundColor Magenta
try {
    $dbHealth = Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ Database service is healthy" -ForegroundColor Green
    Write-Host "  📊 Status: $($dbHealth.status)" -ForegroundColor Cyan
    Write-Host "  🔗 API Docs: http://localhost:8002/docs" -ForegroundColor Blue
} catch {
    Write-Host "  ❌ Database service not accessible" -ForegroundColor Red
}

Write-Host ""

# Check API Gateway
Write-Host "🌐 API Gateway (Port 8000):" -ForegroundColor Magenta
try {
    $apiResponse = Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ API Gateway is running" -ForegroundColor Green
    Write-Host "  📝 Message: $($apiResponse.message)" -ForegroundColor Cyan
    Write-Host "  🔗 Base URL: http://localhost:8000/" -ForegroundColor Blue
} catch {
    Write-Host "  ❌ API Gateway not accessible" -ForegroundColor Red
}

Write-Host ""

# Check Orchestration Service
Write-Host "🤖 Orchestration Service (Port 8001):" -ForegroundColor Magenta
try {
    $orchResponse = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  ✅ Orchestration service is healthy" -ForegroundColor Green
    Write-Host "  🔗 API Docs: http://localhost:8001/docs" -ForegroundColor Blue
} catch {
    Write-Host "  ❌ Orchestration service not accessible" -ForegroundColor Red
}

Write-Host ""

# Check running processes
Write-Host "🔍 Running Processes:" -ForegroundColor Magenta
$pythonProcesses = Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Select-Object ProcessName, Id, CPU -First 5
$nodeProcesses = Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Select-Object ProcessName, Id, CPU -First 3

if ($pythonProcesses) {
    Write-Host "  🐍 Python processes:" -ForegroundColor Yellow
    $pythonProcesses | ForEach-Object { Write-Host "    - PID: $($_.Id), CPU: $($_.CPU)" -ForegroundColor Gray }
}

if ($nodeProcesses) {
    Write-Host "  📦 Node.js processes:" -ForegroundColor Yellow
    $nodeProcesses | ForEach-Object { Write-Host "    - PID: $($_.Id), CPU: $($_.CPU)" -ForegroundColor Gray }
}

Write-Host ""

# Show port usage
Write-Host "🔌 Port Usage:" -ForegroundColor Magenta
$ports = @("8000", "8001", "8002", "5173", "5174", "5175")
foreach ($port in $ports) {
    $listening = netstat -an | findstr "LISTENING" | findstr ":$port"
    if ($listening) {
        Write-Host "  ✅ Port $port is in use" -ForegroundColor Green
    } else {
        Write-Host "  ⚪ Port $port is available" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🚀 AURA Enterprise Platform Summary:" -ForegroundColor Green
Write-Host "  📱 Modern React Frontend with Navigation" -ForegroundColor Cyan
Write-Host "  🗄️ Universal Database Connectivity (12+ databases)" -ForegroundColor Cyan
Write-Host "  📊 Advanced Data Visualization Engine" -ForegroundColor Cyan
Write-Host "  🤖 AI-Powered Query Generation" -ForegroundColor Cyan
Write-Host "  🔌 Extensible Plugin Architecture" -ForegroundColor Cyan
Write-Host "  🏢 Enterprise-Grade Scalability" -ForegroundColor Cyan

Write-Host ""
Write-Host "💡 Quick Actions:" -ForegroundColor Yellow
Write-Host "  • Open Frontend: http://localhost:5175/" -ForegroundColor Blue
Write-Host "  • Database API: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "  • View Logs: docker-compose logs -f [service_name]" -ForegroundColor Blue
Write-Host "  • Stop Services: Get-Process | Where-Object {`$_.ProcessName -like '*python*'} | Stop-Process -Force" -ForegroundColor Blue