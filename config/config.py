# 路径端口配置
config_path = {
    'HostConf': {  # 监听端口
        'host': '0.0.0.0',
        'port': 8081
    },
    'FileConf': {  # 文件上传
        'SaveDataPath': './dataorign',  # 替换为你的数据存储路径
        'SaveDataSetsPath': './datasets',  # 替换为数据迁移路径
        'SaveModelPath': './model',  # 替换为你的模型存储路径
        'SaveRunPath': './app/run/',  # 替换为训练产出路径
        'SaveYamlDataPath': './app/data/',  # yaml存放地
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    },
    'SysConf': {  # 系统设置
        'DbPath': "./db/atp.db",  # 数据库路径
        'LogPath': "./log",  # 日志路径
        # "ResultFileFrom": "" # result.csv路径来源
    },
}


def start_into(data_id: str, work_id: str):
    # 由workid和data_id组成
    return f"docker run --rm --name helmet_train_work_{work_id} -it --ipc=host " \
           f"-v /data/disk2/yolov8/app:/app -p 6006:6006 --gpus all " \
           f"ultralytics/ultralytics:8.2.0 yolo detect train " \
           f"data=/app/data/{data_id}/data.yaml model=/app/model/yolov8s.pt " \
           f"project=/app/runs/helmet/{work_id} name=train epochs=10 imgsz=640 device=0 " \
           f"lr0=0.01 batch=16 > train.log"
    # return "python test2.py"


def exec_into(work_id: str):
    return f"docker exec -it helmet_train_work_{work_id} tensorboard --logdir /app/runs/helmet/{work_id}/train --host 0.0.0.0"
    # return "python test2.py"


def get_data_show(work_id: str):
    # 由workid和data_id组成
    return {
        "prf": f"./app/runs/helmet/{work_id}/train/prf1.json",  # 图1 TODO 改为动态目录
        "matrix": f"./app/runs/helmet/{work_id}/train/confusion_matrix.json"  # 图2 TODO 改为动态目录
    }
    # return "python test2.py"


# docker指令
config_command = {
    'startCommand': 'xxx',
    'stopCommand': 'xxx',
}
