import logging
import os


def setup_logger():
    # 配置日志
    log_dir = 'log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logging.basicConfig(filename=os.path.join(log_dir, 'error.log'), level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        encoding='utf-8')
    return logging.getLogger(__name__)


# 创建并导出日志记录器
logger = setup_logger()