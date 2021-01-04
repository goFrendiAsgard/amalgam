from typing import List
from fastapi import FastAPI, HTTPException
from mymodule import schema

import transport

# 💡 HINT: 
#
#   * If you need other components beside `app` and `mb`, please:
#       * Add them as parameter of `init` function
#       * Declare the component at `main.py`
#   * Whenever possible, don't put business logic here. Instead, try to:
#       * Invoke RPC call (i.e: `mb.call_rpc(rpc_name, *args)`) or
#       * Encapsulate your business logic into another class/function 
#         so that you can import it here
#   * Visit fastapi documentation at: https://fastapi.tiangolo.com/tutorial/first-steps/
#
#
# 📝 EXAMPLE:
#
#   import time
#
#   def init(app: FastAPI, mb: transport.MessageBus):
#
#       @app.get('/favorite-number')
#       def get_favorite_number():
#           # publish hit event to messagebus
#           hit_time = time.strftime('%Y-%m-%d %H:%M:%S')
#           mb.publish('hit', {'url': '/favorite-number', 'time': hit_time})
#           # return favorite number (ref: https://bigbangtheory.fandom.com/wiki/73)
#           num = mb.call_rpc('add', 70, 3)
#           return {'favorite_number': num}


def init(app: FastAPI, mb: transport.MessageBus):


    @app.get('/books/', response_model=List[schema.Book])
    def crud_list_book(skip: int = 0, limit: int = 100):
        db_book_list = mb.call_rpc('list_book', skip, limit)
        return [schema.Book.parse_obj(db_book) for db_book in db_book_list]

    @app.get('/books/{book_id}', response_model=schema.Book)
    def crud_get_book(book_id: int):
        db_book = mb.call_rpc('get_book', book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail='Book not found')
        return schema.Book.parse_obj(db_book)

    @app.post('/books/', response_model=schema.Book)
    def crud_create_book(book_data: schema.BookCreate):
        db_book = mb.call_rpc('create_book', book_data.dict())
        if db_book is None:
            raise HTTPException(status_code=404, detail='Book not found')
        return schema.Book.parse_obj(db_book)

    @app.put('/books/{book_id}', response_model=schema.Book)
    def crud_create_book(book_id: int, book_data: schema.BookCreate):
        db_book = mb.call_rpc('update_book', book_id, book_data.dict())
        if db_book is None:
            raise HTTPException(status_code=404, detail='Book not found')
        return schema.Book.parse_obj(db_book)

    @app.delete('/books/{book_id}', response_model=schema.Book)
    def crud_get_book(book_id: int):
        db_book = mb.call_rpc('delete_book', book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail='Book not found')
        return schema.Book.parse_obj(db_book)


    @app.get('/hello')
    def handle_route__hello():
        return 'response of /hello'

    print('Init {} route handlers'.format('mymodule'))
