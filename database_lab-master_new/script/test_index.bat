@echo off
chcp 65001 >nul
echo ========================================
echo MongoDB Index Performance Test
echo ========================================
echo.

REM Switch to project root directory
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%

REM Set Python path
set PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%

echo [1/3] Checking MongoDB connection...
python -c "import pymongo; pymongo.MongoClient('mongodb://localhost:27017').server_info()" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Cannot connect to MongoDB
    echo Please run script\start_mongodb.bat first to start MongoDB
    pause
    exit /b 1
)
echo MongoDB connection OK
echo.

echo [2/3] Checking backend service...
curl -s http://127.0.0.1:5000/auth/register >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Backend service is not running, but index test does not need it
    echo Index test will connect to MongoDB directly
)
echo.

echo [3/3] Running index tests...
echo.

python fe\test\test_index_performance.py

echo.
pause
