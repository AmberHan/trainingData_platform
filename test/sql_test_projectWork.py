import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.projectWork import ProjectWork  # 你需要把 'your_model_file' 替换为包含 ProjectWork 类的文件路径


class TestProjectWorkModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 使用 SQLite 内存数据库进行测试
        cls.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(cls.engine)

    def setUp(self):
        # 每个测试前都创建会话
        self.session = Session(self.engine)

    def tearDown(self):
        # 每个测试后都关闭会话
        self.session.close()

    # def test_save_project_work(self):
    #     # 测试保存 ProjectWork
    #     project_work = ProjectWork(
    #         id="1",
    #         ProjectId="P001",
    #         ModuleTypeId="M001",
    #         WorkName="Test Work",
    #         CreateUid="U001"
    #     )
    #     project_work.save(self.session)
    #
    #     # 从数据库中查询数据
    #     result = self.session.query(ProjectWork).filter_by(id="1").first()
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ProjectId, "P001")
    #
    # def test_select_by_id(self):
    #     # 测试根据 ID 查询 ProjectWork
    #     project_work = ProjectWork(
    #         id="2",
    #         ProjectId="P002",
    #         ModuleTypeId="M002",
    #         WorkName="Work2",
    #         CreateUid="U002"
    #     )
    #     project_work.save(self.session)
    #
    #     result = ProjectWork.select_by_id(self.session, "2")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ProjectId, "P002")

    # def test_find_by_page(self):
    #     # 添加多条记录以测试分页查询
    #     for i in range(10):
    #         project_work = ProjectWork(
    #             id=str(i + 3),
    #             ProjectId=f"P00{i + 3}",
    #             ModuleTypeId=f"M00{i + 3}",
    #             WorkName=f"Work{i + 3}",
    #             CreateUid=f"U00{i + 3}"
    #         )
    #         project_work.save(self.session)
    #
    #     # 测试分页查询
    #     results, total = ProjectWork.find_by_page(self.session, uid="U003", project_id="P003", page=1, size=5)
    #     self.assertEqual(total, 1)  # 假设只有一条记录的 `CreateUid` 是 U003
    #     self.assertEqual(len(results), 1)
    #
    # def test_name_exists(self):
    #     # 测试是否存在相同的工作名称
    #     project_work = ProjectWork(
    #         id="4",
    #         ProjectId="P004",
    #         ModuleTypeId="M004",
    #         WorkName="Work4",
    #         CreateUid="U004"
    #     )
    #     project_work.save(self.session)
    #
    #     # 查询是否存在
    #     exists = ProjectWork.name_exists(self.session, uid="U004", work_name="Work4")
    #     self.assertTrue(exists)

    def test_delete_project_work(self):
        # 测试删除 ProjectWork
        project_work = ProjectWork(
            Id="5",
            ProjectId="P005",
            ModuleTypeId="M005",
            WorkName="Work5",
            CreateUid="U005"
        )
        project_work.save(self.session)

        # 删除记录
        project_work.delete(self.session)

        # 检查是否已删除
        result = ProjectWork.select_by_id(self.session, "5")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
