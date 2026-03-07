@echo off
echo ========================================
echo   Setting up FREE Groq Configuration
echo ========================================
echo.
echo This will configure the project to use:
echo   - Groq API (FREE, fast LLM)
echo   - Sentence Transformers (FREE, local embeddings)
echo.
echo Step 1: Installing required packages...
call venv\Scripts\activate.bat
pip install langchain-groq sentence-transformers
echo.
echo Step 2: Copying configuration...
copy .env.groq .env
echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Get FREE Groq API key: https://console.groq.com/keys
echo   2. Edit .env file and add your GROQ_API_KEY
echo   3. Run: ingest_docs_groq.bat
echo   4. Run: start_api.bat
echo   5. Run: start_ui.bat
echo.
pause
