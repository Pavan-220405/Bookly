from fastapi import FastAPI, Path, Query
from typing import Optional,Annotated
from pydantic import BaseModel


app = FastAPI(title="Bookly APP")

class CreateBook(BaseModel):
    title : Annotated[str,"Title of the book"]
    author : Annotated[Optional[str],"Author of the book"] = None


# Health Checkup
@app.get('/')
async def health():
    return {"message" : "Status Running"}


# Greet a person using path and query parameters
@app.get('/greet/{user_name}')
async def greet(user_name : str = Path(...,example="Joe"), age : int = Query(default=18,ge=18,example=18)):
    return {"greetings" : f"Hello {user_name}, Welcome to Bookly !!",
            "age" : age}


# A Post method
@app.post('/create_book')
async def create_book(book_data : CreateBook):
    return {
        "title" : book_data.title,
        "author" : book_data.author
    }