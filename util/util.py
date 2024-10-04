import uuid
from datetime import datetime

# 获取当前时间，格式为 'YYYY-MM-DD HH:MM:SS'
def TimeNow() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 生成新的 UUID
def NewId() -> str:
    return str(uuid.uuid4())
