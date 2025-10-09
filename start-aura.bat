@echo off
echo.
echo ===============================================
echo    AURA - Enterprise Data Analysis Platform
echo ===============================================
echo.

REM Check if PowerShell is available
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: PowerShell not found. Please ensure PowerShell is installed.
    pause
    exit /b 1
)

echo Starting AURA setup and development environment...
echo.

REM Run the PowerShell setup script
powershell -ExecutionPolicy Bypass -File "setup-for-team.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Setup script failed. Please check the PowerShell window for details.
    pause
    exit /b 1
)

echo.
echo Setup completed! Check your browser at http://localhost:5174
pause