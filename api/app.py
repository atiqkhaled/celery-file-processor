import sys
import time
sys.path.append("../celery_tasks")
from save_record_task import save_entry
from upload_task import upload_file
import websockets
from fastapi import FastAPI
from celery import current_app
import logging
import os
from fastapi import FastAPI, WebSocket
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from models import Task, Prediction
import uuid
import openpyxl
import pymongo
from bson.json_util import dumps, loads
from openpyxl import load_workbook
from bson.objectid import ObjectId
import json
from pydantic.typing import List
sys.path.insert(0, os.path.realpath(os.path.pardir))
#import pymongo

UPLOAD_FOLDER = 'temp'
STATIC_FOLDER = 'static/results'
origins = [
    "http://localhost:90",
    "http://localhost:4200"
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
    print("Print 1")
    tasks = []
    try:
        for file in files:
            d = {}
            try:
                print("Print 2")
                nameSuffix = str(uuid.uuid4()).split(
                    '-')[0] + str(current_milli_time())
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
                print("APP Py")
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
                                                  'result': result, 'name': name, 'path': path})


@app.get('/api/status/{task_id}', response_model=Prediction)
async def status(task_id: str):
    task = AsyncResult(task_id)
    logging.info(task.status)
    return JSONResponse(status_code=200, content={'task_id': str(task_id), 'status': task.status, 'result': ''})


@app.get('/api/file/{fileId}')
async def saveRecord(fileId: str):
    taskId = save_entry.delay(fileId)
    return {"taskId": str(taskId)}


@app.websocket("/ws")
async def test(websocket: WebSocket):
    await websocket.accept()
    fileTaskRequest = await websocket.receive_json()
    taskId = fileTaskRequest["taskId"]
    #fileId = fileTaskRequest["fileId"]
    a = True
    doneTask = {}
    maxTry = 4
    currentTry = 0
    while a:
        task = AsyncResult(str(taskId))
        if task.ready():
            doneTask = task.get()
            if doneTask["status"] != "FAIL":
                doneTask["fileStatus"] = "INJECTED"
            else:
                doneTask["fileStatus"] = "INJECTION_FAILED"
            a = False
        else:
            if currentTry < maxTry:
                currentTry = currentTry + 1
                time.sleep(2)
            else:
                doneTask["status"] = "FAIL"
                doneTask["fileStatus"] = "INJECTION_FAILED"
                a = False

    await websocket.send_json(doneTask)
