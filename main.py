import uvicorn

from config.db_config import init_data_db
from config.file_config import init_file_conf
from config.config import config_path

if __name__ == '__main__':
    init_data_db()
    init_file_conf()  # 创建config_path['FileConf']配置下的目录路径
    uvicorn.run("router.router:app", host=config_path['HostConf']['host'], port=config_path['HostConf']['port'])
