from typing import Annotated
from fastapi import Depends, HTTPException,APIRouter
from schemas.user import User
from utils import get_current_active_user,check_if_user_is_superuser
from crud.user import user as crud_user
from models.models import User as user_table
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db


router = APIRouter(
    tags = ["test"]
)

@router.post("/change")
async def change_superuser(*,db: AsyncSession = Depends(get_db),username:str,current_user: Annotated[User, Depends(check_if_user_is_superuser)]):
    get_user = await crud_user.get(db,username)
    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found") 
    super_user_condition =  not get_user.is_superuser
    query = update(user_table).where(user_table.id == get_user.id).values(is_superuser = super_user_condition)

    await db.execute(query)
    await db.commit()
    return {"status":f"now {username} disabled is {super_user_condition}"}
    