@echo off
echo === Start installing Standalone PostOS Dependencies ===

rem 1. Create virtual environment
if not exist .venv (
    echo Creating Python virtual environment (.venv)...
    python -m venv .venv
)

rem 2. Install requirements
echo Installing python dependencies...
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

rem 3. Install Playwright browsers
echo Installing Playwright system dependencies...
.venv\Scripts\playwright install chromium

echo === Installation complete! ===
echo To run the GUI: .venv\Scripts\python scripts\postos_gui.py
pause
