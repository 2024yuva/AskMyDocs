@echo off
echo ========================================
echo   Ingesting Documents (FREE Version)
echo ========================================
echo.
echo Using FREE embeddings (sentence-transformers)
echo No OpenAI API needed!
echo.
call venv\Scripts\activate.bat
python -c "from app.ingest_groq import ingest_documents; result = ingest_documents(); print('\n=== INGESTION COMPLETE ==='); print(result)"
echo.
pause
