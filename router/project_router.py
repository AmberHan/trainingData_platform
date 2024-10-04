from common import const
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from common.code import *
from common.const import CURRENT_USER_ID_KEY
from services.db import get_db
from schemas.project_model import GetProjectListByPageReq, GetProjectByIdReq
from services.project import project_service
from services.project.project_service import SaveProjectReq, DeleteListReq
from sqlmodels.project import Project
from util.response_format import response_format

projectHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-p")

@projectHandler.post("/getProjectListByPage")
def get_project_list_by_page(req: GetProjectListByPageReq, db: Session = Depends(get_db)):
    try:
        reply = project_service.get_project_list_by_page_impl(CURRENT_USER_ID_KEY, req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))

@projectHandler.post("/saveProject")
def save_project(req: SaveProjectReq, db: Session = Depends(get_db)):
    try:
        reply = project_service.save_project_impl(CURRENT_USER_ID_KEY, req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))

@projectHandler.post("/deleteProject")
def delete_project(project_req: SaveProjectReq, db: Session = Depends(get_db)):
    try:
        reply = project_service.delete_project_impl(project_req.id, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))

@projectHandler.post("/deleteAllProject")
def delete_all_projects(ids: DeleteListReq, db: Session = Depends(get_db)):
    if len(ids.id) == 0:
        return response_format(DeleteNoIDRequest, "id不能为空")
    try:
        reply = project_service.delete_all_project_impl(ids.id, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))
    pass

@projectHandler.post("/getProjectWorkListByPage")
def get_project_work_list_by_page(req: GetProjectListByPageReq, db: Session = Depends(get_db)):
    pass

@projectHandler.post("/saveProjectWork")
def save_project_work():
    pass

@projectHandler.post("/deleteProjectWork")
def delete_project_work(work_id: int):
    pass

@projectHandler.post("/deleteAllProjectWork")
def delete_all_project_works(project_id: int):
    pass

@projectHandler.post("/getProjectWorkById")
def get_project_work_by_id(req: GetProjectByIdReq, db: Session = Depends(get_db)):
    try:
        reply = project_service.getProjectWorkById(CURRENT_USER_ID_KEY, req, db)
        return response_format(RequestSuccess, reply)
    except HTTPException as e:
        return response_format(ServiceInsideError, e.detail)
    except Exception as e:
        return response_format(ServiceInsideError, str(e))

@projectHandler.post("/flushProjectWorkNum")
def flush_project_work_num(project_id: int):
    pass

@projectHandler.post("/getProjectWorkStageById")
def get_project_work_stage_by_id(work_id: int):
    pass

@projectHandler.post("/getProjectWorkInterById")
def get_project_work_inter_by_id(work_id: int):
    pass

@projectHandler.post("/getProjectWorkInterValById")
def get_project_work_inter_val_by_id(work_id: int):
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
def get_project_work_type_list():
    pass

@projectHandler.post("/downloadProjectWork")
def download_project_work(project_id: int):
    pass
