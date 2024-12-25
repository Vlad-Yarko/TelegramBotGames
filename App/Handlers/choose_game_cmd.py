from aiogram.filters import Command, StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router

from sqlalchemy.ext.asyncio import AsyncSession

from App.Keyboards.Inline.base_inline import choose_all_games, diff
from App.FSM.base_fsm import ChooseGameState
from App.Filters.all_filters import CallDataIn, IsState
from App.Middlewares.db import CreateConnDB
from App.Databases.connect import main_session
from App.Databases.requests import (
    orm_statistics_one_game,
    orm_get_game_difficulty,
    orm_change_difficulty,
    orm_get_game_image
)
from App.Databases.requests import orm_all_games, orm_get_rules


choose_router_main = Router()
choose_router_main.message.middleware(CreateConnDB(main_session))
choose_router_main.callback_query.middleware(CreateConnDB(main_session))

states = ('ChooseGameState:StatisticRPS',
          'ChooseGameState:StatisticWords',
          'ChooseGameState:StatisticHeadTail',
          'ChooseGameState:StatisticSequence')

active_states = (
    'ActiveRPS:active_game',
    'ActiveWords:active_game',
    'ActiveHeadTail:active_game',
    'ActiveSequence:active_game'
)


choose_router_add = Router()
choose_router_add.message.middleware(CreateConnDB(main_session))
choose_router_add.callback_query.middleware(CreateConnDB(main_session))
choose_router_add.message.filter(IsState(*states))


@choose_router_main.message(Command('select'), or_f(StateFilter(None), StateFilter(ChooseGameState)))
async def choose_game(message: Message, session: AsyncSession, state: FSMContext):
    await message.answer(f'Here are all games that we have:',
                         reply_markup=choose_all_games(await orm_all_games(session)))
    await state.set_state(ChooseGameState.game)


@choose_router_main.callback_query(StateFilter(ChooseGameState.game))
async def chose_game(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    game_d, game_name = callback.data.split('_')
    game_photo = await orm_get_game_image(session, callback.data)
    difficulty = await orm_get_game_difficulty(session, callback.from_user.id, game_d)
    await state.update_data(game=game_d,
                            difficulty=difficulty,
                            game_name=game_name)
    await callback.message.answer_photo(photo=game_photo, caption=f"""
You chose game {game_name}
Current mode is {difficulty}
/start_game
""")
    await callback.answer(game_name)
    await state.set_state(f'ChooseGameState:{game_d}')


@choose_router_main.message(Command('menu'), ~StateFilter(None))
async def menu_choose(message: Message, state: FSMContext):
    await message.answer('You returned to menu')
    await state.clear()


@choose_router_add.message(Command('statistics'))
async def stat_chosen_game(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    game_d = data['game']
    game = await orm_statistics_one_game(session, message.from_user.id, game_d)
    await message.answer(f"""
For {game.name} you have overall {game.win} wins and {game.loose} loses

For easy-mode you have {game.win_easy} wins and {game.loose_easy} looses
For middle-mode you have {game.win_middle} wins and {game.loose_middle} looses
For hard-mode you have {game.win_hard} wins and {game.loose_hard} looses
""")


@choose_router_main.message(Command('statistics'), or_f(IsState(*states), IsState(*active_states)))
async def stat_chosen_game(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    game_d = data['game']
    game = await orm_statistics_one_game(session, message.from_user.id, game_d)
    await message.answer(f"""
For {game.name} you have overall {game.win} wins and {game.loose} loses

For easy-mode you have {game.win_easy} wins and {game.loose_easy} looses
For middle-mode you have {game.win_middle} wins and {game.loose_middle} looses
For hard-mode you have {game.win_hard} wins and {game.loose_hard} looses
""")


@choose_router_add.message(Command('difficulty'))
async def difficulty_game(message: Message, state: FSMContext):
    await state.set_state(ChooseGameState.difficulty)
    await message.answer('Choose your difficulty', reply_markup=diff)


@choose_router_add.callback_query(CallDataIn('easy', 'middle', 'hard'))
async def chosen_difficulty(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.message.delete()
    difficulty = callback.data
    await state.update_data(difficulty=difficulty)
    data = await state.get_data()
    await orm_change_difficulty(session, callback.from_user.id, data['game'], data['difficulty'])
    await callback.message.answer(f'You chose {data['difficulty']} mode for {data['game_name']}')
    await state.set_state(f'ChooseGameState:{data['game']}')
    await callback.answer()


@choose_router_add.message(Command('rules'))
async def rules_rps(message: Message, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    query = data['game'] + '_' + data['game_name']
    rules = await orm_get_rules(session, query)
    await message.answer(rules)


@choose_router_main.message(Command('quit'), IsState(*active_states))
async def quit_game(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(f"ChooseGameState:{data['game']}")
    await message.answer("You quit the game and returned to choose menu")
