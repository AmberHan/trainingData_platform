from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from common import const
from common.code import *
from schemas.user_model import UserLoginReq
from services.db import get_db
from services.user.user_service import user_login_impl
from util.response_format import response_format

userHandle = APIRouter(prefix=const.API_URL_PREFIX + "/api-u")

# 用户管理模块
@userHandle.post("/login")
async def login(req: UserLoginReq, db: Session = Depends(get_db)):
    try:
        reply = user_login_impl(req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))
