from fastapi import APIRouter, Path,status, HTTPException
from typing import List
from myapp.books.book_data import books
from myapp.books.schemas import Book, BookUpdate



book_router = APIRouter()


@book_router.get('/',response_model=List[Book])
async def get_all_books():
    return books



@book_router.post('/',status_code=status.HTTP_201_CREATED)
async def create_book(book_data : Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)

    return new_book



@book_router.get('/{book_id}',response_model=Book)
async def get_book(book_id : int = Path(gt=0)) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book  

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book {book_id} doesn't exist")



@book_router.patch('/{book_id}')
async def update_book(book_update_data : BookUpdate, book_id : int = Path(gt=0,title="ID of the book to get")):
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            book['author'] = book_update_data.author

            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book {book_id} doesn't exist")



@book_router.delete('/{book_id}')
async def delete_book(book_id : int = Path(gt=0)) -> dict:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return {"message" : f"Book {book_id} has been successfully deleted"}  

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book {book_id} doesn't exist")