# PowerShell script to run the app with EasyOCR
# Change to app directory
Set-Location $PSScriptRoot

# Run the app using virtual environment Python
Write-Host "Starting Ad Verification App..." -ForegroundColor Green
& C:\venv_easyocr\Scripts\python.exe app.py

