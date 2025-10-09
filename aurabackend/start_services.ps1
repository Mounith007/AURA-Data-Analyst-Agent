# PowerShell script to start all AURA backend microservices in separate terminals
$env:PYTHONPATH = "C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent"

Write-Host "Starting AURA Backend Services..."
Write-Host "Setting PYTHONPATH to: $env:PYTHONPATH"

Start-Process powershell -ArgumentList '-NoExit', '-Command', "`$env:PYTHONPATH='C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent'; cd aurabackend\api_gateway; python -m uvicorn main:api_gateway --host 0.0.0.0 --port 8000 --reload"
Start-Process powershell -ArgumentList '-NoExit', '-Command', "`$env:PYTHONPATH='C:\Users\mouni\Documents\GitHub\Data-Analyst-Agent\Data-Analyst-Agent'; cd aurabackend\orchestration_service; python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

Write-Host "API Gateway starting on port 8000..."
Write-Host "Orchestration Service starting on port 8001..."
Write-Host "Services are starting in separate PowerShell windows."
