from schemas.module_model import GetModuleListByPageReq
from .module_service import *
def get_module_list_by_page(
    uid: str,
    req: GetModuleListByPageReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetModuleTypeReply:
    return get_module_list_by_page_impl(uid, req, db)