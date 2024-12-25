from aiogram.filters import Filter
from aiogram.types import CallbackQuery, TelegramObject
from aiogram.fsm.context import FSMContext


class CallDataIn(Filter):
    def __init__(self, *words):
        self.words = words

    async def __call__(self, callback: CallbackQuery):
        return callback.data in self.words


class CallDataEq(Filter):
    def __init__(self, callback):
        self.callback = callback

    async def __call__(self, callback: CallbackQuery):
        return self.callback == callback.data


class IsState(Filter):
    def __init__(self, *states):
        self.states = states

    async def __call__(self, obj: TelegramObject, state: FSMContext):
        current_state = await state.get_state()
        return current_state in self.states
