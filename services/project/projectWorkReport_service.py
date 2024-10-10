import os.path

from sqlmodel import Session

from config.config import config_path
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
    # save_path = './testFile/results.csv'
    save_path = os.path.join(config_path['SysConf']['LogPath'], work.ProjectId, work.Id, "results.csv")
    row = get_last_row_csv(save_path)
    try:
        precision = float(row[4])
        recall = float(row[5])
        return GetProjectWorkReportReply(
            precision=precision,
            recall=recall,
        )
    except Exception as e:
        raise Exception(f"数据转换失败，{e}")


# 图表返回
def get_project_work_inter_val_by_id(db):
    data = None
    data2 = None
    # 使用 try-except 读取文件
    try:
        data = read_json_file(config_path['SysConf']["Prf"])
        data2 = read_json_file(config_path['SysConf']["Matrix"])
    except Exception as e:
        print(f"读取文件时出错: {e}")
    res = {"prf": data, "matrix": data2}
    return res