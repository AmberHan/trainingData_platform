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
    },
}

# docker指令
config_command = {
    'startCommand': 'xxx',
    'stopCommand': 'xxx',
}
