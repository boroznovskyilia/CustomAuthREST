from typing import AsyncGenerator
from db.database import async_session_maker
from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
from sqlalchemy.ext.asyncio import AsyncSession
from config import SECRET_KEY
from security import oauth2_scheme,ALGORITHM
from schemas.user import UserCreate,UserInDb,UserUpdate,User
from schemas.token import TokenData
from crud.user import user as user_table
from typing_extensions import Annotated
from cache import redis_db


async def get_db() -> AsyncGenerator:
    try:
        db = async_session_maker()
        yield db
    finally:
        await db.close()

async def get_current_user(*,db:AsyncSession = Depends(get_db),token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    id = int(id)
    user = await user_table.get_by_id(db,id=int(token_data.id))
    if user is None:
        raise credentials_exception
    if not redis_db.exists(id):
        raise HTTPException(status_code=400, detail="Inactive user")
    
    disabled = redis_db.hget(id,"disabled")

    if (disabled == "True"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_active_user(*,current_user: Annotated[UserInDb,Depends(get_current_user)]):
    return current_user

async def check_if_user_is_superuser(user:Annotated[UserInDb,Depends(get_current_active_user)]):
    
    if not user.is_superuser:
        raise HTTPException(status_code=401, detail="You have not enough priveleges") 
    return user 