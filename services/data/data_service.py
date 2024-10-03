from typing import Optional, List

from fastapi.logger import logger
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from schemas.data_model import GetDataListByPageReq, SaveDataReq, GetDataListByPageReply
from sqlmodels.data import Data
from sqlmodels.module import Module
from sqlmodels.moduleType import ModuleType
from sqlmodels.user import User


def data_to_save_project_req(data: Data) -> SaveDataReq:
    return SaveDataReq(
        id=data.Id,
        dataName=data.DataName,
        moduleTypeId=data.ModuleTypeId,

        detail=data.Detail,
        dataStatus=data.DataStatus,
        uploadPath=data.UploadPath,
        exportPath=data.ExportPath,
        fileSize=data.FileSize,
        createUid=data.CreateUid,
        createTime=data.CreateTime,
        updateTime=data.UpdateTime,
        classNum=data.ClassNum
    )



def get_data_list_by_page_impl(id: str, req: GetDataListByPageReq, db: Session):
    try:
        # 查询分页数据
        if req.size < 5:
            req.size = 5
        if req.page < 1:
            req.page = 1

            # 调用封装好的分页方法
        projects, total = Data.find_by_page(id, req.page, req.size, req.like, db)
        reply = GetDataListByPageReply(total=total)
        for i, p in enumerate(projects):
            saveDataReq = data_to_save_project_req(p)
            saveDataReq.userName = User.select_by_id(db, p.CreateUid).username
            try:
                saveDataReq.moduleTypeName = ModuleType.select_by_id(db, p.ModuleTypeId).ModuleTypeName
            except:
                saveDataReq.moduleTypeName = "none"
            reply.list.append(saveDataReq)
        return reply
    except Exception as e:
        logger.error(f"Failed to get data by page: {e}")
        raise Exception("Failed to fetch data")