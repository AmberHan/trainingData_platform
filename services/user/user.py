from fastapi import status
from datetime import datetime, timedelta

from pydantic import BaseModel

from .user_service import *
class LoginRespWithToken(BaseModel):
    user_info: LoginUserInfo
    access_token: str
    refresh_token: str
    scope: str
    token_type: str
    expires_in: int
def user_login(req: UserLoginReq, db: Session) -> LoginRespWithToken:
    # 参数验证
    if req.userName == "":
        raise HTTPException(status_code=status.RequestParamError, detail="用户名不能为空")
    if req.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="密码不能为空")

    reply = user_login_service(req, db)

    # 构建回复
    reply = LoginRespWithToken(
        user_info=reply.user_info,
        access_token="",
        refresh_token="",
        scope="app",
        token_type="Bearer",
        expires_in=int((datetime.utcnow() + timedelta(hours=8)).timestamp())
    )

    return reply
