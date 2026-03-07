@echo off
echo Stopping all Python/Uvicorn servers...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.13.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
echo Done!
timeout /t 2
