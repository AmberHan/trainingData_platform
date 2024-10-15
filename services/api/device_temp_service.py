import GPUtil
import psutil

import util.util
from schemas.device_model import GetDeviceReply


def get_device_temp_impl() -> GetDeviceReply:
    try:
        # 获取CPU信息
        cpu_count = psutil.cpu_count(logical=True)  # 逻辑CPU核心数
        cpu_usage = psutil.cpu_percent(interval=1)  # CPU使用率

        # 获取内存信息
        memory_info = psutil.virtual_memory()  # 总内存和可用内存
        total_memory = memory_info.total  # 总内存

        # 获取GPU信息
        gpus = GPUtil.getGPUs()  # 获取GPU信息
        gpu_count = len(gpus)  # GPU数量

        # 创建GetDeviceReply对象
        reply = GetDeviceReply()
        reply.cpu.num = cpu_count
        reply.cpu.present = cpu_usage

        # 设置GPU信息
        reply.gpu.num = gpu_count
        if gpu_count > 0:
            # 假设您想将第一个GPU的使用率作为present值:q

            reply.gpu.present = gpus[0].load * 100  # GPU使用率（百分比）

        # 设置内存信息
        reply.mem.num = total_memory // (1024 ** 3)  # 将总内存转换为MB
        reply.mem.present = memory_info.used / (1024 ** 3)  # 使用率百分比
        return reply
    except Exception as e:
        raise Exception(f"Failed to fetch data: {e}")


def get_id_impl() -> str:
    return util.util.NewId()
