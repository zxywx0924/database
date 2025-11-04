# Bookstore 项目测试指南

## 测试方式

项目提供了多种测试方式，你可以根据需要选择：

### 1. 快速功能测试（推荐新手）

快速验证后端 API 是否正常工作，不依赖 pytest。

**运行方式：**
```cmd
script\quick_test.bat
```

或直接运行：
```cmd
python script\quick_test.py
```

**测试内容：**
- 用户注册
- 用户登录
- 创建店铺
- 添加书籍
- 搜索书籍

### 2. 完整单元测试（推荐开发）

运行项目中的所有 pytest 测试用例。

**运行方式：**
```cmd
script\run_tests.bat
```

或直接运行：
```cmd
python -m pytest fe/test/ -v
```

**运行单个测试文件：**
```cmd
python -m pytest fe/test/test_register.py -v
```

**运行单个测试类：**
```cmd
python -m pytest fe/test/test_register.py::TestRegister -v
```

**运行单个测试方法：**
```cmd
python -m pytest fe/test/test_register.py::TestRegister::test_register_ok -v
```

### 3. 使用 API 测试工具

你可以使用 Postman、curl 或任何 HTTP 客户端工具测试 API。

#### API 端点列表

**认证相关 (http://127.0.0.1:5000/auth/)**
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户登出
- `POST /auth/unregister` - 注销用户
- `POST /auth/password` - 修改密码

**买家相关 (http://127.0.0.1:5000/buyer/)**
- `POST /buyer/new_order` - 创建订单
- `POST /buyer/payment` - 支付订单
- `POST /buyer/add_funds` - 充值
- `POST /buyer/search_book` - 搜索书籍
- `POST /buyer/search_book_advanced` - 高级搜索
- `POST /buyer/search_order` - 查询订单
- `POST /buyer/receive` - 确认收货
- `POST /buyer/delete_order` - 删除订单

**卖家相关 (http://127.0.0.1:5000/seller/)**
- `POST /seller/create_store` - 创建店铺
- `POST /seller/add_book` - 添加书籍
- `POST /seller/add_stock_level` - 增加库存
- `POST /seller/search_order` - 查询订单
- `POST /seller/deliver` - 发货

#### 使用 curl 测试示例

```bash
# 注册用户
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"test_user\",\"password\":\"test_pass\"}"

# 登录
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"test_user\",\"password\":\"test_pass\",\"terminal\":\"web\"}"

# 创建店铺
curl -X POST http://127.0.0.1:5000/seller/create_store \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"test_user\",\"store_id\":\"test_store\"}"
```

#### 使用 Python requests 测试示例

```python
import requests

BASE_URL = "http://127.0.0.1:5000/"

# 注册
response = requests.post(
    f"{BASE_URL}auth/register",
    json={"user_id": "test_user", "password": "test_pass"}
)
print(response.status_code, response.json())

# 登录
response = requests.post(
    f"{BASE_URL}auth/login",
    json={
        "user_id": "test_user",
        "password": "test_pass",
        "terminal": "web"
    }
)
print(response.status_code, response.json())
token = response.json().get("token")

# 创建店铺
response = requests.post(
    f"{BASE_URL}seller/create_store",
    json={"user_id": "test_user", "store_id": "test_store"}
)
print(response.status_code, response.json())
```

## 测试前的准备工作

1. **启动 MongoDB**
   ```cmd
   script\start_mongodb.bat
   ```

2. **启动后端服务**
   ```cmd
   script\start_app.bat
   ```

3. **确保依赖已安装**
   ```cmd
   pip install -r requirements.txt
   ```

## 测试文件说明

所有测试文件位于 `fe/test/` 目录：

- `test_register.py` - 用户注册测试
- `test_login.py` - 用户登录测试
- `test_password.py` - 密码修改测试
- `test_create_store.py` - 创建店铺测试
- `test_add_book.py` - 添加书籍测试
- `test_add_stock_level.py` - 库存管理测试
- `test_new_order.py` - 创建订单测试
- `test_payment.py` - 支付测试
- `test_add_funds.py` - 充值测试
- `test_search_order.py` - 订单查询测试
- `test_book_search.py` - 书籍搜索测试
- `test_deliver.py` - 发货测试
- `test_receive.py` - 收货测试
- `test_delete_order.py` - 删除订单测试
- `test_payment_overtime.py` - 支付超时测试
- `test_bench.py` - 性能基准测试

## 常见问题

### Q: 测试失败，提示连接错误？
A: 确保后端服务已启动，运行 `script\start_app.bat`

### Q: 测试失败，提示 MongoDB 错误？
A: 确保 MongoDB 已启动，运行 `script\start_mongodb.bat` 或 `script\check_mongodb.bat`

### Q: 如何查看详细的测试输出？
A: 使用 `-v` 参数：`python -m pytest fe/test/ -v -s`

### Q: 如何只运行失败的测试？
A: 使用 `--lf` 参数：`python -m pytest fe/test/ --lf`

### Q: 如何生成测试覆盖率报告？
A: 运行 `python -m pytest fe/test/ --cov=be --cov-report=html`，然后打开 `htmlcov/index.html`

## 推荐测试流程

1. **首次测试：** 运行 `script\quick_test.bat` 验证基本功能
2. **完整测试：** 运行 `script\run_tests.bat` 运行所有测试用例
3. **开发调试：** 运行单个测试文件进行调试
4. **API 测试：** 使用 Postman 或其他工具进行集成测试

