from sqlmodel import create_engine,text
from sqlalchemy.ext.asyncio import AsyncEngine
from myapp.books.models import Book
from sqlmodel import SQLModel
from myapp.config import settings


engine = AsyncEngine(
    create_engine(
    url=settings.DATABASE_URL,
    echo=True 
))


async def init_db():
    async with engine.begin() as conn:

        await conn.run_sync(SQLModel.metadata.create_all)