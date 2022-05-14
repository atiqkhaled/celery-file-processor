from celery import Celery
import sys
sys.path.append("./celery_tasks")

BROKER_URI = 'amqp://rabbitmq'
BACKEND_URI = 'redis://redis'

app = Celery(
    'celery_tasks',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['upload_task','save_record_task']
)
