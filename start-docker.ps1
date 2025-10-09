# AURA Backend Docker Startup Script for Windows
Write-Host "🚀 Starting AURA Backend Services in Docker..." -ForegroundColor Green

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down

# Build and start services
Write-Host "🏗️ Building and starting services..." -ForegroundColor Cyan
docker-compose up --build -d

# Wait for services to start
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 Database Service (Port 8002):" -ForegroundColor Magenta
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8002/health" -TimeoutSec 5
    Write-Host "✅ Database service is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Database service not ready: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🌐 API Gateway (Port 8000):" -ForegroundColor Magenta
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ API Gateway is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ API Gateway not ready: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🤖 Orchestration Service (Port 8001):" -ForegroundColor Magenta
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 5
    Write-Host "✅ Orchestration service is healthy" -ForegroundColor Green
} catch {
    Write-Host "❌ Orchestration service not ready: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "📚 API Documentation:" -ForegroundColor Yellow
Write-Host "🔗 Database Service: http://localhost:8002/docs" -ForegroundColor Blue
Write-Host "🔗 API Gateway: http://localhost:8000/docs" -ForegroundColor Blue
Write-Host "🔗 Orchestration: http://localhost:8001/docs" -ForegroundColor Blue

Write-Host ""
Write-Host "✅ AURA Backend is running in Docker!" -ForegroundColor Green
Write-Host "💡 Use 'docker-compose logs -f [service_name]' to view logs" -ForegroundColor Yellow
Write-Host "🛑 Use 'docker-compose down' to stop all services" -ForegroundColor Yellow