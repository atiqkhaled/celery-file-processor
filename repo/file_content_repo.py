from bson.objectid import ObjectId
import pymongo
import sys
sys.path.append("..")
from helper.db_helper import DBHelper


class FileRepo:
    dbHelper = DBHelper()

    def __init__(self):
        #self.connection = "mongodb://host.docker.internal:27017"
        #self.dbName = "test"
        pass

    def getFileContentById(self, fileId):
        mydb = FileRepo.dbHelper.getDb()
        fileContents = mydb.filecontents
        fileContentId = ObjectId(fileId)
        return fileContents.find_one({"_id": fileContentId})

    def update(self, filterStatusId, newStatusId):
        mydb = FileRepo.dbHelper.getDb()
        collections = FileRepo.dbHelper.getCollection("filecontents")
        collections.update_one({"status": filterStatusId}, {
                                    "$set": {"status": newStatusId}})