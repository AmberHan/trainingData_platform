# schemas/project.py
from typing import Optional

from pydantic import BaseModel


from pydantic import BaseModel
from typing import List, Optional

# 假设你已经定义了 SaveProjectReq 模型
class SaveProjectReq(BaseModel):
    id: str
    project_name: str
    module_type_id: str
    create_uid: str
    detail: Optional[str] = None  # 可选字段

# 分页响应模型
class GetProjectListByPageReply(BaseModel):
    total: int  # 总条目数
    list: List[SaveProjectReq]  # 项目列表

class GetProjectListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None



class GetProjectListByPageReq(BaseModel):
    page: Optional[int] = 1  # 默认值为 1
    size: Optional[int] = 5  # 默认值为 5
    like: Optional[str] = None  # 可选字符串，默认为 None

