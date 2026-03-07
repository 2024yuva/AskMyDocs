@echo off
echo Running test suite...
echo.
call venv\Scripts\activate.bat
pytest tests/ -v
pause
