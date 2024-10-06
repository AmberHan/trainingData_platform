from fastapi import FastAPI

from . import user_router, api_router, file_router, module_router, project_router, data_router

app = FastAPI()
app.include_router(user_router.userHandle)
app.include_router(api_router.apiHandler)
app.include_router(file_router.fileHandler)
app.include_router(module_router.moduleHandler)
app.include_router(project_router.projectHandler)
app.include_router(data_router.dataHandler)
