from pydantic import BaseModel


class Task(BaseModel):
    task_id: str
    status: str
    name:str
    path:str


class Prediction(Task):
    task_id: str
    status: str
    result: str
