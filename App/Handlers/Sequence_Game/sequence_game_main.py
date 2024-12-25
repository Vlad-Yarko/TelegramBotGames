from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from random import choice

from sqlalchemy.ext.asyncio import AsyncSession

from App.Middlewares.data import Info
from App.Middlewares.db import CreateConnDB
from App.Databases.connect import main_session
from App.FSM.game_fsm import ActiveSequence
from App.Handlers.Sequence_Game.sequence_game_requests import orm_get_data_equations
from App.Handlers.Sequence_Game.sequence_game_add import (
    modes,
    current_score,
    is_win,
    is_loose,
    starting
)
from App.Filters.sequence_filters import CorrectMess
from App.FSM.base_fsm import ChooseGameState


sequence_router_main = Router()
sequence_router_main.message.middleware(Info())

sequence_router = Router()
sequence_router.message.middleware(Info())
sequence_router.message.middleware(CreateConnDB(main_session))
sequence_router.message.filter(StateFilter(ActiveSequence.active_game))


@sequence_router_main.message(Command('start_game'), StateFilter(ChooseGameState.StatisticSequence))
async def start_game(message: Message, state: FSMContext, game_name, difficulty):
    await state.set_state(ActiveSequence.active_game)
    await message.answer(f"""
You started {game_name} with {difficulty}-mode
To quit game /quit
To return to menu /menu
To see current score /score
""")
    user_equations = await orm_get_data_equations()
    equation = choice(user_equations)
    user_equations.remove(equation)
    sequence = '_'.join(equation.split('_')[:-1])
    missed_num = equation.split('_')[-1]
    await state.update_data(equations=user_equations, sequence=sequence,
                            missed_num=missed_num, equation=equation, round=0)
    await message.answer(f"""
The sequence is {sequence + '_&'}
You have {modes[difficulty]} attempts
""")


@sequence_router.message(Command('score'))
async def score(message: Message, state: FSMContext, difficulty):
    await current_score(message, state, difficulty)


@sequence_router.message(CorrectMess())
async def game(message: Message, state: FSMContext, difficulty, session: AsyncSession):
    data = await state.get_data()
    res = await is_win(message, session, state, difficulty)
    if res:
        await starting(message, state, difficulty)
    else:
        res = await is_loose(message, state, difficulty, session)
        if res:
            await starting(message, state, difficulty)
        else:
            await current_score(message, state, difficulty)
            await message.answer(f"The sequence is {data['sequence'] + '_&'}")
