from asyncpg import Connection
import asyncpg
from fastapi import APIRouter, HTTPException, status, Depends

from myapp.auth.dependencies import get_conn
from myapp.auth.dependencies import access_token_bearer
from myapp.reviews.crud import crud_write_review
from myapp.reviews.schemas import Review, ReviewCRUD


review_router = APIRouter()


@review_router.post('/add_review',status_code=status.HTTP_201_CREATED)
async def add_review(review_details : Review, token_details : dict = Depends(access_token_bearer), conn : Connection = Depends(get_conn)):
    review_crud = ReviewCRUD(**review_details.model_dump(),user_id=token_details["id"])
    try: 
        row = await crud_write_review(review=review_crud,conn=conn)
        return row
    except asyncpg.ForeignKeyViolationError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You have already reviewed this book")
    except asyncpg.PostgresError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database Error")