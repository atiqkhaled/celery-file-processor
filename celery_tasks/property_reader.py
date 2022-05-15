import this
import pymongo
import configparser


class PropertyReader:
    config = configparser.RawConfigParser()
    config.read("config.properties")

    def __init__(self):
        pass

    def getConnectionString(self):
        return PropertyReader.config.get("azure", "CONNECT_STR")

    def getContainer(self):
        return PropertyReader.config.get("azure", "CONTAINER_NAME")

    def getDbConnectionString(self):
        return PropertyReader.config.get("database", "CONNECT_STR")

    def getDbName(self):
        return PropertyReader.config.get("database", "DB_NAME")
