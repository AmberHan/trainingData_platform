from .data_service import *
from sqlalchemy.orm import Session


def get_data_list_by_page(
    uid: str,
    req: GetDataListByPageReq,
    db: Session,
    # current_user_id: str = Depends(get_current_user_id)
) -> GetDataListByPageReply:
    return get_data_list_by_page_impl(uid, req, db)