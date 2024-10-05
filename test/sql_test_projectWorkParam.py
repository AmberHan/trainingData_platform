import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.projectWorkParam import ProjectWorkParam  # 这里替换为包含 ProjectWorkParam 类的文件路径


class TestProjectWorkParamModel(unittest.TestCase):

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

    def test_save_project_work_param(self):
        # 测试保存 ProjectWorkParam
        project_work_param = ProjectWorkParam(
            Id="1",
            ProjectId="P001",
            ProjectWorkId="PW001",
            Evaluation="Good",
            LearningRate="0.01",
            Impulse="High",
            Optimizer="Adam",
            IsUseDataExtend=True
            )
        project_work_param.save(self.session)

        # 从数据库中查询数据
        result = self.session.query(ProjectWorkParam).filter_by(Id="1").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.ProjectId, "P001")

    def test_select_by_id(self):
        # 测试根据 ID 查询 ProjectWorkParam
        project_work_param = ProjectWorkParam(
            Id="2",
            ProjectId="P002",
            ProjectWorkId="PW002",
            Evaluation="Average",
            LearningRate="0.05"
            )
        project_work_param.save(self.session)

        result = ProjectWorkParam.select_by_id(self.session, "2")
        self.assertIsNotNone(result)
        self.assertEqual(result.ProjectId, "P002")

    def test_select_by_project_work_id(self):
        # 测试根据 ProjectWorkId 查询 ProjectWorkParam
        project_work_param = ProjectWorkParam(
            Id="3",
            ProjectId="P003",
            ProjectWorkId="PW003",
            Evaluation="Excellent",
            LearningRate="0.02"
            )
        project_work_param.save(self.session)

        result = ProjectWorkParam.select_by_project_work_id(self.session, "PW003")
        self.assertIsNotNone(result)
        self.assertEqual(result.ProjectWorkId, "PW003")


if __name__ == "__main__":
    unittest.main()
