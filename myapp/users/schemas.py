from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Literal
from uuid import UUID


class UserBase(BaseModel):
    user_name : Annotated[str,Field(description="User Name")]
    first_name : Annotated[str,Field(description="First name of the user")]
    last_name : Annotated[str,Field(description="Last name of the user")]
    email : Annotated[EmailStr,Field(description="Email of the user")]
    password : Annotated[str,Field(description="Password for protection",min_length=7)]

class UserCreate(UserBase):
    pass 


class UserResponse(BaseModel):
    id: UUID
    user_name: str
    first_name: str
    last_name: str
    email: EmailStr
    role : str 


class UserLogin(BaseModel):
    email : Annotated[EmailStr,Field(description="Email of the user")]
    password : Annotated[str,Field(description="Password for protection",min_length=7)]


class UserToken(BaseModel):
    user_id : Annotated[str,Field(description="ID of the user converted from uuid to str")] 
    role : Annotated[Literal["user","admin"],Field(description="Role of the current user : user/admin")]