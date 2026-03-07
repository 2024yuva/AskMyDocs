@echo off
echo ========================================
echo   Testing FREE Groq RAG System
echo ========================================
echo.
call venv\Scripts\activate.bat
python -c "from app.chain_groq import ask; print('Question: What is RAG?\n'); result = ask('What is RAG?'); print('ANSWER:'); print(result['answer']); print('\nCITATIONS:', result['citations'])"
echo.
echo ========================================
echo   Test Complete!
echo ========================================
pause
