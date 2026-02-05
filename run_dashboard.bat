@echo off
echo ========================================
echo Global Macro Intelligence Hub
echo Web Dashboard Starting...
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
streamlit run streamlit_app.py

pause
