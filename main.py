import uvicorn
import time
from fastapi import FastAPI

from src.q7 import Api

app = FastAPI()

VERSION = '1.0.0'
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

app.include_router(Api.router)


@app.get("/")
async def hello():
    result = {'version': VERSION, 'start_time': START_TIME}
    return result


def start_server():
    print('Application Start')
    uvicorn.run(app, host="127.0.0.1", port=6061)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_server()

