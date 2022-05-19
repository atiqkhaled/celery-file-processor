import this
import pymongo
import sys
sys.path.append("./celery_tasks")

from property_reader import PropertyReader


class DBHelper:
    propertyReader = PropertyReader()
    def __init__(self):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass

    def getCollection(self,tableName):
        print(tableName)
        print("DB HHH 2")
        client = pymongo.MongoClient(DBHelper.propertyReader.getDbConnectionString())
        mydb = client[DBHelper.propertyReader.getDbName()]
        return mydb[tableName]


    def getDb(self):
        print("DB HHH")
        print(DBHelper.propertyReader.getDbConnectionString())
        print(DBHelper.propertyReader.getDbName())
        client = pymongo.MongoClient(DBHelper.propertyReader.getDbConnectionString())
        return client[DBHelper.propertyReader.getDbName()]
        
        