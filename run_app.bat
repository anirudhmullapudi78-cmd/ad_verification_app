@echo off
REM Run the app using the virtual environment Python
cd /d "%~dp0"
echo Starting Ad Verification App...
echo.
REM Set UTF-8 encoding to handle EasyOCR progress bars
chcp 65001 >nul 2>&1
C:\venv_easyocr\Scripts\python.exe app.py
pause

