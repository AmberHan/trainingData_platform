import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.data import Data  # 替换为包含 Data 类的实际文件路径


class TestDataModel(unittest.TestCase):

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

    def test_save_data(self):
        # 保存一条 Data 记录
        data = Data(
            Id="1",
            DataName="Test Data",
            ModuleTypeId="MT001",
            Detail="Test Detail",
            CreateUid="U001",
            IsDelete=False
        )
        data.save(self.session)

        # 从数据库中查询
        result = self.session.query(Data).filter_by(Id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.DataName, "Test Data")
        self.assertEqual(result.Detail, "Test Detail")

    def test_select_by_id(self):
        # 插入一条 Data 记录
        data = Data(
            Id="2",
            DataName="Data 2",
            ModuleTypeId="MT002",
            Detail="Detail 2",
            CreateUid="U002",
            IsDelete=False
        )
        data.save(self.session)

        # 测试 select_by_id 方法
        result = Data.select_by_id(self.session, "2")
        self.assertIsNotNone(result)
        self.assertEqual(result.DataName, "Data 2")
        self.assertEqual(result.Detail, "Detail 2")

    def test_find_by_page(self):
        # 插入几条 Data 记录
        for i in range(10):
            data = Data(
                Id=str(i + 3),
                DataName=f"Data {i + 3}",
                ModuleTypeId=f"MT00{i + 3}",
                Detail=f"Detail {i + 3}",
                CreateUid="U003",
                IsDelete=False
            )
            data.save(self.session)

        # 测试分页查询
        results, total = Data.find_by_page(self.session, uid="U003", page=1, size=5)
        self.assertEqual(len(results), 5)
        self.assertEqual(total, 10)  # 总共有 10 条记录
        self.assertEqual(results[0].DataName, "Data 3")
        self.assertEqual(results[1].DataName, "Data 4")

    def test_delete_data(self):
        # 插入一条 Data 记录
        data = Data(
            Id="11",
            DataName="Data 11",
            ModuleTypeId="MT011",
            Detail="Detail 11",
            CreateUid="U003",
            IsDelete=False
        )
        data.save(self.session)

        # 删除记录（软删除）
        data.delete(self.session)

        # 查询记录，检查是否软删除
        result = Data.select_by_id(self.session, "11")
        self.assertIsNotNone(result)
        self.assertTrue(result.IsDelete)


if __name__ == "__main__":
    unittest.main()
