# ======================================================================
#                    AURA ENTERPRISE PLATFORM STARTUP
# ======================================================================
# 
# AURA: Analyst in a Box - Enterprise Data Platform
# TraWrite-Host "🏢 ENTERPRISE FEATURES:" -ForegroundColor Cyansform your data into insights with AI-powered analytics
#
# ======================================================================

Write-Host "🌟====================================================================🌟" -ForegroundColor Magenta
Write-Host "           AURA - Analyst in a Box Enterprise Platform              " -ForegroundColor Yellow
Write-Host "              Scalable Web Application like Azure/AWS               " -ForegroundColor Yellow
Write-Host "🌟====================================================================🌟" -ForegroundColor Magenta
Write-Host ""

# ======================================================================
# PREREQUISITES CHECK
# ======================================================================
Write-Host "� PREREQUISITES CHECK" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>&1
    Write-Host "✅ npm: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found! Please install npm" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ======================================================================
# PROJECT SETUP
# ======================================================================
Write-Host "📁 PROJECT SETUP" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# Navigate to project directory
$projectPath = "C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✅ Project directory: $projectPath" -ForegroundColor Green
} else {
    Write-Host "❌ Project directory not found: $projectPath" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "✅ Python virtual environment found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Check frontend dependencies
if (Test-Path ".\frontend\node_modules") {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location ".\frontend"
    npm install
    Set-Location $projectPath
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
}

Write-Host ""

# ======================================================================
# SERVICE STATUS CHECK
# ======================================================================
Write-Host "🔍 CHECKING EXISTING SERVICES" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$dbRunning = $false
$apiRunning = $false
$frontendRunning = $false
$frontendPort = $null

# Check Database Service
try {
    Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 2 | Out-Null
    $dbRunning = $true
    Write-Host "✅ Database service already running on port 8002" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Database service not running" -ForegroundColor Yellow
}

# Check API Gateway
try {
    Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 2 | Out-Null
    $apiRunning = $true
    Write-Host "✅ API Gateway already running on port 8000" -ForegroundColor Green
} catch {
    Write-Host "⚠️ API Gateway not running" -ForegroundColor Yellow
}

# Check Frontend
$frontendPorts = @(5173, 5174, 5175, 5176)
foreach ($port in $frontendPorts) {
    try {
        Invoke-RestMethod -Uri "http://localhost:$port/" -TimeoutSec 1 -ErrorAction Stop | Out-Null
        $frontendRunning = $true
        Write-Host "✅ Frontend already running on port $port" -ForegroundColor Green
        break
    } catch {
        # Continue checking
    }
}

if (-not $frontendRunning) {
    Write-Host "⚠️ Frontend not running" -ForegroundColor Yellow
}

Write-Host ""

# ======================================================================
# ARCHITECTURE OVERVIEW
# ======================================================================
Write-Host "🏗️  AURA ARCHITECTURE" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "📊 Database Service (Port 8002):" -ForegroundColor White
Write-Host "   * Universal database connectivity - 12 database types" -ForegroundColor Gray
Write-Host "   * Schema introspection and metadata management" -ForegroundColor Gray
Write-Host "   * Query execution engine with connection pooling" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 API Gateway (Port 8000):" -ForegroundColor White
Write-Host "   * Main API entry point for frontend communication" -ForegroundColor Gray
Write-Host "   * Request routing and load balancing" -ForegroundColor Gray
Write-Host "   * Authentication and authorization" -ForegroundColor Gray
Write-Host ""
Write-Host "🎨 Frontend (Port 5175):" -ForegroundColor White
Write-Host "   * React + TypeScript enterprise UI" -ForegroundColor Gray
Write-Host "   * Interactive data visualization with Chart.js" -ForegroundColor Gray
Write-Host "   * Glass Box IDE for SQL editing and approval" -ForegroundColor Gray
Write-Host "   * Plugin marketplace and strategic demos" -ForegroundColor Gray
Write-Host ""

# ======================================================================
# SERVICE STARTUP
# ======================================================================
Write-Host "🚀 STARTING SERVICES" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

if (-not $dbRunning) {
    Write-Host "🗄️  Starting Database Service (Port 8002)..." -ForegroundColor Yellow
    Write-Host "   Command: python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload" -ForegroundColor Gray
    Write-Host "   Directory: $projectPath\aurabackend\database" -ForegroundColor Gray
    Start-Process powershell -ArgumentList "-Command", "cd '$projectPath\aurabackend\database'; python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "   ✅ Database service startup initiated" -ForegroundColor Green
    Write-Host ""
}

if (-not $apiRunning) {
    Write-Host "🌐 Starting API Gateway (Port 8000)..." -ForegroundColor Yellow
    Write-Host "   Command: python main.py" -ForegroundColor Gray
    Write-Host "   Directory: $projectPath\aurabackend\api_gateway" -ForegroundColor Gray
    Write-Host "   Virtual Env: .\.venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Start-Process powershell -ArgumentList "-Command", "cd '$projectPath'; .\.venv\Scripts\Activate.ps1; cd aurabackend\api_gateway; python main.py" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "   ✅ API Gateway startup initiated" -ForegroundColor Green
    Write-Host ""
}

if (-not $frontendRunning) {
    Write-Host "🎨 Starting Frontend (Auto-detect port)..." -ForegroundColor Yellow
    Write-Host "   Command: npm run dev" -ForegroundColor Gray
    Write-Host "   Directory: $projectPath\frontend" -ForegroundColor Gray
    Write-Host "   Build Tool: Vite (React + TypeScript)" -ForegroundColor Gray
    Start-Process powershell -ArgumentList "-Command", "cd '$projectPath\frontend'; npm run dev" -WindowStyle Minimized
    Start-Sleep -Seconds 5
    Write-Host "   ✅ Frontend startup initiated" -ForegroundColor Green
    Write-Host ""
}

# ======================================================================
# FINAL STATUS VERIFICATION
# ======================================================================
Write-Host "🔍 FINAL STATUS VERIFICATION" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "📊 SERVICE HEALTH CHECK:" -ForegroundColor Magenta

try {
    $dbHealth = Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5
    Write-Host "  ✅ Database Service: HEALTHY (http://localhost:8002)" -ForegroundColor Green
    Write-Host "     Status: $($dbHealth.status)" -ForegroundColor Gray
    Write-Host "     Service: $($dbHealth.service)" -ForegroundColor Gray
} catch {
    Write-Host "  ❌ Database Service: NOT RESPONDING (http://localhost:8002)" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
}

try {
    Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5 | Out-Null
    Write-Host "  ✅ API Gateway: RUNNING (http://localhost:8000)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ API Gateway: NOT RESPONDING (http://localhost:8000)" -ForegroundColor Red
    Write-Host "     Error: $($_.Exception.Message)" -ForegroundColor Gray
}

$frontendFound = $false
$frontendPort = $null
foreach ($port in $frontendPorts) {
    try {
        Invoke-RestMethod -Uri "http://localhost:$port/" -TimeoutSec 2 -ErrorAction Stop | Out-Null
        Write-Host "  ✅ Frontend: RUNNING (http://localhost:$port)" -ForegroundColor Green
        $frontendFound = $true
        $frontendPort = $port
        break
    } catch {
        # Continue checking other ports
    }
}

if (-not $frontendFound) {
    Write-Host "  ❌ Frontend: NOT RESPONDING on any port" -ForegroundColor Red
    Write-Host "     Checked ports: $($frontendPorts -join ', ')" -ForegroundColor Gray
}

Write-Host ""

# ======================================================================
# APPLICATION READY
# ======================================================================
Write-Host "🎉====================================================================🎉" -ForegroundColor Green
Write-Host "                    AURA ENTERPRISE PLATFORM READY!                   " -ForegroundColor Yellow
Write-Host "🎉====================================================================🎉" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 ACCESS POINTS:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
if ($frontendPort) {
    Write-Host "📱 Main Application: http://localhost:$frontendPort/" -ForegroundColor Blue
} else {
    Write-Host "📱 Main Application: http://localhost:5175/ (check terminal for actual port)" -ForegroundColor Blue
}
Write-Host "📊 Database API Docs: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "🌐 API Gateway: http://localhost:8000/" -ForegroundColor Blue
Write-Host ""

Write-Host "� ENTERPRISE FEATURES:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "💾 Universal Database Connectivity:" -ForegroundColor White
Write-Host "   * PostgreSQL, MySQL, SQL Server, Oracle, MongoDB" -ForegroundColor Gray
Write-Host "   * Snowflake, BigQuery, Databricks, Redshift" -ForegroundColor Gray
Write-Host "   * ClickHouse, Cassandra, SQLite - 12 types total" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 Advanced Data Visualization:" -ForegroundColor White
Write-Host "   * Interactive charts - Bar, Line, Pie, Radar, Polar" -ForegroundColor Gray
Write-Host "   * Real-time query execution and results" -ForegroundColor Gray
Write-Host "   * Export capabilities - PNG, Data, Share" -ForegroundColor Gray
Write-Host ""
Write-Host "🤖 AI-Powered Analytics:" -ForegroundColor White
Write-Host "   * Glass Box IDE for SQL editing and approval" -ForegroundColor Gray
Write-Host "   * Multi-agent query generation and validation" -ForegroundColor Gray
Write-Host "   * Context-aware query suggestions" -ForegroundColor Gray
Write-Host ""
Write-Host "🏗️  Enterprise Architecture:" -ForegroundColor White
Write-Host "   * Microservices-based scalable design" -ForegroundColor Gray
Write-Host "   * Plugin marketplace and extensibility" -ForegroundColor Gray
Write-Host "   * Strategic vertical market demos" -ForegroundColor Gray
Write-Host ""

Write-Host "📚 NAVIGATION GUIDE:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "💬 AI Chat: Interactive AI assistant for data analysis" -ForegroundColor White
Write-Host "🗄️  Databases: Connect and manage database connections" -ForegroundColor White
Write-Host "📊 Visualize: Create interactive charts from any database" -ForegroundColor White
Write-Host "🚀 Strategy: View strategic demos and competitive advantages" -ForegroundColor White
Write-Host ""

Write-Host "🛠️  TROUBLESHOOTING:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "* If services fail to start, check Windows Defender/Firewall" -ForegroundColor Yellow
Write-Host "* Database connection issues: Verify database credentials" -ForegroundColor Yellow
Write-Host "* Frontend not loading: Clear browser cache and reload" -ForegroundColor Yellow
Write-Host "* Port conflicts: Services will auto-select available ports" -ForegroundColor Yellow
Write-Host ""

Write-Host "📖 QUICK START:" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "1. Open the main application in your browser" -ForegroundColor White
Write-Host "2. Navigate to 'Databases' to add your first connection" -ForegroundColor White
Write-Host "3. Go to 'Visualize' to create charts from your data" -ForegroundColor White
Write-Host "4. Explore 'Strategy' to see AURA's competitive advantages" -ForegroundColor White
Write-Host ""

Write-Host "🌟 AURA transforms your data into enterprise-grade insights!" -ForegroundColor Magenta
Write-Host "🎯 Ready to compete with Azure, AWS, and other cloud giants!" -ForegroundColor Magenta