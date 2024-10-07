import os
import subprocess
import uuid
from datetime import datetime


def TimeNow() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 生成新的 UUID
def NewId() -> str:
    return str(uuid.uuid4())


def exec_command(command):
    """
    执行系统命令，并返回输出结果
    :param command: 要执行的命令字符串
    :return: 命令执行结果
    """
    try:
        # 使用 subprocess.run 执行命令
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)

        # 返回标准输出结果
        return result.stdout, None
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，返回错误信息
        return None, e.stderr


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
