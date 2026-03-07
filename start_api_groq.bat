@echo off
echo ========================================
echo   Starting API Server (FREE Version)
echo ========================================
echo.
echo Using FREE Groq API + sentence-transformers
echo API will be available at http://localhost:8000
echo.
echo Press Ctrl+C to stop
echo.
call venv\Scripts\activate.bat
uvicorn app.api.main_groq:app --reload
