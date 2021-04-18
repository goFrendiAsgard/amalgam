from typing import Mapping
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import transport
import mymodule

# Handle app shutdown event
def handle_shutdown(app: FastAPI, mb: transport.MessageBus):
    @app.on_event('shutdown')
    def on_shutdown():
        mb.shutdown()

# init application component
config: Mapping[str, str] = {
    'message_bus_type': os.getenv('MY_SERVICE_MESSAGE_BUS_TYPE', 'local'),
    'rabbitmq_host' : os.getenv('MY_SERVICE_RABBITMQ_HOST', 'localhost'),
    'rabbitmq_user' : os.getenv('MY_SERVICE_RABBITMQ_USER', 'root'),
    'rabbitmq_pass' : os.getenv('MY_SERVICE_RABBITMQ_PASS', 'toor'),
    'rabbitmq_vhost' : os.getenv('MY_SERVICE_RABBITMQ_VHOST', '/'),
    'sqlalchemy_database_url': os.getenv('MY_SERVICE_SQLALCHEMY_DATABASE_URL', 'sqlite:///./database.db'),
    'enable_route_handler': os.getenv('MY_SERVICE_ENABLE_ROUTE_HANDLER', '1'),
    'enable_event_handler': os.getenv('MY_SERVICE_ENABLE_EVENT_HANDLER', '1'),
}
enable_route_handler: bool = config.get('enable_route_handler') != '0'
enable_event_handler: bool = config.get('enable_event_handler') != '0'
app = FastAPI()
mb: transport.MessageBus = transport.init_mb(config)
engine = create_engine(
    config.get('sqlalchemy_database_url', 'sqlite:///./database.db'),
    connect_args={'check_same_thread': False}
)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
handle_shutdown(app, mb)


# init mymodule
mymodule.model.Base.metadata.create_all(bind=engine)
if enable_event_handler:
    mymodule.event.init(mb, DBSession)
if enable_route_handler:
    mymodule.route.init(app, mb)

