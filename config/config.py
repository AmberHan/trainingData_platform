config_path = {
    'HostConf': {  # 端口
        'host': '0.0.0.0',
        'port': 9988
    },
    'FileConf': {  # 文件上传
        'SavePath': './upload_files',  # 替换为你的存储路径
        'Uri': 'http://localhost/uploads/'  # 替换为你的 URI
    },
    'DbConf': {  # 数据库
        'DbPath': "./db/atp.db",
    },
    'LogConf': {  # 日志
        'LogPath': "./log",
    },
}
