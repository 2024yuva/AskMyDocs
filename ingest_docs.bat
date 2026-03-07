@echo off
echo Ingesting documents...
echo This will load, chunk, and index all documents in the docs/ folder
echo.
call venv\Scripts\activate.bat
python -c "from app.ingest import ingest_documents; result = ingest_documents(); print('\n=== INGESTION COMPLETE ==='); print(result)"
pause
