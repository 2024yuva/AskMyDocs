@echo off
echo Starting AskMyDocs API Server...
echo API will be available at http://localhost:8000
echo Press Ctrl+C to stop
echo.
call venv\Scripts\activate.bat
uvicorn app.api.main:app --reload
