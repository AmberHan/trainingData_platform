import os

from config.config import config_path


def init_file_conf():
    file_conf = config_path.get('FileConf', {})
    for _, path in file_conf.items():
        if not os.path.exists(path):
            os.makedirs(path)
