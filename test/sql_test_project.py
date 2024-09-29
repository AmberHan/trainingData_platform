import unittest
from sqlmodel import create_engine, Session, SQLModel, select
from sqlalchemy import text
from sqlmodels.project import Project  # 替换为包含 Project 类的文件路径

class TestProjectModel(unittest.TestCase):

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

    # def test_save_project(self):
    #     # 保存一条 Project 记录
    #     project = Project(
    #         Id="1",
    #         ProjectName="Test Project",
    #         ModuleTypeId="MT001",
    #         WorkTotalNum=5,
    #         WorkingNum=3,
    #         CompleteNum=2,
    #         CreateUid="U001",
    #         Detail="Test Detail",
    #         IsDelete=False
    #     )
    #     project.save(self.session)
    #
    #     # 从数据库中查询
    #     result = self.session.query(Project).filter_by(Id="1").first()
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ProjectName, "Test Project")
    #     self.assertEqual(result.Detail, "Test Detail")
    # #
    # def test_select_by_id(self):
    #     # 插入一条 Project 记录
    #     project = Project(
    #         Id="2",
    #         ProjectName="Project 2",
    #         ModuleTypeId="MT002",
    #         WorkTotalNum=10,
    #         CreateUid="U002",
    #         Detail="Detail 2",
    #         IsDelete=False
    #     )
    #     project.save(self.session)
    #
    #     # 测试 select_by_id 方法
    #     result = Project.select_by_id(self.session, "2")
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result.ProjectName, "Project 2")
    #     self.assertEqual(result.Detail, "Detail 2")

    # def test_find_by_page(self):
    #     # 插入几条 Project 记录
    #     for i in range(10):
    #         project = Project(
    #             Id=str(i + 3),
    #             ProjectName=f"Project {i + 3}",
    #             ModuleTypeId=f"MT00{i + 3}",
    #             WorkTotalNum=10,
    #             CreateUid="U003",
    #             Detail=f"Detail {i + 3}",
    #             IsDelete=False
    #         )
    #         project.save(self.session)
    #
    #     # 测试分页查询
    #     results, total = Project.find_by_page(uid="U003", page=1, size=5, like="", session=self.session)
    #     self.assertEqual(len(results), 5)
    #     self.assertEqual(total, 10)  # 总共有 10 条记录
    #     self.assertEqual(results[0].ProjectName, "Project 3")
    #
    # def test_delete_project(self):
    #     # 插入一条 Project 记录
    #     project = Project(
    #         Id="11",
    #         ProjectName="Project 11",
    #         ModuleTypeId="MT011",
    #         WorkTotalNum=5,
    #         CreateUid="U003",
    #         Detail="Detail 11",
    #         IsDelete=False
    #     )
    #     project.save(self.session)
    #
    #     # 删除记录（软删除）
    #     project.delete(self.session)
    #
    #     # 查询记录，检查是否软删除
    #     result = Project.select_by_id(self.session, "11")
    #     self.assertIsNotNone(result)
    #     self.assertTrue(result.IsDelete)
    #
    # def test_project_name_exists(self):
    #     # 插入一条 Project 记录
    #     project = Project(
    #         Id="12",
    #         ProjectName="Project 12",
    #         ModuleTypeId="MT012",
    #         WorkTotalNum=5,
    #         CreateUid="U004",
    #         Detail="Detail 12",
    #         IsDelete=False
    #     )
    #     project.save(self.session)
    #
    #     # 检查项目名是否存在
    #     exists = Project.project_name_exists(self.session, uid="U004", project_name="Project 12")
    #     self.assertTrue(exists)
    #
    #     # 检查一个不存在的项目名
    #     exists = Project.project_name_exists(self.session, uid="U004", project_name="Nonexistent Project")
    #     self.assertFalse(exists)

    def test_flush_project_work_num(self):
        # 这部分测试依赖 t_project_work 表的存在，以下为简单模拟

        # 插入 Project 记录
        project = Project(
            Id="13",
            ProjectName="Project 13",
            ModuleTypeId="MT013",
            WorkTotalNum=0,
            WorkingNum=0,
            CompleteNum=0,
            CreateUid="U005",
            Detail="Detail 13",
            IsDelete=False
        )
        project.save(self.session)

        # 创建虚拟表 t_project_work 并插入一些记录以模拟工作数更新
        self.session.execute(text("""
            CREATE TABLE IF NOT EXISTS t_project_work (
                Id TEXT PRIMARY KEY,
                ProjectId TEXT,
                WorkStatus INTEGER,
                IsDelete INTEGER
            )
        """))
        self.session.execute(text("""
            INSERT INTO t_project_work (Id, ProjectId, WorkStatus, IsDelete)
            VALUES ('W1', '13', 0, 0), ('W2', '13', 1, 0), ('W3', '13', 0, 1)
        """))
        self.session.commit()

        # 刷新项目工作数量
        Project.flush_project_work_num(self.session, project_id="13")

        # 查询并检查工作数量是否更新正确
        updated_project = Project.select_by_id(self.session, "13")
        self.assertEqual(updated_project.WorkTotalNum, 2)  # 2 条未删除的工作
        self.assertEqual(updated_project.WorkingNum, 1)    # 1 条正在进行的工作
        self.assertEqual(updated_project.CompleteNum, 1)   # 1 条已完成的工作

if __name__ == "__main__":
    unittest.main()
