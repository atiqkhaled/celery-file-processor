import imp
import logging
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from app_worker import app
from azure.storage.blob import BlobServiceClient
import os
import sys
from destination_handler.destination_enum import DestinationEnum
from app_config import DESTINATION
from destination_handler.destination_factory import DestinationFactory
sys.path.insert(0, os.path.realpath(os.path.pardir))



@app.task(ignore_result=False, bind=True)
def upload_file(self, file):
    i = 90000
    while i > 1:
        logging.info("HELLO")
        i = i -1
    try:
        name = file.split('/')[1]
        destinationFactory = DestinationFactory()
        azureStorageHandler = destinationFactory.create_destination(DESTINATION)
        azureStorageHandler.upload(file)
        return {'status': 'SUCCESS', 'result': 'done',
                    'name':name,'path': name}
    except Exception as ex:
        try:
            logging.info(ex) 
            #self.retry(countdown=1)
        except MaxRetriesExceededError as ex:
            return {'status': 'FAIL', 'result': 'max retried achieved'}
