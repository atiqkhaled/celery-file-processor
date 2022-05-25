import logging
from app_config import CONTAINER_NAME,CONNECT_STR
import sys
sys.path.append("./celery_tasks")
from azure.storage.blob import BlobServiceClient
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))

class AzureStorageHandler():
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)

    def upload(self, file):
        blobName = file.split('/')[2]
        blob_client = self.blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blobName)
        # upload file to azure storage
        with open(file, "rb") as data:
            blob_client.upload_blob(data=data)
        ## If file exists, delete it ##
        if os.path.isfile(file):
          os.remove(file)
        print('upload done')  

    def download(self,file):
        return 'read file from azure' 