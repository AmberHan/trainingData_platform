import logging


def setup_logger():
    # 配置日志
    logging.basicConfig(filename='log/error.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        encoding='utf-8')
    return logging.getLogger(__name__)


# 创建并导出日志记录器
logger = setup_logger()
