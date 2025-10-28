@echo off
REM MongoDB 启动脚本
echo 正在检查 MongoDB 状态...

REM 方法1: 尝试作为 Windows 服务启动
net start MongoDB 2>nul
if %errorlevel% == 0 (
    echo MongoDB 服务已启动！
    goto :end
)

REM 方法2: 检查是否已经在运行（通过测试端口）
python -c "import socket; s=socket.socket(); result=s.connect_ex(('localhost', 27017)); s.close(); exit(0 if result==0 else 1)" 2>nul
if %errorlevel% == 0 (
    echo MongoDB 似乎已经在运行（端口 27017 已打开）
    goto :end
)

echo.
echo MongoDB 未运行，请选择启动方式：
echo.
echo [1] 如果已安装为 Windows 服务，请以管理员身份运行：
echo     net start MongoDB
echo.
echo [2] 手动启动（需要先创建数据目录）：
echo     创建目录: mkdir C:\data\db
echo     启动命令: mongod --dbpath C:\data\db
echo.
echo [3] 如果使用 Docker：
echo     docker run -d -p 27017:27017 --name mongodb mongo
echo.
echo [4] 如果使用 MongoDB Compass 或其他安装，请检查：
echo     - MongoDB 安装路径的 bin 目录
echo     - 数据目录配置
echo.

:end
pause

