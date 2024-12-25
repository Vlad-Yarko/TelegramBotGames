import os

from App.Databases.models import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(url=os.getenv('DB'), echo=True)

main_session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def engine_begin():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
