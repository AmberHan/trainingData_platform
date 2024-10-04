import unittest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodels.module import Module  # 你需要将 'your_model_file' 替换为包含 Module 类的实际文件路径

class TestModuleModel(unittest.TestCase):

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

    # def test_save_module(self):
    #     # 测试保存 Module
    #     module = Module(
    #         id="1",
    #         ModuleName="Test Module",
    #         ModuleTypeId="MT001",
    #         FrameId="F001",
    #         Detail="Test Detail",
    #         CreateUid="U001",
    #         Sort="1"
    #     )
    #     module.save(self.session)
    #
    #     # 从数据库中查询数据
    #     result = self.session.query(Module).filter_by(id="1").first()
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ModuleName, "Test Module")
    #     self.assertEqual(result.Detail, "Test Detail")

    # def test_select_by_id(self):
    #     # 测试根据 ID 查询 Module
    #     module = Module(
    #         id="2",
    #         ModuleName="Test Module 2",
    #         ModuleTypeId="MT002",
    #         FrameId="F002",
    #         Detail="Test Detail 2",
    #         CreateUid="U002",
    #         Sort="2"
    #     )
    #     module.save(self.session)
    #
    #     # 查询 Module 记录
    #     result = Module.select_by_id(self.session, "2")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ModuleName, "Test Module 2")
    #     self.assertEqual(result.FrameId, "F002")
    #
    def test_find_by_page(self):
        # 插入几条记录
        for i in range(10):
            module = Module(
                Id=str(i + 3),
                ModuleName=f"Module {i + 3}",
                ModuleTypeId=f"MT00{i + 3}",
                FrameId=f"F00{i + 3}",
                Detail=f"Detail {i + 3}",
                CreateUid="U003",
                IsDelete=0,
                Sort=str(i + 3)
            )
            module.save(self.session)

        # 测试分页查询
        results, total = Module.find_by_page(self.session, uid="U003", page=1, size=5)
        self.assertEqual(len(results), 5)
        self.assertEqual(total, 10)  # 总共有10条记录
        self.assertEqual(results[0].ModuleName, "Module 3")
        self.assertEqual(results[1].ModuleName, "Module 4")

    def test_delete_module(self):
        # 测试删除 Module
        module = Module(
            Id="11",
            ModuleName="Module 11",
            ModuleTypeId="MT011",
            FrameId="F011",
            Detail="Detail 11",
            CreateUid="U003",
            IsDelete=0,
            Sort="11"
        )
        module.save(self.session)

        # 删除记录
        module.delete(self.session)

        # 查询，检查是否软删除（IsDelete=True）
        result = Module.select_by_id(self.session, "11")
        self.assertIsNotNone(result)
        self.assertTrue(result.IsDelete)

if __name__ == "__main__":
    unittest.main()
