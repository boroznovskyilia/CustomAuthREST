from sqlalchemy.ext.asyncio import  create_async_engine,AsyncSession
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False,autoflush=False)

