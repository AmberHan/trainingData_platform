import os.path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from . import user_router, api_router, file_router, module_router, project_router, data_router, test_router

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.getcwd() +"/"+ "dataorign"), name="static")
app.include_router(user_router.userHandle)
app.include_router(api_router.apiHandler)
app.include_router(file_router.fileHandler)
app.include_router(module_router.moduleHandler)
app.include_router(project_router.projectHandler)
app.include_router(data_router.dataHandler)
# 内部测试接口  后续删除
app.include_router(test_router.testHandler)
