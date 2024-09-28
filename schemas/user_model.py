# schemas/user.py
from pydantic import BaseModel

class UserLoginReq(BaseModel):
    userName: str
    password: str

class LoginUserInfo(BaseModel):
    id: str
    username: str
    need_repass: bool
    repassed: bool
    pic_url: str
    phone_num: str
    position: str
    email: str

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