from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from App.Middlewares.data import Info
from aiogram.filters import StateFilter, Command

from random import choice

from App.Databases.connect import main_session
from App.Middlewares.db import CreateConnDB
from App.FSM.game_fsm import ActiveWords
from App.Handlers.choose_game_cmd import ChooseGameState
from App.Handlers.Words_Game.words_game_add import (
    letters,
    modes,
    guess_let,
    current_score,
    is_loose,
    starting,
    guess_w,
    command_score
)
from App.Filters.words_filters import Letter, Word

from App.Handlers.Words_Game.words_game_requests import orm_get_data_words

words_router_main = Router()
words_router_main.message.middleware(Info())


words_router = Router()
words_router.message.middleware(CreateConnDB(main_session))
words_router.message.middleware(Info())
words_router.message.filter(StateFilter(ActiveWords.active_game))


@words_router_main.message(StateFilter(ChooseGameState.StatisticWords), Command('start_game'))
async def start_words(message: Message, difficulty, game_name, state: FSMContext):
    await state.set_state(ActiveWords.active_game)
    await message.answer(f"""
You started {game_name} with {difficulty}-mode
To quit game /quit
To return to menu /menu
To see current score /score
""")
    user_words = await orm_get_data_words()
    word = choice(user_words)
    user_words.remove(word)
    await state.update_data(main_word=word, word=word, encrypted_word='^' * len(word), words=user_words,
                            wins=0, looses=0, round=0, remaining=len(word))
    await message.answer(f"""
The word is {'^' * len(word)}
You have {modes[difficulty]} attempt
""")
    await message.answer(f"Input one letter or entire word")


@words_router.message(Command('score'))
async def score(message: Message, state: FSMContext, difficulty):
    await command_score(message, state, difficulty)


@words_router.message(StateFilter(ActiveWords.active_game), Letter(letters))
async def guess_letter(message: Message, difficulty, state: FSMContext, session):
    if await guess_let(message, state, difficulty, session):
        await starting(message, state, difficulty)
    else:
        if await is_loose(message, state, difficulty, session):
            await starting(message, state, difficulty)
        else:
            await current_score(message, state, difficulty)


@words_router.message(Word(), StateFilter(ActiveWords.active_game))
async def guess_word(message: Message, state: FSMContext, difficulty, session):
    if await guess_w(message, state, difficulty, session):
        await starting(message, state, difficulty)
    else:
        if await is_loose(message, state, difficulty, session):
            await starting(message, state, difficulty)
        else:
            await current_score(message, state, difficulty)
