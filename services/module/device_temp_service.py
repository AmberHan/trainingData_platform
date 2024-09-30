from schemas.device_model import GetDeviceReply
from fastapi.logger import logger

def get_device_temp_impl():
    try:
        reply = GetDeviceReply()
        reply.cpu.num = 1
        reply.cpu.present = 11
        reply.gpu.num = 1
        reply.gpu.present = 13
        reply.mem.num = 6
        reply.mem.present = 10
        return reply
    except Exception as e:
        logger.error(f"Failed to get data by page: {e}")
        raise Exception("Failed to fetch data")