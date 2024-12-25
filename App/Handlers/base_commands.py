from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from App.Middlewares.db import CreateConnDB
from App.Databases.connect import main_session
from App.Databases.requests import (
    orm_start_bot,
    orm_all_statistics,
)

base_command_router = Router()
base_command_router.message.middleware(CreateConnDB(main_session))
base_command_router.message.filter(StateFilter(None))


@base_command_router.message(Command('start'))
async def start_command(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    await orm_start_bot(session, user_id, message.chat.id)
    await message.answer(f"""
Hello {message.from_user.username}, I'm glad to see you!
I have a lot of games that you can play with me!
""")


@base_command_router.message(Command('statistics'))
async def show_all_statistics(message: Message, session: AsyncSession):
    statistics = await orm_all_statistics(session, message.from_user.id)
    for game in statistics:
        await message.answer(f"""
For {game.name} you have overall {game.win} wins and {game.loose} loses

For easy-mode you have {game.win_easy} wins and {game.loose_easy} looses
For middle-mode you have {game.win_middle} wins and {game.loose_middle} looses
For hard-mode you have {game.win_hard} wins and {game.loose_hard} looses
""")


@base_command_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(f"""
To start bot /start
To see list of all commands /help
/admin is command only for admins of bot
To start game, first of all you must choose it /select
To see overall statistics of all games /statistics

When you choose game, you'll have more commands for game:
To see overall statistics of game you chose /statistics
To start game you chose /start_game
To choose difficulty for game you chose /difficulty
To see rules of chosen game /rules
To return to main menu /menu

When you'll start game, you'll have:
To quit game /quit
To return to main menu /menu
To see overall statistics of game you play /statistics
To see score of current round of chosen game /score
""")
