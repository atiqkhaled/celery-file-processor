import this
import pymongo

class DBHelper:
    
    def __init__(self,connection,dbName):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        self.connection = connection
        self.dbName = dbName
        pass

    def connection(self):
        return self.connection

    def dbName(self):
        return self.dbName

    def getDb(self):
        client = pymongo.MongoClient(self.connection)
        return client[self.dbName]
        
        