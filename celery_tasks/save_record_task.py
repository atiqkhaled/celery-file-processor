from mapper_repo import MapperRepo
from file_content_repo import FileRepo
from db_helper import DBHelper
import os
import openpyxl
from openpyxl import load_workbook
import pymongo
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import json
from app_worker import app
from celery import Task
import sys
sys.path.append("./celery_tasks")
sys.path.insert(0, os.path.realpath(os.path.pardir))



def getMapping(mapper):
    return json.loads(mapper["modelContent"])

def getExcelHeader(rows):
    return [cell.value for cell in next(rows)]

@app.task(ignore_result=False, bind=True)
def save_entry(self, fileId):
    dbHelper = DBHelper("mongodb://host.docker.internal:27017", "test")
    mydb = dbHelper.getDb()
    fileRepo = FileRepo() 
    fileContent = fileRepo.getFileContentById(fileId)

    mapperRepo = MapperRepo()
    mapper = mapperRepo.getMapperById(fileContent["mapperId"])
    
    mappingInfo = getMapping(mapper)
    collections = mydb[mapper["tableName"]]
    mappedHeaders = list(mappingInfo.values())
    book = load_workbook("Employee.xlsx")
    sheets = book.sheetnames
    for sheet in sheets:
        worksheet = book[sheet]
        rows = worksheet.rows
        headers = getExcelHeader(rows)
        headersDict = {k: v for v, k in enumerate(headers)}
        filterdHeaders = [head for head in headers if head in mappedHeaders]
        dbEntries = []
        for row in rows:
            dbEntry = {}
            for entry in mappingInfo:
                excelColumn = mappingInfo[entry]
                print(entry)
                print(excelColumn)
                if excelColumn in filterdHeaders:
                    dbEntry[entry] = row[headersDict[excelColumn]].value
                else:
                    dbEntry[entry] = ""
            dbEntries.append(dbEntry)
            print(row[1].value)
            print(dbEntries)

    collections.insert_many(dbEntries)
    return {'status': 'SUCCESS', 'result': 'done'}
