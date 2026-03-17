from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.mysql as my
from datetime import datetime
import uuid



class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title : str 
    author : str 
    publisher : str 
    published_date : str 
    page_count : int
    language : str 
    created_at : datetime = Field(Column(my.TIMESTAMP,default=datetime.now))
    updated_at : datetime = Field(Column(my.TIMESTAMP,default=datetime.now))

    def __repr__(self):
        return f"<Book {self.title}>"