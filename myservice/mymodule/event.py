from typing import Any, List, Mapping
from sqlalchemy.orm import sessionmaker, Session
from mymodule import schema, crud

import database, transport

# 💡 HINT: 
#
#   * If you need other components beside `mb` and `DBSession`, please:
#       * Add them as parameter of `init` function
#       * Declare the component at `main.py`
#   * Whenever possible, don't put business logic here. Instead, try to:
#     Encapsulate your business logic into another class/function 
#     so that you can import it here
#   * Make sure every event/rpc handler only receive or return:
#       * Primitive data types (str, int, float, boolean)
#       * List
#       * Dictionary
#     List and dictionary can be nested but cannot contain custom object
#     This is necessary because RMQMessageBus will serialize your data into JSON Object
#   * If you really need to pass non primitive object (e.g: DBSession),
#     please inject them by using decorator (see the example below)
#
#
# 📝 EXAMPLE:
#
#   def init(mb: transport.MessageBus, DBSession: sessionmaker):
#
#       @transport.handle('hit')
#       def handle_hit_event(msg: Mapping[str, Any]):
#           print('Receiving message: ', msg)
#
#       @transport.handle_rpc('add')
#       def handle_add_rpc(num1: int, num2: int):
#           return num1 + num2
#
#       @transport.handle('loggedHit')
#       @database.handle(DBSession)
#       def handle_logged_hit(db: Session, msg: Mapping[str, Any]):
#           # log_to_db(db, msg) 
#           print('Receiving message: ', msg)
#           


def init(mb: transport.MessageBus, DBSession: sessionmaker):


    @transport.handle_rpc(mb, 'list_book')
    @database.handle(DBSession)
    def crud_rpc_list_book(db: Session, skip: int = 0, limit: int = 100) -> List[Mapping[str, Any]]:
        db_book_list = crud.list_book(db, skip = skip, limit = limit)
        return [schema.Book.from_orm(db_book).dict() for db_book in db_book_list]

    @transport.handle_rpc(mb, 'get_book')
    @database.handle(DBSession)
    def crud_rpc_get_book(db: Session, book_id: int) -> Mapping[str, Any]:
        db_book = crud.get_book(db, book_id = book_id)
        if db_book is None:
            return None
        return schema.Book.from_orm(db_book).dict()

    @transport.handle_rpc(mb, 'create_book')
    @database.handle(DBSession)
    def crud_rpc_create_book(db: Session, book_dict: Mapping[str, Any]) -> Mapping[str, Any]:
        db_book = crud.create_book(db, book_data = schema.BookCreate.parse_obj(book_dict))
        if db_book is None:
            return None
        return schema.Book.from_orm(db_book).dict()

    @transport.handle_rpc(mb, 'update_book')
    @database.handle(DBSession)
    def crud_rpc_update_book(db: Session, book_id: int, book_dict: Mapping[str, Any]) -> Mapping[str, Any]:
        db_book = crud.update_book(db, book_id = book_id, book_data = schema.BookUpdate.parse_obj(book_dict))
        if db_book is None:
            return None
        return schema.Book.from_orm(db_book).dict()

    @transport.handle_rpc(mb, 'delete_book')
    @database.handle(DBSession)
    def crud_rpc_delete_book(db: Session, book_id: int) -> Mapping[str, Any]:
        db_book = crud.delete_book(db, book_id = book_id)
        if db_book is None:
            return None
        return schema.Book.from_orm(db_book).dict()


    @transport.handle_rpc(mb, 'myRPC')
    def handle_rpc_myrpc(msg: Any) -> Any:
        print('Getting message from myRPC', msg)
        return 'ok'


    @transport.handle(mb, 'myEvent')
    def handle_event_myevent(msg: Any):
        print('Getting message from myEvent', msg)

    print('Init {} event/rpc handlers'.format('mymodule'))