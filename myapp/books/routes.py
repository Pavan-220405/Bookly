from fastapi import APIRouter, Path,status, HTTPException, Query, Depends
from typing import Optional, List
from uuid import UUID
from asyncpg import UniqueViolationError

from myapp.books.schemas import BookCreate, BookResponse
from myapp.books.crud import crud_create_book,crud_delete_book,crud_get_books
from myapp.auth.dependencies import AccessTokenBearer, get_conn


book_router = APIRouter()
access_token_bearer = AccessTokenBearer()


# Get books
@book_router.get('/',response_model=List[BookResponse])
async def get_books(limit : int = Query(default=10,ge=1), offset : int = Query(default=0,ge=0),
                    title : Optional[str] = Query(default=None), author : Optional[str] = Query(default=None),
                    language : Optional[str] = Query(default=None), 
                    conn = Depends(get_conn), token_details = Depends(access_token_bearer)
                ):
    return await crud_get_books(conn=conn, limit=limit, offset=offset, title=title, author=author, language=language)



# Create a book
@book_router.post('/',response_model=BookResponse,status_code=status.HTTP_201_CREATED)
async def create_book(book : BookCreate, conn = Depends(get_conn),token_details = Depends(access_token_bearer)):
    try:
        return await crud_create_book(conn=conn, book=book)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists")

# Delete a book 
@book_router.delete('/{id}')
async def delete_book(id : UUID = Path(...,description="ID of the book to be deleted"), conn = Depends(get_conn),token_details = Depends(access_token_bearer)):
    result = await crud_delete_book(conn=conn, book_id=id)

    if result: 
        return {"message" : "Book deleted Successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book {id} doesn't exist")