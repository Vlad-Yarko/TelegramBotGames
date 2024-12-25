from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Any, Awaitable, Dict

from App.Databases.requests import orm_is_admin


class IsState(BaseMiddleware):
    def __init__(self, *states):
        self.states = states

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        if str(data['state']) in self.states:
            return await handler(event, data)


class IsAdmin(BaseMiddleware):
    def __init__(self, main_session):
        self.main_session = main_session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):

        async with self.main_session() as session:
            result = await orm_is_admin(session, event.from_user.id)
            if result:
                data['session'] = session
                return await handler(event, data)
