from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from asyncpg import Connection, UniqueViolationError
from pydantic import EmailStr

from myapp.auth.utils import verify_password, create_access_token, create_refresh_token
from myapp.users.schemas import UserCreate, UserResponse, UserLogin, UserToken, UserAdmin
from myapp.users.crud import crud_create_user, crud_get_user_by_email, crud_make_user_admin
from myapp.auth.dependencies import access_token_bearer, refresh_token_bearer, get_conn, get_curr_user, RoleChecker
from myapp.db.redis_engine import add_jti_to_blocklist



auth_router = APIRouter()
admin_checker = RoleChecker(["admin"])



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
            access_token = create_access_token(user_details=UserToken(user_id=str(user["id"]),role=user["role"]))
            refresh_token = create_refresh_token(user_details=UserToken(user_id=str(user["id"]),role=user["role"]))

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

    new_access_token = create_access_token(user_details=UserToken(user_id=str(token_details["id"]), role=token_details["role"]))
    return {"new_access_token" : new_access_token}



@auth_router.post('/logout')
async def revoke_token(token_details = Depends(refresh_token_bearer)):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti=jti)

    return {"message" : "Logged Out Successfully"}



@auth_router.get('/me',response_model=UserResponse)
async def current_user(user = Depends(get_curr_user), admin : bool = Depends(admin_checker)):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not found")
    return user


@auth_router.post('/make_admin')
async def make_admin(new_user_email : UserAdmin, admin : bool = Depends(admin_checker), conn : Connection = Depends(get_conn)):
    result = await crud_make_user_admin(conn=conn , user_email=new_user_email.email)

    if result: 
        return {"message":f"Made user {new_user_email.email} as admin successfully"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {new_user_email.email} doesn't exist")