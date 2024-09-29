from sqlmodels.project import Project
from schemas.project_model import GetProjectListByPageReply, GetProjectListByPageReq
from fastapi import HTTPException
from sqlalchemy.orm import Session
from util.encrypt import encrypt_pwd


#
def get_project_list_by_page_impl(
    uid: str,
    req: GetProjectListByPageReq,
    db: Session
    # current_user_id: str = Depends(get_current_user_id)
):
    # 处理分页参数，确保 page 和 size 有效
    if req.size < 5:
        req.size = 5
    if req.page < 1:
        req.page = 1

    # 调用封装好的分页方法
    projects, total = Project.find_by_page(uid, req.page, req.size, req.like, db)

    # 构建响应
    reply = projects

    return reply


