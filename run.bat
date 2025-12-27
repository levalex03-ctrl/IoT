@echo off
echo ========================================
echo  IOT LAB - SMART GARAGE
echo ========================================

echo 1. Installing dependencies...
pip install -r requirements.txt

echo.
echo 2. Starting Flask server (in new window)...
start cmd /k "python server.py"

timeout /t 3 /nobreak

echo.
echo 3. Starting device emulator...
python device.py

echo.
echo Press any key to exit...
pause >nul
