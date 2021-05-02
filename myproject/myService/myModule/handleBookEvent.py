from typing import Any, List, Mapping
from helpers.transport import MessageBus
from schemas.book import Book, BookData
from repos.book import BookRepo

def handle_event(mb: MessageBus, book_repo: BookRepo):

    @mb.handle_rpc('find_book')
    def find_book(keyword: str, limit: int, offset: int) -> List[Mapping[str, Any]]:
        results = book_repo.find(keyword, limit, offset)
        return [result.dict() for result in results]


    @mb.handle_rpc('find_book_by_id')
    def find_book_by_id(id: str) -> Mapping[str, Any]:
        result = book_repo.find_by_id(id)
        if result is None:
            return None
        return result.dict()


    @mb.handle_rpc('insert_book')
    def insert_book(data: Mapping[str, Any]) -> Mapping[str, Any]:
        result = book_repo.insert(BookData.parse_obj(data))
        if result is None:
            return None
        return result.dict()


    @mb.handle_rpc('update_book')
    def update_book(id: str, data: Mapping[str, Any]) -> Mapping[str, Any]:
        result = book_repo.update(id, BookData.parse_obj(data))
        if result is None:
            return None
        return result.dict()


    @mb.handle_rpc('delete_book')
    def delete_book(id: str) -> Mapping[str, Any]:
        result = book_repo.delete(id)
        if result is None:
            return None
        return result.dict()
    

    print('Handle event for book')

