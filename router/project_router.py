from common import const
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.code import *
from common.const import CURRENT_USER_ID_KEY
from schemas.project_work_model import GetProjectWorkListByPageReq, SaveProjectWorkReq
from schemas.req_model import StringIdReq, DeleteListReq
from services.db import get_db
from schemas.project_model import GetProjectListByPageReq
from services.project import project_service, project_work_service
from services.project.project_service import SaveProjectReq
from util.response_format import response_format
from util.util import ret_format

projectHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-p")

@projectHandler.post("/getProjectListByPage")
def get_project_list_by_page(req: GetProjectListByPageReq, db: Session = Depends(get_db)):
    reply = project_service.get_project_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
    return ret_format(reply)


@projectHandler.post("/saveProject")
def save_project(req: SaveProjectReq, db: Session = Depends(get_db)):
    reply = project_service.save_project_impl(CURRENT_USER_ID_KEY, req, db)
    return ret_format(reply)

@projectHandler.post("/deleteProject")
def delete_project(project_req: SaveProjectReq, db: Session = Depends(get_db)):
    reply = project_service.delete_project_impl(project_req.id, db)
    return ret_format(reply)

@projectHandler.post("/deleteAllProject")
def delete_all_projects(ids: DeleteListReq, db: Session = Depends(get_db)):
    if len(ids.id) == 0:
        return response_format(DeleteNoIDRequest, "id不能为空")
    reply = project_service.delete_all_project_impl(ids.id, db)
    return ret_format(reply)

@projectHandler.post("/getProjectWorkListByPage")
def get_project_work_list_by_page(req: GetProjectWorkListByPageReq, db: Session = Depends(get_db)):
    reply = project_work_service.get_project_work_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
    return ret_format(reply)


@projectHandler.post("/saveProjectWork")
def save_project_work(req: SaveProjectWorkReq, db: Session = Depends(get_db)):
    reply = project_work_service.save_project_work_impl(req, db)
    return ret_format(reply)

@projectHandler.post("/deleteProjectWork")
def delete_project_work(req: SaveProjectWorkReq, db: Session = Depends(get_db)):
    reply = project_work_service.delete_project_work(req.work.id, db)
    return ret_format(reply)

@projectHandler.post("/deleteAllProjectWork")
def delete_all_project_works(ids: DeleteListReq, db: Session = Depends(get_db)):
    reply = project_work_service.delete_all_project_work_impl(ids, db)
    return ret_format(reply)

@projectHandler.post("/getProjectWorkById")
def get_project_work_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    reply = project_work_service.get_project_work_by_id(req, db)
    return ret_format(reply)

@projectHandler.post("/flushProjectWorkNum")
def flush_project_work_num(project_id: int):
    pass

@projectHandler.post("/getProjectWorkStageById")
def get_project_work_stage_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    pass

@projectHandler.post("/getProjectWorkInterById")
def get_project_work_inter_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    pass

@projectHandler.post("/getProjectWorkInterValById")
def get_project_work_inter_val_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    pass

@projectHandler.post("/getProjectWorkReport")
def get_project_work_report(project_id: int):
    pass

@projectHandler.post("/startWork")
def start_work(work_id: int):
    pass

@projectHandler.post("/stopWork")
def stop_work(work_id: int):
    pass

@projectHandler.post("/getProjectWorkLog")
def get_project_work_log(work_id: int):
    pass

@projectHandler.post("/getProjectWorkTypeList")
def get_project_work_type_list(db: Session = Depends(get_db)):
    reply = project_work_service.get_project_work_type_list(db)
    return ret_format(reply)

@projectHandler.post("/downloadProjectWork")
def download_project_work(project_id: int):
    pass
