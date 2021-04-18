from sqlalchemy.orm import Session
from mymodule import model, schema

# 💡 HINT: 
#
#   Put your CRUD related business logic here.



# List book
def list_book(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Book).offset(skip).limit(limit).all()


# Get book
def get_book(db: Session, book_id: int):
    return db.query(model.Book).filter(model.Book.id == book_id).first()


# Create book
def create_book(db: Session, book_data: schema.BookCreate):
    db_book = model.Book(title = book_data.title, author = book_data.author, synopsis = book_data.synopsis)
    if db_book is None:
        raise Error('Cannot create book')
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Update book
def update_book(db: Session, book_id: int, book_data: schema.BookUpdate):
    db_book = get_book(db, book_id)
    if db_book is None:
        return None
    db_book.title = book_data.title
    db_book.author = book_data.author
    db_book.synopsis = book_data.synopsis
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Delete book
def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return db_book

