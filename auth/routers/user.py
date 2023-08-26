from typing import List
from fastapi import Depends, HTTPException,APIRouter,status
from config import SUPER_USER_KEY
from crud.user import user as crud_user
from schemas.user import User,UserUpdate,User,UserCreate,UserInDb,SuperUserCreate
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_db
from utils import check_if_user_is_superuser,get_current_active_user

router = APIRouter(
    prefix="/user"
)

@router.post("/",response_model = User,tags=["user"])
async def create_user(*,db: AsyncSession = Depends(get_db),user:UserCreate):
    db_user = await crud_user.get(db,user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="This username has been already registered")
    return await crud_user.create(db,user)

@router.post("/super/",response_model = User,tags=["super_user"])
async def create_super_user(*,db: AsyncSession = Depends(get_db),user:SuperUserCreate):
    db_user = await crud_user.get(db,user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="This username has been already registered")
    if(user.super_user_secret_key == SUPER_USER_KEY):
        return await crud_user.create_super_user(db,user)
    else:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect superuser key",
        )

@router.get("/all/", response_model=List[User],tags=["super_user"])
async def read_users(*,db: AsyncSession = Depends(get_db),current_user:Annotated[UserInDb,Depends(check_if_user_is_superuser)],skip:int = 0):
    users = await crud_user.get_multi(db,skip)
    return users


@router.get("/", response_model=User,tags=["super_user"])
async def read_user(*,db: AsyncSession = Depends(get_db),username: str,current_user:Annotated[User,Depends(check_if_user_is_superuser)]):
    db_user = await crud_user.get(db,username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/me/",response_model=User,tags=["user"])
async def update_user(*,db: AsyncSession = Depends(get_db),user:UserUpdate,current_user: Annotated[User, Depends(get_current_active_user)]):
   
    get_is_this_username_exist = await crud_user.get(db,user.username)
    if(get_is_this_username_exist is None):
       pass
    else:
        if (get_is_this_username_exist.id != current_user.id):
            raise HTTPException(status_code=400, detail="This username has been already registered")
    
    await crud_user.update(db,current_user,user)
    return user
    

@router.delete("/",tags=["super_user"])
async def delete_user(*,db: AsyncSession = Depends(get_db),username:str,current_user:Annotated[User,Depends(check_if_user_is_superuser)]):
    is_user_exist = await crud_user.get(db,username)
    if is_user_exist is None:   
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete(db,is_user_exist.username)
    return {"status":f"user {is_user_exist.username} was deleted"}

@router.get("/me/",response_model=User,tags=["user"])
async def read_users_me(current_user: Annotated[UserInDb, Depends(get_current_active_user)]):
    return current_user
