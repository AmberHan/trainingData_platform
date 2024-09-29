import unittest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodels.dic import Dic  # 替换为包含 Dic 类的文件路径

class TestDicModel(unittest.TestCase):

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

    def test_insert_dic(self):
        # 测试插入新 Dic 记录
        dic = Dic(
            Id="1",
            Value="Value1",
            Name="Name1",
            Type="Type1",
            Description="Description1",
            Sort=1,
            ParentId="0"
        )
        result = Dic.insert(self.session, dic)
        self.assertTrue(result)

        # 验证插入是否成功
        db_dic = self.session.query(Dic).filter_by(Id="1").first()
        self.assertIsNotNone(db_dic)
        self.assertEqual(db_dic.Value, "Value1")

    def test_update_dic(self):
        # 先插入一个 Dic 记录
        dic = Dic(
            Id="2",
            Value="Value2",
            Name="Name2",
            Type="Type2",
            Description="Description2",
            Sort=2,
            ParentId="0"
        )
        Dic.insert(self.session, dic)

        # 更新 Dic 记录
        dic_update = Dic(
            Id="2",
            Value="Updated Value2",
            Name="Updated Name2",
            Type="Updated Type2",
            Description="Updated Description2",
            Sort=5,
            ParentId="1"
        )
        result = Dic.update(self.session, dic_update)
        self.assertTrue(result)

        # 验证更新是否成功
        db_dic = Dic.select_by_id(self.session, "2")
        self.assertIsNotNone(db_dic)
        self.assertEqual(db_dic.Value, "Updated Value2")
        self.assertEqual(db_dic.Sort, 5)

    def test_select_by_id(self):
        # 插入一个 Dic 记录
        dic = Dic(
            Id="3",
            Value="Value3",
            Name="Name3",
            Type="Type3",
            Description="Description3",
            Sort=3,
            ParentId="0"
        )
        Dic.insert(self.session, dic)

        # 测试根据 ID 查询
        db_dic = Dic.select_by_id(self.session, "3")
        self.assertIsNotNone(db_dic)
        self.assertEqual(db_dic.Value, "Value3")
        self.assertEqual(db_dic.Name, "Name3")

    def test_delete_by_id(self):
        # 插入一个 Dic 记录
        dic = Dic(
            Id="4",
            Value="Value4",
            Name="Name4",
            Type="Type4",
            Description="Description4",
            Sort=4,
            ParentId="0"
        )
        Dic.insert(self.session, dic)

        # 删除记录
        result = Dic.delete_by_id(self.session, "4")
        self.assertTrue(result)

        # 验证是否已删除
        db_dic = Dic.select_by_id(self.session, "4")
        self.assertIsNone(db_dic)

    def test_find_by_type(self):
        # 插入多个 Dic 记录
        dic_1 = Dic(
            Id="5",
            Value="Value5",
            Name="Name5",
            Type="TypeA",
            Description="Description5",
            Sort=5,
            ParentId="0"
        )
        dic_2 = Dic(
            Id="6",
            Value="Value6",
            Name="Name6",
            Type="TypeA",
            Description="Description6",
            Sort=6,
            ParentId="0"
        )
        dic_3 = Dic(
            Id="7",
            Value="Value7",
            Name="Name7",
            Type="TypeB",
            Description="Description7",
            Sort=7,
            ParentId="0"
        )
        Dic.insert(self.session, dic_1)
        Dic.insert(self.session, dic_2)
        Dic.insert(self.session, dic_3)

        # 测试根据 Type 查找
        results = Dic.find_by_type(self.session, "TypeA")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].Value, "Value5")
        self.assertEqual(results[1].Value, "Value6")

if __name__ == "__main__":
    unittest.main()
