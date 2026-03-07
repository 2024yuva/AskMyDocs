@echo off
echo Starting AskMyDocs Streamlit UI...
echo UI will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop
echo.
call venv\Scripts\activate.bat
streamlit run app/ui/app.py
