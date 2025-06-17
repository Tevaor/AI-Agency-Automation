@echo off
echo ========================================
echo File Cleanup and Cloud Storage Automation
echo ========================================
echo.
echo This script will:
echo 1. Scan target folders for files to transfer
echo 2. Compress large folders (>500MB)
echo 3. Upload to cloud storage (NordLocker preferred)
echo 4. Securely delete local copies after verification
echo 5. Generate detailed transfer logs
echo.
echo Security: VPN verification and secure deletion included
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Starting cleanup process...
echo.

REM Run the cleanup script
python file_cleanup_automation.py

echo.
echo ========================================
echo Cleanup process completed!
echo Check the following files for details:
echo - file_cleanup.log (detailed execution log)
echo - files_transferred_log.txt (transfer summary)
echo ========================================
echo.
pause 