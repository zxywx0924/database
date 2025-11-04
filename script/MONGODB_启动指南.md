# MongoDB 启动指南

## 快速检查

运行测试脚本检查 MongoDB 是否已运行：
```bash
python script/test_mongodb.py
```

## 启动方法

### 方法 1: Windows 服务（推荐）

如果 MongoDB 已安装为 Windows 服务：

**以管理员身份运行 PowerShell 或 CMD，然后执行：**
```cmd
net start MongoDB
```

**停止服务：**
```cmd
net stop MongoDB
```

**检查服务状态：**
```cmd
sc query MongoDB
```

### 方法 2: 手动启动 mongod

如果 MongoDB 没有作为服务安装，可以手动启动：

1. **创建数据目录（如果不存在）：**
```cmd
mkdir C:\data\db
```

2. **启动 MongoDB：**
```cmd
mongod --dbpath C:\data\db
```

**注意：**
- 这个窗口需要保持打开
- 关闭窗口会停止 MongoDB
- 默认监听 `localhost:27017`

### 方法 3: 使用 Docker（如果已安装 Docker）

```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

**停止容器：**
```bash
docker stop mongodb
```

**重启容器：**
```bash
docker start mongodb
```

### 方法 4: 使用 MongoDB Compass

如果已安装 MongoDB Compass，通常会自动启动 MongoDB 服务。

## 验证连接

启动后，可以通过以下方式验证：

1. **使用 Python 脚本：**
```bash
python script/test_mongodb.py
```

2. **使用 MongoDB Shell（如果已安装）：**
```bash
mongosh
```

3. **直接测试端口：**
```bash
telnet localhost 27017
```

## 项目配置

项目使用的配置（`be/model/store.py`）：
- **连接地址：** `mongodb://localhost:27017`
- **数据库名：** `bookstoredb`

## 常见问题

### 问题 1: "拒绝访问" 或权限错误
**解决：** 以管理员身份运行命令提示符或 PowerShell

### 问题 2: 端口 27017 已被占用
**解决：** 
- 检查是否有其他 MongoDB 实例在运行
- 或更改端口：`mongod --port 27018 --dbpath C:\data\db`
- 同时需要修改 `be/model/store.py` 中的连接地址

### 问题 3: 找不到 mongod 命令
**解决：**
- 将 MongoDB 的 `bin` 目录添加到系统 PATH
- 或使用完整路径启动：`C:\Program Files\MongoDB\Server\8.2\bin\mongod.exe`

### 问题 4: 数据目录不存在
**解决：**
```cmd
mkdir C:\data\db
```

## 安装 MongoDB（如果尚未安装）

1. **下载：** https://www.mongodb.com/try/download/community
2. **选择 Windows 版本**
3. **安装时选择 "Install MongoDB as a Service"**（推荐）
4. **安装完成后，服务会自动启动**

## 下一步

启动 MongoDB 后：
1. 运行后端：`python be/app.py`
2. 测试搜索功能：调用 `/buyer/search_book_advanced` 接口

