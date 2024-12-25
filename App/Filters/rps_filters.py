from aiogram.filters import Filter
from aiogram.types import CallbackQuery


class RPSFilter(Filter):
    def __init__(self, bot_choice, user_choice):
        self.bot_choice = bot_choice
        self.user_choice = user_choice

    async def __call__(self, callback: CallbackQuery):
        return all([
            self.bot_choice == callback.data.split('_')[0],
            self.user_choice == callback.data.split('_')[1],
        ])


class RPSEq(Filter):
    def __init__(self):
        pass

    async def __call__(self, callback: CallbackQuery):
        bot_choice, user_choice = callback.data.split('_')
        return bot_choice == user_choice
