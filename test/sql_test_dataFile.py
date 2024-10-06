import unittest

from sqlmodel import create_engine, Session, SQLModel

from sqlmodels.dataFile import DataFile  # 替换为包含 DataFile 类的文件路径


class TestDataFileModel(unittest.TestCase):

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

    def test_save_data_file(self):
        # 保存一条 DataFile 记录
        data_file = DataFile(
            Id=1,
            DataId="D001",
            FilePath="/path/to/file1",
            Url="http://example.com/file1",
            FileType=1,
            DirPath="/path/to"
        )
        data_file.save(self.session)

        # 从数据库中查询
        result = self.session.query(DataFile).filter_by(Id=1).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.FilePath, "/path/to/file1")

    def test_select_by_id(self):
        # 插入一条 DataFile 记录
        data_file = DataFile(
            Id=2,
            DataId="D002",
            FilePath="/path/to/file2",
            Url="http://example.com/file2",
            FileType=1,
            DirPath="/path/to"
        )
        data_file.save(self.session)

        # 测试 select_by_id 方法
        result = DataFile.select_by_id(self.session, 2)
        self.assertIsNotNone(result)
        self.assertEqual(result.FilePath, "/path/to/file2")

    def test_find_by_page(self):
        # 插入几条 DataFile 记录
        for i in range(10):
            data_file = DataFile(
                Id=i + 3,
                DataId="D003",
                FilePath=f"/path/to/file{i + 3}",
                Url=f"http://example.com/file{i + 3}",
                FileType=1,
                DirPath="/path/to"
            )
            data_file.save(self.session)

        # 测试分页查询
        results, total = DataFile.find_by_page(self.session, data_id="D003", file_type=1, page=1, size=5)
        self.assertEqual(len(results), 5)
        self.assertEqual(total, 10)
        self.assertEqual(results[0].FilePath, "/path/to/file3")

    def test_delete_data_file(self):
        # 插入一条 DataFile 记录
        data_file = DataFile(
            Id=11,
            DataId="D004",
            FilePath="/path/to/file11",
            Url="http://example.com/file11",
            FileType=1,
            DirPath="/path/to"
        )
        data_file.save(self.session)

        # 删除记录
        data_file.delete(self.session)

        # 查询记录，检查是否删除成功
        result = DataFile.select_by_id(self.session, 11)
        self.assertIsNone(result)

    def test_delete_by_data_id(self):
        # 插入几条 DataFile 记录
        data_file_1 = DataFile(Id=12, DataId="D005", FilePath="/path/to/file12", FileType=0, DirPath="/path/to")
        data_file_2 = DataFile(Id=13, DataId="D005", FilePath="/path/to/file13", FileType=1, DirPath="/path/to")
        data_file_1.save(self.session)
        data_file_2.save(self.session)

        # 删除 DataId 为 D005 且 FileType 为 0 的记录
        DataFile.delete_by_data_id(self.session, data_id="D005")

        # 验证删除是否成功
        result = DataFile.select_by_id(self.session, 12)
        self.assertIsNone(result)  # 该记录应该被删除
        result = DataFile.select_by_id(self.session, 13)
        self.assertIsNotNone(result)  # 该记录不应该被删除


if __name__ == "__main__":
    unittest.main()
