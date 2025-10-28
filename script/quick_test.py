#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速功能测试脚本
用于快速验证后端 API 是否正常工作
"""
import requests
import time
import sys

# 服务器地址
BASE_URL = "http://127.0.0.1:5000/"


def print_result(name, success, message=""):
    """打印测试结果"""
    status = "✓" if success else "✗"
    print(f"{status} {name}", end="")
    if message:
        print(f" - {message}")
    else:
        print()


def test_register():
    """测试用户注册 - 保留 test_ 前缀以支持独立 pytest 运行"""
    user_id = f"test_user_{int(time.time())}"
    password = "test_password"
    
    try:
        response = requests.post(
            f"{BASE_URL}auth/register",
            json={"user_id": user_id, "password": password}
        )
        success = response.status_code == 200
        print_result("用户注册", success, f"用户ID: {user_id}")
        # 为 pytest 添加断言
        assert success, f"用户注册失败，状态码: {response.status_code}"
        # pytest 不期望返回值，但为了 main() 函数使用，我们仍然返回
        # 如果作为 pytest 测试运行，返回值会被忽略并发出警告，这是可以接受的
        return success, user_id, password
    except Exception as e:
        print_result("用户注册", False, f"错误: {e}")
        assert False, f"用户注册异常: {e}"
        return False, None, None


def _test_login(user_id, password):
    """测试用户登录"""
    try:
        response = requests.post(
            f"{BASE_URL}auth/login",
            json={
                "user_id": user_id,
                "password": password,
                "terminal": "test_terminal"
            }
        )
        success = response.status_code == 200
        token = response.json().get("token", "") if success else ""
        print_result("用户登录", success, f"Token: {token[:20]}..." if token else "")
        return success, token
    except Exception as e:
        print_result("用户登录", False, f"错误: {e}")
        return False, None


def _test_create_store(user_id):
    """测试创建店铺"""
    store_id = f"test_store_{int(time.time())}"
    
    try:
        response = requests.post(
            f"{BASE_URL}seller/create_store",
            json={"user_id": user_id, "store_id": store_id}
        )
        success = response.status_code == 200
        print_result("创建店铺", success, f"店铺ID: {store_id}")
        return success, store_id
    except Exception as e:
        print_result("创建店铺", False, f"错误: {e}")
        return False, None


def _test_add_book(user_id, store_id):
    """测试添加书籍"""
    book_info = {
        "id": f"book_{int(time.time())}",
        "title": "测试书籍",
        "author": "测试作者",
        "tags": ["测试", "教程"],
        "price": 29.99
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}seller/add_book",
            json={
                "user_id": user_id,
                "store_id": store_id,
                "book_info": book_info,
                "stock_level": 100
            }
        )
        success = response.status_code == 200
        print_result("添加书籍", success, f"书籍: {book_info['title']}")
        return success, book_info["id"]
    except Exception as e:
        print_result("添加书籍", False, f"错误: {e}")
        return False, None


def _test_search_book(store_id):
    """测试搜索书籍"""
    try:
        response = requests.post(
            f"{BASE_URL}buyer/search_book",
            json={"store_id": store_id}
        )
        success = response.status_code == 200
        print_result("搜索书籍", success)
        return success
    except Exception as e:
        print_result("搜索书籍", False, f"错误: {e}")
        return False


def main():
    """主测试流程"""
    print("=" * 50)
    print("Bookstore 快速功能测试")
    print("=" * 50)
    print()
    print("提示: 请确保后端服务已启动 (运行 script\\start_app.bat)")
    print()
    
    # 检查服务是否运行
    try:
        response = requests.get(f"{BASE_URL}auth/register", timeout=2)
    except requests.exceptions.ConnectionError:
        print("✗ 错误: 无法连接到后端服务")
        print("   请先运行 script\\start_app.bat 启动后端服务")
        sys.exit(1)
    except Exception as e:
        print(f"✗ 错误: {e}")
        sys.exit(1)
    
    print("✓ 后端服务连接正常")
    print()
    
    results = []
    
    # 测试注册
    success, user_id, password = test_register()
    results.append(("注册", success))
    if not success:
        print("\n✗ 注册失败，无法继续测试")
        return
    
    # 测试登录
    success, token = _test_login(user_id, password)
    results.append(("登录", success))
    
    # 测试创建店铺
    success, store_id = _test_create_store(user_id)
    results.append(("创建店铺", success))
    if not success:
        print("\n⚠ 创建店铺失败，跳过后续测试")
        return
    
    # 测试添加书籍
    success, book_id = _test_add_book(user_id, store_id)
    results.append(("添加书籍", success))
    
    # 测试搜索书籍
    success = _test_search_book(store_id)
    results.append(("搜索书籍", success))
    
    # 汇总结果
    print()
    print("=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    for name, success in results:
        status = "通过" if success else "失败"
        print(f"{'✓' if success else '✗'} {name}: {status}")
    
    print()
    print(f"总计: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！")
    else:
        print("⚠ 部分测试失败，请检查后端服务")


if __name__ == "__main__":
    main()

