
import time
from typing import Optional

from fastapi import FastAPI
import sys
import os
import logging
sys.path.insert(0, os.path.realpath(os.path.pardir))
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from celery_tasks.upload_task import upload_file
from celery.result import AsyncResult
from models import Task, Prediction
import uuid
import logging
from pydantic.typing import List

UPLOAD_FOLDER = 'temp'
STATIC_FOLDER = 'static/results'
origins = [
    "http://localhost:90",
    "http://localhost:4200",
]

app = FastAPI()
# app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def read_root():
    return {"Hello": "World"}

@app.post('/api/process')
async def process(files: List[UploadFile] = File(...)):
    tasks = []
    try:
        for file in files:
            d = {}
            try:
                nameSuffix = str(uuid.uuid4()).split('-')[0] + str(current_milli_time())
                name = file.filename.split('.')[0]
                ext = file.filename.split('.')[-1]
                fullName = name + nameSuffix
                file_name = f'{UPLOAD_FOLDER}/{fullName}.{ext}'
                with open(file_name, 'wb+') as f:
                    f.write(file.file.read())
                f.close()

                # upload task
                task_id = upload_file.delay(os.path.join('api', file_name))
                d['task_id'] = str(task_id)
                d['status'] = 'PROCESSING'
                d['url_result'] = f'/api/result/{task_id}'
            except Exception as ex:
                logging.info(ex)
                d['task_id'] = str(task_id)
                d['status'] = 'ERROR'
                d['url_result'] = ''
            tasks.append(d)
        return JSONResponse(status_code=202, content=tasks)
    except Exception as ex:
        print('exception caught :', ex)
        return JSONResponse(status_code=400, content=[])


def current_milli_time():
    return round(time.time() * 1000)



@app.get('/api/result/{task_id}', response_model=Prediction)
async def result(task_id: str):
    task = AsyncResult(task_id)
    logging.info(task.status)
    # Task Not Ready
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': task.status, 'result': ''})

    # Task done: return the value
    task_result = task.get()
    result = task_result.get('result')
    name = task_result.get('name')
    path = task_result.get('path')
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 
    'status': task_result.get('status'),
    'result': result,'name':name,'path' : path})


@app.get('/api/status/{task_id}', response_model=Prediction)
async def status(task_id: str):
    task = AsyncResult(task_id)
    logging.info(task.status) 
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': ''})