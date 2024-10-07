from fastapi import APIRouter, UploadFile, File

from common import const
from services.file import file_service
from util.response_format import response_format

fileHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-f")


@fileHandler.post("/file/fileUpload")
async def file_upload():
    return {"message": "Hello World"}


@fileHandler.post("/file/upload")
async def upload():
    return {"message": "Hello World"}


@fileHandler.post("/file/uploadTar")
async def upload_tar(file: UploadFile = File(...)):
    return response_format(lambda: file_service.upload_tar(file))