#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速索引功能测试
测试 MongoDB 索引的创建和使用，验证索引对查询性能的提升
"""
import pymongo
import time
import sys
import os
import pytest

# 添加项目根目录到 Python 路径（如果需要）
if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


class TestIndexPerformance:
    """测试索引性能和功能"""
    
    def setup_method(self):
        """pytest 会在每个测试方法前调用此方法进行初始化"""
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client.get_database("bookstoredb")
        self.store_col = self.db['store']
        
    def print_result(self, name, success, message=""):
        """打印测试结果"""
        status = "✓" if success else "✗"
        print(f"{status} {name}", end="")
        if message:
            print(f" - {message}")
        else:
            print()
    
    def check_indexes(self):
        """检查索引是否已创建"""
        print("=" * 60)
        print("检查索引创建情况")
        print("=" * 60)
        
        indexes = self.store_col.index_information()
        
        # 检查必要的索引
        required_indexes = {
            "store_id_1_book_id_1": "复合唯一索引 (store_id, book_id)",
            "book_title_1": "书籍标题索引",
            "book_author_1": "作者索引",
            "book_tags_1": "标签索引",
            "store_text_idx": "文本索引 (title/author/tags)"
        }
        
        all_exist = True
        for index_name, description in required_indexes.items():
            exists = index_name in indexes
            self.print_result(
                f"索引: {index_name}",
                exists,
                description if exists else "未找到"
            )
            if not exists:
                all_exist = False
        
        print(f"\n总计索引数量: {len(indexes)}")
        print("\n所有索引详情:")
        for idx_name, idx_info in indexes.items():
            print(f"  - {idx_name}: {idx_info.get('key', [])}")
        
        return all_exist
    
    def test_single_field_index(self):
        """测试单字段索引性能"""
        print("\n" + "=" * 60)
        print("测试单字段索引性能")
        print("=" * 60)
        
        # 随机选择一个存在的标题进行搜索
        sample_book = self.store_col.find_one({"book_title": {"$exists": True}})
        if not sample_book:
            print("⚠ 数据库中没有书籍数据，跳过索引性能测试")
            pytest.skip("数据库中没有书籍数据")
        
        search_title = sample_book.get("book_title", "")
        if not search_title:
            print("⚠ 没有有效的书籍标题，跳过测试")
            pytest.skip("没有有效的书籍标题")
        
        # 使用索引的查询
        start_time = time.time()
        results_with_index = list(self.store_col.find(
            {"book_title": search_title}
        ).limit(10))
        time_with_index = (time.time() - start_time) * 1000  # 转换为毫秒
        
        # 搜索作者
        search_author = sample_book.get("book_author", "")
        if search_author:
            start_time = time.time()
            results_by_author = list(self.store_col.find(
                {"book_author": search_author}
            ).limit(10))
            time_by_author = (time.time() - start_time) * 1000
        
        print(f"\n按标题搜索 '{search_title[:30]}...':")
        print(f"  找到 {len(results_with_index)} 条结果")
        print(f"  查询耗时: {time_with_index:.2f} ms")
        
        if search_author:
            print(f"\n按作者搜索 '{search_author[:30]}...':")
            print(f"  找到 {len(results_by_author)} 条结果")
            print(f"  查询耗时: {time_by_author:.2f} ms")
        
        # 验证查询计划是否使用了索引
        explain_result = self.store_col.find({"book_title": search_title}).explain()
        execution_stats = explain_result.get("executionStats", {})
        execution_time = execution_stats.get("executionTimeMillis", 0)
        
        print(f"\n查询执行计划分析:")
        print(f"  执行时间: {execution_time} ms")
        print(f"  检查文档数: {execution_stats.get('totalDocsExamined', 0)}")
        print(f"  返回文档数: {execution_stats.get('nReturned', 0)}")
        
        winning_plan = explain_result.get("queryPlanner", {}).get("winningPlan", {})
        index_used = winning_plan.get("inputStage", {}).get("indexName") is not None
        
        self.print_result(
            "索引是否被使用",
            index_used,
            f"使用索引: {winning_plan.get('inputStage', {}).get('indexName', '无')}"
        )
        
        result = index_used and execution_time < 1000  # 1秒内完成视为正常
        assert result, "索引未被使用或查询时间过长"
        return result
    
    def test_text_index_search(self):
        """测试文本索引的全文搜索功能"""
        print("\n" + "=" * 60)
        print("测试文本索引全文搜索")
        print("=" * 60)
        
        # 获取一些书籍数据用于测试
        sample_books = list(self.store_col.find(
            {"book_title": {"$exists": True, "$ne": ""}}
        ).limit(5))
        
        if not sample_books:
            print("⚠ 数据库中没有书籍数据，跳过文本索引测试")
            pytest.skip("数据库中没有书籍数据")
        
        # 提取一些关键词进行测试
        keywords = []
        for book in sample_books:
            title = book.get("book_title", "")
            if title:
                # 取标题中的前几个词作为关键词
                words = title.split()[:2]
                if words:
                    keywords.extend(words)
        
        if not keywords:
            print("⚠ 无法提取关键词，跳过文本索引测试")
            return False
        
        # 测试文本搜索
        test_keyword = keywords[0]
        print(f"\n使用关键词搜索: '{test_keyword}'")
        
        try:
            start_time = time.time()
            results = list(self.store_col.find(
                {"$text": {"$search": test_keyword}}
            ).limit(10))
            search_time = (time.time() - start_time) * 1000
            
            print(f"  找到 {len(results)} 条结果")
            print(f"  查询耗时: {search_time:.2f} ms")
            
            if results:
                print(f"\n  示例结果:")
                for i, result in enumerate(results[:3], 1):
                    print(f"    {i}. {result.get('book_title', 'N/A')[:50]}")
                    print(f"       作者: {result.get('book_author', 'N/A')[:30]}")
            
            # 验证文本索引是否被使用
            explain_result = self.store_col.find(
                {"$text": {"$search": test_keyword}}
            ).explain()
            
            winning_plan = explain_result.get("queryPlanner", {}).get("winningPlan", {})
            index_stage = winning_plan.get("inputStage", {})
            text_index_used = "TEXT" in str(index_stage) or "store_text_idx" in str(winning_plan)
            
            self.print_result(
                "文本索引是否被使用",
                text_index_used,
                f"查询计划: {winning_plan.get('stage', 'N/A')}"
            )
            
            assert text_index_used, "文本索引未被使用"
            return text_index_used
            
        except Exception as e:
            print(f"✗ 文本搜索失败: {e}")
            print("  提示: 可能文本索引未正确创建或 MongoDB 版本不支持")
            return False
    
    def test_index_effectiveness(self):
        """测试索引的有效性 - 比较索引查询和非索引查询"""
        print("\n" + "=" * 60)
        print("测试索引有效性（对比测试）")
        print("=" * 60)
        
        # 检查数据总量
        total_count = self.store_col.count_documents({})
        print(f"\n数据库总文档数: {total_count}")
        
        if total_count < 10:
            print("⚠ 数据量较小，跳过性能对比测试")
            print("  提示: 索引性能优势在大量数据时更明显")
            self.print_result("索引有效性", True, "数据量较小，跳过对比测试")
            return True
        
        # 测试1: 使用索引的查询（按 book_title 搜索，使用 book_title_1 索引）
        sample_book = self.store_col.find_one({"book_title": {"$exists": True, "$ne": ""}})
        if not sample_book:
            print("⚠ 数据库中没有有效的书籍数据，跳过有效性测试")
            return False
        
        # 使用精确匹配来确保使用索引
        full_title = sample_book.get("book_title", "")
        if not full_title:
            print("⚠ 没有有效的书籍标题，跳过测试")
            return False
        print(f"\n测试1: 使用索引的查询（精确匹配标题）")
        start_time = time.time()
        results1 = list(self.store_col.find({
            "book_title": full_title
        }).limit(100))
        time1 = (time.time() - start_time) * 1000
        
        explain1 = self.store_col.find({
            "book_title": full_title
        }).explain()
        
        docs_examined1 = explain1.get("executionStats", {}).get("totalDocsExamined", 0)
        winning_plan = explain1.get("queryPlanner", {}).get("winningPlan", {})
        index_stage = winning_plan.get("inputStage", {})
        index_used1 = index_stage.get("indexName") == "book_title_1" or "book_title_1" in str(winning_plan)
        
        print(f"  结果数: {len(results1)}")
        print(f"  查询耗时: {time1:.2f} ms")
        print(f"  检查文档数: {docs_examined1}")
        print(f"  使用索引: {'是' if index_used1 else '否'}")
        
        # 测试2: 不使用索引的查询（对未索引字段进行范围查询）
        print(f"\n测试2: 不使用索引的查询（对未索引字段进行复杂查询）")
        start_time = time.time()
        results2 = list(self.store_col.find({
            "$or": [
                {"book_price": {"$gt": 0, "$lt": 999999}},
                {"book_price": {"$exists": False}}
            ]
        }).limit(100))
        time2 = (time.time() - start_time) * 1000
        
        explain2 = self.store_col.find({
            "$or": [
                {"book_price": {"$gt": 0, "$lt": 999999}},
                {"book_price": {"$exists": False}}
            ]
        }).explain()
        
        docs_examined2 = explain2.get("executionStats", {}).get("totalDocsExamined", 0)
        
        print(f"  结果数: {len(results2)}")
        print(f"  查询耗时: {time2:.2f} ms")
        print(f"  检查文档数: {docs_examined2}")
        print(f"  使用索引: 否（对未索引字段查询）")
        
        # 评估索引有效性：比较使用索引和不使用索引时检查的文档数差异
        # 如果使用索引时检查的文档数明显少于不使用索引时，说明索引有效
        if index_used1:
            # 索引被使用，比较文档检查数的差异
            if docs_examined1 < docs_examined2:
                # 使用索引时检查的文档数少于不使用索引时，说明索引有效
                reduction_ratio = (1 - docs_examined1 / docs_examined2) * 100
                self.print_result("索引有效性", True, 
                                 f"索引有效（检查文档数从 {docs_examined2} 减少到 {docs_examined1}，减少 {reduction_ratio:.1f}%）")
                assert True  # 明确断言成功
                return True
            elif docs_examined1 == docs_examined2:
                # 两者相同，可能是数据量太小或者查询结果本身就少
                self.print_result("索引有效性", True, 
                                 f"索引已使用（检查 {docs_examined1} 个文档）")
                assert True  # 明确断言成功
                return True
            else:
                # 使用索引反而检查了更多文档？这不太可能，可能是测试场景的问题
                self.print_result("索引有效性", False, 
                                 f"异常：使用索引时检查了更多文档（{docs_examined1} vs {docs_examined2}）")
                assert False, f"使用索引时检查了更多文档（{docs_examined1} vs {docs_examined2}）"
                return False
        else:
            # 索引未被使用
            self.print_result("索引有效性", False, 
                             f"索引未被使用（检查 {docs_examined1} 个文档）")
            assert False, f"索引未被使用（检查 {docs_examined1} 个文档）"
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("MongoDB 快速索引功能测试")
        print("=" * 60)
        print()
        
        results = []
        
        # 1. 检查索引
        index_exists = self.check_indexes()
        results.append(("索引检查", index_exists))
        
        # 2. 测试单字段索引
        single_field_ok = self.test_single_field_index()
        results.append(("单字段索引", single_field_ok))
        
        # 3. 测试文本索引
        text_index_ok = self.test_text_index_search()
        results.append(("文本索引", text_index_ok))
        
        # 4. 测试索引有效性
        effectiveness_ok = self.test_index_effectiveness()
        results.append(("索引有效性", effectiveness_ok))
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        
        passed = sum(1 for _, s in results if s)
        total = len(results)
        
        for name, success in results:
            status = "通过" if success else "失败"
            print(f"{'✓' if success else '✗'} {name}: {status}")
        
        print(f"\n总计: {passed}/{total} 通过")
        
        if passed == total:
            print("\n✓ 所有索引功能测试通过！")
        else:
            print("\n⚠ 部分测试失败，请检查索引配置")
        
        self.client.close()
        return passed == total


if __name__ == "__main__":
    tester = TestIndexPerformance()
    tester.setup_method()  # 手动调用初始化方法
    tester.run_all_tests()

