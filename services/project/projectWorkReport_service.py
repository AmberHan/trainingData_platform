import os.path

from sqlmodel import Session

from config import config
from config.config import get_data_show, start_assessment
from schemas.projectWorkReport_model import GetProjectWorkReportReply
from schemas.req_model import StringIdReq
from services.project.projectWork_service import run_work
from sqlmodels.projectWork import ProjectWork as ProjectWorkSql
from util.file import get_last_row_csv, read_json_file, count_directories


def get_project_work_report_by_id_impl(
        req: StringIdReq,
        db: Session
) -> GetProjectWorkReportReply:
    work = ProjectWorkSql.select_by_id(db, req.id)
    if work is None:
        raise Exception("Project Work Not Found")
    # save_path = './test/results.csv'
    train_count = count_directories(f".{config.RUNS_HELMET_PATH}/{req.id}", "train1") * '1'
    save_path = os.path.join(get_data_show(work.Id, train_count)["result_csv"])
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
    # 先执行docker命令

    res_work = ProjectWorkSql.select_by_id(db, req.id)
    train_count = count_directories(f".{config.RUNS_HELMET_PATH}/{req.id}", "train") * '1'
    vol_count = count_directories(f".{config.RUNS_HELMET_PATH}/{req.id}", "val") * '1'
    if train_count != vol_count:
        run_work(start_assessment(res_work.DataId, req.id, vol_count))
    vol_count1 = count_directories(f".{config.RUNS_HELMET_PATH}/{req.id}", "val1") * '1'
    path_get = get_data_show(req.id, vol_count1)
    try:
        data = read_json_file(path_get["prf"])
        data2 = read_json_file(path_get["matrix"])
    except Exception as e:
        print(f"读取文件时出错: {e}")
    res = {"prf": data, "matrix": data2}
    return res
