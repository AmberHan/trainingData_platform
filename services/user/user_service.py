from sqlmodels.user import User
from schemas.user_model import UserLoginReq, UserLoginReply, LoginUserInfo
from fastapi import HTTPException
from sqlalchemy.orm import Session
from util.encrypt import encrypt_pwd

# 数据库缺少一些字段
def user_login_service(req: UserLoginReq, db: Session) -> UserLoginReply:
    user = User.get_user(req.userName, db)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 把用户id存在生命周期里面
    pwd = encrypt_pwd(req.password)
    if pwd != user.password:
        raise HTTPException(status_code=400, detail="密码错误")

    user_info = LoginUserInfo(
        id=user.id,
        username=user.username
        )

    return UserLoginReply(user_info=user_info)
