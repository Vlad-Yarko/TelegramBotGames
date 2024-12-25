from sqlalchemy import select

from App.Databases.connect import main_session
from App.Databases.models import DataSequence


async def orm_get_data_equations():
    async with main_session() as session:
        data = await session.execute(select(DataSequence.data))
        return data.scalars().all()
