from fastapi import APIRouter
from common import const

projectHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-p")

@projectHandler.post("/getProjectListByPage")
def get_project_list_by_page():
    pass

@projectHandler.post("/saveProject")
def save_project():
    pass

@projectHandler.post("/deleteProject")
def delete_project(project_id: int):
    pass

@projectHandler.post("/deleteAllProject")
def delete_all_projects():
    pass

@projectHandler.post("/getProjectWorkListByPage")
def get_project_work_list_by_page(project_id: int, page: int, size: int):
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
def get_project_work_by_id(work_id: int):
    pass

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
