@echo off
echo ========================================
echo Global Macro Intelligence Hub
echo Efficient Analysis App Starting...
echo ========================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
streamlit run app.py

pause
