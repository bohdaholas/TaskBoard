import json
from bson.objectid import ObjectId

class SingletonCounter:
    _instance = None
    _count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def increment(self):
        self._count += 1

    def decrement(self):
        self._count -= 1

    def get_count(self):
        return self._count

class Task:
    def __init__(self, task_json):
        self.dto_to_obj(task_json)

    def dto_to_obj(self, task_json):
        if "_id" not in task_json:
            self._id = str(ObjectId())
        else:
            self._id = task_json["_id"]
        self.title = task_json["title"]
        self.description = task_json["description"]
        self.due_date = task_json["due_date"]

    def obj_to_dto(self) -> dict:
        dto = {
            "_id": self._id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date
        }
        return dto

