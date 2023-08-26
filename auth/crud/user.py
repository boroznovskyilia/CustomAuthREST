from typing import Any, Dict, Optional, Union
from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from crud.base import ModelType
from security import get_password_hash
from schemas.user import UserCreate,UserInDb,UserUpdate,User,SuperUserCreate
from models.models import User as user_table
from crud.base import CRUDBase
import security
from config import SUPER_USER_KEY

class CRUDUser(CRUDBase[user_table,UserCreate,UserUpdate,UserInDb]):
    async def create(self,db,user:UserCreate)->User:
        hashed_password = get_password_hash(user.password)
        db_obj = user_table(
            username=user.username,
            email = user.email,
            hashed_password=hashed_password,
            is_superuser = False,
        )
        await super().create(db,obj_in=db_obj)
        return user

    async def update(self,db,db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)
    
    async def authenticate_user(self,db:AsyncSession,username: str, password: str):
        get_user = await super().get(db,username)
        if not get_user:
            return False

        user = UserInDb(username=get_user.username,
            email=get_user.email,
            hashed_password=get_user.hashed_password,
            id = get_user.id,
            is_superuser = get_user.is_superuser)
        
        hashed_password = user.hashed_password
        if not security.verify_password(password, hashed_password):
            return False
        return user
    
    async def get_by_id(self,db:AsyncSession,id: int)->Optional[ModelType]:
       query = select(self.model).where(self.model.id == id)
       result = await db.scalar(query)
       return result
    
    async def create_super_user(self,db,user:SuperUserCreate):
        hashed_password = get_password_hash(user.password)
        db_obj = user_table(
            username=user.username,
            email = user.email,
            hashed_password=hashed_password,
            is_superuser = True)
        await super().create(db,obj_in=db_obj)

        return user
    
user = CRUDUser(user_table)