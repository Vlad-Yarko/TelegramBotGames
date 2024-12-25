from aiogram import Router
from App.Middlewares.data import Info
from aiogram.filters import Command, StateFilter
from App.FSM.base_fsm import ChooseGameState
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from App.FSM.game_fsm import ActiveHeadTail
from App.Keyboards.Inline.coin_game_inline import coin_choice
from App.Filters.coin_filters import (
    FlipWin,
    FlipLoose,
    FlipBotWin,
    FlipUserWin
)
from App.Middlewares.db import CreateConnDB
from App.Databases.connect import main_session
from App.Handlers.Coin_Game.coin_game_add import (
    main_image,
    round_game,
    current_score,
    game,
    is_bot_win,
    is_user_win
)
from sqlalchemy.ext.asyncio import AsyncSession


coin_router_main = Router()
coin_router_main.message.middleware(Info())

coin_router = Router()
coin_router.callback_query.middleware(CreateConnDB(main_session))
coin_router.callback_query.middleware(Info())
coin_router.callback_query.filter(StateFilter(ActiveHeadTail.active_game))
coin_router.message.filter(StateFilter(ActiveHeadTail.active_game))


@coin_router_main.message(Command('start_game'), StateFilter(ChooseGameState.StatisticHeadTail))
async def start_game(message: Message, state: FSMContext, difficulty, game_name):
    await state.set_state(ActiveHeadTail.active_game)
    await message.answer(f"""
You started {game_name} with {difficulty}-mode
To quit game /quit
To return to menu /menu
""")
    await message.answer_photo(photo=main_image, caption=f"""
Bot flipped coin!
Head/Tail
""", reply_markup=coin_choice())
    await state.update_data(bot_wins=0, bot_looses=0, user_wins=0, user_looses=0)


@coin_router.message(Command('score'))
async def score(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"""
You have {data['user_wins']} wins and {data['user_looses']} looses
Bot has {data['bot_wins']} wins and {data['bot_looses']} looses
""")


@coin_router.callback_query(FlipWin())
async def all_win(callback: CallbackQuery, state: FSMContext):
    await round_game(callback)
    await callback.message.answer(f"Draw!")
    await current_score(callback, state)
    await game(callback)


@coin_router.callback_query(FlipLoose())
async def all_loose(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await round_game(callback)
    await callback.message.answer(f"Double loose!")
    await state.update_data(user_looses=data['user_looses'] + 1, bot_looses=data['bot_looses'] + 1)
    await current_score(callback, state)
    await game(callback)


@coin_router.callback_query(FlipUserWin())
async def user_win(callback: CallbackQuery, state: FSMContext, session: AsyncSession, difficulty):
    await round_game(callback)
    await callback.message.answer(f"Win!")
    data = await state.get_data()
    await state.update_data(user_wins=data['user_wins'] + 1, bot_looses=data['bot_looses'] + 1)
    res = await is_user_win(session, callback, state, difficulty)
    if res:
        await game(callback)
    else:
        await current_score(callback, state)
        await game(callback)


@coin_router.callback_query(FlipBotWin())
async def bot_win(callback: CallbackQuery, state: FSMContext, session: AsyncSession, difficulty):
    await round_game(callback)
    await callback.message.answer(f"Loose!")
    data = await state.get_data()
    await state.update_data(user_looses=data['user_looses'] + 1, bot_wins=data['bot_wins'] + 1)
    res = await is_bot_win(session, callback, state, difficulty)
    if res:
        await game(callback)
    else:
        await current_score(callback, state)
        await game(callback)
