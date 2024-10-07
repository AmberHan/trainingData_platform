import os
import shutil

from fastapi import UploadFile, File

from config.config import config_path
from schemas.file_model import FileReply, ChunkUploadResult
from util.file import get_file_size
from util.util import NewId


def upload_tar_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(file)
    if is_complete:
        return FileReply(
            path=file_path,
            url=config_path['FileConf']['Uri'] + os.path.basename(file_path),
            fileSize=str(get_file_size(file_path))
        )
    return Exception(file_path)


def upload_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(file)
    if is_complete:
        return ChunkUploadResult(
            path=file_path,
            isComplete=is_complete
        )


def upload_data(file: UploadFile = File(...)):
    file_path, ok = get_path(file.filename)
    if not ok:
        return file_path, ok
    # 保存文件
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return f"保存失败: {str(e)}", False
    return file_path, True


def get_path(file_name: str) -> (str, bool):
    save_dir = config_path['FileConf']['SavePath']
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
        except OSError as e:
            return f"存储路径创建失败: {str(e)}", False

    _, file_ext = os.path.splitext(file_name)
    if file_ext == "":
        return "没有后缀", False
    save_path = os.path.join(save_dir, file_name)
    if os.path.exists(save_path):
        return os.path.join(save_dir, NewId() + file_ext), True
    return save_path, True
