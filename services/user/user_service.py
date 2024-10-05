from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from schemas.user_model import UserLoginReq, UserLoginReply, LoginUserInfo, LoginRespWithToken
from sqlmodels.user import User
from util.encrypt import encrypt_pwd


def user_login_impl(req: UserLoginReq, db: Session) -> LoginRespWithToken:
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


# 数据库缺少一些字段
def user_login_service(req: UserLoginReq, db: Session) -> UserLoginReply:
    user = User.get_user(db, req.userName)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    pwd = encrypt_pwd(req.password)
    if pwd != user.password:
        raise HTTPException(status_code=400, detail="密码错误")

    user_info = LoginUserInfo(
        id=user.id,
        username=user.username
        )

    return UserLoginReply(user_info=user_info)
