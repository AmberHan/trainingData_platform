from fastapi import APIRouter

from common import const

fileHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-f")


@fileHandler.post("/file/fileUpload")
async def file_upload():
    return {"message": "Hello World"}


@fileHandler.post("/file/upload")
async def upload():
    return {"message": "Hello World"}


@fileHandler.post("/file/uploadTar")
async def upload_tar():
    return {"message": "Hello World"}
