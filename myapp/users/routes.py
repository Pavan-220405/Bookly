from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.responses import JSONResponse
from asyncpg import Connection, UniqueViolationError

from myapp.auth.utils import verify_password, create_access_token, create_refresh_token
from myapp.users.schemas import UserCreate, UserResponse, UserLogin
from myapp.users.crud import crud_create_user, crud_get_user_by_email
from myapp.db.engine import get_pool
from myapp.auth.dependencies import RefreshTokenBearer
from myapp.db.redis_engine import add_jti_to_blocklist


async def get_conn():
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn 


auth_router = APIRouter()
refresh_token_bearer = RefreshTokenBearer()


@auth_router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def signup(new_user_data : UserCreate, conn : Connection = Depends(get_conn)):
    try:
        row =  await crud_create_user(conn, new_user_data)
        return row
    
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email {new_user_data.email} already exists. Try Login")
    

@auth_router.post('/login')
async def login(user_data : UserLogin, conn : Connection = Depends(get_conn)):
    user = await crud_get_user_by_email(conn=conn,email=user_data.email)

    if user:
        password_valid = verify_password(user_data.password, user["hashed_password"])

        if password_valid:
            access_token = create_access_token(user_id=str(user["id"]))
            refresh_token = create_refresh_token(user_id=str(user["id"]))

            return JSONResponse(
                content={
                        "message" : "Login Successful",
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                        "user" : {
                            "email" : user["email"],
                            "id" : str(user["id"])
                        }           
            })
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Email or Password")


@auth_router.post('/refresh_token')
async def new_access_token(token_details = Depends(refresh_token_bearer)):

    new_access_token = create_access_token(user_id=token_details["sub"])
    return {"new_access_token" : new_access_token}



@auth_router.post('/logout')
async def revoke_token(token_details = Depends(refresh_token_bearer)):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti=jti)

    return {"message" : "Logged Out Successfully"}
