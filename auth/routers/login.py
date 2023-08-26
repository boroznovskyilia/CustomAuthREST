from fastapi import Depends, HTTPException,status,APIRouter
from schemas.user import UserInDb
from security import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import timedelta
from crud.user import user as user_table
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db,get_current_active_user
from cache import redis_db

router = APIRouter()

@router.post("/login",tags=["user"])
async def login(*,db: AsyncSession = Depends(get_db),form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = await user_table.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    if(redis_db.exists(user.id)):
        redis_db.hset(user.id,mapping={"disabled":"False"})
    else:
        redis_db.hset(user.id,mapping={
            "token":access_token,
            "disabled":"False"
        })
        redis_db.expire(user.id,ACCESS_TOKEN_EXPIRE_MINUTES*60)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/logout",tags=["user"])
async def logout(current_user: Annotated[UserInDb, Depends(get_current_active_user)]):
    redis_db.hset(current_user.id,mapping={"disabled":"True"})
    return{f"{current_user.username} was logged out"}


    
   


