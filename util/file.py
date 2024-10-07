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
    save_path = config_path['FileConf']['SavePath']
    uri = config_path['FileConf']['Uri']

    if len(file_path) > len(save_path) and file_path.startswith(save_path):
        file_path = uri + file_path[len(save_path):]

    return file_path
