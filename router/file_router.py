from fastapi import APIRouter, UploadFile, File, Query

from common import const
from schemas.req_model import DownloadParams
from services.file import file_service
from util.response_format import response_format

fileHandler = APIRouter(prefix=const.API_URL_PREFIX + "/api-f")


@fileHandler.post("/file/fileUpload")
async def file_upload():
    return {"message": "Hello World"}


@fileHandler.post("/file/upload")
async def upload(file: UploadFile = File(...)):
    return response_format(lambda: file_service.upload_impl(file))


@fileHandler.post("/file/uploadTar")
async def upload_tar(file: UploadFile = File(...)):
    return response_format(lambda: file_service.upload_tar_impl(file))


@fileHandler.get("/file/download")
def download_project_work(params: DownloadParams = Query(..., description="查询参数")):
    return file_service.download_impl(params)
