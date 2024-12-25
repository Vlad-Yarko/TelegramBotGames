from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from App.Handlers.choose_game_cmd import ChooseGameState
from App.FSM.game_fsm import ActiveRPS
from App.Keyboards.Inline.rps_game_inline import rps_choice
from App.Middlewares.data import Info
from App.Middlewares.db import CreateConnDB
from App.Databases.connect import main_session
from App.Filters.rps_filters import RPSFilter, RPSEq
from App.Handlers.RPS_Game.rps_game_add import (
    main_image,
    game,
    choice,
    user_win,
    user_loose,
    user_draw
)

r_p_s_router_main = Router()
r_p_s_router_main.message.middleware(Info())


r_p_s_router = Router()
r_p_s_router.callback_query.middleware(CreateConnDB(main_session))
r_p_s_router.callback_query.middleware(Info())
r_p_s_router.callback_query.filter(StateFilter(ActiveRPS.active_game))
r_p_s_router.message.filter(StateFilter(ActiveRPS.active_game))


@r_p_s_router_main.message(Command('start_game'), StateFilter(ChooseGameState.StatisticRPS))
async def start_r_p_s(message: Message, state: FSMContext, difficulty, game_name):
    await state.set_state(ActiveRPS.active_game)
    await message.answer(f"""
You started {game_name} with {difficulty}-mode
To quit game /quit
To return to menu /menu
""")
    await message.answer_photo(photo=main_image,
                               caption="""
Choose rock/scissors/paper                               
""", reply_markup=rps_choice())
    await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)


@r_p_s_router.message(Command('score'))
async def score(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"""
You have {data['user_wins']} wins and {data['user_looses']} looses
Bot has {data['bot_wins']} wins and {data['bot_looses']} looses
""")


@r_p_s_router.callback_query(RPSEq())
async def draw(callback: CallbackQuery, state: FSMContext):
    await game(callback)
    await user_draw(callback, state)
    await choice(callback)


@r_p_s_router.callback_query(RPSFilter('paper', 'rock'))
@r_p_s_router.callback_query(RPSFilter('rock', 'scissors'))
@r_p_s_router.callback_query(RPSFilter('scissors', 'paper'))
async def s_p(callback: CallbackQuery, state: FSMContext, session: AsyncSession, difficulty):
    await game(callback)
    await user_loose(callback, difficulty, session, state)
    await choice(callback)


@r_p_s_router.callback_query(RPSFilter('rock', 'paper'))
@r_p_s_router.callback_query(RPSFilter('scissors', 'rock'))
@r_p_s_router.callback_query(RPSFilter('paper', 'scissors'))
async def p_s(callback: CallbackQuery, state: FSMContext, session: AsyncSession, difficulty):
    await game(callback)
    await user_win(callback, difficulty, session, state)
    await choice(callback)
