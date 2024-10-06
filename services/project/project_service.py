from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from schemas.project_model import GetProjectListByPageReply, SaveProjectReq
from schemas.req_model import ListByPageReq
from services.module import module_service
from sqlmodels.project import Project
from sqlmodels.user import User
from util import util


def get_project_list_by_page_impl(
        uid: str,
        req: ListByPageReq,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    # 处理分页参数，确保 page 和 size 有效
    if req.size < 5:
        req.size = 5
    if req.page < 1:
        req.page = 1

    # 调用封装好的分页方法
    projects, total = Project.find_by_page(uid, req.page, req.size, req.like, db)
    reply = GetProjectListByPageReply(total=total)
    for i, p in enumerate(projects):
        saveProjectReq = SaveProjectReq.from_project_orm(p)
        module_type_reply = module_service.get_module_type_by_id_impl(module_service.StringIdReq(id=p.ModuleTypeId), db)

        if module_type_reply:
            saveProjectReq.icon = module_type_reply.icon
            saveProjectReq.moduleTypeName = module_type_reply.moduleTypeName
            saveProjectReq.createWay = module_type_reply.createWay
        user = User.select_by_id(db, p.CreateUid)
        if user:
            saveProjectReq.userName = user.username
        reply.list.append(saveProjectReq)
    return reply


# 保存项目信息
def save_project_impl(
        uid: str,
        req: SaveProjectReq,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
):
    project = Project()
    try:
        # 判断是否是更新项目
        if req.id:
            project = Project.select_by_id(db, req.id)
            if not project:
                raise Exception("项目不存在")

            # 验证用户是否有权限操作
            if project.CreateUid != uid:
                raise Exception("无权操作")

        # 如果是新项目，检查项目名称是否已存在
        else:
            if Project.project_name_exists(db, uid, req.projectName):
                raise Exception("项目名称已存在")
            # 生成新项目 ID 和创建时间
            project.Id = util.NewId()
            project.CreateTime = util.TimeNow()

        project.ProjectName = req.projectName
        project.ModuleTypeId = req.moduleTypeId
        project.CreateUid = uid
        project.Detail = req.detail
        project.save(db)

    except SQLAlchemyError as e:
        raise Exception(f"Failed to save project: {e}")


# 删除项目信息
def delete_project_impl(
        id: str,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
):
    project = Project()
    try:
        project.Id = id
        project.delete(db)
    except SQLAlchemyError as e:
        raise Exception(e)


def delete_all_project_impl(
        ids: list,
        db: Session,
        # current_user_id: str = Depends(get_current_user_id)
):
    try:
        if len(ids) == 0:
            raise Exception("id不能为空")
        Project.delete_all(db, ids)
    except SQLAlchemyError as e:
        raise Exception(e)
