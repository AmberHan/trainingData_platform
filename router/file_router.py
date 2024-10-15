from fastapi import APIRouter, UploadFile, File, Query, Form

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


@fileHandler.post("/upload/{chunk_id}")
async def upload_chunk(chunk_id: int, file: UploadFile, file_md5: str = Form(...)):
    return file_service.upload_chunk_impl(chunk_id, file, file_md5)


@fileHandler.post("/upload/merge")
async def merge_chunks(file_name: str = Form(...), file_md5: str = Form(...)):
    return file_service.merge_chunks_impl(file_name, file_md5)
