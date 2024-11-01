@echo off
chcp 65001 >nul
echo ========================================
echo Bookstore 快速功能测试
echo ========================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."

REM 运行快速测试脚本
python script\quick_test.py

pause

