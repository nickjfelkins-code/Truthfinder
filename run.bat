@echo off
REM Truth-Finder for Windows. Double-click, then open http://127.0.0.1:5000
REM Needs Python 3.10+ from python.org ("Add python to PATH" checked).
cd /d "%~dp0"
if not exist .venv python -m venv .venv
.venv\Scripts\pip install -q -r requirements.txt
.venv\Scripts\python app.py
pause
