# schemas/user.py
from typing import Optional

from pydantic import BaseModel

class UserLoginReq(BaseModel):
    userName: str
    password: str

class LoginUserInfo(BaseModel):
    id: str
    username: str
    need_repass: Optional[bool] = None
    repassed: Optional[bool] = None
    pic_url: Optional[str] = None
    phone_num: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None

class UserLoginReply(BaseModel):
    user_info: LoginUserInfo

class GetUserByIdReq(BaseModel):
    user_id: str

class GetUserByIdReply(BaseModel):
    username: str
    phone_num: str
    user_type: int
    type: int
    true_name: str
    email: str
    industry_id: str
    company_name: str
    contact: str
    province_id: int
    area_id: int
    industry_name: str
    province_name: str
    city_name: str
    source: int