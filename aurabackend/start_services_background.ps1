# Single-window startup script
Write-Host "Starting AURA Backend Services..."
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.api_gateway.main:api_gateway --port 8000 --reload }
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.orchestration_service.main:app --port 8001 --reload }
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.code_generation_service.main:code_gen_app --port 8002 --reload }
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.execution_sandbox.main:execution_app --port 8003 --reload }
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.knowledge_base.main:kb_app --port 8004 --reload }
Start-Job -ScriptBlock { .venv\Scripts\uvicorn.exe aurabackend.metadata_store.main:metadata_app --port 8005 --reload }
Write-Host "All services started as background jobs. Use 'Get-Job' to check status."