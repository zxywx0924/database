@echo off
chcp 65001 >nul
echo ========================================
echo Bookstore 后端启动脚本
echo ========================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%

echo [1/2] 检查项目目录...
if not exist "be\app.py" (
    echo ✗ 错误: 找不到 be\app.py
    echo   当前目录: %CD%
    pause
    exit /b 1
)
echo ✓ 项目目录正确: %PROJECT_ROOT%
echo.

echo [2/2] 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ 错误: 未找到 Python，请先安装 Python 3.6+
    pause
    exit /b 1
)
python --version
echo.

echo ========================================
echo 启动应用...
echo ========================================
echo.
echo 提示: 按 Ctrl+C 可以停止服务器
echo   服务器地址: http://localhost:5000
echo.

REM 运行应用（app.py 已自动处理路径问题）
python be/app.py

pause

