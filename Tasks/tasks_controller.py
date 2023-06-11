#!/usr/bin/env python3
import json
import socket
import configparser
import asyncio
import signal
from typing import List
import aiohttp_cors
from aiohttp import web

from tasks_persistence import TasksPersistence
from tasks_model import SingletonCounter, Task

ONE_KB = 1024
SUCCESS = 0
FAILURE = 1

def is_port_busy(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def get_first_usable_port(st_port):
    test_port = st_port
    while is_port_busy(test_port):
        test_port += 1
    return test_port

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def sigterm_handler(signum, frame):
    asyncio.get_running_loop().stop()
    # services = client.agent.services()
    # for service_id in services:
    #     client.agent.service.deregister(service_id)
    # tasks_controller.message_persistence.is_running = False
    print("--- Message microservice is off")
    exit(SUCCESS)

def is_valid_json(my_json_string):
    try:
        json.loads(my_json_string)
        return True
    except ValueError:
        return False

class TasksController:
    def __init__(self, tasks_persistence):
        self.tasks_persistence = tasks_persistence
        self.json_data = None
    def handle_get(self) -> List[Task]:
        return tasks_persistence.retrieve_task_list()

    def handle_post(self):
        self.tasks_persistence.create_task(Task(self.json_data))

    def handle_patch(self):
        self.tasks_persistence.update_task(Task(self.json_data))

    def handle_delete(self):
        self.tasks_persistence.remove_task(self.json_data["_id"])

    async def handle_connection(self, request: web.Request):
        SingletonCounter().increment()
        user_id = request.query.get('user')
        if not user_id:
            return web.Response(text="User ID is missing")
        self.tasks_persistence.collection = self.tasks_persistence.db[user_id]
        response_str = ""
        if request.body_exists:
            self.json_data = await request.json()
        match request.method:
            case "GET":
                tasks_list = self.handle_get()
                tasks_dto = []
                for task in tasks_list:
                    json_data = json.dumps(task.obj_to_dto())
                    tasks_dto.append(json_data)
                response_str = f"[{','.join(tasks_dto)}]"
                print(f"[{SingletonCounter().get_count()}] got GET request -> retrieving tasks")
            case "POST":
                self.handle_post()
                print(f"[{SingletonCounter().get_count()}] got POST request -> creating task")
            case "PATCH":
                self.handle_patch()
                print(f"[{SingletonCounter().get_count()}] got PATCH request -> updating task")
            case "DELETE":
                self.handle_delete()
                print(f"[{SingletonCounter().get_count()}] got REMOVE request -> removing task")
            case _:
                raise ValueError("Unknown request type")
        response = web.Response(text=response_str)
        return response

    async def tell_health_status(self, request: web.Request):
        return web.Response()

    async def accept_connections(self, msg_microservice_port):
        # global consumer_thread
        app = web.Application()
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })
        app.router.add_get('/taskboard', self.handle_connection)
        app.router.add_post('/taskboard', self.handle_connection)
        app.router.add_patch('/taskboard', self.handle_connection)
        app.router.add_delete('/taskboard', self.handle_connection)
        app.router.add_get('/health', self.tell_health_status)
        for route in list(app.router.routes()):
            cors.add(route)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', msg_microservice_port)
        await site.start()
        print(f"--- Tasks microservice #{msg_microservice_port} is on")
        await asyncio.Event().wait()

if __name__ == '__main__':
    for signame in ('SIGINT', 'SIGTERM'):
        signal.signal(getattr(signal, signame), sigterm_handler)

    config = configparser.ConfigParser()
    config.read('../config.cfg')

    service_port = config.getint('MICROSERVICES_INFO', 'microservices_start_port')
    db_primary_port = config.getint('DB_INFO', 'db_primary_port')
    replica_set_name = config.get('DB_INFO', 'replica_set_name')

    tasks_persistence = TasksPersistence(db_primary_port, replica_set_name, "test_db", "test_collection")
    tasks_controller = TasksController(tasks_persistence)
    asyncio.run(tasks_controller.accept_connections(service_port))
