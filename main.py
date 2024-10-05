import uvicorn

from services import db

# pip install 'uvicorn[standard]'

if __name__ == '__main__':
    db.init_data_db()
    uvicorn.run("router.router:app", host="0.0.0.0", port=9988)
