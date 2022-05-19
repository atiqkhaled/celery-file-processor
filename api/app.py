
from celery import current_app
import logging
import os
from fastapi import FastAPI,WebSocket
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
import sys

sys.path.append("../celery_tasks")

from save_record_task import save_entry
from celery import current_app 
from pydantic.typing import List
import json
from bson.objectid import ObjectId
from openpyxl import load_workbook
from bson.json_util import dumps, loads
import pymongo
import openpyxl
import uuid
from models import Task, Prediction
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import websockets
import os
import logging
from upload_task import upload_file
import time
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

# @app.post("/socket")
# async def test():
#     print("hello socket")
#     async with websockets.connect('ws://localhost:8999/') as websocket:
#         await websocket.send("hello from py")
#         response = await websocket.recv()
#         print(response)
#         return response

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


# @app.get('/api/file/{fileId}')
# async def readFIle(fileId: str):
#     print(str)
#     client = pymongo.MongoClient("mongodb://host.docker.internal:27017")
#     mydb = client["test"]
#     fileContents = mydb.filecontents
#     fileContentId = ObjectId(fileId)
#     fileContent = fileContents.find_one({"_id": fileContentId})
#     mapperId = ObjectId(fileContent["mapperId"])
#     mappers = mydb.mappers
#     mapper = mappers.find_one({"_id": mapperId})
#     mappingInfo = json.loads(mapper["modelContent"])
#     collections = mydb[mapper["tableName"]]
#     mappedHeaders = list(mappingInfo.values())
#     book = load_workbook("Employee.xlsx")
#     sheets = book.sheetnames
#     for sheet in sheets:
#         worksheet = book[sheet]
#         rows = worksheet.rows
#         headers = [cell.value for cell in next(rows)]
#         headersDict = {k: v for v, k in enumerate(headers)}
#         filterdHeaders = [head for head in headers if head in mappedHeaders]
#         dbEntries = []
#         for row in rows:
#             dbEntry = {}
#             for entry in mappingInfo:
#                 excelColumn = mappingInfo[entry]
#                 print(entry)
#                 print(excelColumn)
#                 if excelColumn in filterdHeaders:
#                     dbEntry[entry] = row[headersDict[excelColumn]].value
#                 else:
#                     dbEntry[entry] = ""
#             dbEntries.append(dbEntry)
#             print(row[1].value)
#             print(dbEntries)

#     collections.insert_many(dbEntries)


@app.get('/api/file/{fileId}')
async def saveRecord(fileId: str):
    tasks = current_app.tasks.keys()
    print(tasks)
    print("Readddd")
    taskId = save_entry.delay(fileId)
    return {"task_id": taskId}


@app.websocket("/ws")
async def test(websocket:WebSocket):
    print("Accepting connection")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")




    