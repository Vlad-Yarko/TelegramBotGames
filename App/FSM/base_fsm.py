from aiogram.fsm.state import StatesGroup, State


class ChooseGameState(StatesGroup):
    game = State()
    difficulty = State()

    StatisticRPS = State()
    StatisticWords = State()
    StatisticHeadTail = State()
    StatisticSequence = State()


class Admin(StatesGroup):
    active = State()
    photo = State()
    send_message = State()
    send_photo = State()
    send_text = State()
    edit_games = State()

    add_words = State()
    add_equations = State()
