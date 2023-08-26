from typing import Annotated, Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Base
from sqlalchemy import delete,select


ModelType = TypeVar("ModelType",bound = Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DBSchemaType = TypeVar("DBSchemaType",bound = BaseModel)
UserInDb = TypeVar("UserInDb",bound = BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType,DBSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self,db:AsyncSession,username: str)->Optional[ModelType]:
       query = select(self.model).where(self.model.username == username)
       result = await db.scalar(query)
       return result

    async def get_multi(self,db:AsyncSession,skip:int)->List[ModelType]:
        query = select(self.model).offset(skip).limit(100)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self,db:AsyncSession,obj_in:CreateSchemaType)-> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db:AsyncSession,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:

        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self,db:AsyncSession,username: str):
        query = delete(self.model).where(self.model.username == username)
        await db.execute(query)
        await db.commit()
        return {"status":f"user {username} was deleted"}