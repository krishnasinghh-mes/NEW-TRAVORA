@echo off
cd /d "%~dp0"
echo ==================================================================
echo   Starting TRAVORA -- AI-Powered Dynamic Tour Platform
echo   Opening: http://localhost:8000
echo ==================================================================

:: Wait 1 second and open browser
start "" "http://localhost:8000"

:: Start the Python backend server
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_server.py
) else (
    python run_server.py
)

pause
