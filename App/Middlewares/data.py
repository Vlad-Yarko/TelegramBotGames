from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Any, Awaitable, Dict


class Info(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]):
        state = data['state']
        all_data = await state.get_data()
        diff = all_data['difficulty']
        data['difficulty'] = diff
        data['game_name'] = all_data['game_name']
        return await handler(event, data)
