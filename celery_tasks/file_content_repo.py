import sys
sys.path.append("./celery_tasks")
from db_helper import DBHelper
import pymongo
from bson.objectid import ObjectId



class FileRepo:
    dbHelper = DBHelper("mongodb://host.docker.internal:27017", "test")

    def __init__(self):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass


    def getFileContentById(self, fileId):
        mydb = FileRepo.dbHelper.getDb()
        fileContents = mydb.filecontents
        fileContentId = ObjectId(fileId)
        return fileContents.find_one({"_id": fileContentId})
