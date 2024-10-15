from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from common import const
from config.config import config_path
from config.db_config import get_db
from schemas.user_model import UserLoginReq
from services.user.user_service import user_login_impl
from util.response_format import response_format

userHandle = APIRouter(prefix=const.API_URL_PREFIX + "/api-u")

userHandle.mount("/static", StaticFiles(directory=config_path['PathConf']['SaveDataPath']), name="static")

# 用户管理模块
@userHandle.post("/login")
async def login(req: UserLoginReq, db: Session = Depends(get_db)):
    return response_format(lambda: user_login_impl(req, db))
