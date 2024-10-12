# region 路径及端口配置
config_path = {
    'HostConf': {  # 监听端口
        'host': '0.0.0.0',
        'port': 9202,
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    },
    'FileConf': {  # 相关路径配置
        'SaveDataPath': './dataorign',  # 替换为你数据上传的存储路径
        'SaveDataSetsPath': './app/datasets',  # 替换为数据迁移保存的路径
        'SaveModelPath': './model',  # 替换为你的模型上传的存储路径
        'SaveRunPath': './app/run/',  # 替换为训练产出路径
        'SaveYamlDataPath': './app/data/',  # yaml存放地
    },
    'SysConf': {  # 系统设置
        'DbPath': "./db/atp.db",  # 数据库路径
        'LogPath': "./log",  # 日志路径
    },
}


# endregion


# region 配置docker命令
# 开始work命令
# todo 需要根据情况修改下面的路径，通用的路径可以在config_path里配置
def start_into(data_id: str, work_id: str, model_path: str, epochs: int = 10, lr0: float = 0.01, batch: int = 16):
    # 由workid和data_id组成
    start_command = f"docker run --rm --name helmet_train_work_{work_id} -it --ipc=host " \
           f"-v /data/disk2/yolov8/app:/app -p 6006:6006 --gpus all " \
           f"ultralytics/ultralytics:8.2.0 yolo detect train " \
           f"data=/app/data/{data_id}/data.yaml model= {model_path}.pt " \
           f"project=/app/runs/helmet/{work_id} name=train epochs={epochs} imgsz=640 device=0 " \
           f"lr0={lr0} batch={batch} > train.log"
    print(start_command)
    return start_command
    # return "python test2.py"


# 过程读取
def exec_into(work_id: str):
    process_command = f"docker exec -it helmet_train_work_{work_id} tensorboard --logdir /app/runs/helmet/{work_id}/train --host 0.0.0.0"
    print(process_command)
    return process_command
    # return "python test2.py"


# 结果数据读取
# todo 需要根据情况修改下面的路径，通用的路径可以在config_path里配置
def get_data_show(work_id: str):
    # 由workid和data_id组成
    # return "python test2.py"
    return {
        "prf": f"./app/runs/helmet/{work_id}/train/prf1.json",  # 图1 TODO 改为动态目录
        "matrix": f"./app/runs/helmet/{work_id}/train/confusion_matrix.json",  # 图2 TODO 改为动态目录
        "result_csv": f"./app/runs/helmet/{work_id}/train/results.csv"  # 图2 TODO 改为动态目录
    }
# endregion
