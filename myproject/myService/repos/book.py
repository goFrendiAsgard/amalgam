from typing import List
from schemas.book import Book, BookData

import abc

class BookRepo(abc.ABC):

    @abc.abstractmethod
    def find_by_id(self, id: str) -> Book:
        pass

    @abc.abstractmethod
    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        pass

    @abc.abstractmethod
    def insert(self, book_data: BookData) -> Book:
        pass

    @abc.abstractmethod
    def update(self, id: str, book_data: BookData) -> Book:
        pass

    @abc.abstractmethod
    def delete(self, id: str) -> Book:
        pass