import sys
sys.path.append("..")
from helper.db_helper import DBHelper
import pymongo
from bson.objectid import ObjectId



class StatusRepo:
    dbHelper = DBHelper()

    def __init__(self):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass


    def getStatusById(self, stausId):
        mydb = StatusRepo.dbHelper.getDb()
        status = mydb.status
        stausId = ObjectId(status["_id"])
        return status.find_one({"_id": stausId})

    def getStatusByName(self, stausName):
        mydb = StatusRepo.dbHelper.getDb()
        status = mydb.status
        return status.find_one({"name": stausName})
