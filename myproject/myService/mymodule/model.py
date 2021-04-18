from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 💡 HINT: 
#
#   Put your SQL Alchemy models here.

Base = declarative_base()



# book model
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    synopsis = Column(String)

