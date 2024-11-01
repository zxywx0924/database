#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 MongoDB 连接"""

import sys
import pymongo

try:
    # 尝试连接 MongoDB (默认 localhost:27017)
    client = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
    # 测试连接
    client.server_info()  # 会抛出异常如果连接失败
    print("✓ MongoDB 连接成功！")
    print(f"  版本: {client.server_info()['version']}")
    print(f"  数据库列表: {client.list_database_names()}")
    # 只在直接运行时才退出（防止 pytest 收集时出错）
    if __name__ == "__main__":
        sys.exit(0)
except pymongo.errors.ServerSelectionTimeoutError:
    print("✗ MongoDB 未运行或无法连接")
    print("\n请启动 MongoDB：")
    print("  方法1: 如果作为 Windows 服务安装，以管理员身份运行:")
    print("    net start MongoDB")
    print("\n  方法2: 手动启动（在 MongoDB 安装目录的 bin 文件夹下）:")
    print("    mongod --dbpath C:\\data\\db")
    print("    注意: 请先创建 C:\\data\\db 目录")
    print("\n  方法3: 使用 Docker（如果已安装）:")
    print("    docker run -d -p 27017:27017 --name mongodb mongo")
    # 只在直接运行时才退出（防止 pytest 收集时出错）
    if __name__ == "__main__":
        sys.exit(1)
except Exception as e:
    print(f"✗ 连接错误: {e}")
    # 只在直接运行时才退出（防止 pytest 收集时出错）
    if __name__ == "__main__":
        sys.exit(1)

