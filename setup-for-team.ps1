# ======================================================================
# AURA TEAM SETUP SCRIPT
# ======================================================================
# Complete setup and startup script for team members
# Run this once to set up everything, then use for daily development

param(
    [switch]$SetupOnly,
    [switch]$StartOnly
)

Write-Host "🌟 AURA - Team Setup & Startup Script 🌟" -ForegroundColor Magenta
Write-Host "Welcome to the AURA Enterprise Platform!" -ForegroundColor Cyan
Write-Host ""

# ======================================================================
# ENVIRONMENT CHECKS
# ======================================================================

if (-not $StartOnly) {
    Write-Host "🔍 CHECKING DEVELOPMENT ENVIRONMENT" -ForegroundColor Yellow
    Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

    # Check Python
    Write-Host "• Python: " -NoNewline
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.([0-9]+)") {
            $majorVersion = [int]$matches[1]
            if ($majorVersion -ge 11) {
                Write-Host "$pythonVersion ✅" -ForegroundColor Green
            } else {
                Write-Host "$pythonVersion ⚠️  (Recommend 3.11+)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "$pythonVersion ✅" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ NOT FOUND" -ForegroundColor Red
        Write-Host "  Please install Python 3.11+ from https://python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }

    # Check Node.js
    Write-Host "• Node.js: " -NoNewline
    try {
        $nodeVersion = node --version 2>&1
        Write-Host "$nodeVersion ✅" -ForegroundColor Green
    } catch {
        Write-Host "❌ NOT FOUND" -ForegroundColor Red
        Write-Host "  Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Yellow
        exit 1
    }

    # Check npm
    Write-Host "• npm: " -NoNewline
    try {
        $npmVersion = npm --version 2>&1
        Write-Host "v$npmVersion ✅" -ForegroundColor Green
    } catch {
        Write-Host "❌ NOT FOUND" -ForegroundColor Red
        exit 1
    }

    # Check Git
    Write-Host "• Git: " -NoNewline
    try {
        $gitVersion = git --version 2>&1
        Write-Host "$gitVersion ✅" -ForegroundColor Green
    } catch {
        Write-Host "❌ NOT FOUND" -ForegroundColor Red
        Write-Host "  Please install Git from https://git-scm.com/downloads" -ForegroundColor Yellow
        exit 1
    }

    Write-Host ""

    # ======================================================================
    # PROJECT SETUP
    # ======================================================================

    Write-Host "🛠️  SETTING UP PROJECT" -ForegroundColor Yellow
    Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

    # Set project path
    $projectPath = Get-Location
    Write-Host "📁 Project directory: $projectPath" -ForegroundColor Gray

    # Python Virtual Environment
    Write-Host "🐍 Python Virtual Environment: " -NoNewline
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        Write-Host "Found ✅" -ForegroundColor Green
    } else {
        Write-Host "Creating..." -ForegroundColor Yellow
        python -m venv .venv
        Write-Host "  Created ✅" -ForegroundColor Green
    }

    # Activate virtual environment and install dependencies
    Write-Host "📦 Backend Dependencies: " -NoNewline
    try {
        .\.venv\Scripts\Activate.ps1
        pip install --quiet -r aurabackend\requirements.txt
        Write-Host "Installed ✅" -ForegroundColor Green
    } catch {
        Write-Host "Installing..." -ForegroundColor Yellow
        pip install fastapi uvicorn pydantic python-dotenv httpx pandas numpy
        Write-Host "  Installed ✅" -ForegroundColor Green
    }

    # Frontend Dependencies
    Write-Host "🎨 Frontend Dependencies: " -NoNewline
    if (Test-Path ".\frontend\node_modules") {
        Write-Host "Found ✅" -ForegroundColor Green
    } else {
        Write-Host "Installing..." -ForegroundColor Yellow
        Set-Location ".\frontend"
        npm install --silent
        Set-Location $projectPath
        Write-Host "  Installed ✅" -ForegroundColor Green
    }

    # Environment File
    Write-Host "⚙️  Environment Config: " -NoNewline
    if (Test-Path ".\aurabackend\.env") {
        Write-Host "Found ✅" -ForegroundColor Green
    } else {
        Write-Host "Creating..." -ForegroundColor Yellow
        @"
# AURA Backend Environment Variables
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./aura.db
DEBUG=true
LOG_LEVEL=info
"@ | Out-File -FilePath ".\aurabackend\.env" -Encoding utf8
        Write-Host "  Created ✅" -ForegroundColor Green
    }

    Write-Host ""
    Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
    Write-Host ""

    if ($SetupOnly) {
        Write-Host "Setup completed. Run the script again without -SetupOnly to start services." -ForegroundColor Cyan
        exit 0
    }
}

# ======================================================================
# START SERVICES
# ======================================================================

Write-Host "🚀 STARTING DEVELOPMENT SERVICES" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

$projectPath = Get-Location

Write-Host "Starting services in separate windows..." -ForegroundColor Gray
Write-Host ""

# Database Service
Write-Host "📊 Database Service (Port 8002)" -ForegroundColor Cyan
Write-Host "   Universal database connectivity & API" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\aurabackend\database'; python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload"
Start-Sleep -Seconds 2

# API Gateway
Write-Host "🌐 API Gateway (Port 8000)" -ForegroundColor Cyan
Write-Host "   Main backend coordination service" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath'; .\.venv\Scripts\Activate.ps1; cd aurabackend\api_gateway; python main.py"
Start-Sleep -Seconds 2

# Frontend Development Server
Write-Host "🎨 Frontend Development Server" -ForegroundColor Cyan
Write-Host "   React + TypeScript with hot reload" -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectPath\frontend'; npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# ======================================================================
# SERVICE VERIFICATION
# ======================================================================

Write-Host "🔍 VERIFYING SERVICES" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────────────" -ForegroundColor Gray

# Check Database Service
Write-Host "📊 Database Service: " -NoNewline
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5
    Write-Host "HEALTHY ✅" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Gray
} catch {
    Write-Host "STARTING ⏳" -ForegroundColor Yellow
    Write-Host "   (May take a few more seconds)" -ForegroundColor Gray
}

# Check API Gateway
Write-Host "🌐 API Gateway: " -NoNewline
try {
    Invoke-RestMethod -Uri "http://localhost:8000/" -TimeoutSec 5 | Out-Null
    Write-Host "RUNNING ✅" -ForegroundColor Green
} catch {
    Write-Host "STARTING ⏳" -ForegroundColor Yellow
    Write-Host "   (May take a few more seconds)" -ForegroundColor Gray
}

# Check Frontend
Write-Host "🎨 Frontend: " -NoNewline
$frontendPort = $null
$ports = @(5173, 5174, 5175, 5176, 5177)
foreach ($port in $ports) {
    try {
        Invoke-RestMethod -Uri "http://localhost:$port/" -TimeoutSec 2 | Out-Null
        Write-Host "RUNNING on port $port ✅" -ForegroundColor Green
        $frontendPort = $port
        break
    } catch {
        # Continue checking
    }
}

if (-not $frontendPort) {
    Write-Host "STARTING ⏳" -ForegroundColor Yellow
    Write-Host "   (Check the frontend terminal window)" -ForegroundColor Gray
}

Write-Host ""

# ======================================================================
# SUCCESS MESSAGE
# ======================================================================

Write-Host "🎉 AURA DEVELOPMENT ENVIRONMENT READY! 🎉" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

Write-Host "🌐 ACCESS YOUR APPLICATION:" -ForegroundColor Cyan
if ($frontendPort) {
    Write-Host "   📱 Main Application: http://localhost:$frontendPort/" -ForegroundColor Blue
} else {
    Write-Host "   📱 Main Application: http://localhost:5174/ (or check frontend terminal)" -ForegroundColor Blue
}
Write-Host "   📊 Database API Docs: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "   🌐 API Gateway: http://localhost:8000/" -ForegroundColor Blue
Write-Host ""

Write-Host "💻 DEVELOPMENT WORKFLOW:" -ForegroundColor Cyan
Write-Host "   • Frontend auto-reloads on file changes (hot reload enabled)" -ForegroundColor White
Write-Host "   • Backend auto-restarts on Python file changes" -ForegroundColor White
Write-Host "   • Database API documentation available at /docs" -ForegroundColor White
Write-Host "   • All services run in separate terminal windows" -ForegroundColor White
Write-Host ""

Write-Host "🗂️  PROJECT FEATURES:" -ForegroundColor Cyan
Write-Host "   💬 AI Chat - Interactive data analysis assistant" -ForegroundColor White
Write-Host "   🗄️  Databases - Universal database connectivity (12+ types)" -ForegroundColor White
Write-Host "   📊 Visualize - Interactive charts and data visualization" -ForegroundColor White
Write-Host "   🚀 Strategy - Enterprise competitive demonstrations" -ForegroundColor White
Write-Host ""

Write-Host "🐛 TROUBLESHOOTING:" -ForegroundColor Cyan
Write-Host "   • If services don't start: Check the individual terminal windows" -ForegroundColor Yellow
Write-Host "   • Port conflicts: Services will auto-select available ports" -ForegroundColor Yellow
Write-Host "   • Python issues: Ensure virtual environment is activated" -ForegroundColor Yellow
Write-Host "   • Node issues: Try 'npm cache clean --force' in frontend/" -ForegroundColor Yellow
Write-Host ""

Write-Host "📚 HELPFUL COMMANDS:" -ForegroundColor Cyan
Write-Host "   .\setup-for-team.ps1 -SetupOnly    # Just setup, don't start" -ForegroundColor White
Write-Host "   .\setup-for-team.ps1 -StartOnly    # Just start services" -ForegroundColor White
Write-Host "   cd frontend && npm test            # Run frontend tests" -ForegroundColor White
Write-Host "   cd aurabackend && python -m pytest # Run backend tests" -ForegroundColor White
Write-Host ""

Write-Host "🎯 HAPPY CODING! Welcome to the AURA team! 🎯" -ForegroundColor Magenta
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")