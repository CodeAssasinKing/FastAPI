from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models.defaults import Base
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
DB_NAME = os.getenv("POSTGRES_DB", "app_db")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_NAME}"

engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def get_session():
    async with async_session() as session:
        yield session



