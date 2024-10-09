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

def start_into(data_id: str):
    return f"docker run --rm --name helmet_train_work_{data_id} -it --ipc=host -v /data/disk2/yolov8/app:/app -p 6006:6006 --gpus all ultralytics/ultralytics:8.2.0 yolo detect train data=/app/data/{data_id}/data.yaml model=/app/model/yolov8s.pt project=/app/runs/{data_id}=train epochs=10 imgsz=640 device=0 lr0=0.01 batch=16 > train.log"

# docker指令
config_command = {
    'startCommand': 'xxx',
    'stopCommand': 'xxx',
}
