@echo off
chcp 65001 >nul
echo ========================================
echo Bookstore 功能测试脚本
echo ========================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%

echo [1/3] 检查项目目录...
if not exist "fe\test" (
    echo ✗ 错误: 找不到 fe\test 目录
    echo   当前目录: %CD%
    pause
    exit /b 1
)
echo ✓ 项目目录正确: %PROJECT_ROOT%
echo.

echo [2/3] 检查 Python 和依赖...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ 错误: 未找到 Python，请先安装 Python 3.6+
    pause
    exit /b 1
)
python --version

REM 检查 pytest
python -c "import pytest" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 警告: 未安装 pytest，正在安装...
    python -m pip install pytest --quiet
    if %errorlevel% neq 0 (
        echo ✗ 安装 pytest 失败
        pause
        exit /b 1
    )
    echo ✓ pytest 已安装
) else (
    echo ✓ pytest 已安装
)
echo.

echo [3/3] 检查后端服务...
echo 提示: 请确保后端服务已启动（运行 script\start_app.bat）
echo.
curl -s http://127.0.0.1:5000/auth/register >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠ 警告: 无法连接到后端服务 http://127.0.0.1:5000
    echo    请先运行 script\start_app.bat 启动后端服务
    echo.
    set /p choice="是否继续运行测试？(Y/N): "
    if /i not "%choice%"=="Y" (
        exit /b 1
    )
) else (
    echo ✓ 后端服务运行正常
)
echo.

echo ========================================
echo 运行测试...
echo ========================================
echo.
echo 提示: 按 Ctrl+C 可以中断测试
echo.

REM 运行所有测试
python -m pytest fe/test/ -v

echo.
echo ========================================
echo 测试完成
echo ========================================
pause

