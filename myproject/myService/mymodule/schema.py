from pydantic import BaseModel

# 💡 HINT: 
#
#   Put your pydantic schemas here.
#   You can later use those schema in your `route.py` or `crud.py`


# book schema

class BookBase(BaseModel):
    title : str
    author : str
    synopsis : str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True
