import configparser
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
from azure.storage.blob import BlobServiceClient
sys.path.append("./celery_tasks")
from property_reader import PropertyReader


sys.path.insert(0, os.path.realpath(os.path.pardir))

propertyReader = PropertyReader()

STORAGEACCOUNTURL = "https://<STORAGE_ACCOUNT_NAME>.blob.core.windows.net"
CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=flexmax;AccountKey=uzaBDMo/m9r+qke6J9asWAqzkLhJ18QdvC3OezDo6o7mHz6MSYw1sFUZhthpPDCB39T/jRAKtDM4+ASttqij1w==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)


def getMapping(mapper):
    return json.loads(mapper["modelContent"])


def getExcelHeader(rows):
    return [cell.value for cell in next(rows)]


@app.task(ignore_result=False, bind=True)
def save_entry(self, fileId):
    dbHelper = DBHelper()
    #mydb = dbHelper.getDb()
    fileRepo = FileRepo()
    fileContent = fileRepo.getFileContentById(fileId)
    filePath = fileContent["path"]
    mapperRepo = MapperRepo()
    mapper = mapperRepo.getMapperById(fileContent["mapperId"])
    mappingInfo = getMapping(mapper)
    collections = dbHelper.getCollection(mapper["tableName"])
    mappedHeaders = list(mappingInfo.values())
    
    blob_client = blob_service_client.get_blob_client(
        container=propertyReader.getContainer(), blob=filePath)

    download_file_path = os.path.join("temp",  fileContent["path"])
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(download_file_path, "wb") as download_file:
       download_file.write(blob_client.download_blob().readall())

    book = load_workbook(download_file_path)
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
                if excelColumn in filterdHeaders:
                    dbEntry[entry] = row[headersDict[excelColumn]].value
                else:
                    dbEntry[entry] = ""
            dbEntries.append(dbEntry)

    collections.insert_many(dbEntries)
    return {'status': 'SUCCESS', 'result': 'done'}
