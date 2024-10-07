import math
import os
import shutil

from sqlalchemy.orm import Session

import util.util
from schemas.dataStrong_model import DataStrong, DataStrongParam
from sqlmodels import dataFile as dataFileSql
from sqlmodels.data import Data as DataSql
from sqlmodels.dataFile import DataFile
from sqlmodels.dataStrong import DataStrong as DataStrongSql
from util.convert import model_to_string


def save_data_strong_impl(req: DataStrongParam, db: Session):
    if req.dataId == "" or None:
        raise Exception("未选择任何数据,DataId不能为空")

    # TODO 此处可以优化
    dataStrongSql = DataStrongSql()
    dataStrongSql.DataId = req.dataId
    dataStrongSql.Id = req.id
    dataStrongSql.StrongParam = model_to_string(req)

    dataId = save_data_strong(dataStrongSql, db)

    # 文件分类迁移
    # 添加清洗文件夹的区分
    # res = DataFile.find_all_by_data_id(db, "0b7ad095-3efe-4e42-8286-448a7e631792")
    res = DataFile.find_all_by_data_id(db, dataId)
    # 查找 'images' 在路径中的位置
    images_dir_index = res[0].FilePath.find('/images/')

    # 如果找到了 'images'，则提取到 'images' 之前的部分
    if images_dir_index != -1:
        images_parent_dir = res[0].FilePath[:images_dir_index + len('images')]
        print(f"Images 目录: {images_parent_dir}")
    else:
        print("未找到 'images' 目录")
    split_and_move_files(res, int(req.validation_num), int(req.test_data_num), int(req.training_data_num), images_parent_dir)


def move_file_to_folder(file_path, destination_folder):
    try:
        # 检查目标文件夹是否存在，如果不存在则创建
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # 移动文件
        shutil.copy(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        print(f"文件已成功移动到 {destination_folder}")

    except FileNotFoundError as fnf_error:
        print(f"错误: 找不到文件 {file_path}. 错误信息: {str(fnf_error)}")
    except PermissionError as perm_error:
        print(f"错误: 没有权限移动文件 {file_path}. 错误信息: {str(perm_error)}")
    except OSError as os_error:
        print(f"错误: 操作系统错误。无法移动文件 {file_path}. 错误信息: {str(os_error)}")
    except Exception as e:
        print(f"未知错误: {str(e)}")

def split_and_move_files(res, validation_num, test_data_num, training_data_num, base_dir):


    # 按照文件类型分类
    png_files = [file for file in res if file.FileType == 'png']
    txt_files = [file for file in res if file.FileType == 'txt']

    # 计算文件划分的数量
    total_files = len(png_files) + len(txt_files)

    if total_files == 0:
        raise ValueError("没有可用的PNG文件进行划分")

        # 按比例计算验证集、测试集和训练集的数量
    validation_count = math.ceil(total_files * validation_num / 100)
    test_count = math.ceil(total_files * test_data_num / 100)
    training_count = total_files - validation_count - test_count

    if validation_count + test_count + training_count > total_files:
        raise ValueError("文件数量不足，无法按照比例划分")

    # 将文件分配到不同文件夹
    print(validation_count)
    print(test_count)
    print(training_count)
    subfolder = "images"
    folder = ""
    for index, value in enumerate(res):
        # 根据文件类型设置路径
        if value.FileType == "png":
            subfolder = "images"
        else:
            subfolder = "labels"
        # 根据索引确定文件存放的文件夹
        if index < validation_count:
            folder = os.path.join(base_dir, "valid", subfolder)
        elif index < validation_count + test_count:
            folder = os.path.join(base_dir, "test", subfolder)
        else:
            folder = os.path.join(base_dir, "train", subfolder)

        # 将文件移动到相应的文件夹
        move_file_to_folder(value.FilePath, folder)





def save_data_strong(req: DataStrongSql, db: Session):
    data = DataSql.select_by_id(db, req.DataId)
    if data is None:
        raise Exception("fail to model.Data.SelectById")
    dataStrong = DataStrongSql.select_by_data_id(db, req.DataId)
    if dataStrong is None:
        req.Id = util.util.NewId()
    else:
        req.Id = dataStrong.Id
    req.save(db)

    # 删除文件
    dataFileSql.DataFile.delete_by_type_and_data_id(db, 1, req.DataId)
    dataFileSql.DataFile.delete_by_type_and_data_id(db, 2, req.DataId)
    dataFileSql.DataFile.delete_by_type_and_data_id(db, 3, req.DataId)

    return req.DataId




def get_data_strong_impl(req: DataStrong, db: Session) -> DataStrongParam:
    data = get_data_strong(req, db)
    if data is not None:
        data_strong_param = DataStrongParam.parse_raw(data.StrongParam)
        data_strong_param.id = data.Id
        data_strong_param.dataId = data.DataId
        return data_strong_param


def get_data_strong(req: DataStrong, db: Session) -> DataStrongSql:
    if req.dataId:
        data = DataStrongSql.select_by_data_id(db, req.dataId)
        return data
    elif req.id:
        data = DataStrongSql.select_by_id(db, req.id)
        return data
