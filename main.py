import uvicorn

from config import db
from config.config import config_path

if __name__ == '__main__':
    db.init_data_db()
    uvicorn.run("router.router:app", host=config_path['HostConf']['host'], port=config_path['HostConf']['port'])
