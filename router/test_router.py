import subprocess
import threading
import time

from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from common import const
from config.config import config_path
from util.file import delete_file_and_directory, read_file_content
from util.response_format import response_format

testHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-t")


@testHandler.post("/initAll")
async def init_all():
    return response_format(lambda: initAll())


@testHandler.get("/getCommandTxt")
async def get_command_txt(path: str = Query(None, description="查询参数")):
    content = getCommandTxt(path)
    html_content = f"<pre>{content}</pre>"
    return HTMLResponse(content=html_content)


def getCommandTxt(path: str):
    try:
        return read_file_content(path)
    except Exception as e:
        return f"{e}"


# 删除除了SaveRunPath以为的目录,暂不包含删除数据库
def initAll():
    try:
        file_conf = config_path.get('PathConf', {})
        for key, path in file_conf.items():
            if key != 'SaveRunPath':
                delete_file_and_directory(path)
    except Exception as e:
        raise Exception("e")


class TestReq(BaseModel):
    cmd: str
    timeout: int


# 执行简单的不需要长时间等待的
@testHandler.post("/excCommand")
async def exc_command(req: TestReq):
    content = run_command(req.cmd, req.timeout)
    html_content = f"<pre>{content}</pre>"
    return HTMLResponse(content=html_content)


def read_output(pipe, buffer):
    for line in iter(pipe.readline, ''):
        buffer.append(line)
    pipe.close()


def run_command(command, timeout=3):
    try:
        # 创建子进程
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 初始化输出和错误缓冲区
        stdout_buffer = []
        stderr_buffer = []

        # 启动线程读取输出和错误
        stdout_thread = threading.Thread(target=read_output, args=(process.stdout, stdout_buffer))
        stderr_thread = threading.Thread(target=read_output, args=(process.stderr, stderr_buffer))

        stdout_thread.start()
        stderr_thread.start()

        # 等待子进程结束或超时
        start_time = time.time()
        while process.poll() is None:
            if time.time() - start_time > timeout:
                process.terminate()  # 终止子进程
                process.wait()  # 等待子进程完全终止
                return f"命令执行超时，超过 {timeout} 秒\n部分输出:\n{''.join(stdout_buffer)}\n部分错误:\n{''.join(stderr_buffer)}"
            time.sleep(0.1)  # 避免高 CPU 使用率

        # 等待读取线程完成
        stdout_thread.join()
        stderr_thread.join()

        if process.returncode == 0:
            return ''.join(stdout_buffer)
        else:
            return f"命令执行失败，返回码: {process.returncode}\n标准错误:\n{''.join(stderr_buffer)}"

    except Exception as e:
        return f"执行命令时发生错误: {e}"
