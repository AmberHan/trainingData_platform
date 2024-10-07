import os

from sqlalchemy.orm import Session

from schemas.data_model import SaveDataReq, GetDataListByPageReply, SaveDataForm
from schemas.req_model import ListByPageReq
from services.module import module_service
from services.module.moduleType_service import get_module_type_by_id_impl
from services.module.module_service import StringIdReq
from sqlmodels.data import Data as DataSql, Data
from sqlmodels.dataFile import DataFile
from sqlmodels.moduleType import ModuleType
from sqlmodels.user import User
from util.file import unzip_file, untar_file, file_path_to_url
from util.util import NewId, TimeNow, exec_command


def get_data_list_by_page_impl(id: str, req: ListByPageReq, db: Session) -> GetDataListByPageReply:
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
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
def save_data_file(data_file_req: DataFile, db: Session):
    data_file_req.save(db)



def save_data(req: SaveDataForm, db: Session):
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

    mod.DataName = req.dataName
    mod.ModuleTypeId = req.moduleTypeId
    mod.Detail = req.detail
    mod.DataStatus = 2
    mod.UploadPath = req.uploadPath
    mod.ExportPath = file_path
    mod.FileSize = req.fileSize
    mod.UpdateTime = TimeNow()
    mod.save(db)

    # 获取文件列表并保存入库
    try:
        res = exec_command(f"ls {file_path}*")
        if res:
            res_list = res[0].strip().split("\n")
            class_num = 0

            for val in res_list:
                if not val:
                    continue
                res_l = val.split("\n")
                class_num += 1

                for k, v in enumerate(res_l):
                    img_path = ""
                    dir_path = ""
                    if k == 0:
                        # imgPath
                        img_path = v.strip(":") + "/"
                        dir_path = v[len(file_path):].strip(":")
                    else:
                        # img
                        img_file = img_path + v
                        # 保存文件
                        data_file_req = DataFile(
                            DataId=mod.Id,
                            FilePath=img_file,
                            Url=file_path_to_url(img_file),
                            DirPath=dir_path)
                        save_data_file(data_file_req, db)

            # 修改类型数量
            mod.ClassNum = class_num
            mod.save(db)
    except Exception as e:
        print(f"Error processing files: {str(e)}")
        raise

    return None


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
