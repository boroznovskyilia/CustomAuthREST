from typing import Optional
from sqlalchemy import Integer,String,Boolean,MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column,Mapped

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[Optional[int]] = mapped_column(Integer,primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String,nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String,nullable=False)
    is_superuser: Mapped[Optional[bool]] = mapped_column(Boolean,nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String,nullable=False)