from fastapi import APIRouter, Path,status, HTTPException, Query, Depends
from typing import Optional
from myapp.books.schemas import BookCreate
from myapp.books.crud import create_book, delete_book, get_books
from myapp.db.engine import get_pool


book_router = APIRouter()


# Dependency function
async def get_conn():
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn  



# Get books
@book_router.get('/')
async def GetBooks(limit : int = Query(default=10,ge=1), offset : int = Query(default=0,ge=0),
                    title : Optional[str] = Query(default=None), author : Optional[str] = Query(default=None),
                    language : Optional[str] = Query(default=None), conn = Depends(get_conn)
                ):
    return await get_books(conn=conn, limit=limit, offset=offset, title=title, author=author, language=language) 



# Create a book
@book_router.post('/')
async def CreateBook(book : BookCreate, conn = Depends(get_conn)):
    return await create_book(conn=conn, book=book)


# Delete a book 
@book_router.delete('/{id}')
async def DeleteBook(id : int = Path(...,description="ID of the book to be deleted"), conn = Depends(get_conn)):
    result = await delete_book(conn=conn, book_id=id)

    if result: 
        return {"message" : "Book deleted Successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book {id} doesn't exist")