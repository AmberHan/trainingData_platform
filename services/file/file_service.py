import os
import shutil

from fastapi import UploadFile, File

from schemas.file_model import FileReply
from util.file import get_file_size
from util.util import NewId

config = {
    'FileConf': {
        'SavePath': './upload_files',  # 替换为你的存储路径
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    }
}


def upload_tar(file: UploadFile = File(...)):
    # 检查存储路径是否存在
    save_path = config['FileConf']['SavePath']
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)  # 创建目录，包括中间目录
        except OSError as e:
            return {"error": f"存储路径创建失败: {str(e)}"}
    if file.filename == '':
        return {"error": "未选择文件"}

    filename = file.filename
    file_ext = os.path.splitext(filename)[1]  # 获取文件扩展名
    new_name = NewId() + file_ext  # 生成新文件名

    file_path = os.path.join(save_path, new_name)

    # 保存文件
    try:
        file_location = os.path.join(save_path, new_name)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise ""

    reply = FileReply(
        path=file_path,
        url=config['FileConf']['Uri'] + new_name,
        fileSize=str(get_file_size(file_path))
    )
    return reply
