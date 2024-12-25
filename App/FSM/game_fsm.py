from aiogram.fsm.state import StatesGroup, State


class ActiveWords(StatesGroup):
    active_game = State()


class ActiveRPS(StatesGroup):
    active_game = State()


class ActiveHeadTail(StatesGroup):
    active_game = State()


class ActiveSequence(StatesGroup):
    active_game = State()
