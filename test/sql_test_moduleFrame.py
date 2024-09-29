import unittest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodels.moduleFrame import ModuleFrame  # 替换为包含 ModuleFrame 类的文件路径

class TestModuleFrameModel(unittest.TestCase):

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

    def test_save_module_frame(self):
        # 保存一条 ModuleFrame 记录
        module_frame = ModuleFrame(Id="1", FrameName="Test Frame")
        self.session.add(module_frame)
        self.session.commit()

        # 从数据库中查询
        result = self.session.query(ModuleFrame).filter_by(Id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.FrameName, "Test Frame")

    def test_select_by_id(self):
        # 插入一个 ModuleFrame 记录
        module_frame = ModuleFrame(Id="2", FrameName="Frame 2")
        self.session.add(module_frame)
        self.session.commit()

        # 测试 select_by_id 方法
        result = ModuleFrame.select_by_id(self.session, "2")
        self.assertIsNotNone(result)
        self.assertEqual(result.FrameName, "Frame 2")

    def test_find_all(self):
        # 插入多个 ModuleFrame 记录
        module_frame_1 = ModuleFrame(Id="3", FrameName="Frame 3")
        module_frame_2 = ModuleFrame(Id="4", FrameName="Frame 4")
        self.session.add(module_frame_1)
        self.session.add(module_frame_2)
        self.session.commit()

        # 测试 find_all 方法
        results = ModuleFrame.find_all(self.session)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].FrameName, "Frame 3")
        self.assertEqual(results[1].FrameName, "Frame 4")

if __name__ == "__main__":
    unittest.main()
