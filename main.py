import uvicorn

from config import db

if __name__ == '__main__':
    db.init_data_db()
    uvicorn.run("router.router:app", host="0.0.0.0", port=8080)
