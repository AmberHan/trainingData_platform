import tarfile
import zipfile

from config.config import config_path


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
    save_path = config_path['FileConf']['SaveDataPath']
    uri = config_path['FileConf']['Uri']

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
    return save_path, True
