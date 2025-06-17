@echo off
echo ========================================
echo    Social Media Automation System
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Installing required packages...
pip install flask >nul 2>&1

echo.
echo ========================================
echo    Starting Automation System
echo ========================================
echo.
echo 🌐 Web Interface: http://localhost:5000
echo 📱 Open this URL in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python web_interface.py

pause 