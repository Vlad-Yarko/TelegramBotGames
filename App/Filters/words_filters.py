from aiogram.filters import Filter
from aiogram.types import Message


class Letter(Filter):
    def __init__(self, letters):
        self.letters = letters

    async def __call__(self, message: Message):
        return message.text.lower() in self.letters


class Word(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message):
        return len(message.text) in (4, 5, 6) and message.text.isalpha()