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


# 时间转数字
def transfor_time(date_str: str):
    # 将字符串转换为 datetime 对象
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # 将 datetime 对象转换为 Unix 时间戳
    timestamp = date_obj.timestamp()
    return timestamp
