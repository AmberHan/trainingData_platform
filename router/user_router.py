from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import const
from schemas.user_model import UserLoginReq
from config.db import get_db
from services.user.user_service import user_login_impl
from util.util import ret_format

userHandle = APIRouter(prefix=const.API_URL_PREFIX + "/api-u")


# 用户管理模块
@userHandle.post("/login")
async def login(req: UserLoginReq, db: Session = Depends(get_db)):
    return ret_format(lambda: user_login_impl(req, db))
