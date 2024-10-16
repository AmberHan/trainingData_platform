import os
import shutil
from pathlib import Path

from fastapi import UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse

from config import config
from config.config import config_path
from schemas.file_model import FileReply, ChunkUploadResult
from schemas.req_model import DownloadParams
from util.file import get_file_size, get_unique_path, count_directories
from util.util import calculate_md5


def upload_tar_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(config_path['PathConf']['SaveDataPath'], file)
    if is_complete:
        return FileReply(
            path=file_path,
            url=config_path['HostConf']['Uri'] + "?path=" + os.path.basename(file_path),
            fileSize=str(get_file_size(file_path))
        )
    return Exception(file_path)


def upload_impl(file: UploadFile = File(...)):
    file_path, is_complete = upload_data(config_path['PathConf']['SaveModelPath'], file)
    if is_complete:
        return ChunkUploadResult(
            path=os.path.basename(file_path),
            isComplete=is_complete
        )
    else:
        raise Exception(file_path)


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


def download_impl(
        req: DownloadParams
):
    file_location = ""
    add = False
    if req.workId is not None:
        work_path = f".{config.RUNS_HELMET_PATH}/{req.workId}"
        train_count = count_directories(work_path, "train1") * '1'
        file_location = f"{work_path}/train{train_count}/weights/best.pt"
    elif req.modelName is not None:
        file_location = f"{config.config_path['PathConf']['SaveModelPath']}/{req.modelName}"
    elif req.path is not None:
        file_location = f"{config.config_path['PathConf']['SaveDataPath']}/{req.path}"
        add = True
    return download_file(file_location, add)


def download_file(path: str, add: bool = False):
    # 检查路径是否安全
    safe_path = Path(path).resolve()
    if not safe_path.is_file() or not safe_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # 获取文件的基本名称
    filename = os.path.basename(safe_path)

    # 设置响应头
    headers = {}
    if add:
        headers = {
            "Content-Disposition": f"inline; filename={filename}",
            "Content-Length": str(safe_path.stat().st_size),
        }

    # 返回文件
    return FileResponse(path=str(safe_path), filename=filename, headers=headers)


async def upload_chunk_impl(chunk_id: int, file: UploadFile, md5: str = Form(...)):
    chunk_path = os.path.join(config_path['PathConf']['SaveDataPath'], f"{chunk_id}_{file.filename}")
    if os.path.exists(chunk_path):
        if calculate_md5(chunk_path) == md5:
            return FileReply(
                path=chunk_path,
                url=config_path['HostConf']['Uri'] + "?path=" + os.path.basename(chunk_path),
                fileSize=str(get_file_size(chunk_path))
            )
        else:
            print("上传的数据不一致，已删除，重新保存")
            os.remove(chunk_path)

    with open(chunk_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # 验证分片的MD5值
    calculated_md5 = calculate_md5(chunk_path)
    if calculated_md5 != md5:
        os.remove(chunk_path)
        raise HTTPException(status_code=400, detail=f"MD5 mismatch for chunk {chunk_id}")

    return FileReply(
            path=chunk_path,
            url=config_path['HostConf']['Uri'] + "?path=" + os.path.basename(chunk_path),
            fileSize=str(get_file_size(chunk_path))
        )


def merge_chunks_impl(file_name: str, file_md5: str):
    try:
        # 获取所有分片
        chunks = [f for f in os.listdir(config_path['PathConf']['SaveDataPath']) if f.endswith(f"_{file_name}")]
        chunks.sort(key=lambda x: int(x.split('_')[0]))  # 按分片编号排序

        # 合并分片
        merged_path = os.path.join(config_path['PathConf']['SaveDataPath'], file_name)
        with open(merged_path, "wb") as merged_file:
            for chunk in chunks:
                chunk_path = os.path.join(config_path['PathConf']['SaveDataPath'], chunk)
                with open(chunk_path, "rb") as chunk_file:
                    shutil.copyfileobj(chunk_file, merged_file)
                os.remove(chunk_path)  # 删除已合并的分片

        # 验证合并后的文件的MD5值
        calculated_file_md5 = calculate_md5(merged_path)
        if calculated_file_md5 != file_md5:
            os.remove(merged_path)
            raise HTTPException(status_code=400, detail="MD5 mismatch for the merged file")

        return FileReply(
            path=merged_path,
            url=config_path['HostConf']['Uri'] + "?path=" + os.path.basename(merged_path),
            fileSize=str(get_file_size(merged_path))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
