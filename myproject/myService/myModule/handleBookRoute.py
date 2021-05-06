from typing import Any, List, Mapping
from helpers.transport import MessageBus
from fastapi import FastAPI, HTTPException
from schemas.book import Book, BookData

import traceback

def handle_route(app: FastAPI, mb: MessageBus):

    @app.get('/book/', response_model=List[Book])
    def find_book(keyword: str='', limit: int=100, offset: int=0):
        try:
            results = mb.call_rpc('find_book', keyword, limit, offset)
            return [Book.parse_obj(result) for result in results]
        except HTTPException as error:
            raise error
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')


    @app.get('/book/{id}', response_model=Book)
    def find_book_by_id(id: str):
        try:
            result = mb.call_rpc('find_book_by_id', id)
            if result is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(result)
        except HTTPException as error:
            raise error
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')


    @app.post('/book/', response_model=Book)
    def insert_book(data: BookData):
        try:
            result = mb.call_rpc('insert_book', data.dict())
            if result is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(result)
        except HTTPException as error:
            raise error
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')


    @app.put('/book/{id}', response_model=Book)
    def update_book(id: str, data: BookData):
        try:
            result = mb.call_rpc('update_book', id, data.dict())
            if result is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(result)
        except HTTPException as error:
            raise error
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')


    @app.delete('/book/{id}')
    def delete_book(id: str):
        try:
            result = mb.call_rpc('delete_book', id)
            if result is None:
                raise HTTPException(status_code=404, detail='Not Found')
            return Book.parse_obj(result)
        except HTTPException as error:
            raise error
        except Exception as error:
            print(traceback.format_exc()) 
            raise HTTPException(status_code=500, detail='Internal Server Error')


    print('Handle route for book')
