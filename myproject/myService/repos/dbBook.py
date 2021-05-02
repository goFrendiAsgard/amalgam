from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from schemas.book import Book, BookData
from repos.book import BookRepo

import uuid
import datetime

Base = declarative_base()

class DBBookEntity(Base):
    __tablename__ = "book"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(20), index=True)
    author = Column(String(20), index=True)
    synopsis = Column(String(20), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class DBBookRepo(BookRepo):

    def __init__(self, engine: Engine, create_all: bool):
        self.engine = engine
        if create_all:
            Base.metadata.create_all(bind=engine)


    def find_by_id(self, id: str) -> Book:
        db = Session(self.engine)
        result: Book
        try:
            db_result = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_result is None:
                return None
            result = Book.from_orm(db_result)
        finally:
            db.close()
        return result

    
    def find(self, keyword: str, limit: int, offset: int) -> List[Book]:
        db = Session(self.engine)
        results: List[Book] = []
        try:
            keyword = '%{}%'.format(keyword) if keyword != '' else '%'
            db_results = db.query(DBBookEntity).filter(DBBookEntity.title.like(keyword)).offset(offset).limit(limit).all()
            results = [Book.from_orm(db_result) for db_result in db_results]
        finally:
            db.close()
        return results

    
    def insert(self, book_data: BookData) -> Book:
        db = Session(self.engine)
        result: Book
        try:
            db_entity = DBBookEntity(
                id=str(uuid.uuid4()),
                title=book_data.title, 
                author=book_data.author, 
                synopsis=book_data.synopsis, 
                created_at=datetime.datetime.utcnow()
            )
            db.add(db_entity)
            db.commit()
            db.refresh(db_entity) 
            result = Book.from_orm(db_entity)
        finally:
            db.close()
        return result
    
    def update(self, id: str, book_data: BookData) -> Book:
        db = Session(self.engine)
        result: Book
        try:
            db_entity = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_entity is None:
                return None
            db_entity.title = book_data.title
            db_entity.author = book_data.author
            db_entity.synopsis = book_data.synopsis
            db_entity.updated_at = datetime.datetime.utcnow()
            db.add(db_entity)
            db.commit()
            db.refresh(db_entity) 
            result = Book.from_orm(db_entity)
        finally:
            db.close()
        return result

 
    def delete(self, id: str) -> Book:
        db = Session(self.engine)
        result: Book
        try:
            db_entity = db.query(DBBookEntity).filter(DBBookEntity.id == id).first()
            if db_entity is None:
                return None
            db.delete(db_entity)
            db.commit()
            result = Book.from_orm(db_entity)
        finally:
            db.close()
        return result

