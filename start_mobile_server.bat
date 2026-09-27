@echo off
cd /d "%~dp0"
echo ==================================================================
echo   Starting TRAVORA Mobile 9:16 Studio -- Dedicated Mobile Server
echo   Opening: http://localhost:8001
echo ==================================================================

:: Wait 1 second and open browser
start "" "http://localhost:8001"

:: Start the Python mobile backend server on port 8001
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_mobile_server.py
) else (
    python run_mobile_server.py
)

pause
