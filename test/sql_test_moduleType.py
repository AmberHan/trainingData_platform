import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.moduleType import ModuleType  # 替换为包含 ModuleType 类的文件路径


class TestModuleTypeModel(unittest.TestCase):

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

    def test_save_module_type(self):
        # 保存一条 ModuleType 记录
        module_type = ModuleType(
            id="1",
            moduleTypeName="Type A",
            createWay="Automatic",
            icon="icon_a.png",
            createTime="2024-09-01"
            )
        self.session.add(module_type)
        self.session.commit()

        # 从数据库中查询
        result = self.session.query(ModuleType).filter_by(id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.moduleTypeName, "Type A")
        self.assertEqual(result.icon, "icon_a.png")

    def test_select_by_id(self):
        # 插入一个 ModuleType 记录
        module_type = ModuleType(
            id="2",
            moduleTypeName="Type B",
            createWay="Manual",
            icon="icon_b.png",
            createTime="2024-09-02"
            )
        self.session.add(module_type)
        self.session.commit()

        # 测试 select_by_id 方法
        result = ModuleType.select_by_id(self.session, "2")
        self.assertIsNotNone(result)
        self.assertEqual(result.moduleTypeName, "Type B")
        self.assertEqual(result.icon, "icon_b.png")

    def test_find_all(self):
        # 插入多个 ModuleType 记录
        module_type_1 = ModuleType(id="3", moduleTypeName="Type C", createWay="Manual", icon="icon_c.png",
                                   createTime="2024-09-03")
        module_type_2 = ModuleType(id="4", moduleTypeName="Type D", createWay="Automatic", icon="icon_d.png",
                                   createTime="2024-09-04")
        self.session.add(module_type_1)
        self.session.add(module_type_2)
        self.session.commit()

        # 测试 find_all 方法
        results = ModuleType.find_all(self.session)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].moduleTypeName, "Type C")
        self.assertEqual(results[1].moduleTypeName, "Type D")


if __name__ == "__main__":
    unittest.main()
