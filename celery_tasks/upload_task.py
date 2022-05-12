import logging
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from .app_worker import app
from azure.storage.blob import BlobServiceClient
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))



CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=eymax;AccountKey=lHstQLqp+88xbnfGh36Pfhoq21ekRHgfNZHkZ4AsGkuhF3DO9TcYsj0dV9T8S6VCocXuFpZZiL6++AStDpkI8g==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "max"
output_blob_name = "output_blob.csv"
blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob="testMe.xlsx")

# class PredictTask(Task):
#     def __init__(self):
#         super().__init__()
#         self.model = None

#     def __call__(self, *args, **kwargs):
#         if not self.model:
#             logging.info('Loading Model...')
#             self.model = YoloModel()
#             logging.info('Model loaded')
#         return self.run(*args, **kwargs)


@app.task(ignore_result=False, bind=True)
def upload_file(self, file):
    i = 110000
    while i > 1:
        logging.info("HELLO")
        i = i -1
    try:
        # data_pred = self.model.predict(data)
        # with open(file, "rb") as data:
        #     blob_client.upload_blob(data=data)
        name = file.split('/')[2]
        ## If file exists, delete it ##
        if os.path.isfile(file):
          os.remove(file)
        return {'status': 'SUCCESS', 'result': 'done',
                    'name':name,'path': name}
    except Exception as ex:
        try:
            logging.info(ex) 
            self.retry(countdown=1)
        except MaxRetriesExceededError as ex:
            return {'status': 'FAIL', 'result': 'max retried achieved'}


@app.task(ignore_result=False, bind=True)
def test_task(self):
    i = 110000
    while i > 1:
        logging.info("HELLO")
        i = i -1
    try:
        # data_pred = self.model.predict(data)
        # with open(file, "rb") as data:
        #     blob_client.upload_blob(data=data)
        # name = file.split('/')[2]
        # ## If file exists, delete it ##
        # if os.path.isfile(file):
        #   os.remove(file)
        return {'status': 'SUCCESS', 'result': 'done'}
    except Exception as ex:
        try:
            logging.info(ex) 
            self.retry(countdown=1)
        except MaxRetriesExceededError as ex:
            return {'status': 'FAIL', 'result': 'max retried achieved'}

