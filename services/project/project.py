from .project_service import *
def get_project_list_by_page(
    uid: str,
    req: GetProjectListByPageReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetProjectListByPageReply:
    return get_project_list_by_page_impl(uid, req, db)