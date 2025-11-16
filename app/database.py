
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os

# Используем переменную окружения из Docker Compose
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://testfastapi2_user:Cir73SPb+@db:5432/testfastapi2_db"
)

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass