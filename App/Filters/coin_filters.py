from aiogram.filters import Filter
from aiogram.types import CallbackQuery


class FlipWin(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        flip, bot_choice, user_choice = callback.data.split('_')
        return flip == user_choice and flip == bot_choice


class FlipLoose(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        flip, bot_choice, user_choice = callback.data.split('_')
        return flip != user_choice and flip != bot_choice


class FlipUserWin(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        flip, bot_choice, user_choice = callback.data.split('_')
        return flip == user_choice and flip != bot_choice


class FlipBotWin(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        flip, bot_choice, user_choice = callback.data.split('_')
        return flip != user_choice and flip == bot_choice
