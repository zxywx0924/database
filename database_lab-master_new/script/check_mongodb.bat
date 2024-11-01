@echo off
chcp 65001 >nul
echo 正在检查 MongoDB 状态...
echo.

REM 检查端口 27017 是否打开
python -c "import socket; s=socket.socket(); s.settimeout(1); result=s.connect_ex(('localhost', 27017)); s.close(); exit(0 if result==0 else 1)" 2>nul
if %errorlevel% == 0 (
    echo ✓ MongoDB 正在运行！
    echo   端口 27017 已打开，可以正常使用
    echo.
    echo 如果需要停止，请：
    echo   - 如果使用服务：net stop MongoDB （需要管理员）
    echo   - 如果手动启动：关闭启动 MongoDB 的命令窗口
    goto :end
)

echo ✗ MongoDB 未运行
echo.
echo 启动方法（选择其一）：
echo.
echo [方法 1] 手动启动（推荐，无需管理员权限）：
echo   双击运行: script\start_mongodb_manual.bat
echo.
echo [方法 2] 以管理员身份启动服务：
echo   1. 右键点击"命令提示符"或"PowerShell"
echo   2. 选择"以管理员身份运行"
echo   3. 执行: net start MongoDB
echo.
echo [方法 3] 在命令行手动启动：
echo   mongod --dbpath %USERPROFILE%\mongodb_data
echo.

:end
pause

