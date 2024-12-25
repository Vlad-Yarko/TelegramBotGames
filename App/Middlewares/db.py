from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Any, Awaitable, Callable, Dict


class CreateConnDB(BaseMiddleware):
    def __init__(self, main_session):
        self.main_session = main_session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        async with self.main_session() as session:
            data['session'] = session
            return await handler(event, data)
