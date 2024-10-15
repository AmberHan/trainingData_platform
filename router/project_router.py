from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from common import const
from common.const import CURRENT_USER_ID_KEY
from config.db_config import get_db
from schemas.projectWork_model import SaveProjectWorkReq
from schemas.req_model import StringIdReq, DeleteListReq, ListByPageReq
from services.project import project_service, projectWork_service, projectWorkReport_service
from services.project.project_service import SaveProjectReq
from util.response_format import response_format

projectHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-p")


@projectHandler.post("/getProjectListByPage")
async def get_project_list_by_page(req: ListByPageReq, db: Session = Depends(get_db)):
    return response_format(lambda: project_service.get_project_list_by_page_impl(CURRENT_USER_ID_KEY, req, db))


@projectHandler.post("/saveProject")
async def save_project(req: SaveProjectReq, db: Session = Depends(get_db)):
    return response_format(lambda: project_service.save_project_impl(CURRENT_USER_ID_KEY, req, db))


@projectHandler.post("/deleteProject")
async def delete_project(project_req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: project_service.delete_project_impl(project_req.id, db))


@projectHandler.post("/deleteAllProject")
def delete_all_projects(ids: DeleteListReq, db: Session = Depends(get_db)):
    return response_format(lambda: project_service.delete_all_project_impl(ids.id, db))


@projectHandler.post("/getProjectWorkListByPage")
async def get_project_work_list_by_page(req: ListByPageReq, db: Session = Depends(get_db)):
    return response_format(
        lambda: projectWork_service.get_project_work_list_by_page_impl(CURRENT_USER_ID_KEY, req, db))


@projectHandler.post("/saveProjectWork")
async def save_project_work(req: SaveProjectWorkReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.save_project_work_impl(CURRENT_USER_ID_KEY, req, db))


@projectHandler.post("/deleteProjectWork")
async def delete_project_work(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.delete_project_work_impl(req.id, db))


@projectHandler.post("/deleteAllProjectWork")
async def delete_all_project_works(ids: DeleteListReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.delete_all_project_work_impl(ids.id, db))


@projectHandler.post("/getProjectWorkTypeList")
async def get_project_work_type_list(db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.get_project_work_type_list_impl(db))


@projectHandler.post("/getProjectWorkById")
async def get_project_work_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.get_project_work_by_id_impl(req, db))


@projectHandler.post("/flushProjectWorkNum")
async def flush_project_work_num(project_id: int):
    pass


@projectHandler.post("/getProjectWorkStageById")
async def get_project_work_stage_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.get_project_work_stage_by_id_impl(req, db))


@projectHandler.post("/getProjectWorkInterById")
async def get_project_work_inter_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.get_project_work_inter_by_id_impl(req, db))


@projectHandler.post("/getProjectWorkInterValById")
async def get_project_work_inter_val_by_id(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWorkReport_service.get_project_work_inter_val_by_id(req, db))


@projectHandler.post("/getProjectWorkReport")
async def get_project_work_report(req: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWorkReport_service.get_project_work_report_by_id_impl(req, db))


@projectHandler.post("/startWork")
async def start_work(work_id: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.start_work(work_id, db))


@projectHandler.post("/stopWork")
async def stop_work(work_id: StringIdReq, db: Session = Depends(get_db)):
    return response_format(lambda: projectWork_service.stop_work(work_id, db))


@projectHandler.post("/getProjectWorkLog")
async def get_project_work_log(req: StringIdReq):
    return response_format(lambda: projectWorkReport_service.get_project_work_log_by_id_impl(req))
