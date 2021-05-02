from fastapi import FastAPI
from sqlalchemy import create_engine
from helpers.transport import MessageBus, RMQMessageBus, RMQEventMap, LocalMessageBus
from myModule.controller import Controller as MyModuleController
from repos.dbBook import DBBookRepo


import os

def create_message_bus(mb_type: str) -> MessageBus:
    if mb_type == 'rmq':
        rmq_host = os.getenv('MY_SERVICE_RABBITMQ_HOST', 'localhost')
        rmq_user = os.getenv('MY_SERVICE_RABBITMQ_USER', 'root')
        rmq_pass = os.getenv('MY_SERVICE_RABBITMQ_PASS', 'toor')
        rmq_vhost = os.getenv('MY_SERVICE_RABBITMQ_VHOST', '/')
        rmq_event_map = RMQEventMap({})
        return RMQMessageBus(rmq_host, rmq_user, rmq_pass, rmq_vhost, rmq_event_map)
    return LocalMessageBus()

db_url = os.getenv('MY_SERVICE_SQLALCHEMY_DATABASE_URL', 'sqlite://')
mb_type = os.getenv('MY_SERVICE_MESSAGE_BUS_TYPE', 'local')
enable_route = os.getenv('MY_SERVICE_ENABLE_ROUTE_HANDLER', '1') != '0'
enable_event = os.getenv('MY_SERVICE_ENABLE_EVENT_HANDLER', '1') != '0'

engine = create_engine(db_url, echo=True)
app = FastAPI()
mb = create_message_bus(mb_type)

@app.on_event('shutdown')
def on_shutdown():
    mb.shutdown()

book_repo = DBBookRepo(engine=engine, create_all=True)
my_module_controller = MyModuleController(app=app, mb=mb, enable_route=enable_route, enable_event=enable_event, book_repo=book_repo)
my_module_controller.start()
