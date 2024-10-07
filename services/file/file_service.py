import os
import shutil

from fastapi import UploadFile, File

from config.config import config_path
from schemas.file_model import FileReply, ChunkUploadResult
from util.file import get_file_size, get_unique_path


def upload_tar_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(config_path['FileConf']['SaveDataPath'], file)
    if is_complete:
        return FileReply(
            path=file_path,
            url=config_path['FileConf']['Uri'] + os.path.basename(file_path),
            fileSize=str(get_file_size(file_path))
        )
    return Exception(file_path)


def upload_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(config_path['FileConf']['SaveModelPath'], file)
    if is_complete:
        return ChunkUploadResult(
            path=file_path,
            isComplete=is_complete
        )


def upload_data(save_dir, file: UploadFile = File(...)):
    file_path, ok = get_unique_path(save_dir, file.filename)
    if not ok:
        return file_path, ok
    # 保存文件
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return f"保存失败: {str(e)}", False
    return file_path, True



