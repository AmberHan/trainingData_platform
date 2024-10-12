import csv
import json
import math
import shutil
import tarfile
import zipfile

import yaml

from config.config import config_path
from schemas.projectWork_model import StageReply, LossReply
from util.util import NewId, TimeNow


def unzip_file(zip_path, extract_to):
    """
    解压 ZIP 文件
    :param zip_path: 压缩文件的路径
    :param extract_to: 解压到的目标路径
    """
    try:
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"解压成功: {zip_path} 到 {extract_to}")
    except zipfile.BadZipFile:
        print(f"文件 {zip_path} 不是有效的 ZIP 文件")
    except Exception as e:
        print(f"解压过程中发生错误: {str(e)}")


def untar_file(tar_path, extract_to):
    """
    解压 .tar.gz 文件
    :param tar_path: 压缩文件的路径
    :param extract_to: 解压到的目标路径
    """
    try:
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        with tarfile.open(tar_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
        print(f"解压成功: {tar_path} 到 {extract_to}")
    except tarfile.TarError:
        print(f"文件 {tar_path} 不是有效的 tar 文件")
    except Exception as e:
        print(f"解压过程中发生错误: {str(e)}")


def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)  # 以字节为单位返回文件大小
        return size
    except OSError as e:
        print(f"Error: {e}")
        return None


import os


# file_urls
def file_path_to_url(file_path: str) -> str:
    save_path = config_path['PathConf']['SaveDataPath']
    uri = config_path['HostConf']['Uri']

    if len(file_path) > len(save_path) and file_path.startswith(save_path):
        file_path = uri + file_path[len(save_path):]

    return file_path


a = file_path_to_url("aa")


# 解析images和labels文件
def get_files_from_images_and_labels(directory):
    images_files = []
    labels_files = []

    # 遍历所有子目录
    for root, dirs, files in os.walk(directory):
        # 判断当前目录是否是二级目录下的 "images" 或 "labels"
        if root.endswith("images"):
            for file in files:
                # 把images目录下的文件路径存储到images_files
                images_files.append(os.path.join(root, file))

        if root.endswith("labels"):
            for file in files:
                # 把labels目录下的文件路径存储到labels_files
                labels_files.append(os.path.join(root, file))

    return images_files, labels_files


def find_parent_directory(path, folder_name):
    # 规范化路径
    norm_path = os.path.normpath(path)
    # 将路径按路径分隔符分割成多个部分
    parts = norm_path.split(os.sep)

    # 查找包含指定文件夹的部分
    for i, part in enumerate(parts):
        if part == folder_name:
            images_directory = os.sep.join(parts[:i])
            return images_directory

    return None


def get_unique_path(save_dir, file_name: str) -> (str, bool):
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except OSError as e:
            return f"存储路径创建失败: {str(e)}", False

    _, file_ext = os.path.splitext(file_name)
    if file_ext == "":
        return "没有后缀", False
    save_path = os.path.join(save_dir, file_name)
    if os.path.exists(save_path):
        return os.path.join(save_dir, NewId() + file_ext), True
    return os.path.normpath(save_path).replace(os.sep, '/'), True


# 获取子目录list
def get_all_subfolders(base_dir):
    # 获取 base_dir 下所有的文件夹名称
    subfolders = ""
    if not os.path.exists(base_dir):
        print(f"Base directory '{base_dir}' does not exist.")
    else:
        subfolders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    return subfolders


# 目录移动
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


# 复制迁移
def split_and_move_files(res, validation_num, test_data_num, training_data_num, base_dir):
    # 按照文件类型分类
    png_files = [file.FilePath for file in res if file.FileType == 'png']

    # 计算文件划分的数量
    total_files = len(png_files)

    if total_files == 0:
        raise ValueError("没有可用的PNG文件进行划分")

        # 按比例计算验证集、测试集和训练集的数量
    validation_count = math.ceil(total_files * validation_num / 100)
    test_count = math.ceil(total_files * test_data_num / 100)
    training_count = total_files - validation_count - test_count

    if validation_count + test_count + training_count > total_files:
        raise ValueError("文件数量不足，无法按照比例划分")

    # 将文件分配到不同文件夹
    subfolder = "images"
    folder = ""

    # 取最长的字符串加1
    # 取最长的字符串加1
    # sub_dir = get_all_subfolders(base_dir)
    # train_folders = [folder for folder in sub_dir if 'train' in folder.lower()]
    # str_add = '1' * len(train_folders)
    if os.path.exists(base_dir):
        # 删除目录及其内容
        shutil.rmtree(base_dir)

    for index, value in enumerate(png_files):

        # 根据索引确定文件存放的文件夹
        if index < validation_count:
            folder = os.path.join(base_dir, "valid", "images")
        elif index < validation_count + test_count:
            folder = os.path.join(base_dir, "test", "images")
        else:
            folder = os.path.join(base_dir, "train", "images")

        # 将文件移动到相应的文件夹
        move_file_to_folder(value, folder)

        # 根据索引确定文件存放的文件夹
        if index < validation_count:
            folder = os.path.join(base_dir, "valid", "labels")
        elif index < validation_count + test_count:
            folder = os.path.join(base_dir, "test", "labels")
        else:
            folder = os.path.join(base_dir, "train", "labels")

        # 将文件移动到相应的文件夹
        move_file_to_folder(value.replace("images", "labels").replace(".jpg", ".txt"), folder)
    data_yaml = {
        'train': os.path.join(base_dir, "train").lstrip("."),
        'test': os.path.join(base_dir, "test").lstrip("."),
        'val': os.path.join(base_dir, "valid").lstrip("."),
        'names': {
            0: "two_wheeler",
            1: "helmet",
            2: "without_helmet"
        }
    }

    dir_path = os.path.join(config_path['PathConf']['SaveYamlDataPath'], res[0].DataId)
    # 如果目录不存在，则创建目录
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    generate_yaml(data_yaml, os.path.join(dir_path, "data.yaml"))


def generate_yaml(data, file_path):
    # 将数据写入 YAML 文件
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def get_last_row_csv(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            last_row = None
            for row in reader:
                last_row = row
            return last_row
    except:
        raise Exception("训练未完成！无法查看报告内容")


def read_json_file(file_path):  # 读取文件内容并进行异常处理
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")

        if os.path.getsize(file_path) == 0:
            raise ValueError(f"文件 {file_path} 为空")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # 将 JSON 文件内容解析为 Python 字典
    except FileNotFoundError as e:
        print(f"错误: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON 解码错误: {e}")
        return {}
    except Exception as e:
        print(f"其他错误: {e}")
        return {}
    return data


def get_last_row_log(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        last_row = None
        for row in reader:
            last_row = row
        return last_row


# 读log最新的一行,获取loss
def get_last_row_loss(file_path):
    epo_list = []
    cls_list = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 跳过第一行（表头）
        next(reader, None)
        for row in reader:
            if row:  # 确保行不为空
                epo_list.append(int(row[0].strip()))  # 去掉左右空格
                cls_list.append(float(row[2].strip()))  # 去掉左右空格
    reply_loss = LossReply(time=epo_list, loss=cls_list)
    return reply_loss


# 读log最新的一行,获取百分比
def get_last_row_log_stage(file_path):
    last_row = None
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            last_row = row
    # 假设 last_row[0] 是一个整数或能转换为整数的字符串
    value = int(last_row[0]) / 10
    # 计算百分比，保留小数
    percentage = value * 100
    stage = StageReply(stage=percentage, time=TimeNow())
    return stage


def delete_file_and_directory(path: str):
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
    except OSError as e:
        raise Exception(f"删除文件 {path} 时出错: {str(e)}")


def count_directories(path: str, fold_name: str) -> int:
    try:
        entries = os.listdir(path)

        # 统计其中的目录数量
        directory_count = sum(
            1 for entry in entries if os.path.isdir(os.path.join(path, entry)) and entry.startswith(fold_name))

        return directory_count
    except OSError as e:
        raise Exception(f"{e}")


def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"文件 {file_path} 未找到"
    except IOError as e:
        return f"读取文件 {file_path} 时出错: {str(e)}"
