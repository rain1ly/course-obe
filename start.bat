@echo off
REM Double-click to start the app. No Chinese in this file on purpose (encoding safety).
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv not found. Run: python -m venv .venv
    pause
    exit /b 1
)
echo Starting CourseOBE ...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
