from typing import Mapping, List, Any
from fastapi import FastAPI, HTTPException
from helpers.transport import MessageBus
from repos.book import BookRepo
from myModule.handleBookRoute import handle_route as handle_book_route
from myModule.handleBookEvent import handle_event as handle_book_event

import traceback

class Controller():

    def __init__(self, app: FastAPI, mb: MessageBus, enable_route: bool, enable_event: bool, book_repo: BookRepo):
        self.app = app
        self.mb = mb
        self.enable_route = enable_route
        self.enable_event = enable_event
        self.book_repo = book_repo


    def start(self):
        if self.enable_event:
            handle_book_event(self.mb, self.book_repo)
            self.handle_event()
        if self.enable_route:
            handle_book_route(self.app, self.mb)
            self.handle_route()
    

    def handle_event(self):

        @self.mb.handle_rpc('myRPC')
        def handle_rpc_my_r_p_c(parameter: str) -> str:
            print('handle RPC call myRPC with parameter: {}'.format(parameter))
            return parameter


        @self.mb.handle_event('myEvent')
        def handle_event_my_event(message: Mapping[str, Any]):
            print('handle event myEvent with message: {}'.format(message))

        print('Handle events for myModule')
    

    def handle_route(self):

        @self.app.get('/hello')
        def get_hello():
            try:
                return 'OK'
            except HTTPException as error:
                raise error
            except Exception as error:
                print(traceback.format_exc()) 
                raise HTTPException(status_code=500, detail='Internal Server Error')

        print('Handle routes for myModule')


