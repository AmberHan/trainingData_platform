import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.dataStrong import DataStrong  # 替换为包含 DataStrong 类的文件路径


class TestDataStrongModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 创建 SQLite 内存数据库
        cls.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(cls.engine)

    def setUp(self):
        # 每个测试前创建新的会话
        self.session = Session(self.engine)

    def tearDown(self):
        # 每个测试结束后关闭会话
        self.session.close()

    def test_save_data_strong(self):
        # 保存一条 DataStrong 记录
        data_strong = DataStrong(
            Id="1",
            DataId="D001",
            StrongParam="param1",
            IsDelete=False
            )
        data_strong.save(self.session)

        # 从数据库中查询
        result = self.session.query(DataStrong).filter_by(Id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.StrongParam, "param1")

    # def test_select_by_id(self):
    #     # 插入一条 DataStrong 记录
    #     data_strong = DataStrong(
    #         id="2",
    #         DataId="D002",
    #         StrongParam="param2",
    #         IsDelete=False
    #     )
    #     data_strong.save(self.session)
    #
    #     # 测试 select_by_id 方法
    #     result = DataStrong.select_by_id(self.session, "2")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.StrongParam, "param2")

    # def test_find_by_page(self):
    #     # 插入几条 DataStrong 记录
    #     for i in range(10):
    #         data_strong = DataStrong(
    #             id=str(i + 3),
    #             DataId=f"D00{i + 3}",
    #             StrongParam=f"param{i + 3}",
    #             IsDelete=False
    #         )
    #         data_strong.save(self.session)
    #
    #     # 测试分页查询
    #     results, total = DataStrong.find_by_page(self.session, uid="U003", page=1, size=5)
    #     self.assertEqual(len(results), 5)
    #     self.assertEqual(total, 10)  # 总共有 10 条记录
    #     self.assertEqual(results[0].StrongParam, "param3")

    # def test_delete_data_strong(self):
    #     # 插入一条 DataStrong 记录
    #     data_strong = DataStrong(
    #         id="11",
    #         DataId="D011",
    #         StrongParam="param11",
    #         IsDelete=False
    #     )
    #     data_strong.save(self.session)
    #
    #     # 删除记录（软删除）
    #     data_strong.delete(self.session)
    #
    #     # 查询记录，检查是否软删除
    #     result = DataStrong.select_by_id(self.session, "11")
    #     self.assertIsNotNone(result)
    #     self.assertTrue(result.IsDelete)


if __name__ == "__main__":
    unittest.main()
