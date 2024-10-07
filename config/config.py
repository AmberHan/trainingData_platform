config_path = {
    'HostConf': {  # 端口
        'host': '0.0.0.0',
        'port': 8080
    },
    'FileConf': {  # 文件上传
        'SaveDataPath': './data',  # 替换为你的数据存储路径
        'SaveDataSetsPath': './datasets',  # 替换为数据迁移路径
        'SaveModelPath': './model',  # 替换为你的模型存储路径
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    },
    'DbConf': {  # 数据库
        'DbPath': "./db/atp.db",
    },
    'LogConf': {  # 日志
        'LogPath': "./log",
    },
}
