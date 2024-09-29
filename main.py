import uvicorn
from services import db
# pip install 'uvicorn[standard]'

if __name__ == '__main__':
    db.init_data_db()
    uvicorn.run("router.router:app", host="127.0.0.1", port=8080)
