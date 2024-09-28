from fastapi import FastAPI
from . import user_router, api_router, file_router, moudle_router


app = FastAPI()
app.include_router(user_router.userHandle)
app.include_router(api_router.apiHandler)
app.include_router(file_router.fileHandler)
app.include_router(moudle_router.moduleHandler)

@app.get("/")
async def root():
    return {"message": "Hello World"}
