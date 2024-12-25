from aiogram.filters import Filter
from aiogram.types import Message


class CorrectMess(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message):
        return message.text.isdigit()