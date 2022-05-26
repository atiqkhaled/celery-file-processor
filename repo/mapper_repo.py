import sys
sys.path.append("..")
from helper.db_helper import DBHelper
import pymongo
from bson.objectid import ObjectId



class MapperRepo:
    dbHelper = DBHelper()

    def __init__(self):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass


    def getMapperById(self, mapperId):
        mydb = MapperRepo.dbHelper.getDb()
        mappers = mydb.mappers
        mapperIdObj = ObjectId(mapperId)
        return mappers.find_one({"_id": mapperIdObj})
