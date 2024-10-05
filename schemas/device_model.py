from typing import Optional
from pydantic import BaseModel


# 定义嵌套的 DeviceStatus 类
class DeviceStatus(BaseModel):
    num: Optional[int] = 0
    present: Optional[int] = 0

# 定义 GetDeviceReply 类，使用嵌套的 DeviceStatus
class GetDeviceReply(BaseModel):
    cpu: DeviceStatus = DeviceStatus()
    gpu: DeviceStatus = DeviceStatus()
    mem: DeviceStatus = DeviceStatus()