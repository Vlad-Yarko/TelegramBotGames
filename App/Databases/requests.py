from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from App.Databases.models import (User,
                                  Game,
                                  StatisticRPS,
                                  StatisticWords,
                                  Admin,
                                  StatisticHeadTail,
                                  StatisticSequence,
                                  DataWords,
                                  DataSequence)


games = {
        'StatisticRPS': StatisticRPS,
        'StatisticWords': StatisticWords,
        'StatisticHeadTail': StatisticHeadTail,
        'StatisticSequence': StatisticSequence
    }

game_data = {
    'DataWords': DataWords,
    'DataSequence': DataSequence
}


async def orm_is_admin(session: AsyncSession, tg_id: int):
    data = await session.execute(select(Admin.tg_id).where(Admin.tg_id == tg_id))
    return data.scalar()


async def orm_start_bot(session: AsyncSession, tg_id: int, chat_id: int):
    data = await session.execute(select(User).where(User.tg_id == tg_id))
    if not data.scalar():
        await session.execute(insert(User).values(tg_id=tg_id, chat_id=chat_id))
    data = await session.execute(select(StatisticRPS).where(StatisticRPS.tg_id == tg_id))
    if not data.scalar():
        await session.execute(insert(StatisticRPS).values(tg_id=tg_id))
    data = await session.execute(select(StatisticWords).where(StatisticWords.tg_id == tg_id))
    if not data.scalar():
        await session.execute(insert(StatisticWords).values(tg_id=tg_id))
    data = await session.execute(select(StatisticHeadTail).where(StatisticHeadTail.tg_id == tg_id))
    if not data.scalar():
        await session.execute(insert(StatisticHeadTail).values(tg_id=tg_id))
    data = await session.execute(select(StatisticSequence).where(StatisticSequence.tg_id == tg_id))
    if not data.scalar():
        await session.execute(insert(StatisticSequence).values(tg_id=tg_id))
    await session.commit()


async def orm_all_statistics(session: AsyncSession, tg_id: int):
    data = await session.execute(select(StatisticRPS).where(StatisticRPS.tg_id == tg_id))
    rps = data.scalar()
    data = await session.execute(select(StatisticWords).where(StatisticWords.tg_id == tg_id))
    words = data.scalar()
    data = await session.execute(select(StatisticHeadTail).where(StatisticHeadTail.tg_id == tg_id))
    coin = data.scalar()
    data = await session.execute(select(StatisticSequence).where(StatisticSequence.tg_id == tg_id))
    sequence = data.scalar()
    return [rps, words, coin, sequence]


async def orm_all_games(session: AsyncSession):
    data = await session.execute(select(Game))
    return data.scalars()


async def orm_get_game_image(session: AsyncSession, game):
    data = await session.execute(select(Game.image).where(Game.callback_data == str(game)))
    return data.scalar()


async def orm_get_game_difficulty(session: AsyncSession, tg_id: int, game_d):
    game = games[game_d]
    data = await session.execute(select(game.difficulty).where(game.tg_id == tg_id))
    return data.scalar()


async def orm_statistics_one_game(session: AsyncSession, tg_id: int, game_d):
    game = games[game_d]
    data = await session.execute(select(game).where(game.tg_id == tg_id))
    return data.scalar()


async def orm_change_difficulty(session: AsyncSession, tg_id: int, game_d, difficulty: str):
    game = games[game_d]
    await session.execute(update(game).where(game.tg_id == tg_id).values(difficulty=difficulty))
    await session.commit()


async def orm_get_rules(session: AsyncSession, game: str):
    data = await session.execute(select(Game.rules).where(Game.callback_data == game))
    return data.scalar()


async def orm_win(session: AsyncSession, tg_id: int, game: str, difficulty: str):
    cls = games[game]
    data = await session.execute(select(cls).where(cls.tg_id == tg_id))
    user_data = data.scalar()
    res = 'win_' + difficulty
    column = {
        res: getattr(cls, res) + 1
    }
    await session.execute(update(cls).where(cls.tg_id == tg_id).values(
        win=user_data.win + 1,
        **column
    ))
    await session.commit()


async def orm_loose(session: AsyncSession, tg_id: int, game: str, difficulty: str):
    cls = games[game]
    data = await session.execute(select(cls).where(cls.tg_id == tg_id))
    user_data = data.scalar()
    res = 'loose_' + difficulty
    column = {
        res: getattr(cls, res) + 1
    }
    await session.execute(update(cls).where(cls.tg_id == tg_id).values(
        loose=user_data.loose + 1,
        **column
    ))
    await session.commit()


async def orm_get_user_chats(session: AsyncSession):
    data = await session.execute(select(User.chat_id))
    return data.scalars()


async def orm_add_data(session: AsyncSession, game_d, data):
    game = game_data[game_d]
    await session.execute(insert(game).values(data=data))
    await session.commit()
