import datetime
import os

# region const设置
DATASETS = "datasets"  # 迁移目录名
DATA = "/app/data"  # yaml存放地
MODELS = "/app/model"  # 为你的模型上传的存储路径
RUNS_HELMET = "/app/runs/helmet"  # 为训练产出路径
ULTRALYTICS = "ultralytics:basic"
DOCKER_PORT = 6006  # docker映射端口
SERVER_HOST = 9202  # server映射端口
# endregion


# region 路径及端口配置


config_path = {
    'HostConf': {  # 监听端口
        'host': '0.0.0.0',
        'port': SERVER_HOST,
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    },
    'PathConf': {  # 相关路径不做修改
        'SaveDataPath': './dataorign',  # 替换为你数据上传的存储路径
        'SaveDataSetsPath': f'./{DATASETS}',  # 为数据迁移保存的路径
        'SaveYamlDataPath': f'./{DATA}',  # yaml存放地
        'SaveModelPath': f'.{MODELS}',  # 为你的模型上传的存储路径
        'SaveRunPath': f'.{RUNS_HELMET}',  # 为训练产出路径
        'TestPath': f'./test',  # 为训练产出路径
    },
    'SysConf': {  # 系统设置
        'DbPath': "./db/atp.db",  # 数据库路径
        'LogPath': "./log",  # 系统日志路径
    },
}


# endregion


# region 配置docker命令


# 开始work命令 data_id找到对应的yaml
# project路径 /app/runs/helmet/{work_id}； 下一层目录格式train{train_count}
def start_into(data_id: str, work_id: str, model_path: str, train_count: str, epochs: int = 10, lr0: float = 0.01,
               batch: int = 16):
    project_path = f"{RUNS_HELMET}/{work_id}"
    start_command = f"docker run --rm --name helmet_train_work_{work_id} -it --ipc=host " \
                    f"-v {os.getcwd()}/app:/app -v {os.getcwd()}/{DATASETS}:/{DATASETS} " \
                    f"-p {DOCKER_PORT}:{DOCKER_PORT} " \
                    f"--gpus all " \
                    f"{ULTRALYTICS} " \
                    f"yolo detect train data={DATA}/{data_id}/data.yaml model= /app/{model_path}.pt " \
                    f"project={project_path} name=train{train_count} " \
                    f"epochs={epochs} imgsz=640 device=0 lr0={lr0} batch={batch} > train.log"
    append_to_test_file(config_path["PathConf"]["TestPath"] + "/test.txt", start_command)
    return start_command


# 重新评估
def start_assessment(data_id: str, work_id: str, train_count: str):
    project_path = f"{RUNS_HELMET}/{work_id}"
    assessment_command = f"docker run --rm --name val_work_{work_id} --ipc=host " \
                         f"-v {os.getcwd()}/app:/app -v {os.getcwd()}/{DATASETS}:/{DATASETS} " \
                         f"--gpus all " \
                         f"{ULTRALYTICS} " \
                         f"yolo val data={DATA}/{data_id}/data.yaml model={project_path}/train{train_count}/weights/best.pt " \
                         f"project={project_path} name=val{train_count}"
    append_to_test_file(config_path["PathConf"]["TestPath"] + "/test.txt", assessment_command)
    return assessment_command


# 过程读取
def exec_into(work_id: str, train_count: str):
    project_path = f"{RUNS_HELMET}/{work_id}"
    process_command = f"docker exec -it helmet_train_work_{work_id} tensorboard --logdir {project_path}/train{train_count} --host 0.0.0.0"
    append_to_test_file(config_path["PathConf"]["TestPath"] + "/test.txt", process_command)
    return process_command


# 结果数据读取
def get_data_show(work_id: str, train_count: str):
    project_path = f"{RUNS_HELMET}/{work_id}"
    return {
        "prf": f".{project_path}/val{train_count}/prf1.json",
        "matrix": f".{project_path}/val{train_count}/confusion_matrix.json",
        "result_csv": f".{project_path}/train{train_count}/results.csv"
    }


# endregion

def append_to_test_file(file_path: str, content: str):
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file_path, 'a') as file:
            file.write(f"[{current_time}] {content}\n")
    except IOError as e:
        raise Exception(f"追究文件失败：{e}")
