#!/usr/bin/env python3

import configparser
import time
import sys
import typing
import json
from bson.objectid import ObjectId
from tasks_model import SingletonCounter, Task
from pymongo import MongoClient
from typing import List

class TasksPersistence:
    def __init__(self, db_primary_port, rep_set_name, db_name, collection_name):
        self.messages = []
        replica_set_uri = f'mongodb://localhost:{db_primary_port}/?replicaSet={rep_set_name}'
        self.db_client = MongoClient(replica_set_uri)
        self.db = self.db_client[db_name]
        self.collection = None

    def create_task(self, task_obj: Task):
        self.collection.insert_one(task_obj.obj_to_dto())

    def update_task(self, task_obj: Task):
        query = {"_id": task_obj._id}
        update_data = {"$set": task_obj.obj_to_dto()}
        result = self.collection.update_one(query, update_data)
        if result.modified_count == 1:
            print(f"Successfully updated document with task_id: {task_obj._id}")
        else:
            print(f"No document found with task_id: {task_obj._id}")

    def remove_task(self, task_id: str):
        query = {"_id": task_id}
        result = self.collection.delete_one(query)
        if result.deleted_count == 1:
            print(f"Successfully removed document with task_id: {task_id}")
        else:
            print(f"No document found with task_id: {task_id}")

    def retrieve_task_list(self) -> List[Task]:
        tasks_list = []
        tasks_dto = self.collection.find()
        for task_dto in tasks_dto:
            tasks_list.append(Task(task_dto))
        return tasks_list

    def clear_db(self):
        if self.collection is not None:
            self.collection.delete_many({})

    def drop_db(self):
        if self.db is not None:
            self.db_client.drop_database(self.db.name)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../config.cfg')
    db_primary_port = config.getint('DB_INFO', 'db_primary_port')
    replica_set_name = config.get('DB_INFO', 'replica_set_name')

    req_str = """POST / HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "_id": "646b8703c3ec563b3a693d54",
    "title": "dawjdawjdwajkJohn Doe",
    "labels": 30,
    "description": "johndoe@example.com",
    "members_ids": "BIG BOSS",
    "checklists": 30,
    "due_date": "johndoe@example.com"
}
"""
    json_start_index = req_str.index("{")
    json_str = req_str[json_start_index:]
    json_data = json.loads(json_str)

    taskspers = TasksPersistence(db_primary_port, replica_set_name, "test_db", "test_collection")
    # taskspers.clear_db()
    # task_id = "646b8705c3ec563b3a693d5d"
    # taskspers.remove_task(task_id)
    # count = 0
    # while count < 10:
    task = Task(json_data)
    # taskspers.update_task(task)
    #     count += 1
    #     print(f'Elements added {count}')
    #     time.sleep(0.1)
    taskspers.retrieve_task_list()
    # taskspers.retrieve_task_list()

    # db = client['test_db']
    # collection = db['test_collection']
    # count = 0
    # while count < 50:
    #     document = {'name': 'John Doe', 'age': 30}
    #     result = collection.insert_one(document)
    #     time.sleep(1)
    #     count += 1
    #     print(f'Added {count} elements')
    taskspers.db_client.close()
