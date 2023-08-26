from typing import Union
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str  = Field(min_length = 3)
    email:EmailStr
    

class UserCreate(BaseModel):
    username: str  = Field(min_length = 3)
    email:EmailStr
    password:str = Field(min_length=4)
    class Config:
        from_attributes = True

class SuperUserCreate(UserCreate):
    super_user_secret_key:str

class User(UserBase):
    class Config:
        from_attributes = True

class UserUpdate(UserCreate):
    pass

class UserLogin(User):
    hashed_password:str = Field(min_length=4)
    disabled:Union[bool,None] = None

class UserInDb(User):
    id: int  = Field(ge = 1)
    hashed_password:str = Field(min_length=4)
    is_superuser: Union[bool, None] = False