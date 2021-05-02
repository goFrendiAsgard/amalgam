from pydantic import BaseModel
import datetime

class BookData(BaseModel):
    title: str
    author: str
    synopsis: str


class Book(BookData):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        orm_mode = True
