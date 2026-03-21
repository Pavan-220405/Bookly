from fastapi import APIRouter, HTTPException, Path, Depends, status
from asyncpg import Connection, UniqueViolationError

from myapp.users.schemas import UserCreate, UserResponse
from myapp.users.crud import crud_create_user
from myapp.db.engine import get_pool


async def get_conn():
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn 


auth_router = APIRouter()


@auth_router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def signup(new_user_data : UserCreate, conn : Connection = Depends(get_conn)):
    try:
        row =  await crud_create_user(conn, new_user_data)
        return row
    
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email {new_user_data.email} already exists. Try Login")