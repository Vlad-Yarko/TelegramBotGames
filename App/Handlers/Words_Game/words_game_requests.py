from sqlalchemy import select

from App.Databases.connect import main_session
from App.Databases.models import DataWords


async def orm_get_data_words():
    async with main_session() as session:
        data = await session.execute(select(DataWords.data))
        return data.scalars().all()
