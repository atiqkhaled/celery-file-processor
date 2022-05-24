import this
import pymongo
import configparser
from configparser import ConfigParser
from configparser import RawConfigParser

class PropertyReader:
    #config = configparser.RawConfigParser()
    #config.read("config.properties")

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config.properties")
        pass

    def getConnectionString(self):
        return self.config.get("azure", "CONNECT_STR")

    def getContainer(self):
        return self.config.get("azure", "CONTAINER_NAME")

    def getDbConnectionString(self):
        #print(PropertyReader.config)
        return self.config.get("database", "CONNECT_STR")

    def getDbName(self):
        return self.config.get("database", "DB_NAME")
