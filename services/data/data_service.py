import os

from sqlalchemy.orm import Session

from config.config import config_path
from schemas.data_model import SaveDataReq, GetDataListByPageReply, SaveDataForm
from schemas.req_model import ListByPageReq
from services.module import module_service
from services.module.moduleType_service import get_module_type_by_id_impl
from services.module.module_service import StringIdReq
from sqlmodels.data import Data as DataSql, Data
from sqlmodels.dataFile import DataFile
from sqlmodels.moduleType import ModuleType
from sqlmodels.user import User
from util.file import unzip_file, untar_file, file_path_to_url, delete_file_and_directory, split_and_move_files
from util.util import NewId, TimeNow


def get_data_list_by_page_impl(id: str, req: ListByPageReq, db: Session) -> GetDataListByPageReply:
    try:
        # 查询分页数据
        if req.size < 15:
            req.size = 15
        if req.page < 1:
            req.page = 1

        # 调用封装好的分页方法
        projects, total = DataSql.find_by_page(id, req.page, req.size, req.like, db)
        reply = GetDataListByPageReply(total=total)
        for i, p in enumerate(projects):
            saveDataReq = SaveDataReq.from_orm(p)
            user = User.select_by_id(db, p.CreateUid)
            if user is not None:
                saveDataReq.userName = user.username
            moduleType = ModuleType.select_by_id(db, p.ModuleTypeId)
            if moduleType is not None:
                saveDataReq.moduleTypeName = moduleType.ModuleTypeName
            reply.list.append(saveDataReq)
        return reply
    except Exception as e:
        raise Exception(f"Failed to get data by page: {e}")


def get_data_by_id_impl(req: StringIdReq, db: Session) -> SaveDataReq:
    return get_data_by_id(req, db)


def get_data_by_id(req: StringIdReq, db: Session) -> SaveDataReq:
    data = DataSql.select_by_id(db, req.id)
    if data is None:
        return None
    saveData = SaveDataReq.from_orm(data)
    m = get_module_type_by_id_impl(module_service.StringIdReq(id=data.ModuleTypeId), db)
    if m is not None:
        saveData.moduleTypeName = m.moduleTypeName
    user = User.select_by_id(db, data.CreateUid)
    saveData.userName = user.username
    return saveData


# data管理保存


def save_data(uid: str, req: SaveDataForm, db: Session):
    if not os.path.exists(req.uploadPath):
        raise Exception("文件不存在，请重新上传")

    # 解压文件
    tar_zip_path = req.uploadPath
    file_ext = os.path.splitext(tar_zip_path)[1]
    file_name = os.path.basename(tar_zip_path)
    file_path = os.path.dirname(tar_zip_path) + "/" + file_name.replace(file_ext, '') + "/"

    try:
        if file_ext == ".zip":
            unzip_file(tar_zip_path, file_path)
            print(f"Unzipped {tar_zip_path} to {file_path}")
        elif file_ext == ".gz":
            untar_file(tar_zip_path, file_path)
            print(f"Untarred {tar_zip_path} to {file_path}")
        else:
            raise Exception(f"不支持 {file_ext} 格式的文件解压")
    except Exception as e:
        print(f"Failed to unzip {tar_zip_path}: {str(e)}")
        raise Exception("解压失败，请重新上传合法的压缩包")

    image_files = get_files_from_directory(file_path, 'images')

    # 获取 labels 文件夹下的所有文件
    label_files = get_files_from_directory(file_path, 'labels')

    if len(image_files) != len(label_files):
        # 找出没有对应label的image文件
        unmatched_images = []
        for img in image_files:
            # 假设图像是 .png 文件，对应的标签文件是 .txt
            label_name = img.replace("images", "labels").replace(".jpg", ".txt")

            # 检查转换后的标签是否在 label_files 中
            if label_name not in label_files:
                unmatched_images.append(img)
        res = ", ".join(unmatched_images)
        delete_file_and_directory(tar_zip_path)
        delete_file_and_directory(file_path)
        raise Exception(f"上传失败，images和labels数据未对应， 如下{res}", "请重新上传合法的压缩包")

    # 保存数据
    mod = Data()

    # TODO 目前无对应id
    # if req['id']:
    #     mod = Data.select_by_id(req['id'])
    #     if not mod:
    #         raise Exception(f"Failed to find data with ID: {req['id']}")
    # else:
    mod.Id = NewId()
    mod.CreateTime = TimeNow()
    mod.CreateUid = uid
    mod.DataName = req.dataName
    mod.ModuleTypeId = req.moduleTypeId
    mod.Detail = req.detail
    mod.DataStatus = 2
    mod.UploadPath = req.uploadPath
    mod.ExportPath = file_path
    mod.FileSize = req.fileSize
    mod.UpdateTime = TimeNow()
    mod.save(db)

    print(file_path)
    # 获取文件列表并保存入库
    try:
        res_list = ['images', 'labels']
        class_num = 0
        #
        for val in res_list:
            if not val:
                continue
            class_num += 1
        #
        for k, v in enumerate(image_files):
            # 保存图片
            data_file = DataFile()
            data_file.Id = NewId()
            data_file.DataId = mod.Id
            data_file.FilePath = v
            data_file.FileType = "png"
            data_file.Url = file_path_to_url(v)
            data_file.DirPath = "images"
            data_file.save(db)
            # 保存文件
            data_file2 = DataFile()
            data_file2.Id = NewId()
            data_file2.DataId = mod.Id
            data_file2.FilePath = label_files[k]
            data_file2.FileType = "txt"
            data_file2.Url = file_path_to_url(label_files[k])
            data_file2.DirPath = "labels"
            data_file2.save(db)
        #         # 修改类型数量
        mod.ClassNum = class_num
        mod.save(db)
    except Exception as e:
        print(f"Error processing files: {str(e)}")
        raise
    res = DataFile.find_all_by_data_id(db, mod.Id)
    images_parent_dir = config_path['PathConf']['SaveDataSetsPath'] + "/" + mod.Id
    split_and_move_files(res, 10, 10, 80, images_parent_dir)
    return None


def get_files_from_directory(base_dir, subfolder_name):
    """
    在 base_dir 目录下递归查找指定子文件夹 subfolder_name 中的所有文件
    """
    file_list = []
    for root, dirs, files in os.walk(base_dir):
        if subfolder_name in dirs:
            folder_path = os.path.join(root, subfolder_name)
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    file_list.append(file_path)
    return file_list


def delete_data_impl(
        id: str,
        db: Session,
):
    delete_data(id, db)


def delete_all_data_impl(
        ids: list,
        db: Session,
):
    if len(ids) == 0:
        raise Exception("id不能为空")
    for id in ids:
        delete_data(id, db)


def delete_data(
        id: str,
        db: Session,
):
    data_sql = DataSql()
    data_sql.Id = id
    data_sql.delete(db)
