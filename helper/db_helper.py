import sys
sys.path.append(".")
from helper.property_reader import PropertyReader
import this
import pymongo



class DBHelper:
    def __init__(self):
        self.propertyReader = PropertyReader()
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass

    def getCollection(self, tableName):
        client = pymongo.MongoClient(
            self.propertyReader.getDbConnectionString())
        mydb = client[self.propertyReader.getDbName()]
        return mydb[tableName]

    def getDb(self):
        client = pymongo.MongoClient(
            self.propertyReader.getDbConnectionString())
        return client[self.propertyReader.getDbName()]
