from fastapi import HTTPException

from schemas.device_model import GetDeviceReply


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
        raise HTTPException(status_code=400, detail=f"Failed to fetch data: {e}")
