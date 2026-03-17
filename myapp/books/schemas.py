from pydantic import BaseModel,Field
from typing import Annotated

class Book(BaseModel):
    id : Annotated[int,Field(description="ID of the book",ge=1)]
    title : str 
    author : str 
    publisher : str 
    published_date : str 
    page_count : Annotated[int,Field(description="Number of pages in the book",ge=1)] 
    language : str 

class BookUpdate(BaseModel):
    title : str 
    author : str 
    publisher : str  
    page_count : int 
    language : str 