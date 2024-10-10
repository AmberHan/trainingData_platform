import os.path

from sqlmodel import Session

from config.config import config_path, get_data_show
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from schemas.projectWorkReport_model import GetProjectWorkReportReply
from schemas.req_model import StringIdReq
from util.file import get_last_row_csv, read_json_file
import json

def get_project_work_report_by_id_impl(
        req: StringIdReq,
        db: Session
) -> GetProjectWorkReportReply:
    work = ProjectWorkSql.select_by_id(db, req.id)
    if work is None:
        raise Exception("Project Work Not Found")
    # todo 确定路径, 转移路径
    # save_path = './test/results.csv'
    save_path = os.path.join(get_data_show(work.Id))
    row = get_last_row_csv(save_path)
    try:
        precision = float(row[4])
        recall = float(row[5])
        mAp = float(row[6])
        return GetProjectWorkReportReply(
            precision=precision,
            recall=recall,
            mAp=mAp
        )
    except Exception as e:
        raise Exception(f"数据转换失败，{e}")


# 图表返回
def get_project_work_inter_val_by_id(req: StringIdReq, db: Session):
    data = None
    data2 = None
    # 使用 try-except 读取文件
    path_get = get_data_show(req.id)
    print(path_get)
    try:
        data = read_json_file(path_get["prf"])
        data2 = read_json_file(path_get["matrix"])
    except Exception as e:
        print(f"读取文件时出错: {e}")
    res = {"prf": data, "matrix": data2}
    return res


