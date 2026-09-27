@echo off
cd /d "%~dp0"
echo ==================================================================
echo   TRAVORA DUAL LAUNCHER:
echo   [1] Desktop Web Portal  : http://localhost:8000
echo   [2] Mobile 9:16 Studio  : http://localhost:8001
echo ==================================================================

:: Launch Desktop Server in a separate window
start "TRAVORA Desktop Portal (Port 8000)" cmd /c "if exist .venv\Scripts\python.exe (.venv\Scripts\python.exe run_server.py) else (python run_server.py)"

:: Launch Mobile 9:16 Server in a separate window
start "TRAVORA Mobile 9:16 Studio (Port 8001)" cmd /c "if exist .venv\Scripts\python.exe (.venv\Scripts\python.exe run_mobile_server.py) else (python run_mobile_server.py)"

echo Dual servers initiated successfully.
