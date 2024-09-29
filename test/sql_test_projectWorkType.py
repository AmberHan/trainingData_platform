import unittest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodels.projectWorkType import ProjectWorkType  # 你需要将 'your_model_file' 替换为包含 ProjectWorkType 类的实际文件路径

class TestProjectWorkTypeModel(unittest.TestCase):

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

    def test_save_project_work_type(self):
        # 测试保存 ProjectWorkType
        project_work_type = ProjectWorkType(
            Id="1",
            TypeName="Type A",
            Icon="icon_a.png"
        )
        project_work_type.save(self.session)

        # 从数据库中查询数据
        result = self.session.query(ProjectWorkType).filter_by(Id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.TypeName, "Type A")
        self.assertEqual(result.Icon, "icon_a.png")

    def test_select_by_id(self):
        # 测试根据 ID 查询 ProjectWorkType
        project_work_type = ProjectWorkType(
            Id="2",
            TypeName="Type B",
            Icon="icon_b.png"
        )
        project_work_type.save(self.session)

        # 查询 ProjectWorkType 记录
        result = ProjectWorkType.select_by_id(self.session, "2")
        self.assertIsNotNone(result)
        self.assertEqual(result.TypeName, "Type B")
        self.assertEqual(result.Icon, "icon_b.png")

    def test_find_all(self):
        # 插入几条记录
        project_work_type_1 = ProjectWorkType(Id="3", TypeName="Type C", Icon="icon_c.png")
        project_work_type_2 = ProjectWorkType(Id="4", TypeName="Type D", Icon="icon_d.png")
        project_work_type_1.save(self.session)
        project_work_type_2.save(self.session)

        # 测试查找所有记录
        results = ProjectWorkType.find_all(self.session)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].TypeName, "Type C")
        self.assertEqual(results[1].TypeName, "Type D")

if __name__ == "__main__":
    unittest.main()
