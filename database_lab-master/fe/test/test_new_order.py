import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
import uuid


class TestNewOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_new_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_new_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_new_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        yield

    def test_non_exist_book_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=True, low_stock_level=False
        )
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_low_stock_level(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=True
        )
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_ok(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200

    def test_non_exist_user_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        self.buyer.user_id = self.buyer.user_id + "_x"
        code, _ = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code != 200

    def test_non_exist_store_id(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        code, _ = self.buyer.new_order(self.store_id + "_x", buy_book_id_list)
        assert code != 200

    def test_all_error_functions_basic(self):
        """测试所有错误函数的基本功能"""
        from be.model import error
    
        test_id = "test_error_id"
    
        # 测试主要的错误函数
        test_cases = [
        (error.error_non_exist_user_id, test_id),
        (error.error_exist_user_id, test_id),
        (error.error_non_exist_store_id, test_id),
        (error.error_exist_store_id, test_id),
        (error.error_non_exist_book_id, test_id),
        (error.error_exist_book_id, test_id),
        (error.error_stock_level_low, test_id),
        (error.error_invalid_order_id, test_id),
        (error.error_not_sufficient_funds, test_id),
        (error.error_non_order_delete, test_id),
        (error.error_order_repay, test_id),
        (error.error_non_order_pay, test_id),
        (error.error_non_exist_order, test_id),
        (error.error_unable_to_delete, test_id),
        (error.empty_order_search, test_id),
        ]
    
        for error_func, arg in test_cases:
            code, msg = error_func(arg)
            assert code >= 400  # 错误码应该大于等于400
            assert str(arg) in msg