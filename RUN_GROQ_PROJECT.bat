@echo off
echo ========================================
echo   Starting AskMyDocs with FREE Groq
echo ========================================
echo.
echo Step 1: Stopping any running servers...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.13.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
timeout /t 2
echo.
echo Step 2: Starting API server (Groq version)...
start "API Server" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && uvicorn app.api.main_groq:app --reload --port 8000"
timeout /t 5
echo.
echo Step 3: Starting Streamlit UI...
start "Streamlit UI" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && streamlit run app/ui/app.py"
echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo.
echo API Server: http://localhost:8000
echo Streamlit UI: http://localhost:8501
echo.
echo Press any key to stop all servers...
pause
echo.
echo Stopping servers...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.13.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
echo Done!
